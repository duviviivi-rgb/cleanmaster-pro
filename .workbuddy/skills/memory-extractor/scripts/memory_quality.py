#!/usr/bin/env python3
"""Evaluate memory quality based on recency, consistency, completeness, and relevance."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


class MemoryQualityEvaluator:
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
                
                # Extract date information
                created_date = None
                if "created" in frontmatter:
                    try:
                        created_date = datetime.fromisoformat(frontmatter["created"])
                    except ValueError:
                        pass
                
                # Extract tags
                tags = frontmatter.get("tags", "").split(",") if "tags" in frontmatter else []
                tags = [tag.strip() for tag in tags if tag.strip()]
                
                self.memories[path.name] = {
                    "path": str(path),
                    "text": text,
                    "frontmatter": frontmatter,
                    "created_date": created_date,
                    "modified_date": datetime.fromtimestamp(path.stat().st_mtime),
                    "tags": tags,
                    "size_bytes": path.stat().st_size
                }
                
            except Exception as e:
                print(f"Error loading {path}: {e}")

    def evaluate_recency(self, memory: Dict[str, Any]) -> float:
        """Evaluate how recent the memory is (0-1)."""
        if memory["created_date"]:
            age_days = (datetime.now() - memory["created_date"]).days
        else:
            age_days = (datetime.now() - memory["modified_date"]).days
        
        # Memories less than a week old get 1.0
        # Memories older than 6 months get 0.0
        if age_days < 7:
            return 1.0
        elif age_days > 180:
            return 0.0
        else:
            return 1.0 - (age_days - 7) / (180 - 7)

    def evaluate_consistency(self, memory: Dict[str, Any]) -> float:
        """Evaluate how consistent the memory is with others (0-1)."""
        # Look for conflicting information
        conflicts = 0
        checks = 0
        
        # Extract key information from the memory
        title = memory["frontmatter"].get("title", "")
        content = memory["text"]
        
        # Check against other memories
        for other_name, other_memory in self.memories.items():
            if other_name == memory["path"].split("\\")[-1]:
                continue
            
            # Check for conflicting titles or content
            other_title = other_memory["frontmatter"].get("title", "")
            other_content = other_memory["text"]
            
            # Simple conflict detection: same title but different content
            if title and title == other_title:
                checks += 1
                if content != other_content:
                    conflicts += 1
        
        if checks == 0:
            return 1.0
        else:
            return max(0.0, 1.0 - conflicts / checks)

    def evaluate_completeness(self, memory: Dict[str, Any]) -> float:
        """Evaluate how complete the memory is (0-1)."""
        text = memory["text"]
        frontmatter = memory["frontmatter"]
        
        # Check for essential fields
        essential_fields = ["title", "type"]
        missing_fields = 0
        for field in essential_fields:
            if field not in frontmatter:
                missing_fields += 1
        
        # Check content length
        content_length = len(text)
        if content_length < 50:
            length_score = 0.0
        elif content_length > 500:
            length_score = 1.0
        else:
            length_score = content_length / 500
        
        # Calculate completeness score
        field_score = max(0.0, 1.0 - missing_fields / len(essential_fields))
        return (field_score + length_score) / 2

    def evaluate_relevance(self, memory: Dict[str, Any], context: str = "") -> float:
        """Evaluate how relevant the memory is to the given context (0-1)."""
        if not context:
            return 0.5  # Default relevance if no context provided
        
        # Check for keyword matches
        text = memory["text"].lower()
        context_words = context.lower().split()
        
        matches = 0
        for word in context_words:
            if word in text:
                matches += 1
        
        if not context_words:
            return 0.5
        else:
            return min(1.0, matches / len(context_words))

    def evaluate_memory(self, memory: Dict[str, Any], context: str = "") -> Dict[str, float]:
        """Evaluate a single memory."""
        return {
            "recency": self.evaluate_recency(memory),
            "consistency": self.evaluate_consistency(memory),
            "completeness": self.evaluate_completeness(memory),
            "relevance": self.evaluate_relevance(memory, context),
            "overall": self.calculate_overall_score(memory, context)
        }

    def calculate_overall_score(self, memory: Dict[str, Any], context: str = "") -> float:
        """Calculate overall quality score."""
        recency = self.evaluate_recency(memory)
        consistency = self.evaluate_consistency(memory)
        completeness = self.evaluate_completeness(memory)
        relevance = self.evaluate_relevance(memory, context)
        
        # Weigh recency and consistency higher
        weights = {
            "recency": 0.3,
            "consistency": 0.3,
            "completeness": 0.2,
            "relevance": 0.2
        }
        
        return (
            recency * weights["recency"] +
            consistency * weights["consistency"] +
            completeness * weights["completeness"] +
            relevance * weights["relevance"]
        )

    def evaluate_all_memories(self, context: str = "") -> Dict[str, Dict[str, float]]:
        """Evaluate all memories."""
        results = {}
        for name, memory in self.memories.items():
            results[name] = self.evaluate_memory(memory, context)
        return results

    def get_low_quality_memories(self, threshold: float = 0.5) -> List[Tuple[str, float]]:
        """Get memories with quality score below threshold."""
        results = []
        evaluations = self.evaluate_all_memories()
        for name, scores in evaluations.items():
            if scores["overall"] < threshold:
                results.append((name, scores["overall"]))
        return sorted(results, key=lambda x: x[1])

    def get_high_quality_memories(self, threshold: float = 0.8) -> List[Tuple[str, float]]:
        """Get memories with quality score above threshold."""
        results = []
        evaluations = self.evaluate_all_memories()
        for name, scores in evaluations.items():
            if scores["overall"] > threshold:
                results.append((name, scores["overall"]))
        return sorted(results, key=lambda x: x[1], reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True)
    parser.add_argument("--context", default="", help="Context for relevance evaluation")
    parser.add_argument("--threshold", type=float, default=0.5, help="Quality threshold for low-quality memories")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    memory_root = Path(args.memory_root).expanduser()
    evaluator = MemoryQualityEvaluator(memory_root)
    
    # Evaluate all memories
    evaluations = evaluator.evaluate_all_memories(args.context)
    
    # Get low and high quality memories
    low_quality = evaluator.get_low_quality_memories(args.threshold)
    high_quality = evaluator.get_high_quality_memories()
    
    if args.json:
        output = {
            "evaluations": evaluations,
            "low_quality": low_quality,
            "high_quality": high_quality
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("Memory quality evaluations:")
        print("=" * 80)
        
        for name, scores in evaluations.items():
            print(f"Memory: {name}")
            print(f"  Overall: {scores['overall']:.2f}")
            print(f"  Recency: {scores['recency']:.2f}")
            print(f"  Consistency: {scores['consistency']:.2f}")
            print(f"  Completeness: {scores['completeness']:.2f}")
            print(f"  Relevance: {scores['relevance']:.2f}")
            print()
        
        print("Low quality memories:")
        print("-" * 40)
        for name, score in low_quality:
            print(f"- {name}: {score:.2f}")
        
        print()
        print("High quality memories:")
        print("-" * 40)
        for name, score in high_quality:
            print(f"- {name}: {score:.2f}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
