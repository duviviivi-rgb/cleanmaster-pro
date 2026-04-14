#!/usr/bin/env python3
"""Automatic memory synchronization service."""

from __future__ import annotations

import argparse
import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Try to import watchdog for file system monitoring
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    has_watchdog = True
except ImportError:
    has_watchdog = False

# Try to import APScheduler for scheduled tasks
try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    has_apscheduler = True
except ImportError:
    has_apscheduler = False

from memory_sync import MemorySync


class MemoryAutoSync:
    """Automatic memory synchronization service."""
    
    def __init__(self, local_root: Path, remote_root: Path):
        self.local_root = local_root
        self.remote_root = remote_root
        self.sync = MemorySync(local_root, remote_root)
        self.observer = None
        self.scheduler = None
        self.logger = logging.getLogger("MemoryAutoSync")
        self.sync_config_path = local_root / ".auto_sync_config.json"
        self.sync_config = self._load_sync_config()
        self.running = False
    
    def _load_sync_config(self) -> Dict[str, Any]:
        """Load synchronization configuration."""
        if self.sync_config_path.exists():
            try:
                with open(self.sync_config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading sync config: {e}")
        return {
            "auto_sync": True,
            "sync_interval": 300,  # 5 minutes
            "watch_changes": True,
            "sync_on_start": True,
            "sync_log": []
        }
    
    def _save_sync_config(self):
        """Save synchronization configuration."""
        try:
            with open(self.sync_config_path, "w", encoding="utf-8") as f:
                json.dump(self.sync_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving sync config: {e}")
    
    def _add_sync_log(self, message: str):
        """Add synchronization log entry."""
        log_entry = {
            "timestamp": time.time(),
            "message": message
        }
        self.sync_config["sync_log"].append(log_entry)
        # Keep only last 100 log entries
        if len(self.sync_config["sync_log"]) > 100:
            self.sync_config["sync_log"] = self.sync_config["sync_log"][-100:]
        self._save_sync_config()
    
    def sync_now(self) -> Dict[str, Any]:
        """Perform synchronization now."""
        self.logger.info("Starting manual synchronization")
        try:
            result = self.sync.sync()
            message = f"Synchronization completed: uploaded={len(result.get('uploaded', []))}, downloaded={len(result.get('downloaded', []))}, conflicts={len(result.get('conflicts', []))}"
            self.logger.info(message)
            self._add_sync_log(message)
            return result
        except Exception as e:
            error_message = f"Synchronization failed: {e}"
            self.logger.error(error_message)
            self._add_sync_log(error_message)
            return {"error": str(e)}
    
    def start(self):
        """Start the automatic synchronization service."""
        if self.running:
            self.logger.warning("Auto sync service is already running")
            return
        
        self.running = True
        
        # Start file system watcher if enabled and watchdog is available
        if self.sync_config.get("watch_changes", True) and has_watchdog:
            self._start_file_watcher()
        
        # Start scheduled sync if enabled and apscheduler is available
        if self.sync_config.get("auto_sync", True) and has_apscheduler:
            self._start_scheduled_sync()
        
        # Sync on start if enabled
        if self.sync_config.get("sync_on_start", True):
            threading.Thread(target=self.sync_now, daemon=True).start()
        
        self.logger.info("Auto sync service started")
    
    def stop(self):
        """Stop the automatic synchronization service."""
        if not self.running:
            self.logger.warning("Auto sync service is not running")
            return
        
        # Stop file system watcher
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=5)
            self.observer = None
        
        # Stop scheduled sync
        if self.scheduler:
            self.scheduler.shutdown(wait=False)
            self.scheduler = None
        
        self.running = False
        self.logger.info("Auto sync service stopped")
    
    def _start_file_watcher(self):
        """Start file system watcher."""
        event_handler = MemoryChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.local_root), recursive=True)
        self.observer.start()
        self.logger.info(f"File system watcher started for {self.local_root}")
    
    def _start_scheduled_sync(self):
        """Start scheduled synchronization."""
        self.scheduler = BackgroundScheduler()
        interval = self.sync_config.get("sync_interval", 300)
        self.scheduler.add_job(
            self.sync_now,
            trigger=IntervalTrigger(seconds=interval),
            id="scheduled_sync",
            name="Scheduled memory synchronization",
            replace_existing=True
        )
        self.scheduler.start()
        self.logger.info(f"Scheduled sync started with interval {interval} seconds")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the auto sync service."""
        return {
            "running": self.running,
            "config": self.sync_config,
            "last_sync": self.sync_config["sync_log"][-1] if self.sync_config["sync_log"] else None,
            "watchdog_available": has_watchdog,
            "apscheduler_available": has_apscheduler
        }
    
    def update_config(self, config: Dict[str, Any]):
        """Update synchronization configuration."""
        self.sync_config.update(config)
        self._save_sync_config()
        
        # Restart service if running
        if self.running:
            self.stop()
            self.start()
        
        self.logger.info(f"Sync config updated: {config}")


class MemoryChangeHandler(FileSystemEventHandler):
    """Handle file system events for memory synchronization."""
    
    def __init__(self, auto_sync: MemoryAutoSync):
        self.auto_sync = auto_sync
        self.logger = logging.getLogger("MemoryChangeHandler")
        self.last_event_time = 0
        self.debounce_time = 2  # seconds
    
    def on_modified(self, event):
        """Handle file modified event."""
        if event.is_directory:
            return
        
        # Debounce events to avoid multiple syncs for the same change
        current_time = time.time()
        if current_time - self.last_event_time < self.debounce_time:
            return
        self.last_event_time = current_time
        
        # Only sync markdown files
        if not event.src_path.endswith(".md"):
            return
        
        # Skip sync database and other non-memory files
        file_name = os.path.basename(event.src_path)
        if file_name == ".sync_db.json" or file_name == ".auto_sync_config.json":
            return
        
        self.logger.info(f"File modified: {event.src_path}")
        # Run sync in a separate thread to avoid blocking the event loop
        threading.Thread(target=self.auto_sync.sync_now, daemon=True).start()
    
    def on_created(self, event):
        """Handle file created event."""
        if event.is_directory:
            return
        
        # Debounce events
        current_time = time.time()
        if current_time - self.last_event_time < self.debounce_time:
            return
        self.last_event_time = current_time
        
        # Only sync markdown files
        if not event.src_path.endswith(".md"):
            return
        
        self.logger.info(f"File created: {event.src_path}")
        # Run sync in a separate thread
        threading.Thread(target=self.auto_sync.sync_now, daemon=True).start()
    
    def on_deleted(self, event):
        """Handle file deleted event."""
        if event.is_directory:
            return
        
        # Debounce events
        current_time = time.time()
        if current_time - self.last_event_time < self.debounce_time:
            return
        self.last_event_time = current_time
        
        # Only sync markdown files
        if not event.src_path.endswith(".md"):
            return
        
        self.logger.info(f"File deleted: {event.src_path}")
        # Run sync in a separate thread
        threading.Thread(target=self.auto_sync.sync_now, daemon=True).start()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-root", required=True, help="Path to local memory directory")
    parser.add_argument("--remote-root", required=True, help="Path to remote memory directory")
    parser.add_argument("--action", choices=["start", "stop", "sync", "status"], default="start", help="Action to perform")
    parser.add_argument("--interval", type=int, help="Sync interval in seconds")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    local_root = Path(args.local_root).expanduser()
    remote_root = Path(args.remote_root).expanduser()
    
    # Initialize auto sync service
    auto_sync = MemoryAutoSync(local_root, remote_root)
    
    # Update interval if provided
    if args.interval:
        auto_sync.update_config({"sync_interval": args.interval})
    
    # Perform action
    if args.action == "start":
        auto_sync.start()
        print("Auto sync service started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping auto sync service...")
            auto_sync.stop()
    elif args.action == "stop":
        auto_sync.stop()
    elif args.action == "sync":
        result = auto_sync.sync_now()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.action == "status":
        status = auto_sync.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
