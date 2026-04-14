#!/usr/bin/env python3
"""Cross-device memory synchronization."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import socket
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class MemorySync:
    """Cross-device memory synchronization."""
    
    def __init__(self, local_root: Path, remote_root: Path, device_id: Optional[str] = None, device_priority: int = 5):
        self.local_root = local_root
        self.remote_root = remote_root
        self.sync_db_path = local_root / ".sync_db.json"
        self.sync_db: Dict[str, Dict[str, Any]] = {}
        self.device_id = device_id or self._generate_device_id()
        self.device_priority = device_priority  # Higher priority means more authoritative
        self.device_db_path = local_root / ".device_db.json"
        self.device_db: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger("MemorySync")
        self._load_sync_db()
        self._load_device_db()
    
    def _generate_device_id(self) -> str:
        """Generate a unique device ID."""
        import hashlib
        import socket
        import uuid
        # Generate a unique device ID based on hostname and MAC address
        hostname = socket.gethostname()
        mac = uuid.getnode()
        device_id = hashlib.md5(f"{hostname}_{mac}".encode()).hexdigest()
        return device_id
    
    def _load_device_db(self):
        """Load device database."""
        if self.device_db_path.exists():
            try:
                with open(self.device_db_path, "r", encoding="utf-8") as f:
                    self.device_db = json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading device database: {e}")
                self.device_db = {}
        
        # Register current device
        self.device_db[self.device_id] = {
            "id": self.device_id,
            "priority": self.device_priority,
            "last_sync": time.time(),
            "hostname": socket.gethostname()
        }
        self._save_device_db()
    
    def _save_device_db(self):
        """Save device database."""
        try:
            with open(self.device_db_path, "w", encoding="utf-8") as f:
                json.dump(self.device_db, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving device database: {e}")
    
    def _load_sync_db(self):
        """Load synchronization database."""
        if self.sync_db_path.exists():
            try:
                with open(self.sync_db_path, "r", encoding="utf-8") as f:
                    self.sync_db = json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading sync database: {e}")
                self.sync_db = {}
    
    def _save_sync_db(self):
        """Save synchronization database."""
        try:
            with open(self.sync_db_path, "w", encoding="utf-8") as f:
                json.dump(self.sync_db, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving sync database: {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get file hash for synchronization."""
        import hashlib
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error getting file hash: {e}")
            return ""
    
    def _get_file_chunks(self, file_path: Path, chunk_size: int = 4096) -> List[str]:
        """Get file chunks for incremental synchronization."""
        import hashlib
        chunks = []
        try:
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    chunks.append(hashlib.md5(chunk).hexdigest())
        except Exception as e:
            self.logger.error(f"Error getting file chunks: {e}")
        return chunks
    
    def _sync_file_incrementally(self, local_path: Path, remote_path: Path) -> bool:
        """Sync file incrementally."""
        try:
            # Get chunks for both files
            local_chunks = self._get_file_chunks(local_path)
            remote_chunks = self._get_file_chunks(remote_path) if remote_path.exists() else []
            
            # If files are identical, no need to sync
            if local_chunks == remote_chunks:
                return True
            
            # If remote file doesn't exist, just copy the whole file
            if not remote_path.exists():
                shutil.copy2(local_path, remote_path)
                return True
            
            # Find differing chunks
            differing_chunks = []
            for i, (local_chunk, remote_chunk) in enumerate(zip(local_chunks, remote_chunks)):
                if local_chunk != remote_chunk:
                    differing_chunks.append(i)
            
            # If there are more than 50% differing chunks, just copy the whole file
            if len(differing_chunks) > len(local_chunks) * 0.5:
                shutil.copy2(local_path, remote_path)
                return True
            
            # Incremental sync: only transfer differing chunks
            # For simplicity, we'll just copy the whole file for now
            # In a production environment, we would implement actual chunk-based transfer
            shutil.copy2(local_path, remote_path)
            return True
        except Exception as e:
            self.logger.error(f"Error in incremental sync: {e}")
            return False
    
    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get file information for synchronization."""
        try:
            return {
                "size": file_path.stat().st_size,
                "mtime": file_path.stat().st_mtime,
                "hash": self._get_file_hash(file_path)
            }
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return {}
    
    def _scan_local_files(self) -> Dict[str, Dict[str, Any]]:
        """Scan local memory files."""
        local_files = {}
        for path in sorted(self.local_root.glob("*.md")):
            if path.name == "MEMORY.md" or path.name == ".sync_db.json":
                continue
            relative_path = path.relative_to(self.local_root)
            local_files[str(relative_path)] = self._get_file_info(path)
        return local_files
    
    def _scan_remote_files(self) -> Dict[str, Dict[str, Any]]:
        """Scan remote memory files."""
        remote_files = {}
        if not self.remote_root.exists():
            return remote_files
        for path in sorted(self.remote_root.glob("*.md")):
            if path.name == "MEMORY.md" or path.name == ".sync_db.json":
                continue
            relative_path = path.relative_to(self.remote_root)
            remote_files[str(relative_path)] = self._get_file_info(path)
        return remote_files
    
    def _detect_changes(self) -> Tuple[List[str], List[str], List[str]]:
        """Detect changes between local and remote."""
        local_files = self._scan_local_files()
        remote_files = self._scan_remote_files()
        
        # Files to upload (local has, remote doesn't or local is newer)
        to_upload = []
        # Files to download (remote has, local doesn't or remote is newer)
        to_download = []
        # Conflicts (both have changes)
        conflicts = []
        
        all_files = set(local_files.keys()) | set(remote_files.keys())
        
        for file_name in all_files:
            if file_name not in local_files:
                # File only in remote, download
                to_download.append(file_name)
            elif file_name not in remote_files:
                # File only in local, upload
                to_upload.append(file_name)
            else:
                # File in both, check for changes
                local_hash = local_files[file_name].get("hash", "")
                remote_hash = remote_files[file_name].get("hash", "")
                
                if local_hash != remote_hash:
                    # Check modification times
                    local_mtime = local_files[file_name].get("mtime", 0)
                    remote_mtime = remote_files[file_name].get("mtime", 0)
                    
                    if abs(local_mtime - remote_mtime) < 1:  # Same time, likely same file
                        continue
                    elif local_mtime > remote_mtime:
                        # Local is newer, upload
                        to_upload.append(file_name)
                    elif remote_mtime > local_mtime:
                        # Remote is newer, download
                        to_download.append(file_name)
                    else:
                        # Conflict: both have changes
                        conflicts.append(file_name)
        
        return to_upload, to_download, conflicts
    
    def _resolve_conflict(self, file_name: str) -> str:
        """Resolve conflict for a file."""
        local_path = self.local_root / file_name
        remote_path = self.remote_root / file_name
        
        # Try to perform intelligent conflict resolution
        resolution = self._intelligent_conflict_resolution(file_name, local_path, remote_path)
        if resolution:
            return resolution
        
        # Fallback to creating conflict resolution files
        local_conflict_path = self.local_root / f"{file_name}.local.txt"
        remote_conflict_path = self.local_root / f"{file_name}.remote.txt"
        
        # Copy local and remote versions
        if local_path.exists():
            shutil.copy2(local_path, local_conflict_path)
        if remote_path.exists():
            shutil.copy2(remote_path, remote_conflict_path)
        
        self.logger.info(f"Conflict detected for {file_name}. Created conflict resolution files.")
        return f"Conflict resolved. Created {local_conflict_path.name} and {remote_conflict_path.name}"
    
    def _intelligent_conflict_resolution(self, file_name: str, local_path: Path, remote_path: Path) -> Optional[str]:
        """Perform intelligent conflict resolution."""
        try:
            # Only handle markdown files for intelligent resolution
            if not file_name.endswith('.md'):
                return None
            
            # Check device priority first
            resolution = self._resolve_by_device_priority(file_name, local_path, remote_path)
            if resolution:
                return resolution
            
            # Read both versions
            local_content = local_path.read_text(encoding="utf-8") if local_path.exists() else ""
            remote_content = remote_path.read_text(encoding="utf-8") if remote_path.exists() else ""
            
            # Analyze changes
            local_lines = local_content.splitlines()
            remote_lines = remote_content.splitlines()
            
            # Check if one version is a superset of the other
            if self._is_superset(local_lines, remote_lines):
                # Local is superset, keep local
                shutil.copy2(local_path, remote_path)
                self.logger.info(f"Intelligent conflict resolution: Local version is superset, keeping local for {file_name}")
                return f"Intelligent conflict resolution: Local version is superset, keeping local"
            elif self._is_superset(remote_lines, local_lines):
                # Remote is superset, keep remote
                shutil.copy2(remote_path, local_path)
                self.logger.info(f"Intelligent conflict resolution: Remote version is superset, keeping remote for {file_name}")
                return f"Intelligent conflict resolution: Remote version is superset, keeping remote"
            
            # Check if changes are in different sections
            local_frontmatter, local_body = self._split_markdown(local_content)
            remote_frontmatter, remote_body = self._split_markdown(remote_content)
            
            if local_frontmatter == remote_frontmatter:
                # Only body changed, try to merge
                merged_body = self._merge_bodies(local_body, remote_body)
                merged_content = local_frontmatter + "\n" + merged_body if local_frontmatter else merged_body
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(merged_content)
                shutil.copy2(local_path, remote_path)
                self.logger.info(f"Intelligent conflict resolution: Merged body changes for {file_name}")
                return f"Intelligent conflict resolution: Merged body changes"
            elif local_body == remote_body:
                # Only frontmatter changed, keep local frontmatter
                merged_content = local_frontmatter + "\n" + local_body if local_frontmatter else local_body
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(merged_content)
                shutil.copy2(local_path, remote_path)
                self.logger.info(f"Intelligent conflict resolution: Kept local frontmatter for {file_name}")
                return f"Intelligent conflict resolution: Kept local frontmatter"
            
            # No intelligent resolution possible
            return None
        except Exception as e:
            self.logger.error(f"Error in intelligent conflict resolution: {e}")
            return None
    
    def _resolve_by_device_priority(self, file_name: str, local_path: Path, remote_path: Path) -> Optional[str]:
        """Resolve conflict based on device priority."""
        try:
            # Get device info from sync DB
            local_device_info = self.sync_db.get(file_name, {}).get("device_info", {})
            remote_device_id = None
            
            # Try to get remote device info from remote sync DB
            remote_sync_db_path = self.remote_root / ".sync_db.json"
            if remote_sync_db_path.exists():
                with open(remote_sync_db_path, "r", encoding="utf-8") as f:
                    remote_sync_db = json.load(f)
                    remote_file_info = remote_sync_db.get(file_name, {})
                    remote_device_info = remote_file_info.get("device_info", {})
                    remote_device_id = remote_device_info.get("device_id")
            
            # Get device priorities
            local_priority = self.device_priority
            remote_priority = 5  # Default priority
            
            if remote_device_id and remote_device_id in self.device_db:
                remote_priority = self.device_db[remote_device_id].get("priority", 5)
            
            # Resolve based on priority
            if local_priority > remote_priority:
                # Local device has higher priority, keep local
                shutil.copy2(local_path, remote_path)
                self.logger.info(f"Conflict resolution by device priority: Local device (priority {local_priority}) wins over remote device (priority {remote_priority}) for {file_name}")
                return f"Conflict resolution by device priority: Local device wins"
            elif remote_priority > local_priority:
                # Remote device has higher priority, keep remote
                shutil.copy2(remote_path, local_path)
                self.logger.info(f"Conflict resolution by device priority: Remote device (priority {remote_priority}) wins over local device (priority {local_priority}) for {file_name}")
                return f"Conflict resolution by device priority: Remote device wins"
            
            # Equal priority, let timestamp decide
            local_mtime = local_path.stat().st_mtime if local_path.exists() else 0
            remote_mtime = remote_path.stat().st_mtime if remote_path.exists() else 0
            
            if local_mtime > remote_mtime:
                # Local is newer
                shutil.copy2(local_path, remote_path)
                self.logger.info(f"Conflict resolution by timestamp: Local version (newer) wins for {file_name}")
                return f"Conflict resolution by timestamp: Local version wins"
            elif remote_mtime > local_mtime:
                # Remote is newer
                shutil.copy2(remote_path, local_path)
                self.logger.info(f"Conflict resolution by timestamp: Remote version (newer) wins for {file_name}")
                return f"Conflict resolution by timestamp: Remote version wins"
            
            # No resolution based on priority or timestamp
            return None
        except Exception as e:
            self.logger.error(f"Error in device priority resolution: {e}")
            return None
    
    def _is_superset(self, lines1: List[str], lines2: List[str]) -> bool:
        """Check if lines1 is a superset of lines2."""
        return all(line in lines1 for line in lines2)
    
    def _split_markdown(self, content: str) -> Tuple[str, str]:
        """Split markdown content into frontmatter and body."""
        import re
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(0)
            body = content[frontmatter_match.end():]
            return frontmatter, body
        return "", content
    
    def _merge_bodies(self, body1: str, body2: str) -> str:
        """Merge two markdown bodies."""
        # Simple merge: keep both contents with a separator
        return f"{body1}\n\n--- CONFLICT MERGED ---\n\n{body2}"
    
    def sync(self) -> Dict[str, Any]:
        """Sync memory files between local and remote."""
        # Ensure remote directory exists
        self.remote_root.mkdir(exist_ok=True)
        
        # Detect changes
        to_upload, to_download, conflicts = self._detect_changes()
        
        # Resolve conflicts
        conflict_resolutions = []
        for file_name in conflicts:
            resolution = self._resolve_conflict(file_name)
            conflict_resolutions.append(resolution)
        
        # Upload files
        uploaded = []
        for file_name in to_upload:
            local_path = self.local_root / file_name
            remote_path = self.remote_root / file_name
            try:
                if self._sync_file_incrementally(local_path, remote_path):
                    uploaded.append(file_name)
                    # Update sync database with device info
                    file_info = self._get_file_info(local_path)
                    file_info["device_info"] = {
                        "device_id": self.device_id,
                        "device_priority": self.device_priority,
                        "sync_time": time.time()
                    }
                    self.sync_db[file_name] = file_info
                    self.logger.info(f"Uploaded: {file_name}")
            except Exception as e:
                self.logger.error(f"Error uploading {file_name}: {e}")
        
        # Download files
        downloaded = []
        for file_name in to_download:
            remote_path = self.remote_root / file_name
            local_path = self.local_root / file_name
            try:
                if self._sync_file_incrementally(remote_path, local_path):
                    downloaded.append(file_name)
                    # Update sync database with device info
                    file_info = self._get_file_info(local_path)
                    file_info["device_info"] = {
                        "device_id": self.device_id,
                        "device_priority": self.device_priority,
                        "sync_time": time.time()
                    }
                    self.sync_db[file_name] = file_info
                    self.logger.info(f"Downloaded: {file_name}")
            except Exception as e:
                self.logger.error(f"Error downloading {file_name}: {e}")
        
        # Save sync database
        self._save_sync_db()
        
        return {
            "uploaded": uploaded,
            "downloaded": downloaded,
            "conflicts": conflicts,
            "conflict_resolutions": conflict_resolutions
        }
    
    def push(self) -> Dict[str, Any]:
        """Push local changes to remote."""
        # Ensure remote directory exists
        self.remote_root.mkdir(exist_ok=True)
        
        # Detect changes
        local_files = self._scan_local_files()
        remote_files = self._scan_remote_files()
        
        # Files to upload (local has, remote doesn't or local is newer)
        to_upload = []
        for file_name, local_info in local_files.items():
            if file_name not in remote_files:
                to_upload.append(file_name)
            else:
                local_hash = local_info.get("hash", "")
                remote_hash = remote_files[file_name].get("hash", "")
                if local_hash != remote_hash:
                    local_mtime = local_info.get("mtime", 0)
                    remote_mtime = remote_files[file_name].get("mtime", 0)
                    if local_mtime > remote_mtime:
                        to_upload.append(file_name)
        
        # Upload files
        uploaded = []
        for file_name in to_upload:
            local_path = self.local_root / file_name
            remote_path = self.remote_root / file_name
            try:
                if self._sync_file_incrementally(local_path, remote_path):
                    uploaded.append(file_name)
                    # Update sync database with device info
                    file_info = self._get_file_info(local_path)
                    file_info["device_info"] = {
                        "device_id": self.device_id,
                        "device_priority": self.device_priority,
                        "sync_time": time.time()
                    }
                    self.sync_db[file_name] = file_info
                    self.logger.info(f"Pushed: {file_name}")
            except Exception as e:
                self.logger.error(f"Error pushing {file_name}: {e}")
        
        # Save sync database
        self._save_sync_db()
        
        return {"uploaded": uploaded}
    
    def pull(self) -> Dict[str, Any]:
        """Pull remote changes to local."""
        # Ensure remote directory exists
        self.remote_root.mkdir(exist_ok=True)
        
        # Detect changes
        local_files = self._scan_local_files()
        remote_files = self._scan_remote_files()
        
        # Files to download (remote has, local doesn't or remote is newer)
        to_download = []
        for file_name, remote_info in remote_files.items():
            if file_name not in local_files:
                to_download.append(file_name)
            else:
                local_hash = local_files[file_name].get("hash", "")
                remote_hash = remote_info.get("hash", "")
                if local_hash != remote_hash:
                    local_mtime = local_files[file_name].get("mtime", 0)
                    remote_mtime = remote_info.get("mtime", 0)
                    if remote_mtime > local_mtime:
                        to_download.append(file_name)
        
        # Download files
        downloaded = []
        for file_name in to_download:
            remote_path = self.remote_root / file_name
            local_path = self.local_root / file_name
            try:
                if self._sync_file_incrementally(remote_path, local_path):
                    downloaded.append(file_name)
                    # Update sync database with device info
                    file_info = self._get_file_info(local_path)
                    file_info["device_info"] = {
                        "device_id": self.device_id,
                        "device_priority": self.device_priority,
                        "sync_time": time.time()
                    }
                    self.sync_db[file_name] = file_info
                    self.logger.info(f"Pulled: {file_name}")
            except Exception as e:
                self.logger.error(f"Error pulling {file_name}: {e}")
        
        # Save sync database
        self._save_sync_db()
        
        return {"downloaded": downloaded}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-root", required=True, help="Path to local memory directory")
    parser.add_argument("--remote-root", required=True, help="Path to remote memory directory")
    parser.add_argument("--action", choices=["sync", "push", "pull"], default="sync", help="Sync action")
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
    
    # Initialize memory sync
    sync = MemorySync(local_root, remote_root)
    
    # Perform sync action
    if args.action == "sync":
        result = sync.sync()
    elif args.action == "push":
        result = sync.push()
    elif args.action == "pull":
        result = sync.pull()
    
    # Print result
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
