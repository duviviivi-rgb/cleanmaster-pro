#!/usr/bin/env python3
"""Intelligently compress memories by prioritizing important information."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


class MemoryCompressor:
    def __init__(self, memory_root: Path):
        self.memory_root = memory_root
        self.memories: Dict[str, Dict[str, Any]] = {}
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
                
                # Calculate importance score
                importance_score = self.calculate_importance(
                    content, 
                    frontmatter, 
                    tags,
                    path.stat().st_mtime
                )
                
                self.memories[path.name] = {
                    "path": str(path),
                    "text": text,
                    "content": content,
                    "frontmatter": frontmatter,
                    "tags": tags,
                    "size_bytes": path.stat().st_size,
                    "modified_date": path.stat().st_mtime,
                    "importance_score": importance_score
                }
                
            except Exception as e:
                print(f"Error loading {path}: {e}")

    def calculate_importance(self, content: str, frontmatter: Dict[str, str], 
                           tags: List[str], modified_time: float) -> float:
        """Calculate importance score for a memory (0-1)."""
        score = 0.0
        
        # Recency factor (0.3 weight)
        days_since_modified = (datetime.now().timestamp() - modified_time) / (24 * 3600)
        if days_since_modified < 7:
            recency_score = 1.0
        elif days_since_modified > 180:
            recency_score = 0.1
        else:
            recency_score = 1.0 - (days_since_modified - 7) / (180 - 7) * 0.9
        score += recency_score * 0.3
        
        # Content length factor (0.2 weight)
        content_length = len(content)
        if content_length < 100:
            length_score = 0.3
        elif content_length > 1000:
            length_score = 1.0
        else:
            length_score = 0.3 + (content_length - 100) / (1000 - 100) * 0.7
        score += length_score * 0.2
        
        # Tag importance factor (0.2 weight)
        important_tags = {"important", "critical", "key", "essential", "priority"}
        tag_score = 0.0
        for tag in tags:
            if tag.lower() in important_tags:
                tag_score = 1.0
                break
        score += tag_score * 0.2
        
        # Type importance factor (0.2 weight)
        memory_type = frontmatter.get("type", "").lower()
        important_types = {"user", "feedback", "project"}
        type_score = 1.0 if memory_type in important_types else 0.5
        score += type_score * 0.2
        
        # Content quality factor (0.1 weight)
        # Check for structured content, proper formatting, etc.
        content_score = 0.5
        if "#" in content:  # Has headings
            content_score += 0.2
        if "- " in content:  # Has lists
            content_score += 0.2
        if len(re.findall(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", content, re.IGNORECASE)) > 0:
            content_score += 0.1  # Has email
        score += min(1.0, content_score) * 0.1
        
        return min(1.0, score)

    def compress_memory(self, memory: Dict[str, Any], compression_level: float = 0.5) -> str:
        """Compress a memory based on its importance."""
        content = memory["content"]
        frontmatter = memory["frontmatter"]
        
        # Extract key sentences
        sentences = re.split(r'[.!?]+', content)
        key_sentences = []
        
        # Priority sentences: those with important keywords
        important_keywords = {
            "must", "need", "require", "important", "critical", "essential",
            "deadline", "date", "time", "meeting", "appointment",
            "contact", "email", "phone", "address",
            "decision", "agreement", "conclusion", "result"
        }
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check if sentence contains important keywords
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in important_keywords):
                key_sentences.append(sentence)
            # Also include the first sentence as it often contains the main idea
            elif len(key_sentences) == 0:
                key_sentences.append(sentence)
        
        # Compress based on importance and compression level
        if memory["importance_score"] > 0.7:
            # High importance: keep most content
            compressed_content = content
        elif memory["importance_score"] > 0.4:
            # Medium importance: keep key sentences
            compressed_content = ". ".join(key_sentences) + "."
        else:
            # Low importance: keep only the most essential information
            if key_sentences:
                compressed_content = key_sentences[0] + "."
            else:
                # If no key sentences found, keep a very brief summary
                words = content.split()
                if len(words) > 20:
                    compressed_content = " ".join(words[:20]) + "..."
                else:
                    compressed_content = content
        
        # Reconstruct the memory with compressed content
        frontmatter_str = "---\n"
        for key, value in frontmatter.items():
            frontmatter_str += f"{key}: {value}\n"
        if memory["tags"]:
            frontmatter_str += f"tags: {', '.join(memory['tags'])}\n"
        frontmatter_str += "---\n"
        
        return frontmatter_str + compressed_content

    def compress_all_memories(self, output_dir: Path, threshold: float = 0.5):
        """Compress all memories below the importance threshold."""
        # Create output directory if it doesn't exist
        output_dir.mkdir(exist_ok=True)
        
        compressed_count = 0
        kept_count = 0
        total_size_before = 0
        total_size_after = 0
        
        for file_name, memory in self.memories.items():
            total_size_before += memory["size_bytes"]
            
            if memory["importance_score"] < threshold:
                # Compress the memory
                compressed_content = self.compress_memory(memory)
                compressed_path = output_dir / file_name
                compressed_path.write_text(compressed_content, encoding="utf-8")
                compressed_size = len(compressed_content.encode("utf-8"))
                total_size_after += compressed_size
                compressed_count += 1
                print(f"Compressed: {file_name} ({memory['size_bytes']} → {compressed_size} bytes)")
            else:
                # Keep the original memory
                src_path = Path(memory["path"])
                dst_path = output_dir / src_path.name
                dst_path.write_text(memory["text"], encoding="utf-8")
                total_size_after += memory["size_bytes"]
                kept_count += 1
                print(f"Kept: {file_name}")
        
        # Generate compression report
        compression_ratio = (total_size_before - total_size_after) / total_size_before * 100 if total_size_before > 0 else 0
        
        report = {
            "total_memories": len(self.memories),
            "compressed_count": compressed_count,
            "kept_count": kept_count,
            "total_size_before": total_size_before,
            "total_size_after": total_size_after,
            "compression_ratio": compression_ratio
        }
        
        return report

    def generate_compression_report(self, threshold: float = 0.5) -> Dict[str, Any]:
        """Generate a compression report without actually compressing."""
        compressible_memories = []
        total_size_before = 0
        estimated_size_after = 0
        
        for file_name, memory in self.memories.items():
            total_size_before += memory["size_bytes"]
            
            if memory["importance_score"] < threshold:
                # Estimate compressed size
                compressed_content = self.compress_memory(memory)
                estimated_size = len(compressed_content.encode("utf-8"))
                estimated_size_after += estimated_size
                compressible_memories.append({
                    "file_name": file_name,
                    "importance_score": memory["importance_score"],
                    "size_before": memory["size_bytes"],
                    "estimated_size_after": estimated_size
                })
            else:
                estimated_size_after += memory["size_bytes"]
        
        compression_ratio = (total_size_before - estimated_size_after) / total_size_before * 100 if total_size_before > 0 else 0
        
        return {
            "total_memories": len(self.memories),
            "compressible_count": len(compressible_memories),
            "total_size_before": total_size_before,
            "estimated_size_after": estimated_size_after,
            "compression_ratio": compression_ratio,
            "compressible_memories": compressible_memories
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True)
    parser.add_argument("--output-dir", help="Directory to write compressed memories")
    parser.add_argument("--threshold", type=float, default=0.5, help="Importance threshold for compression")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    memory_root = Path(args.memory_root).expanduser()
    compressor = MemoryCompressor(memory_root)
    
    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser()
        report = compressor.compress_all_memories(output_dir, args.threshold)
    else:
        report = compressor.generate_compression_report(args.threshold)
    
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("Memory compression report:")
        print("=" * 80)
        print(f"Total memories: {report['total_memories']}")
        if "compressible_count" in report:
            print(f"Compressible memories: {report['compressible_count']}")
        if "compressed_count" in report:
            print(f"Compressed memories: {report['compressed_count']}")
            print(f"Kept memories: {report['kept_count']}")
        print(f"Size before: {report['total_size_before']} bytes")
        if "estimated_size_after" in report:
            print(f"Estimated size after: {report['estimated_size_after']} bytes")
        if "total_size_after" in report:
            print(f"Actual size after: {report['total_size_after']} bytes")
        print(f"Compression ratio: {report['compression_ratio']:.2f}%")
        
        if "compressible_memories" in report:
            print()
            print("Compressible memories:")
            print("-" * 80)
            for item in report['compressible_memories']:
                print(f"{item['file_name']}")
                print(f"  Importance: {item['importance_score']:.2f}")
                print(f"  Size: {item['size_before']} → {item['estimated_size_after']} bytes")
                print()
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
