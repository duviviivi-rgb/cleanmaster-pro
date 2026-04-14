#!/usr/bin/env python3
"""Real-time behavior tracking system for memory recommendations."""

from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Try to import optional dependencies
try:
    import threading
    has_threading = True
except ImportError:
    has_threading = False

try:
    import queue
    has_queue = True
except ImportError:
    has_queue = False

from memory_recommender import MemoryRecommender
from memory_ml import MemoryML


class MemoryTracker:
    """Real-time behavior tracking system."""
    
    def __init__(self, memory_root: Path, behavior_db_path: Path, model_path: Path):
        self.memory_root = memory_root
        self.behavior_db_path = behavior_db_path
        self.model_path = model_path
        self.behavior_db: Dict[str, List[Dict[str, Any]]] = {}
        self.recommender = MemoryRecommender(memory_root, behavior_db_path)
        self.memory_ml = MemoryML(memory_root, model_path)
        self.logger = logging.getLogger("MemoryTracker")
        self._load_behavior_db()
        
        # Initialize queue for real-time processing
        if has_queue:
            self.queue = queue.Queue()
        else:
            self.queue = []
        
        # Start processing thread
        if has_threading:
            self.running = True
            self.thread = threading.Thread(target=self._process_queue, daemon=True)
            self.thread.start()
        
    def _load_behavior_db(self):
        """Load behavior database."""
        if self.behavior_db_path.exists():
            try:
                with open(self.behavior_db_path, "r", encoding="utf-8") as f:
                    self.behavior_db = json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading behavior database: {e}")
                self.behavior_db = {}
    
    def _save_behavior_db(self):
        """Save behavior database."""
        try:
            with open(self.behavior_db_path, "w", encoding="utf-8") as f:
                json.dump(self.behavior_db, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving behavior database: {e}")
    
    def record_behavior(self, memory_id: str, action: str, context: Optional[str] = None, user_id: Optional[str] = None):
        """Record user behavior."""
        behavior_entry = {
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "user_id": user_id
        }
        
        # Add to queue for real-time processing
        if has_queue:
            self.queue.put((memory_id, behavior_entry))
        else:
            self.queue.append((memory_id, behavior_entry))
        
        # Process immediately if no threading
        if not has_threading:
            self._process_queue()
    
    def _process_queue(self):
        """Process behavior queue."""
        while has_threading and self.running:
            try:
                if has_queue:
                    if not self.queue.empty():
                        memory_id, behavior_entry = self.queue.get(block=False)
                        self._process_behavior(memory_id, behavior_entry)
                        self.queue.task_done()
                    else:
                        time.sleep(0.1)
                else:
                    if self.queue:
                        memory_id, behavior_entry = self.queue.pop(0)
                        self._process_behavior(memory_id, behavior_entry)
                    else:
                        time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Error processing queue: {e}")
                time.sleep(0.1)
        
        # Process remaining items when stopping
        if not has_threading:
            while self.queue:
                try:
                    memory_id, behavior_entry = self.queue.pop(0)
                    self._process_behavior(memory_id, behavior_entry)
                except Exception as e:
                    self.logger.error(f"Error processing queue: {e}")
    
    def _process_behavior(self, memory_id: str, behavior_entry: Dict[str, Any]):
        """Process a single behavior entry."""
        try:
            # Add to behavior database
            if memory_id not in self.behavior_db:
                self.behavior_db[memory_id] = []
            self.behavior_db[memory_id].append(behavior_entry)
            
            # Save to disk
            self._save_behavior_db()
            
            # Update recommendations
            self.update_recommendations(behavior_entry.get("context"))
            
            self.logger.info(f"Recorded behavior: {behavior_entry['action']} on {memory_id}")
        except Exception as e:
            self.logger.error(f"Error processing behavior: {e}")
    
    def update_recommendations(self, context: Optional[str] = None):
        """Update recommendations based on recent behavior."""
        try:
            # Get updated recommendations
            recommendations = self.memory_ml.get_recommended_memories(context, 5)
            self.logger.info(f"Updated recommendations: {[m.get('title', 'Untitled') for m in recommendations]}")
            return recommendations
        except Exception as e:
            self.logger.error(f"Error updating recommendations: {e}")
            return []
    
    def get_behavior_stats(self, memory_id: Optional[str] = None, time_range: Optional[int] = 24) -> Dict[str, Any]:
        """Get behavior statistics."""
        stats = {
            "total_actions": 0,
            "action_counts": {},
            "recent_actions": []
        }
        
        cutoff_time = datetime.now().timestamp() - (time_range * 3600)  # Default to last 24 hours
        
        memories_to_process = [memory_id] if memory_id else self.behavior_db.keys()
        
        for mid in memories_to_process:
            if mid not in self.behavior_db:
                continue
            
            for behavior in self.behavior_db[mid]:
                behavior_time = datetime.fromisoformat(behavior["timestamp"].replace("Z", "+00:00")).timestamp()
                if behavior_time >= cutoff_time:
                    stats["total_actions"] += 1
                    action = behavior["action"]
                    stats["action_counts"][action] = stats["action_counts"].get(action, 0) + 1
                    stats["recent_actions"].append({
                        "memory_id": mid,
                        "action": action,
                        "timestamp": behavior["timestamp"],
                        "context": behavior.get("context")
                    })
        
        # Sort recent actions by timestamp
        stats["recent_actions"].sort(key=lambda x: x["timestamp"], reverse=True)
        
        return stats
    
    def get_user_stats(self, user_id: str, time_range: Optional[int] = 24) -> Dict[str, Any]:
        """Get user behavior statistics."""
        stats = {
            "total_actions": 0,
            "action_counts": {},
            "memory_interactions": {},
            "recent_actions": []
        }
        
        cutoff_time = datetime.now().timestamp() - (time_range * 3600)  # Default to last 24 hours
        
        for memory_id, behaviors in self.behavior_db.items():
            for behavior in behaviors:
                if behavior.get("user_id") == user_id:
                    behavior_time = datetime.fromisoformat(behavior["timestamp"].replace("Z", "+00:00")).timestamp()
                    if behavior_time >= cutoff_time:
                        stats["total_actions"] += 1
                        action = behavior["action"]
                        stats["action_counts"][action] = stats["action_counts"].get(action, 0) + 1
                        stats["memory_interactions"][memory_id] = stats["memory_interactions"].get(memory_id, 0) + 1
                        stats["recent_actions"].append({
                            "memory_id": memory_id,
                            "action": action,
                            "timestamp": behavior["timestamp"],
                            "context": behavior.get("context")
                        })
        
        # Sort recent actions by timestamp
        stats["recent_actions"].sort(key=lambda x: x["timestamp"], reverse=True)
        
        return stats
    
    def stop(self):
        """Stop the behavior tracker."""
        if has_threading:
            self.running = False
            self.thread.join(timeout=2.0)
        self.logger.info("Behavior tracker stopped")


class RealTimeRecommender:
    """Real-time memory recommender."""
    
    def __init__(self, memory_root: Path, behavior_db_path: Path, model_path: Path):
        self.tracker = MemoryTracker(memory_root, behavior_db_path, model_path)
        self.logger = logging.getLogger("RealTimeRecommender")
    
    def get_recommendations(self, context: Optional[str] = None, user_id: Optional[str] = None, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get real-time recommendations."""
        try:
            # Get base recommendations
            recommendations = self.tracker.memory_ml.get_recommended_memories(context, top_n)
            
            # Adjust based on user behavior
            if user_id:
                user_stats = self.tracker.get_user_stats(user_id)
                # Weight memories based on user interaction frequency
                for memory in recommendations:
                    memory_id = memory["path"].split("\\")[-1]
                    interaction_count = user_stats["memory_interactions"].get(memory_id, 0)
                    # Boost score based on interaction count
                    memory["recommendation_score"] *= (1 + interaction_count * 0.1)
                # Re-sort based on adjusted scores
                recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
            
            return recommendations
        except Exception as e:
            self.logger.error(f"Error getting real-time recommendations: {e}")
            return []
    
    def record_interaction(self, memory_id: str, action: str, context: Optional[str] = None, user_id: Optional[str] = None):
        """Record user interaction with memory."""
        self.tracker.record_behavior(memory_id, action, context, user_id)
    
    def get_behavior_insights(self, time_range: Optional[int] = 24) -> Dict[str, Any]:
        """Get behavior insights."""
        try:
            # Get overall stats
            stats = self.tracker.get_behavior_stats(time_range=time_range)
            
            # Get most interacted memories
            most_interacted = sorted(
                stats["action_counts"].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
            
            # Get recent activity
            recent_activity = stats["recent_actions"][:10]
            
            return {
                "total_actions": stats["total_actions"],
                "most_common_actions": most_interacted,
                "recent_activity": recent_activity
            }
        except Exception as e:
            self.logger.error(f"Error getting behavior insights: {e}")
            return {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--behavior-db", default=".behavior_db.json", help="Path to behavior database")
    parser.add_argument("--model-path", default=".memory_ml_model.pkl", help="Path to ML model")
    parser.add_argument("--record", action="store_true", help="Record behavior")
    parser.add_argument("--memory-id", help="Memory ID for behavior recording")
    parser.add_argument("--action", help="Action for behavior recording")
    parser.add_argument("--context", help="Context for behavior recording")
    parser.add_argument("--user-id", help="User ID for behavior recording")
    parser.add_argument("--stats", action="store_true", help="Get behavior statistics")
    parser.add_argument("--recommend", action="store_true", help="Get real-time recommendations")
    parser.add_argument("--top-n", type=int, default=5, help="Number of recommendations")
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
    model_path = Path(args.model_path).expanduser()
    
    # Initialize real-time recommender
    recommender = RealTimeRecommender(memory_root, behavior_db_path, model_path)
    
    if args.record and args.memory_id and args.action:
        # Record behavior
        recommender.record_interaction(args.memory_id, args.action, args.context, args.user_id)
        print(f"Recorded interaction: {args.action} on {args.memory_id}")
    elif args.stats:
        # Get behavior statistics
        insights = recommender.get_behavior_insights()
        print(json.dumps(insights, indent=2, ensure_ascii=False))
    elif args.recommend:
        # Get real-time recommendations
        recommendations = recommender.get_recommendations(args.context, args.user_id, args.top_n)
        print(json.dumps(recommendations, indent=2, ensure_ascii=False))
    else:
        print("Please specify an action: --record, --stats, or --recommend")
    
    # Stop the tracker
    recommender.tracker.stop()
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
