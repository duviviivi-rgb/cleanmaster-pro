#!/usr/bin/env python3
"""Real-time memory updater with event-based triggers."""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Try to import watchdog
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
    has_watchdog = True
except ImportError:
    has_watchdog = False

from memory_index import MemoryIndex
from memory_graph import MemoryGraph


class MemoryUpdateHandler(FileSystemEventHandler):
    """Handle file system events for memory updates."""
    
    def __init__(self, memory_root: Path, index_path: Path, graph_path: Path):
        self.memory_root = memory_root
        self.index_path = index_path
        self.graph_path = graph_path
        self.logger = logging.getLogger("MemoryUpdateHandler")
    
    def on_created(self, event: FileSystemEvent):
        """Handle file creation event."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix == ".md" and file_path.parent == self.memory_root:
            self.logger.info(f"New memory file created: {file_path}")
            self.update_memory_index()
            self.update_memory_graph()
    
    def on_modified(self, event: FileSystemEvent):
        """Handle file modification event."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix == ".md" and file_path.parent == self.memory_root:
            self.logger.info(f"Memory file modified: {file_path}")
            self.update_memory_index()
            self.update_memory_graph()
    
    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion event."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix == ".md" and file_path.parent == self.memory_root:
            self.logger.info(f"Memory file deleted: {file_path}")
            self.update_memory_index()
            self.update_memory_graph()
    
    def update_memory_index(self):
        """Update memory index."""
        try:
            indexer = MemoryIndex(self.memory_root)
            indexer.save_index(self.index_path)
            self.logger.info(f"Memory index updated: {self.index_path}")
        except Exception as e:
            self.logger.error(f"Error updating memory index: {e}")
    
    def update_memory_graph(self):
        """Update memory graph."""
        try:
            graph = MemoryGraph(self.memory_root)
            graph.save_graph(self.graph_path)
            self.logger.info(f"Memory graph updated: {self.graph_path}")
        except Exception as e:
            self.logger.error(f"Error updating memory graph: {e}")


class MemoryUpdater:
    """Real-time memory updater."""
    
    def __init__(self, memory_root: Path, index_path: Path, graph_path: Path):
        self.memory_root = memory_root
        self.index_path = index_path
        self.graph_path = graph_path
        self.observer: Optional[Observer] = None
        self.logger = logging.getLogger("MemoryUpdater")
    
    def start(self):
        """Start the memory updater."""
        if not has_watchdog:
            self.logger.error("Watchdog library not available. Please install it with 'pip install watchdog'")
            return False
        
        event_handler = MemoryUpdateHandler(self.memory_root, self.index_path, self.graph_path)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.memory_root), recursive=False)
        
        try:
            self.observer.start()
            self.logger.info(f"Memory updater started. Monitoring: {self.memory_root}")
            return True
        except Exception as e:
            self.logger.error(f"Error starting memory updater: {e}")
            return False
    
    def stop(self):
        """Stop the memory updater."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.logger.info("Memory updater stopped")
    
    def run(self):
        """Run the memory updater indefinitely."""
        if not self.start():
            return
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt. Stopping...")
        finally:
            self.stop()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--index-path", default=".memory_index.json", help="Path to save index")
    parser.add_argument("--graph-path", default=".memory_graph.json", help="Path to save graph")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    memory_root = Path(args.memory_root).expanduser()
    index_path = Path(args.index_path).expanduser()
    graph_path = Path(args.graph_path).expanduser()
    
    # Initialize memory updater
    updater = MemoryUpdater(memory_root, index_path, graph_path)
    
    # Run the updater
    updater.run()
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
