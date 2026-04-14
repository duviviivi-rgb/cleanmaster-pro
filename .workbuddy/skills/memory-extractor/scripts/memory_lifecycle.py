#!/usr/bin/env python3
"""Memory lifecycle management for automatic archiving and cleanup."""

from __future__ import annotations

import argparse
import json
import logging
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class MemoryLifecycleManager:
    """Manage memory lifecycle for automatic archiving and cleanup."""
    
    def __init__(self, memory_root: Path, archive_dir: Path, config_path: Path):
        self.memory_root = memory_root
        self.archive_dir = archive_dir
        self.config_path = config_path
        self.config: Dict[str, Any] = {
            "active_days": 30,      # Days before memory becomes inactive
            "archive_days": 90,      # Days before memory is archived
            "delete_days": 180,      # Days before memory is deleted
            "min_access_count": 3,   # Minimum accesses to avoid deletion
            "auto_archive": True,     # Automatically archive old memories
            "auto_delete": False,     # Automatically delete very old memories
            "exclude_patterns": ["MEMORY.md", ".*_profile.json", ".behavior_db.json"]
        }
        self.logger = logging.getLogger("MemoryLifecycleManager")
        self._ensure_directories()
        self._load_config()
    
    def _ensure_directories(self):
        """Ensure necessary directories exist."""
        self.memory_root.mkdir(exist_ok=True)
        self.archive_dir.mkdir(exist_ok=True)
    
    def _load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config.update(json.load(f))
                self.logger.info(f"Loaded configuration from {self.config_path}")
            except Exception as e:
                self.logger.error(f"Error loading configuration: {e}")
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved configuration to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
    
    def _should_exclude(self, file_path: Path) -> bool:
        """Check if a file should be excluded from lifecycle management."""
        for pattern in self.config.get("exclude_patterns", []):
            if file_path.name == pattern or pattern.startswith(".*") and file_path.name.endswith(pattern[2:]):
                return True
        return False
    
    def get_memory_age(self, file_path: Path) -> int:
        """Get memory age in days."""
        try:
            created_time = file_path.stat().st_ctime
            age = (datetime.now().timestamp() - created_time) / (24 * 3600)
            return int(age)
        except Exception as e:
            self.logger.error(f"Error getting memory age: {e}")
            return 0
    
    def get_memory_status(self, file_path: Path) -> str:
        """Get memory status based on age and configuration."""
        age = self.get_memory_age(file_path)
        
        if age < self.config.get("active_days", 30):
            return "active"
        elif age < self.config.get("archive_days", 90):
            return "inactive"
        elif age < self.config.get("delete_days", 180):
            return "archivable"
        else:
            return "deletable"
    
    def analyze_memories(self) -> Dict[str, List[Path]]:
        """Analyze all memories and categorize by status."""
        status_map = {
            "active": [],
            "inactive": [],
            "archivable": [],
            "deletable": []
        }
        
        for file_path in self.memory_root.glob("*.md"):
            if self._should_exclude(file_path):
                continue
            
            status = self.get_memory_status(file_path)
            status_map[status].append(file_path)
        
        return status_map
    
    def archive_memory(self, file_path: Path) -> bool:
        """Archive a memory."""
        try:
            archive_path = self.archive_dir / file_path.name
            
            # Check if file already exists in archive
            if archive_path.exists():
                # Append timestamp to avoid overwriting
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_path = self.archive_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
            
            # Move file to archive
            shutil.move(file_path, archive_path)
            self.logger.info(f"Archived memory: {file_path} -> {archive_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error archiving memory {file_path}: {e}")
            return False
    
    def delete_memory(self, file_path: Path) -> bool:
        """Delete a memory."""
        try:
            file_path.unlink()
            self.logger.info(f"Deleted memory: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting memory {file_path}: {e}")
            return False
    
    def run_lifecycle(self) -> Dict[str, int]:
        """Run memory lifecycle management."""
        status_map = self.analyze_memories()
        results = {
            "archived": 0,
            "deleted": 0,
            "errors": 0
        }
        
        # Archive memories
        if self.config.get("auto_archive", True):
            for file_path in status_map.get("archivable", []):
                if self.archive_memory(file_path):
                    results["archived"] += 1
                else:
                    results["errors"] += 1
        
        # Delete memories
        if self.config.get("auto_delete", False):
            for file_path in status_map.get("deletable", []):
                if self.delete_memory(file_path):
                    results["deleted"] += 1
                else:
                    results["errors"] += 1
        
        return results
    
    def get_lifecycle_report(self) -> Dict[str, Any]:
        """Get lifecycle report."""
        status_map = self.analyze_memories()
        report = {
            "total_memories": sum(len(files) for files in status_map.values()),
            "status_breakdown": {
                status: len(files)
                for status, files in status_map.items()
            },
            "config": self.config,
            "archive_size": sum(file.stat().st_size for file in self.archive_dir.glob("*.md"))
        }
        return report
    
    def update_config(self, config: Dict[str, Any]):
        """Update configuration."""
        self.config.update(config)
        self._save_config()
        self.logger.info(f"Updated configuration: {config}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--archive-dir", default=".archive", help="Path to archive directory")
    parser.add_argument("--config", default=".lifecycle_config.json", help="Path to configuration file")
    parser.add_argument("--run", action="store_true", help="Run lifecycle management")
    parser.add_argument("--report", action="store_true", help="Get lifecycle report")
    parser.add_argument("--update-config", action="store_true", help="Update configuration")
    parser.add_argument("--config-json", help="Configuration JSON")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    memory_root = Path(args.memory_root).expanduser()
    archive_dir = Path(args.archive_dir).expanduser()
    config_path = Path(args.config).expanduser()
    
    # Initialize lifecycle manager
    manager = MemoryLifecycleManager(memory_root, archive_dir, config_path)
    
    if args.run:
        # Run lifecycle management
        results = manager.run_lifecycle()
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.report:
        # Get lifecycle report
        report = manager.get_lifecycle_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.update_config and args.config_json:
        # Update configuration
        try:
            config = json.loads(args.config_json)
            manager.update_config(config)
            print("Configuration updated successfully")
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration: {e}")
    else:
        print("Please specify an action: --run, --report, or --update-config")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
