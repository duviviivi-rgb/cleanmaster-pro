#!/usr/bin/env python3
"""Memory association graph for WorkBuddy."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Try to import NetworkX
try:
    import networkx as nx
    has_networkx = True
except ImportError:
    has_networkx = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    has_sklearn = True
except ImportError:
    has_sklearn = False


class MemoryGraph:
    """Manage memory associations using a graph structure."""
    
    def __init__(self, memory_root: Path):
        self.memory_root = memory_root
        self.graph = nx.Graph() if has_networkx else {}
        self.memories: Dict[str, Dict[str, Any]] = {}
        self._load_memories()
        self._build_graph()
    
    def _load_memories(self):
        """Load memories from the memory directory."""
        for path in sorted(self.memory_root.glob("*.md")):
            if path.name == "MEMORY.md":
                continue
            
            try:
                text = path.read_text(encoding="utf-8")
                # Extract frontmatter
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
                
                self.memories[path.name] = {
                    "path": str(path),
                    "frontmatter": frontmatter,
                    "content": content,
                    "title": frontmatter.get("title", path.stem)
                }
            except Exception as e:
                print(f"Error loading memory {path}: {e}")
    
    def _build_graph(self):
        """Build the association graph."""
        if not has_networkx:
            print("Warning: NetworkX not available, using simple dictionary structure")
            return
        
        # Add nodes
        for memory_name, memory in self.memories.items():
            self.graph.add_node(memory_name, **memory)
        
        # Calculate similarities and add edges
        if has_sklearn:
            self._add_similarity_edges()
        
        # Add semantic edges based on common keywords
        self._add_semantic_edges()
        
        # Add hierarchical edges based on categories and projects
        self._add_hierarchical_edges()
        
        # Add temporal edges based on creation and modification times
        self._add_temporal_edges()
        
        # Add cross-reference edges based on links between memories
        self._add_cross_reference_edges()
    
    def _add_similarity_edges(self):
        """Add edges based on text similarity."""
        if not has_sklearn:
            return
        
        # Prepare texts for similarity calculation
        memory_names = list(self.memories.keys())
        texts = []
        
        for name in memory_names:
            memory = self.memories[name]
            text = memory["title"] + " " + memory["content"]
            # Remove markdown and special characters
            text = re.sub(r"[#*`>]", " ", text)
            text = re.sub(r"\s+", " ", text)
            texts.append(text)
        
        # Calculate TF-IDF and cosine similarity
        vectorizer = TfidfVectorizer(stop_words="english")
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Add edges for similarities above threshold
            threshold = 0.3
            for i in range(len(memory_names)):
                for j in range(i + 1, len(memory_names)):
                    similarity = similarity_matrix[i][j]
                    if similarity > threshold:
                        self.graph.add_edge(
                            memory_names[i], 
                            memory_names[j], 
                            weight=similarity,
                            type="similarity"
                        )
        except Exception as e:
            print(f"Error calculating similarity: {e}")
    
    def _add_semantic_edges(self):
        """Add edges based on semantic relationships."""
        # Extract keywords from each memory
        memory_keywords = {}
        for name, memory in self.memories.items():
            text = memory["title"] + " " + memory["content"]
            # Extract keywords (simple approach)
            words = re.findall(r"\b\w+\b", text.lower())
            # Filter out stop words
            stop_words = {
                "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by",
                "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did"
            }
            keywords = set(word for word in words if len(word) > 3 and word not in stop_words)
            memory_keywords[name] = keywords
        
        # Add edges for common keywords
        for name1, keywords1 in memory_keywords.items():
            for name2, keywords2 in memory_keywords.items():
                if name1 >= name2:  # Avoid duplicate edges
                    continue
                common_keywords = keywords1.intersection(keywords2)
                if len(common_keywords) >= 2:  # At least 2 common keywords
                    if not self.graph.has_edge(name1, name2):
                        self.graph.add_edge(
                            name1, 
                            name2, 
                            weight=len(common_keywords),
                            type="semantic",
                            keywords=list(common_keywords)
                        )
    
    def _add_hierarchical_edges(self):
        """Add hierarchical edges based on categories and projects."""
        # Group memories by category and project
        category_groups = {}
        project_groups = {}
        
        for memory_name, memory in self.memories.items():
            # Get category from frontmatter or path
            category = memory.get("frontmatter", {}).get("category", "")
            if category:
                if category not in category_groups:
                    category_groups[category] = []
                category_groups[category].append(memory_name)
            
            # Get project from frontmatter or path
            project = memory.get("frontmatter", {}).get("project", "")
            if project:
                if project not in project_groups:
                    project_groups[project] = []
                project_groups[project].append(memory_name)
        
        # Add edges within categories
        for category, memories in category_groups.items():
            for i, memory1 in enumerate(memories):
                for memory2 in memories[i+1:]:
                    self.graph.add_edge(memory1, memory2, weight=0.8, type="hierarchical", category=category)
        
        # Add edges within projects
        for project, memories in project_groups.items():
            for i, memory1 in enumerate(memories):
                for memory2 in memories[i+1:]:
                    self.graph.add_edge(memory1, memory2, weight=0.9, type="hierarchical", project=project)
    
    def _add_temporal_edges(self):
        """Add temporal edges based on creation and modification times."""
        # Get memory timestamps
        memory_timestamps = {}
        for memory_name, memory in self.memories.items():
            # Try to get creation time from frontmatter
            created = memory.get("frontmatter", {}).get("created", "")
            modified = memory.get("frontmatter", {}).get("modified", "")
            
            # Use file modification time as fallback
            try:
                import os
                mtime = os.path.getmtime(memory["path"])
                memory_timestamps[memory_name] = mtime
            except:
                memory_timestamps[memory_name] = 0
        
        # Sort memories by timestamp
        sorted_memories = sorted(memory_timestamps.items(), key=lambda x: x[1])
        
        # Add temporal edges between consecutive memories
        for i, (memory1, ts1) in enumerate(sorted_memories[:-1]):
            memory2, ts2 = sorted_memories[i+1]
            # Only add edge if timestamps are close (within 24 hours)
            if ts2 - ts1 < 86400:  # 24 hours in seconds
                weight = 1.0 / (1 + (ts2 - ts1) / 3600)  # Weight decreases with time difference
                self.graph.add_edge(memory1, memory2, weight=weight, type="temporal", time_diff=ts2 - ts1)
    
    def _add_cross_reference_edges(self):
        """Add cross-reference edges based on links between memories."""
        for memory_name, memory in self.memories.items():
            content = memory["content"]
            # Look for links to other memories
            # Simple pattern: [[memory_name]] or [memory_title](memory_name.md)
            links = re.findall(r"\[\[(.*?)\]\]", content)
            links.extend(re.findall(r"\[.*?\]\((.*?)\.md\)", content))
            
            for link in links:
                # Try to find the linked memory
                for target_memory, target_info in self.memories.items():
                    if link == target_memory or link == target_info.get("title", ""):
                        self.graph.add_edge(memory_name, target_memory, weight=1.0, type="cross_reference", link=link)
    
    def add_memory(self, memory_name: str, memory_data: Dict[str, Any]):
        """Add a new memory to the graph."""
        if has_networkx:
            self.graph.add_node(memory_name, **memory_data)
        self.memories[memory_name] = memory_data
        # Rebuild edges for the new memory
        self._add_edges_for_memory(memory_name)
    
    def _add_edges_for_memory(self, memory_name: str):
        """Add edges for a specific memory."""
        if not has_networkx:
            return
        
        memory = self.memories[memory_name]
        # Check similarity with existing memories
        if has_sklearn:
            memory_text = memory["title"] + " " + memory["content"]
            memory_text = re.sub(r"[#*`>]", " ", memory_text)
            memory_text = re.sub(r"\s+", " ", memory_text)
            
            for other_name, other_memory in self.memories.items():
                if other_name == memory_name:
                    continue
                
                other_text = other_memory["title"] + " " + other_memory["content"]
                other_text = re.sub(r"[#*`>]", " ", other_text)
                other_text = re.sub(r"\s+", " ", other_text)
                
                # Calculate similarity
                vectorizer = TfidfVectorizer(stop_words="english")
                try:
                    tfidf_matrix = vectorizer.fit_transform([memory_text, other_text])
                    similarity = cosine_similarity(tfidf_matrix)[0][1]
                    if similarity > 0.3:
                        self.graph.add_edge(
                            memory_name, 
                            other_name, 
                            weight=similarity,
                            type="similarity"
                        )
                except Exception as e:
                    pass
        
        # Check semantic relationships
        memory_text = memory["title"] + " " + memory["content"]
        memory_words = re.findall(r"\b\w+\b", memory_text.lower())
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did"
        }
        memory_keywords = set(word for word in memory_words if len(word) > 3 and word not in stop_words)
        
        for other_name, other_memory in self.memories.items():
            if other_name == memory_name:
                continue
            
            other_text = other_memory["title"] + " " + other_memory["content"]
            other_words = re.findall(r"\b\w+\b", other_text.lower())
            other_keywords = set(word for word in other_words if len(word) > 3 and word not in stop_words)
            
            common_keywords = memory_keywords.intersection(other_keywords)
            if len(common_keywords) >= 2:
                if not self.graph.has_edge(memory_name, other_name):
                    self.graph.add_edge(
                        memory_name, 
                        other_name, 
                        weight=len(common_keywords),
                        type="semantic",
                        keywords=list(common_keywords)
                    )
    
    def get_related_memories(self, memory_name: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """Get related memories for a given memory."""
        if not has_networkx or memory_name not in self.graph:
            return []
        
        # Get neighbors and their weights
        neighbors = []
        for neighbor, attrs in self.graph[memory_name].items():
            weight = attrs.get("weight", 0.0)
            neighbors.append((neighbor, weight))
        
        # Sort by weight and return top N
        neighbors.sort(key=lambda x: x[1], reverse=True)
        return neighbors[:top_n]
    
    def get_shortest_path(self, start_memory: str, end_memory: str) -> Optional[List[str]]:
        """Get the shortest path between two memories."""
        if not has_networkx:
            return None
        
        try:
            return nx.shortest_path(self.graph, start_memory, end_memory)
        except nx.NetworkXNoPath:
            return None
    
    def save_graph(self, output_path: Path):
        """Save the graph to a file."""
        if has_networkx:
            # Save graph data
            graph_data = {
                "nodes": [],
                "edges": []
            }
            
            for node, attrs in self.graph.nodes(data=True):
                graph_data["nodes"].append({
                    "id": node,
                    "data": attrs
                })
            
            for u, v, attrs in self.graph.edges(data=True):
                graph_data["edges"].append({
                    "source": u,
                    "target": v,
                    "data": attrs
                })
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)
        else:
            # Save simple structure
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def load_graph(self, input_path: Path):
        """Load the graph from a file."""
        if not input_path.exists():
            return
        
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if has_networkx and "nodes" in data and "edges" in data:
                # Load graph data
                self.graph.clear()
                self.memories.clear()
                
                for node_data in data["nodes"]:
                    node_id = node_data["id"]
                    node_attrs = node_data["data"]
                    self.graph.add_node(node_id, **node_attrs)
                    self.memories[node_id] = node_attrs
                
                for edge_data in data["edges"]:
                    source = edge_data["source"]
                    target = edge_data["target"]
                    edge_attrs = edge_data["data"]
                    self.graph.add_edge(source, target, **edge_attrs)
            else:
                # Load simple structure
                self.memories = data
        except Exception as e:
            print(f"Error loading graph: {e}")
    
    def generate_graph_visualization(self, output_path: Path):
        """Generate a graph visualization."""
        if not has_networkx:
            return
        
        try:
            import matplotlib.pyplot as plt
            
            pos = nx.spring_layout(self.graph, k=0.3)
            plt.figure(figsize=(12, 10))
            
            # Draw nodes
            nx.draw_networkx_nodes(self.graph, pos, node_size=300, node_color="lightblue")
            
            # Draw edges
            edges = self.graph.edges(data=True)
            weights = [d.get("weight", 1.0) for u, v, d in edges]
            nx.draw_networkx_edges(self.graph, pos, width=[w * 2 for w in weights])
            
            # Draw labels
            nx.draw_networkx_labels(self.graph, pos, font_size=8)
            
            plt.title("Memory Association Graph")
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(output_path)
            print(f"Graph visualization saved to: {output_path}")
        except ImportError:
            print("Warning: Matplotlib not available, cannot generate visualization")
        except Exception as e:
            print(f"Error generating visualization: {e}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, help="Path to memory directory")
    parser.add_argument("--output", help="Path to save graph")
    parser.add_argument("--visualize", help="Path to save visualization")
    parser.add_argument("--related", help="Get related memories for a specific memory")
    args = parser.parse_args()
    
    memory_root = Path(args.memory_root).expanduser()
    graph = MemoryGraph(memory_root)
    
    if args.related:
        related = graph.get_related_memories(args.related)
        print(f"Related memories for {args.related}:")
        for memory, weight in related:
            print(f"  - {memory} (weight: {weight:.2f})")
    
    if args.output:
        output_path = Path(args.output).expanduser()
        graph.save_graph(output_path)
        print(f"Graph saved to: {output_path}")
    
    if args.visualize:
        viz_path = Path(args.visualize).expanduser()
        graph.generate_graph_visualization(viz_path)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
