#!/usr/bin/env python3
"""Optimize memory storage structure by identifying duplicates and organizing content."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


class MemoryOptimizer:
    def __init__(self, memory_root: Path):
        self.memory_root = memory_root
        self.memories: Dict[str, Dict[str, Any]] = {}
        self.similar_groups: List[List[str]] = []
        self.load_memories()

    def parse_frontmatter(self, text: str) -> Dict[str, str]:
        """Parse YAML frontmatter from a markdown file."""
        match = FRONTMATTER_RE.match(text)
        if not match:
            return {}
        data: Dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
        return data

    def load_memories(self):
        """Load all memory files."""
        for path in sorted(self.memory_root.glob("*.md")):
            if path.name == "MEMORY.md":
                continue
            
            try:
                text = path.read_text(encoding="utf-8")
                frontmatter = self.parse_frontmatter(text)
                
                # Extract content without frontmatter
                content = FRONTMATTER_RE.sub("", text)
                
                # Extract tags
                tags = frontmatter.get("tags", "").split(",") if "tags" in frontmatter else []
                tags = [tag.strip() for tag in tags if tag.strip()]
                
                self.memories[path.name] = {
                    "path": str(path),
                    "text": text,
                    "content": content,
                    "frontmatter": frontmatter,
                    "tags": tags,
                    "size_bytes": path.stat().st_size
                }
                
            except Exception as e:
                print(f"Error loading {path}: {e}")

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using Jaccard index."""
        # Remove punctuation and convert to lowercase
        text1 = re.sub(r"[.!?,;:()\[\]{}]", " ", text1.lower())
        text2 = re.sub(r"[.!?,;:()\[\]{}]", " ", text2.lower())
        
        # Split into words
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        # Calculate Jaccard index
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0

    def find_similar_memories(self, threshold: float = 0.5):
        """Find similar memories based on content similarity."""
        processed = set()
        
        for name1, memory1 in self.memories.items():
            if name1 in processed:
                continue
            
            group = [name1]
            processed.add(name1)
            
            for name2, memory2 in self.memories.items():
                if name2 in processed:
                    continue
                
                similarity = self.calculate_similarity(
                    memory1["content"], 
                    memory2["content"]
                )
                
                if similarity > threshold:
                    group.append(name2)
                    processed.add(name2)
            
            if len(group) > 1:
                self.similar_groups.append(group)

    def identify_duplicates(self) -> List[List[str]]:
        """Identify duplicate memories."""
        duplicates = []
        processed = set()
        
        for name1, memory1 in self.memories.items():
            if name1 in processed:
                continue
            
            group = [name1]
            processed.add(name1)
            
            for name2, memory2 in self.memories.items():
                if name2 in processed:
                    continue
                
                # Check if content is identical
                if memory1["content"].strip() == memory2["content"].strip():
                    group.append(name2)
                    processed.add(name2)
            
            if len(group) > 1:
                duplicates.append(group)
        
        return duplicates

    def analyze_memory_types(self) -> Dict[str, int]:
        """Analyze memory types distribution."""
        types = {}
        for memory in self.memories.values():
            memory_type = memory["frontmatter"].get("type", "unknown")
            types[memory_type] = types.get(memory_type, 0) + 1
        return types

    def generate_optimization_report(self) -> Dict[str, Any]:
        """Generate optimization report."""
        # Find similar memories
        self.find_similar_memories()
        
        # Find duplicates
        duplicates = self.identify_duplicates()
        
        # Analyze memory types
        type_distribution = self.analyze_memory_types()
        
        # Calculate statistics
        total_memories = len(self.memories)
        total_size = sum(memory["size_bytes"] for memory in self.memories.values())
        duplicate_count = sum(len(group) - 1 for group in duplicates)
        similar_count = sum(len(group) - 1 for group in self.similar_groups)
        
        # Generate optimization suggestions
        suggestions = []
        
        if duplicates:
            suggestions.append(f"Remove {duplicate_count} duplicate memories")
        
        if self.similar_groups:
            suggestions.append(f"Merge {similar_count} similar memories")
        
        # Check for memory organization issues
        if len(self.memories) > 50:
            suggestions.append("Consider organizing memories into subdirectories by type or topic")
        
        if total_size > 1000000:  # 1MB
            suggestions.append("Consider compressing or archiving old memories")
        
        return {
            "total_memories": total_memories,
            "total_size_bytes": total_size,
            "type_distribution": type_distribution,
            "duplicate_groups": duplicates,
            "similar_groups": self.similar_groups,
            "optimization_suggestions": suggestions
        }

    def optimize_memory_structure(self, output_dir: Path):
        """Optimize memory structure by merging similar memories."""
        # Create output directory if it doesn't exist
        output_dir.mkdir(exist_ok=True)
        
        # Generate optimization report
        report = self.generate_optimization_report()
        
        # Process duplicates first
        kept_files = set()
        for group in report["duplicate_groups"]:
            # Keep the first file in the group
            kept_files.add(group[0])
            # Mark others for removal
            for file_name in group[1:]:
                print(f"Marking duplicate for removal: {file_name}")
        
        # Process similar memories
        for group in report["similar_groups"]:
            if len(group) > 1:
                # Merge similar memories
                merged_content = ""
                merged_frontmatter = {}
                merged_tags = set()
                
                # Collect content from all similar memories
                for file_name in group:
                    memory = self.memories[file_name]
                    merged_content += memory["content"] + "\n\n"
                    # Merge frontmatter (prioritize non-empty values)
                    for key, value in memory["frontmatter"].items():
                        if key not in merged_frontmatter or not merged_frontmatter[key]:
                            merged_frontmatter[key] = value
                    # Merge tags
                    merged_tags.update(memory["tags"])
                
                # Create merged file
                merged_file_name = f"merged_{'_'.join(group[0].split('.')[:-1])}.md"
                merged_path = output_dir / merged_file_name
                
                # Write merged content
                frontmatter_str = "---\n"
                for key, value in merged_frontmatter.items():
                    frontmatter_str += f"{key}: {value}\n"
                if merged_tags:
                    frontmatter_str += f"tags: {', '.join(merged_tags)}\n"
                frontmatter_str += "---\n"
                
                merged_text = frontmatter_str + merged_content.strip()
                merged_path.write_text(merged_text, encoding="utf-8")
                
                print(f"Created merged memory: {merged_file_name}")
                
                # Mark original files for removal
                for file_name in group:
                    print(f"Marking similar for removal: {file_name}")
        
        # Copy non-duplicate, non-similar files
        for file_name, memory in self.memories.items():
            if file_name not in kept_files:
                # Check if this file is in any similar group
                in_similar_group = False
                for group in report["similar_groups"]:
                    if file_name in group:
                        in_similar_group = True
                        break
                
                if not in_similar_group:
                    # Copy the file to output directory
                    src_path = Path(memory["path"])
                    dst_path = output_dir / src_path.name
                    dst_path.write_text(memory["text"], encoding="utf-8")
                    print(f"Copied: {file_name}")
        
        return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True)
    parser.add_argument("--output-dir", help="Directory to write optimized memories")
    parser.add_argument("--threshold", type=float, default=0.5, help="Similarity threshold")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    memory_root = Path(args.memory_root).expanduser()
    optimizer = MemoryOptimizer(memory_root)
    
    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser()
        report = optimizer.optimize_memory_structure(output_dir)
    else:
        report = optimizer.generate_optimization_report()
    
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("Memory optimization report:")
        print("=" * 80)
        print(f"Total memories: {report['total_memories']}")
        print(f"Total size: {report['total_size_bytes']} bytes")
        print()
        
        print("Memory type distribution:")
        for memory_type, count in report['type_distribution'].items():
            print(f"  {memory_type}: {count}")
        print()
        
        if report['duplicate_groups']:
            print("Duplicate memory groups:")
            for i, group in enumerate(report['duplicate_groups']):
                print(f"  Group {i+1}:")
                for file_name in group:
                    print(f"    - {file_name}")
            print()
        
        if report['similar_groups']:
            print("Similar memory groups:")
            for i, group in enumerate(report['similar_groups']):
                print(f"  Group {i+1}:")
                for file_name in group:
                    print(f"    - {file_name}")
            print()
        
        print("Optimization suggestions:")
        for suggestion in report['optimization_suggestions']:
            print(f"  - {suggestion}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
