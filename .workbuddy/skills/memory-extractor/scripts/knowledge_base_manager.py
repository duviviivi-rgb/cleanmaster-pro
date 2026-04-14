#!/usr/bin/env python3
"""Knowledge base manager for WorkBuddy."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class KnowledgeBaseManager:
    """Manage knowledge base structure and organization."""
    
    def __init__(self, memory_root: Path):
        self.memory_root = memory_root
        self.config_path = memory_root / ".kb_config.json"
        self.config = self._load_config()
        self.logger = logging.getLogger("KnowledgeBaseManager")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load knowledge base configuration."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading KB config: {e}")
        return {
            "categories": [],
            "projects": [],
            "tags": [],
            "directory_structure": "flat",  # flat, hierarchical, or project-based
            "auto_organize": False,
            "organize_rules": []
        }
    
    def _save_config(self):
        """Save knowledge base configuration."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving KB config: {e}")
    
    def create_category(self, name: str, description: Optional[str] = None):
        """Create a new category."""
        category = {
            "name": name,
            "description": description or "",
            "created_at": str(os.path.getctime(__file__))
        }
        self.config["categories"].append(category)
        self._save_config()
        self.logger.info(f"Created category: {name}")
    
    def create_project(self, name: str, description: Optional[str] = None, categories: Optional[List[str]] = None):
        """Create a new project."""
        project = {
            "name": name,
            "description": description or "",
            "categories": categories or [],
            "created_at": str(os.path.getctime(__file__))
        }
        self.config["projects"].append(project)
        self._save_config()
        self.logger.info(f"Created project: {name}")
    
    def add_tag(self, name: str, description: Optional[str] = None):
        """Add a new tag."""
        tag = {
            "name": name,
            "description": description or "",
            "created_at": str(os.path.getctime(__file__))
        }
        self.config["tags"].append(tag)
        self._save_config()
        self.logger.info(f"Added tag: {name}")
    
    def organize_by_category(self):
        """Organize memories by category."""
        if self.config["directory_structure"] != "hierarchical":
            self.config["directory_structure"] = "hierarchical"
            self._save_config()
        
        # Create category directories
        for category in self.config["categories"]:
            category_dir = self.memory_root / category["name"]
            category_dir.mkdir(exist_ok=True)
        
        # Move memories to appropriate categories
        for memory_path in self.memory_root.glob("*.md"):
            if memory_path.name in ["MEMORY.md", ".kb_config.json", ".sync_db.json", ".auto_sync_config.json"]:
                continue
            
            # Extract category from frontmatter
            category = self._extract_category_from_memory(memory_path)
            if category:
                category_dir = self.memory_root / category
                category_dir.mkdir(exist_ok=True)
                new_path = category_dir / memory_path.name
                if not new_path.exists():
                    memory_path.rename(new_path)
                    self.logger.info(f"Moved {memory_path.name} to {category} category")
    
    def organize_by_project(self):
        """Organize memories by project."""
        if self.config["directory_structure"] != "project-based":
            self.config["directory_structure"] = "project-based"
            self._save_config()
        
        # Create project directories
        for project in self.config["projects"]:
            project_dir = self.memory_root / project["name"]
            project_dir.mkdir(exist_ok=True)
        
        # Move memories to appropriate projects
        for memory_path in self.memory_root.glob("*.md"):
            if memory_path.name in ["MEMORY.md", ".kb_config.json", ".sync_db.json", ".auto_sync_config.json"]:
                continue
            
            # Extract project from frontmatter
            project = self._extract_project_from_memory(memory_path)
            if project:
                project_dir = self.memory_root / project
                project_dir.mkdir(exist_ok=True)
                new_path = project_dir / memory_path.name
                if not new_path.exists():
                    memory_path.rename(new_path)
                    self.logger.info(f"Moved {memory_path.name} to {project} project")
    
    def organize_flat(self):
        """Organize memories in a flat structure."""
        if self.config["directory_structure"] != "flat":
            self.config["directory_structure"] = "flat"
            self._save_config()
        
        # Move all memories to the root directory
        for memory_path in self.memory_root.rglob("*.md"):
            if memory_path.parent == self.memory_root:
                continue
            if memory_path.name in ["MEMORY.md", ".kb_config.json", ".sync_db.json", ".auto_sync_config.json"]:
                continue
            
            new_path = self.memory_root / memory_path.name
            if not new_path.exists():
                memory_path.rename(new_path)
                self.logger.info(f"Moved {memory_path.name} to root directory")
    
    def _extract_category_from_memory(self, memory_path: Path) -> Optional[str]:
        """Extract category from memory frontmatter."""
        try:
            text = memory_path.read_text(encoding="utf-8")
            frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
            if frontmatter_match:
                frontmatter_text = frontmatter_match.group(1)
                for line in frontmatter_text.splitlines():
                    if line.strip().startswith("category:"):
                        return line.split(":", 1)[1].strip().strip('"')
        except Exception as e:
            self.logger.error(f"Error extracting category from {memory_path}: {e}")
        return None
    
    def _extract_project_from_memory(self, memory_path: Path) -> Optional[str]:
        """Extract project from memory frontmatter."""
        try:
            text = memory_path.read_text(encoding="utf-8")
            frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
            if frontmatter_match:
                frontmatter_text = frontmatter_match.group(1)
                for line in frontmatter_text.splitlines():
                    if line.strip().startswith("project:"):
                        return line.split(":", 1)[1].strip().strip('"')
        except Exception as e:
            self.logger.error(f"Error extracting project from {memory_path}: {e}")
        return None
    
    def get_memory_structure(self) -> Dict[str, Any]:
        """Get current memory structure."""
        structure = {
            "directories": {},
            "files": [],
            "total_files": 0
        }
        
        for root, dirs, files in os.walk(self.memory_root):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            
            relative_root = os.path.relpath(root, self.memory_root)
            if relative_root == ".":
                relative_root = "root"
            
            structure["directories"][relative_root] = {
                "files": [],
                "subdirectories": dirs
            }
            
            for file in files:
                if file.endswith(".md") and file not in ["MEMORY.md"]:
                    structure["directories"][relative_root]["files"].append(file)
                    structure["files"].append(os.path.join(relative_root, file))
                    structure["total_files"] += 1
        
        return structure
    
    def generate_manifest(self) -> List[Dict[str, Any]]:
        """Generate a manifest of all memories."""
        manifest = []
        
        for memory_path in self.memory_root.rglob("*.md"):
            if memory_path.name in ["MEMORY.md", ".kb_config.json", ".sync_db.json", ".auto_sync_config.json"]:
                continue
            
            try:
                text = memory_path.read_text(encoding="utf-8")
                frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
                frontmatter = {}
                content = text
                
                if frontmatter_match:
                    frontmatter_text = frontmatter_match.group(1)
                    content = text[frontmatter_match.end():]
                    for line in frontmatter_text.splitlines():
                        if ":" in line:
                            key, value = line.split(":", 1)
                            frontmatter[key.strip()] = value.strip().strip('"')
                
                manifest.append({
                    "path": str(memory_path.relative_to(self.memory_root)),
                    "title": frontmatter.get("title", memory_path.stem),
                    "type": frontmatter.get("type", "unknown"),
                    "category": frontmatter.get("category", "uncategorized"),
                    "project": frontmatter.get("project", "unassigned"),
                    "tags": frontmatter.get("tags", "").split(",") if "tags" in frontmatter else [],
                    "size": memory_path.stat().st_size,
                    "modified": memory_path.stat().st_mtime
                })
            except Exception as e:
                self.logger.error(f"Error generating manifest for {memory_path}: {e}")
        
        return manifest
    
    def update_config(self, config: Dict[str, Any]):
        """Update knowledge base configuration."""
        self.config.update(config)
        self._save_config()
        self.logger.info(f"KB config updated: {config}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the knowledge base."""
        structure = self.get_memory_structure()
        manifest = self.generate_manifest()
        
        # Calculate statistics
        category_count = len(self.config["categories"])
        project_count = len(self.config["projects"])
        tag_count = len(self.config["tags"])
        file_count = structure["total_files"]
        
        # Calculate files per category
        files_per_category = {}
        for item in manifest:
            category = item["category"]
            files_per_category[category] = files_per_category.get(category, 0) + 1
        
        # Calculate files per project
        files_per_project = {}
        for item in manifest:
            project = item["project"]
            files_per_project[project] = files_per_project.get(project, 0) + 1
        
        return {
            "structure": self.config["directory_structure"],
            "categories": category_count,
            "projects": project_count,
            "tags": tag_count,
            "files": file_count,
            "files_per_category": files_per_category,
            "files_per_project": files_per_project,
            "auto_organize": self.config["auto_organize"]
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--action", choices=["create-category", "create-project", "add-tag", "organize", "status", "manifest"], required=True, help="Action to perform")
    parser.add_argument("--name", help="Name for category, project, or tag")
    parser.add_argument("--description", help="Description for category, project, or tag")
    parser.add_argument("--structure", choices=["flat", "hierarchical", "project-based"], help="Directory structure to use for organization")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    memory_root = Path(args.memory_root).expanduser()
    kb_manager = KnowledgeBaseManager(memory_root)
    
    if args.action == "create-category":
        if not args.name:
            parser.error("--name is required for create-category")
        kb_manager.create_category(args.name, args.description)
    elif args.action == "create-project":
        if not args.name:
            parser.error("--name is required for create-project")
        kb_manager.create_project(args.name, args.description)
    elif args.action == "add-tag":
        if not args.name:
            parser.error("--name is required for add-tag")
        kb_manager.add_tag(args.name, args.description)
    elif args.action == "organize":
        if not args.structure:
            parser.error("--structure is required for organize")
        if args.structure == "hierarchical":
            kb_manager.organize_by_category()
        elif args.structure == "project-based":
            kb_manager.organize_by_project()
        elif args.structure == "flat":
            kb_manager.organize_flat()
    elif args.action == "status":
        status = kb_manager.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    elif args.action == "manifest":
        manifest = kb_manager.generate_manifest()
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
