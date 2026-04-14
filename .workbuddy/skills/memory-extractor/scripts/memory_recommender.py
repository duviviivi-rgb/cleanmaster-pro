#!/usr/bin/env python3
"""Intelligent memory recommendation system based on user behavior and context."""

from __future__ import annotations

import argparse
import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from memory_index import MemoryIndex
from memory_graph import MemoryGraph


class MemoryRecommender:
    """Intelligent memory recommendation system."""
    
    def __init__(self, memory_root: Path, behavior_db_path: Path):
        self.memory_root = memory_root
        self.behavior_db_path = behavior_db_path
        self.behavior_db: Dict[str, List[Dict[str, Any]]] = {}
        self.index = MemoryIndex(memory_root)
        self.graph = MemoryGraph(memory_root)
        self.logger = logging.getLogger("MemoryRecommender")
        self._load_behavior_db()
    
    def _load_behavior_db(self):
        """Load user behavior database."""
        if self.behavior_db_path.exists():
            try:
                with open(self.behavior_db_path, "r", encoding="utf-8") as f:
                    self.behavior_db = json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading behavior database: {e}")
                self.behavior_db = {}
    
    def _save_behavior_db(self):
        """Save user behavior database."""
        try:
            with open(self.behavior_db_path, "w", encoding="utf-8") as f:
                json.dump(self.behavior_db, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving behavior database: {e}")
    
    def record_behavior(self, memory_id: str, action: str, context: Optional[str] = None):
        """Record user behavior."""
        if memory_id not in self.behavior_db:
            self.behavior_db[memory_id] = []
        
        behavior_entry = {
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "context": context
        }
        
        self.behavior_db[memory_id].append(behavior_entry)
        self._save_behavior_db()
        self.logger.info(f"Recorded behavior: {action} on {memory_id}")
    
    def get_memory_usage_score(self, memory_id: str) -> float:
        """Calculate memory usage score based on user behavior."""
        if memory_id not in self.behavior_db:
            return 0.0
        
        behaviors = self.behavior_db[memory_id]
        score = 0.0
        
        # Weight recent actions more heavily
        now = datetime.now()
        for behavior in behaviors:
            behavior_time = datetime.fromisoformat(behavior["timestamp"])
            time_diff = (now - behavior_time).total_seconds() / 3600  # Hours
            
            # Decay factor: older actions have less weight
            decay = max(0.1, 1.0 - time_diff / 168)  # 1 week decay
            
            # Action weight
            action_weight = {
                "view": 0.1,
                "edit": 0.5,
                "search": 0.2,
                "share": 0.8,
                "delete": -0.5
            }.get(behavior["action"], 0.1)
            
            score += action_weight * decay
        
        return score
    
    def get_context_similarity(self, memory: Dict[str, Any], context: str) -> float:
        """Calculate similarity between memory and context."""
        if not context:
            return 0.0
        
        # Extract text from memory
        memory_text = str(memory.get("title", "")) + " " + str(memory.get("description", ""))
        if "content" in memory and memory["content"]:
            memory_text += " " + str(memory["content"])
        
        # Simple keyword matching
        context_words = set(re.findall(r"\b\w+\b", context.lower()))
        memory_words = set(re.findall(r"\b\w+\b", memory_text.lower()))
        
        if not context_words:
            return 0.0
        
        common_words = context_words.intersection(memory_words)
        return len(common_words) / len(context_words)
    
    def get_recommendations(self, context: Optional[str] = None, top_n: int = 5) -> List[Tuple[str, float]]:
        """Get memory recommendations based on user behavior and context."""
        memories = self.index.get_manifest()
        scores = []
        
        for memory in memories:
            memory_id = memory["path"].split("\\")[-1]
            
            # Calculate usage score
            usage_score = self.get_memory_usage_score(memory_id)
            
            # Calculate context similarity
            context_score = self.get_context_similarity(memory, context or "")
            
            # Calculate relatedness score
            related_score = 0.0
            related_memories = self.graph.get_related_memories(memory_id, 3)
            for rel_memory, weight in related_memories:
                rel_usage_score = self.get_memory_usage_score(rel_memory)
                related_score += weight * rel_usage_score
            
            # Calculate final score
            final_score = (
                usage_score * 0.4 +  # Weight usage history
                context_score * 0.4 +  # Weight context similarity
                related_score * 0.2  # Weight related memories
            )
            
            scores.append((memory_id, final_score))
        
        # Sort by score and return top N
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]
    
    def get_recommended_memories(self, context: Optional[str] = None, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get recommended memories with details."""
        recommendations = self.get_recommendations(context, top_n)
        recommended_memories = []
        
        for memory_id, score in recommendations:
            # Find the memory in the index
            for memory in self.index.get_manifest():
                if memory["path"].split("\\")[-1] == memory_id:
                    memory_with_score = memory.copy()
                    memory_with_score["recommendation_score"] = score
                    recommended_memories.append(memory_with_score)
                    break
        
        return recommended_memories
    
    def update_recommendations(self, context: Optional[str] = None):
        """Update recommendations based on current context."""
        recommendations = self.get_recommended_memories(context)
        self.logger.info(f"Updated recommendations: {[m['title'] for m in recommendations]}")
        return recommendations


class MemoryContextAnalyzer:
    """Analyze context to improve memory recommendations."""
    
    def __init__(self):
        self.logger = logging.getLogger("MemoryContextAnalyzer")
    
    def analyze_text_context(self, text: str) -> Dict[str, Any]:
        """Analyze text context."""
        # Extract keywords
        keywords = set(re.findall(r"\b\w+\b", text.lower()))
        
        # Filter stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did"
        }
        keywords = {word for word in keywords if len(word) > 2 and word not in stop_words}
        
        # Extract entities (simple approach)
        entities = set()
        # Look for proper nouns (capitalized words)
        proper_nouns = re.findall(r"\b[A-Z][a-z]+\b", text)
        entities.update(proper_nouns)
        
        return {
            "keywords": list(keywords),
            "entities": list(entities),
            "context_length": len(text)
        }
    
    def analyze_conversation_context(self, conversation: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze conversation context."""
        # Combine all messages
        full_text = " ".join([msg.get("content", "") for msg in conversation])
        
        # Analyze text context
        text_context = self.analyze_text_context(full_text)
        
        # Additional conversation-specific analysis
        user_messages = [msg for msg in conversation if msg.get("role") == "user"]
        assistant_messages = [msg for msg in conversation if msg.get("role") == "assistant"]
        
        return {
            **text_context,
            "user_message_count": len(user_messages),
            "assistant_message_count": len(assistant_messages),
            "total_messages": len(conversation)
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--behavior-db", default=".behavior_db.json", help="Path to behavior database")
    parser.add_argument("--context", help="Context for recommendations")
    parser.add_argument("--top-n", type=int, default=5, help="Number of recommendations")
    parser.add_argument("--record", action="store_true", help="Record behavior")
    parser.add_argument("--memory-id", help="Memory ID for behavior recording")
    parser.add_argument("--action", help="Action for behavior recording")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    memory_root = Path(args.memory_root).expanduser()
    behavior_db_path = Path(args.behavior_db).expanduser()
    
    # Initialize recommender
    recommender = MemoryRecommender(memory_root, behavior_db_path)
    
    if args.record and args.memory_id and args.action:
        # Record behavior
        recommender.record_behavior(args.memory_id, args.action, args.context)
        print(f"Recorded behavior: {args.action} on {args.memory_id}")
    else:
        # Get recommendations
        recommendations = recommender.get_recommended_memories(args.context, args.top_n)
        print(json.dumps(recommendations, indent=2, ensure_ascii=False))
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
