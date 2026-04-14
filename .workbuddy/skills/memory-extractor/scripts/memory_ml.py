#!/usr/bin/env python3
"""Machine learning integration for memory recommendation."""

from __future__ import annotations

import argparse
import json
import logging
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Try to import optional dependencies
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    has_sklearn = True
except ImportError:
    has_sklearn = False

try:
    from sentence_transformers import SentenceTransformer
    has_sentence_transformers = True
except ImportError:
    has_sentence_transformers = False

from memory_index import MemoryIndex
from memory_graph import MemoryGraph
from memory_recommender import MemoryRecommender


class MemoryML:
    """Machine learning integration for memory recommendation."""
    
    def __init__(self, memory_root: Path, model_path: Path):
        self.memory_root = memory_root
        self.model_path = model_path
        self.vectorizer = None
        self.model = None
        self.sentence_model = None
        self.index = MemoryIndex(memory_root)
        self.graph = MemoryGraph(memory_root)
        self.logger = logging.getLogger("MemoryML")
        self._load_model()
    
    def _load_model(self):
        """Load trained model and vectorizer."""
        if self.model_path.exists():
            try:
                with open(self.model_path, "rb") as f:
                    data = pickle.load(f)
                    self.vectorizer = data.get("vectorizer")
                    self.model = data.get("model")
                    self.logger.info(f"Loaded model from {self.model_path}")
            except Exception as e:
                self.logger.error(f"Error loading model: {e}")
        
        # Load sentence transformer model if available
        if has_sentence_transformers:
            try:
                self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
                self.logger.info("Loaded sentence transformer model")
            except Exception as e:
                self.logger.error(f"Error loading sentence transformer: {e}")
    
    def _save_model(self):
        """Save trained model and vectorizer."""
        if self.model and self.vectorizer:
            try:
                data = {
                    "vectorizer": self.vectorizer,
                    "model": self.model
                }
                with open(self.model_path, "wb") as f:
                    pickle.dump(data, f)
                self.logger.info(f"Saved model to {self.model_path}")
            except Exception as e:
                self.logger.error(f"Error saving model: {e}")
    
    def _extract_features(self, memory: Dict[str, Any], context: Optional[str] = None) -> np.ndarray:
        """Extract features from memory and context."""
        features = []
        
        # Memory metadata features
        features.append(len(memory.get("title", "")))
        features.append(len(memory.get("description", "")))
        features.append(len(memory.get("tags", [])))
        features.append(memory.get("size_bytes", 0) / 1024)  # Size in KB
        
        # Text features using TF-IDF
        if self.vectorizer:
            text = memory.get("title", "") + " " + memory.get("description", "")
            if "content" in memory:
                text += " " + memory["content"]
            text_features = self.vectorizer.transform([text]).toarray()[0]
            features.extend(text_features)
        
        # Context similarity features
        if context:
            if self.sentence_model:
                # Use sentence transformer for better context similarity
                memory_text = memory.get("title", "") + " " + memory.get("description", "")
                if "content" in memory:
                    memory_text += " " + memory["content"]
                memory_embedding = self.sentence_model.encode(memory_text)
                context_embedding = self.sentence_model.encode(context)
                similarity = np.dot(memory_embedding, context_embedding) / (
                    np.linalg.norm(memory_embedding) * np.linalg.norm(context_embedding)
                )
                features.append(similarity)
            else:
                # Fallback to simple keyword matching
                context_words = set(context.lower().split())
                memory_words = set((memory.get("title", "") + " " + memory.get("description", "")).lower().split())
                if context_words:
                    similarity = len(context_words.intersection(memory_words)) / len(context_words)
                    features.append(similarity)
                else:
                    features.append(0.0)
        
        # Relatedness features
        memory_id = memory["path"].split("\\")[-1]
        related_memories = self.graph.get_related_memories(memory_id, 3)
        related_score = sum(weight for _, weight in related_memories)
        features.append(related_score)
        
        return np.array(features)
    
    def train_model(self, behavior_db_path: Path):
        """Train machine learning model."""
        if not has_sklearn:
            self.logger.error("scikit-learn not available. Please install it with 'pip install scikit-learn'")
            return False
        
        # Load behavior data
        import json
        if not behavior_db_path.exists():
            self.logger.error(f"Behavior database not found: {behavior_db_path}")
            return False
        
        with open(behavior_db_path, "r", encoding="utf-8") as f:
            behavior_db = json.load(f)
        
        # Prepare training data
        X = []
        y = []
        
        for memory_id, behaviors in behavior_db.items():
            # Find memory in index
            memory = None
            for m in self.index.get_manifest():
                if m["path"].split("\\")[-1] == memory_id:
                    memory = m
                    break
            
            if not memory:
                continue
            
            # Calculate usage score
            score = 0.0
            for behavior in behaviors:
                action_weight = {
                    "view": 0.1,
                    "edit": 0.5,
                    "search": 0.2,
                    "share": 0.8,
                    "delete": -0.5
                }.get(behavior["action"], 0.1)
                score += action_weight
            
            # Extract features
            context = behavior.get("context", "") if behaviors else ""
            features = self._extract_features(memory, context)
            X.append(features)
            y.append(score)
        
        if not X:
            self.logger.error("No training data available")
            return False
        
        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        self.logger.info(f"Model trained. MSE: {mse}")
        
        # Save model
        self._save_model()
        
        return True
    
    def predict_score(self, memory: Dict[str, Any], context: Optional[str] = None) -> float:
        """Predict recommendation score using machine learning model."""
        if not self.model:
            # Fallback to rule-based approach
            recommender = MemoryRecommender(self.memory_root, Path(""))
            memory_id = memory["path"].split("\\")[-1]
            usage_score = recommender.get_memory_usage_score(memory_id)
            context_score = recommender.get_context_similarity(memory, context or "")
            related_score = 0.0
            related_memories = self.graph.get_related_memories(memory_id, 3)
            for rel_memory, weight in related_memories:
                rel_usage_score = recommender.get_memory_usage_score(rel_memory)
                related_score += weight * rel_usage_score
            return usage_score * 0.4 + context_score * 0.4 + related_score * 0.2
        
        # Use machine learning model
        features = self._extract_features(memory, context)
        features = features.reshape(1, -1)
        return float(self.model.predict(features)[0])
    
    def get_recommendations(self, context: Optional[str] = None, top_n: int = 5) -> List[Tuple[str, float]]:
        """Get memory recommendations using machine learning."""
        memories = self.index.get_manifest()
        scores = []
        
        for memory in memories:
            score = self.predict_score(memory, context)
            scores.append((memory["path"].split("\\")[-1], score))
        
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
                    memory_with_score["recommendation_method"] = "machine_learning"
                    recommended_memories.append(memory_with_score)
                    break
        
        return recommended_memories


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--model-path", default=".memory_ml_model.pkl", help="Path to save/load model")
    parser.add_argument("--behavior-db", default=".behavior_db.json", help="Path to behavior database")
    parser.add_argument("--train", action="store_true", help="Train model")
    parser.add_argument("--context", help="Context for recommendations")
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
    model_path = Path(args.model_path).expanduser()
    behavior_db_path = Path(args.behavior_db).expanduser()
    
    # Initialize memory ML
    memory_ml = MemoryML(memory_root, model_path)
    
    if args.train:
        # Train model
        success = memory_ml.train_model(behavior_db_path)
        if success:
            print("Model trained successfully")
        else:
            print("Failed to train model")
    else:
        # Get recommendations
        recommendations = memory_ml.get_recommended_memories(args.context, args.top_n)
        print(json.dumps(recommendations, indent=2, ensure_ascii=False))
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
