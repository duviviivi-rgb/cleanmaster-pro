#!/usr/bin/env python3
"""Memory context compressor for WorkBuddy."""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class MemoryContextCompressor:
    """Compress memory context to reduce memory usage and improve system response speed."""
    
    def __init__(self, memory_root: Path):
        self.memory_root = memory_root
        self.config_path = memory_root / ".context_compress_config.json"
        self.config = self._load_config()
        self.logger = logging.getLogger("MemoryContextCompressor")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load compression configuration."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading compression config: {e}")
        return {
            "compression_level": "medium",  # low, medium, high
            "min_compression_size": 1024,  # Minimum size to compress (bytes)
            "preserve_keywords": True,
            "preserve_headers": True,
            "preserve_links": True,
            "max_compression_ratio": 0.3,  # Maximum compression ratio (30%)
            "compression_stats": {}
        }
    
    def _save_config(self):
        """Save compression configuration."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving compression config: {e}")
    
    def compress_memory(self, memory_path: Path) -> Dict[str, Any]:
        """Compress a single memory file."""
        try:
            # Check if file is large enough to compress
            if memory_path.stat().st_size < self.config["min_compression_size"]:
                return {
                    "status": "skipped",
                    "reason": "File too small",
                    "original_size": memory_path.stat().st_size,
                    "compressed_size": memory_path.stat().st_size
                }
            
            # Read the file
            content = memory_path.read_text(encoding="utf-8")
            original_size = len(content)
            
            # Compress the content
            compressed_content = self._compress_content(content)
            compressed_size = len(compressed_content)
            
            # Calculate compression ratio
            compression_ratio = compressed_size / original_size
            
            # Check if compression is effective
            if compression_ratio > self.config["max_compression_ratio"]:
                return {
                    "status": "skipped",
                    "reason": "Compression not effective",
                    "original_size": original_size,
                    "compressed_size": compressed_size,
                    "compression_ratio": compression_ratio
                }
            
            # Write the compressed content back
            memory_path.write_text(compressed_content, encoding="utf-8")
            
            # Update compression stats
            self.config["compression_stats"][memory_path.name] = {
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_ratio": compression_ratio,
                "timestamp": str(memory_path.stat().st_mtime)
            }
            self._save_config()
            
            return {
                "status": "compressed",
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_ratio": compression_ratio
            }
        except Exception as e:
            self.logger.error(f"Error compressing {memory_path}: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def compress_all_memories(self) -> Dict[str, Any]:
        """Compress all memory files."""
        results = {
            "total": 0,
            "compressed": 0,
            "skipped": 0,
            "errors": 0,
            "details": {}
        }
        
        for memory_path in self.memory_root.glob("*.md"):
            if memory_path.name == "MEMORY.md":
                continue
            
            results["total"] += 1
            result = self.compress_memory(memory_path)
            results["details"][memory_path.name] = result
            
            if result["status"] == "compressed":
                results["compressed"] += 1
            elif result["status"] == "skipped":
                results["skipped"] += 1
            elif result["status"] == "error":
                results["errors"] += 1
        
        return results
    
    def _compress_content(self, content: str) -> str:
        """Compress content intelligently."""
        # Preserve frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        frontmatter = ""
        body = content
        
        if frontmatter_match:
            frontmatter = frontmatter_match.group(0)
            body = content[frontmatter_match.end():]
        
        # Compress body
        compressed_body = self._compress_body(body)
        
        # Reassemble content
        return frontmatter + compressed_body
    
    def _compress_body(self, body: str) -> str:
        """Compress the body of the content."""
        # Split into paragraphs
        paragraphs = body.split("\n\n")
        compressed_paragraphs = []
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                compressed_paragraphs.append(paragraph)
                continue
            
            # Compress paragraph based on compression level
            if self.config["compression_level"] == "low":
                compressed = self._compress_low(paragraph)
            elif self.config["compression_level"] == "high":
                compressed = self._compress_high(paragraph)
            else:  # medium
                compressed = self._compress_medium(paragraph)
            
            compressed_paragraphs.append(compressed)
        
        return "\n\n".join(compressed_paragraphs)
    
    def _compress_low(self, text: str) -> str:
        """Low level compression: remove extra whitespace."""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove trailing whitespace
        text = re.sub(r"\s+$|^\s+", "", text)
        return text
    
    def _compress_medium(self, text: str) -> str:
        """Medium level compression: remove extra whitespace and redundant phrases."""
        # Start with low compression
        text = self._compress_low(text)
        
        # Remove redundant phrases
        redundant_phrases = [
            "in order to", "due to the fact that", "the reason why",
            "it is important to note that", "it should be noted that",
            "in the event that", "with regard to", "with respect to"
        ]
        
        for phrase in redundant_phrases:
            text = text.replace(phrase, "")
        
        return text
    
    def _compress_high(self, text: str) -> str:
        """High level compression: remove extra whitespace, redundant phrases, and summarize."""
        # Start with medium compression
        text = self._compress_medium(text)
        
        # Split into sentences
        sentences = re.split(r"[.!?]+\s*", text)
        sentences = [s for s in sentences if s.strip()]
        
        # If there are too many sentences, summarize
        if len(sentences) > 5:
            # Simple summarization: keep first and last sentences, and key sentences
            key_sentences = [sentences[0]]
            
            # Keep sentences that contain keywords
            keywords = self._extract_keywords(text)
            for sentence in sentences[1:-1]:
                if any(keyword in sentence.lower() for keyword in keywords):
                    key_sentences.append(sentence)
            
            if sentences:
                key_sentences.append(sentences[-1])
            
            # Join key sentences
            text = ". ".join(key_sentences) + "."
        
        return text
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text."""
        # Remove punctuation
        text = re.sub(r"[.!?,;:()\[\]{}]", " ", text)
        # Split into words
        words = text.lower().split()
        # Filter stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did"
        }
        # Filter short words and stop words
        keywords = {word for word in words if len(word) > 3 and word not in stop_words}
        return keywords
    
    def decompress_memory(self, memory_path: Path) -> Dict[str, Any]:
        """Decompress a memory file (if needed)."""
        try:
            # For now, we just return the original content
            # In a more advanced system, we could store compressed content with a marker
            content = memory_path.read_text(encoding="utf-8")
            return {
                "status": "success",
                "content": content
            }
        except Exception as e:
            self.logger.error(f"Error decompressing {memory_path}: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression statistics."""
        total_original = 0
        total_compressed = 0
        
        for stats in self.config["compression_stats"].values():
            total_original += stats.get("original_size", 0)
            total_compressed += stats.get("compressed_size", 0)
        
        if total_original > 0:
            overall_ratio = total_compressed / total_original
        else:
            overall_ratio = 0
        
        return {
            "total_files": len(self.config["compression_stats"]),
            "total_original_size": total_original,
            "total_compressed_size": total_compressed,
            "overall_compression_ratio": overall_ratio,
            "detailed_stats": self.config["compression_stats"]
        }
    
    def update_config(self, config: Dict[str, Any]):
        """Update compression configuration."""
        self.config.update(config)
        self._save_config()
        self.logger.info(f"Compression config updated: {config}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--action", choices=["compress", "decompress", "stats"], default="compress", help="Action to perform")
    parser.add_argument("--level", choices=["low", "medium", "high"], help="Compression level")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    memory_root = Path(args.memory_root).expanduser()
    compressor = MemoryContextCompressor(memory_root)
    
    # Update compression level if provided
    if args.level:
        compressor.update_config({"compression_level": args.level})
    
    # Perform action
    if args.action == "compress":
        result = compressor.compress_all_memories()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.action == "decompress":
        # Decompress all memories
        results = {}
        for memory_path in memory_root.glob("*.md"):
            if memory_path.name == "MEMORY.md":
                continue
            result = compressor.decompress_memory(memory_path)
            results[memory_path.name] = result
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.action == "stats":
        stats = compressor.get_compression_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
