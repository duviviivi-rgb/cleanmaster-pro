#!/usr/bin/env python3
"""Personalized memory recommendation system."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from memory_recommender import MemoryRecommender
from memory_ml import MemoryML
from memory_tracker import MemoryTracker


class UserProfile:
    """User profile for personalized recommendations."""
    
    def __init__(self, user_id: str, profile_path: Path):
        self.user_id = user_id
        self.profile_path = profile_path
        self.profile: Dict[str, Any] = {
            "user_id": user_id,
            "preferences": {},
            "interaction_history": {},
            "topic_interests": {},
            "recent_activities": [],
            "created_at": None,
            "updated_at": None
        }
        self.logger = logging.getLogger(f"UserProfile.{user_id}")
        self._load_profile()
    
    def _load_profile(self):
        """Load user profile from file."""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, "r", encoding="utf-8") as f:
                    self.profile = json.load(f)
                self.logger.info(f"Loaded profile for user {self.user_id}")
            except Exception as e:
                self.logger.error(f"Error loading user profile: {e}")
                # Reset to default profile
                self.profile = {
                    "user_id": self.user_id,
                    "preferences": {},
                    "interaction_history": {},
                    "topic_interests": {},
                    "recent_activities": [],
                    "created_at": None,
                    "updated_at": None
                }
    
    def _save_profile(self):
        """Save user profile to file."""
        try:
            import datetime
            self.profile["updated_at"] = datetime.datetime.now().isoformat()
            if not self.profile.get("created_at"):
                self.profile["created_at"] = self.profile["updated_at"]
            
            with open(self.profile_path, "w", encoding="utf-8") as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved profile for user {self.user_id}")
        except Exception as e:
            self.logger.error(f"Error saving user profile: {e}")
    
    def update_preference(self, key: str, value: Any):
        """Update user preference."""
        self.profile["preferences"][key] = value
        self._save_profile()
    
    def record_interaction(self, memory_id: str, action: str, context: Optional[str] = None):
        """Record user interaction with memory."""
        import datetime
        
        # Update interaction history
        if memory_id not in self.profile["interaction_history"]:
            self.profile["interaction_history"][memory_id] = {
                "total_interactions": 0,
                "last_interaction": None,
                "actions": {}
            }
        
        interaction = self.profile["interaction_history"][memory_id]
        interaction["total_interactions"] += 1
        interaction["last_interaction"] = datetime.datetime.now().isoformat()
        interaction["actions"][action] = interaction["actions"].get(action, 0) + 1
        
        # Update recent activities
        activity = {
            "memory_id": memory_id,
            "action": action,
            "timestamp": datetime.datetime.now().isoformat(),
            "context": context
        }
        self.profile["recent_activities"].insert(0, activity)
        # Keep only last 50 activities
        if len(self.profile["recent_activities"]) > 50:
            self.profile["recent_activities"] = self.profile["recent_activities"][:50]
        
        # Update topic interests based on memory content
        # (This would typically use NLP to extract topics from memory content)
        # For now, we'll use a simple approach based on tags
        
        self._save_profile()
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences."""
        return self.profile["preferences"]
    
    def get_interaction_history(self) -> Dict[str, Any]:
        """Get user interaction history."""
        return self.profile["interaction_history"]
    
    def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent user activities."""
        return self.profile["recent_activities"][:limit]
    
    def get_topic_interests(self) -> Dict[str, float]:
        """Get user topic interests."""
        return self.profile["topic_interests"]


class MemoryPersonalizer:
    """Personalized memory recommendation system."""
    
    def __init__(self, memory_root: Path, profiles_dir: Path, behavior_db_path: Path, model_path: Path):
        self.memory_root = memory_root
        self.profiles_dir = profiles_dir
        self.behavior_db_path = behavior_db_path
        self.model_path = model_path
        self.profiles: Dict[str, UserProfile] = {}
        self.recommender = MemoryRecommender(memory_root, behavior_db_path)
        self.memory_ml = MemoryML(memory_root, model_path)
        self.tracker = MemoryTracker(memory_root, behavior_db_path, model_path)
        self.logger = logging.getLogger("MemoryPersonalizer")
        self._ensure_profiles_dir()
    
    def _ensure_profiles_dir(self):
        """Ensure profiles directory exists."""
        self.profiles_dir.mkdir(exist_ok=True)
    
    def get_user_profile(self, user_id: str) -> UserProfile:
        """Get or create user profile."""
        if user_id not in self.profiles:
            profile_path = self.profiles_dir / f"{user_id}_profile.json"
            self.profiles[user_id] = UserProfile(user_id, profile_path)
        return self.profiles[user_id]
    
    def record_user_interaction(self, user_id: str, memory_id: str, action: str, context: Optional[str] = None):
        """Record user interaction with memory."""
        # Get user profile
        profile = self.get_user_profile(user_id)
        
        # Record interaction in profile
        profile.record_interaction(memory_id, action, context)
        
        # Record interaction in behavior tracker
        self.tracker.record_behavior(memory_id, action, context, user_id)
        
        self.logger.info(f"Recorded interaction: {action} on {memory_id} by user {user_id}")
    
    def get_personalized_recommendations(self, user_id: str, context: Optional[str] = None, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get personalized recommendations for user."""
        # Get user profile
        profile = self.get_user_profile(user_id)
        
        # Get base recommendations from ML model
        base_recommendations = self.memory_ml.get_recommended_memories(context, top_n * 2)  # Get more to personalize
        
        # Personalize recommendations
        personalized_recommendations = self._personalize_recommendations(base_recommendations, profile)
        
        # Return top N
        return personalized_recommendations[:top_n]
    
    def _personalize_recommendations(self, recommendations: List[Dict[str, Any]], profile: UserProfile) -> List[Dict[str, Any]]:
        """Personalize recommendations based on user profile."""
        # Get user preferences and interaction history
        preferences = profile.get_preferences()
        interaction_history = profile.get_interaction_history()
        
        # Score each recommendation
        scored_recommendations = []
        for memory in recommendations:
            memory_id = memory["path"].split("\\")[-1]
            score = memory.get("recommendation_score", 0.0)
            
            # Adjust score based on user interaction history
            if memory_id in interaction_history:
                interaction = interaction_history[memory_id]
                # Boost score based on total interactions
                score *= (1 + interaction["total_interactions"] * 0.1)
                # Boost score based on recent interaction
                import datetime
                last_interaction = interaction.get("last_interaction")
                if last_interaction:
                    last_interaction_time = datetime.datetime.fromisoformat(last_interaction.replace("Z", "+00:00"))
                    days_since_last = (datetime.datetime.now() - last_interaction_time).days
                    if days_since_last < 7:
                        # Recently interacted, boost more
                        score *= 1.2
            
            # Adjust score based on user preferences
            # Example: if user prefers certain types of memories
            memory_type = memory.get("type", "")
            if memory_type in preferences:
                score *= preferences[memory_type]
            
            # Adjust score based on file type
            file_type = memory.get("file_type", "text")
            if file_type in preferences:
                score *= preferences[file_type]
            
            memory["personalized_score"] = score
            scored_recommendations.append(memory)
        
        # Sort by personalized score
        scored_recommendations.sort(key=lambda x: x.get("personalized_score", 0.0), reverse=True)
        
        return scored_recommendations
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences."""
        profile = self.get_user_profile(user_id)
        for key, value in preferences.items():
            profile.update_preference(key, value)
        self.logger.info(f"Updated preferences for user {user_id}")
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get user insights."""
        profile = self.get_user_profile(user_id)
        
        # Get interaction statistics
        interaction_history = profile.get_interaction_history()
        total_interactions = sum(interaction["total_interactions"] for interaction in interaction_history.values())
        most_interacted_memories = sorted(
            interaction_history.items(),
            key=lambda x: x[1]["total_interactions"],
            reverse=True
        )[:5]
        
        # Get action statistics
        action_counts = {}
        for interaction in interaction_history.values():
            for action, count in interaction["actions"].items():
                action_counts[action] = action_counts.get(action, 0) + count
        
        # Get recent activities
        recent_activities = profile.get_recent_activities(10)
        
        # Get topic interests
        topic_interests = profile.get_topic_interests()
        
        return {
            "user_id": user_id,
            "total_interactions": total_interactions,
            "most_interacted_memories": most_interacted_memories,
            "action_counts": action_counts,
            "recent_activities": recent_activities,
            "topic_interests": topic_interests,
            "preferences": profile.get_preferences()
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--profiles-dir", default=".user_profiles", help="Path to user profiles directory")
    parser.add_argument("--behavior-db", default=".behavior_db.json", help="Path to behavior database")
    parser.add_argument("--model-path", default=".memory_ml_model.pkl", help="Path to ML model")
    parser.add_argument("--user-id", required=True, help="User ID")
    parser.add_argument("--recommend", action="store_true", help="Get personalized recommendations")
    parser.add_argument("--record", action="store_true", help="Record user interaction")
    parser.add_argument("--memory-id", help="Memory ID for interaction recording")
    parser.add_argument("--action", help="Action for interaction recording")
    parser.add_argument("--context", help="Context for recommendations or interaction")
    parser.add_argument("--update-preferences", action="store_true", help="Update user preferences")
    parser.add_argument("--preferences", help="User preferences as JSON")
    parser.add_argument("--insights", action="store_true", help="Get user insights")
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
    profiles_dir = Path(args.profiles_dir).expanduser()
    behavior_db_path = Path(args.behavior_db).expanduser()
    model_path = Path(args.model_path).expanduser()
    
    # Initialize memory personalizer
    personalizer = MemoryPersonalizer(memory_root, profiles_dir, behavior_db_path, model_path)
    
    if args.recommend:
        # Get personalized recommendations
        recommendations = personalizer.get_personalized_recommendations(args.user_id, args.context, args.top_n)
        print(json.dumps(recommendations, indent=2, ensure_ascii=False))
    elif args.record and args.memory_id and args.action:
        # Record user interaction
        personalizer.record_user_interaction(args.user_id, args.memory_id, args.action, args.context)
        print(f"Recorded interaction: {args.action} on {args.memory_id} by user {args.user_id}")
    elif args.update_preferences and args.preferences:
        # Update user preferences
        try:
            preferences = json.loads(args.preferences)
            personalizer.update_user_preferences(args.user_id, preferences)
            print(f"Updated preferences for user {args.user_id}")
        except json.JSONDecodeError as e:
            print(f"Error parsing preferences: {e}")
    elif args.insights:
        # Get user insights
        insights = personalizer.get_user_insights(args.user_id)
        print(json.dumps(insights, indent=2, ensure_ascii=False))
    else:
        print("Please specify an action: --recommend, --record, --update-preferences, or --insights")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
