#!/usr/bin/env python3
"""Build and maintain an index for memory files to support keyword and tag search."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from memory_graph import MemoryGraph


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


class MemoryIndex:
    def __init__(self, memory_root: Path):
        self.memory_root = memory_root
        self.index: Dict[str, Dict[str, Any]] = {}
        self.tag_index: Dict[str, List[str]] = {}
        self.keyword_index: Dict[str, List[str]] = {}
        self.file_type_index: Dict[str, List[str]] = {}
        self.graph = MemoryGraph(memory_root)
        self.index_timestamp = 0
        self.build_index()
        self.search_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.cache_size = 100

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

    def extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text."""
        # Remove frontmatter
        text = FRONTMATTER_RE.sub("", text)
        # Remove markdown syntax
        text = re.sub(r"[#*`>]", " ", text)
        # Remove punctuation
        text = re.sub(r"[.!?,;:()\[\]{}]", " ", text)
        # Split into words and filter stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
            "will", "would", "should", "could", "may", "might", "must", "shall"
        }
        words = text.lower().split()
        keywords = {word for word in words if len(word) > 2 and word not in stop_words}
        return keywords

    def build_index(self):
        """Build the memory index."""
        start_time = time.time()
        for path in sorted(self.memory_root.glob("*.md")):
            if path.name == "MEMORY.md":
                continue
            
            try:
                text = path.read_text(encoding="utf-8")
                frontmatter = self.parse_frontmatter(text)
                
                # Extract tags from frontmatter
                tags = frontmatter.get("tags", "").split(",") if "tags" in frontmatter else []
                tags = [tag.strip() for tag in tags if tag.strip()]
                
                # Extract keywords from content
                keywords = self.extract_keywords(text)
                
                # Extract file type (for multimodal support)
                file_type = frontmatter.get("file_type", "text")
                
                # Build file index
                self.index[path.name] = {
                    "path": str(path),
                    "type": frontmatter.get("type"),
                    "file_type": file_type,
                    "title": frontmatter.get("title"),
                    "description": frontmatter.get("description"),
                    "tags": tags,
                    "keywords": list(keywords),
                    "size_bytes": path.stat().st_size,
                    "modified": path.stat().st_mtime
                }
                
                # Build tag index
                for tag in tags:
                    if tag not in self.tag_index:
                        self.tag_index[tag] = []
                    self.tag_index[tag].append(path.name)
                
                # Build keyword index
                for keyword in keywords:
                    if keyword not in self.keyword_index:
                        self.keyword_index[keyword] = []
                    self.keyword_index[keyword].append(path.name)
                
                # Build file type index
                if file_type not in self.file_type_index:
                    self.file_type_index[file_type] = []
                self.file_type_index[file_type].append(path.name)
                    
            except Exception as e:
                print(f"Error processing {path}: {e}")
        
        self.index_timestamp = time.time()
        # Clear cache after rebuilding index
        self.search_cache.clear()
        print(f"Index built in {time.time() - start_time:.2f} seconds")
    
    def update_index(self):
        """Update the index incrementally."""
        start_time = time.time()
        updated = 0
        
        # Check for new or modified files
        for path in sorted(self.memory_root.glob("*.md")):
            if path.name == "MEMORY.md":
                continue
            
            # Check if file is new or modified
            mtime = path.stat().st_mtime
            if path.name not in self.index or mtime > self.index[path.name].get("modified", 0):
                try:
                    text = path.read_text(encoding="utf-8")
                    frontmatter = self.parse_frontmatter(text)
                    
                    # Extract tags from frontmatter
                    tags = frontmatter.get("tags", "").split(",") if "tags" in frontmatter else []
                    tags = [tag.strip() for tag in tags if tag.strip()]
                    
                    # Extract keywords from content
                    keywords = self.extract_keywords(text)
                    
                    # Extract file type (for multimodal support)
                    file_type = frontmatter.get("file_type", "text")
                    
                    # Update file index
                    self.index[path.name] = {
                        "path": str(path),
                        "type": frontmatter.get("type"),
                        "file_type": file_type,
                        "title": frontmatter.get("title"),
                        "description": frontmatter.get("description"),
                        "tags": tags,
                        "keywords": list(keywords),
                        "size_bytes": path.stat().st_size,
                        "modified": mtime
                    }
                    
                    # Update tag index
                    for tag in tags:
                        if tag not in self.tag_index:
                            self.tag_index[tag] = []
                        if path.name not in self.tag_index[tag]:
                            self.tag_index[tag].append(path.name)
                    
                    # Update keyword index
                    for keyword in keywords:
                        if keyword not in self.keyword_index:
                            self.keyword_index[keyword] = []
                        if path.name not in self.keyword_index[keyword]:
                            self.keyword_index[keyword].append(path.name)
                    
                    # Update file type index
                    if file_type not in self.file_type_index:
                        self.file_type_index[file_type] = []
                    if path.name not in self.file_type_index[file_type]:
                        self.file_type_index[file_type].append(path.name)
                    
                    updated += 1
                        
                except Exception as e:
                    print(f"Error updating {path}: {e}")
        
        # Check for deleted files
        deleted = 0
        files_to_delete = []
        for file_name in self.index:
            file_path = self.memory_root / file_name
            if not file_path.exists():
                files_to_delete.append(file_name)
        
        for file_name in files_to_delete:
            # Remove from indices
            del self.index[file_name]
            
            # Remove from tag index
            for tag, files in self.tag_index.items():
                if file_name in files:
                    files.remove(file_name)
            
            # Remove from keyword index
            for keyword, files in self.keyword_index.items():
                if file_name in files:
                    files.remove(file_name)
            
            # Remove from file type index
            for file_type, files in self.file_type_index.items():
                if file_name in files:
                    files.remove(file_name)
            
            deleted += 1
        
        self.index_timestamp = time.time()
        # Clear cache after updating index
        self.search_cache.clear()
        print(f"Index updated in {time.time() - start_time:.2f} seconds. Updated: {updated}, Deleted: {deleted}")
    
    def _sort_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Sort search results by relevance."""
        def relevance_score(result: Dict[str, Any]) -> float:
            score = 0.0
            query_terms = query.lower().split()
            
            # Title match
            if result.get("title"):
                title_lower = result["title"].lower()
                for term in query_terms:
                    if term in title_lower:
                        score += 2.0
            
            # Description match
            if result.get("description"):
                desc_lower = result["description"].lower()
                for term in query_terms:
                    if term in desc_lower:
                        score += 1.0
            
            # Keyword match
            if result.get("keywords"):
                keywords_lower = [k.lower() for k in result["keywords"]]
                for term in query_terms:
                    if term in keywords_lower:
                        score += 0.5
            
            # Tag match
            if result.get("tags"):
                tags_lower = [t.lower() for t in result["tags"]]
                for term in query_terms:
                    if term in tags_lower:
                        score += 1.5
            
            # Related weight
            if "related_weight" in result:
                score += result["related_weight"] * 3.0
            
            # Recency
            if "modified" in result:
                # Give higher score to more recent files
                recency_score = (time.time() - result["modified"]) / (30 * 24 * 3600)  # 30 days
                score += max(0, 1.0 - recency_score)
            
            return score
        
        return sorted(results, key=relevance_score, reverse=True)
    
    def _cache_search_result(self, query: str, results: List[Dict[str, Any]]):
        """Cache search results."""
        if len(self.search_cache) >= self.cache_size:
            # Remove oldest cache entry
            oldest_key = next(iter(self.search_cache))
            del self.search_cache[oldest_key]
        self.search_cache[query] = results
    
    def _get_cached_search(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached search results."""
        return self.search_cache.get(query)
    
    def search_parallel(self, query: str) -> List[Dict[str, Any]]:
        """Search memory files in parallel for better performance."""
        # Check cache first
        cached_results = self._get_cached_search(query)
        if cached_results:
            return cached_results
        
        query_terms = query.lower().split()
        results = []
        
        # Use threading to search in parallel
        import threading
        from concurrent.futures import ThreadPoolExecutor
        
        def search_term(term: str):
            term_results = []
            if term.startswith("tag:"):
                tag = term[4:]
                term_results.extend(self.search_by_tag(tag))
            elif term.startswith("type:"):
                file_type = term[5:]
                term_results.extend(self.search_by_file_type(file_type))
            elif term.startswith("related:"):
                memory_name = term[8:]
                term_results.extend(self.search_by_related(memory_name))
            else:
                term_results.extend(self.search_by_keyword(term))
            return term_results
        
        # Search each term in parallel
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(search_term, term) for term in query_terms]
            for future in futures:
                results.extend(future.result())
        
        # Remove duplicates
        seen = set()
        unique_results = []
        for result in results:
            if result["path"] not in seen:
                seen.add(result["path"])
                unique_results.append(result)
        
        # Sort results by relevance
        sorted_results = self._sort_results(unique_results, query)
        
        # Cache results
        self._cache_search_result(query, sorted_results)
        
        return sorted_results

    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Search memory files by keyword."""
        keyword = keyword.lower()
        results = []
        
        # Search in keyword index
        if keyword in self.keyword_index:
            for file_name in self.keyword_index[keyword]:
                results.append(self.index[file_name])
        
        # Also search in titles and descriptions
        for file_name, info in self.index.items():
            if file_name not in [r["path"].split("\\")[-1] for r in results]:
                if (
                    (info.get("title") and keyword in info["title"].lower()) or
                    (info.get("description") and keyword in info["description"].lower())
                ):
                    results.append(info)
        
        return results

    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Search memory files by tag."""
        tag = tag.lower()
        results = []
        
        # Search in tag index
        for file_tag, file_names in self.tag_index.items():
            if tag in file_tag.lower():
                for file_name in file_names:
                    results.append(self.index[file_name])
        
        return results

    def search_by_file_type(self, file_type: str) -> List[Dict[str, Any]]:
        """Search memory files by file type."""
        file_type = file_type.lower()
        results = []
        
        # Search in file type index
        for ftype, file_names in self.file_type_index.items():
            if file_type in ftype.lower():
                for file_name in file_names:
                    results.append(self.index[file_name])
        
        return results

    def search_by_related(self, memory_name: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """Search memory files related to a specific memory."""
        results = []
        related = self.graph.get_related_memories(memory_name, top_n)
        for memory, weight in related:
            if memory in self.index:
                result = self.index[memory].copy()
                result["related_weight"] = weight
                results.append(result)
        return results

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search memory files by query (keywords, tags, file types, and related memories)."""
        query_terms = query.lower().split()
        results = []
        
        # Process each term
        for term in query_terms:
            if term.startswith("tag:"):
                tag = term[4:]
                tag_results = self.search_by_tag(tag)
                results.extend(tag_results)
            elif term.startswith("type:"):
                file_type = term[5:]
                type_results = self.search_by_file_type(file_type)
                results.extend(type_results)
            elif term.startswith("related:"):
                memory_name = term[8:]
                related_results = self.search_by_related(memory_name)
                results.extend(related_results)
            else:
                keyword_results = self.search_by_keyword(term)
                results.extend(keyword_results)
        
        # Remove duplicates
        seen = set()
        unique_results = []
        for result in results:
            if result["path"] not in seen:
                seen.add(result["path"])
                unique_results.append(result)
        
        return unique_results

    def get_manifest(self) -> List[Dict[str, Any]]:
        """Get a manifest of all memory files."""
        return list(self.index.values())

    def save_index(self, index_path: Path):
        """Save the index to a file."""
        data = {
            "index": self.index,
            "tag_index": self.tag_index,
            "keyword_index": self.keyword_index,
            "file_type_index": self.file_type_index
        }
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_index(self, index_path: Path):
        """Load the index from a file."""
        if index_path.exists():
            with open(index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.index = data.get("index", {})
                self.tag_index = data.get("tag_index", {})
                self.keyword_index = data.get("keyword_index", {})
                self.file_type_index = data.get("file_type_index", {})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True)
    parser.add_argument("--index-path", default=".memory_index.json")
    parser.add_argument("--search", help="Search query")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    memory_root = Path(args.memory_root).expanduser()
    index_path = Path(args.index_path).expanduser()

    # Create memory index
    index = MemoryIndex(memory_root)
    
    # Save index
    index.save_index(index_path)
    
    if args.search:
        results = index.search(args.search)
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"Search results for '{args.search}':")
            for result in results:
                print(f"- {result['path']}")
                print(f"  Type: {result.get('type', 'unknown')}")
                print(f"  File Type: {result.get('file_type', 'text')}")
                print(f"  Title: {result.get('title', '-')}")
                print(f"  Tags: {', '.join(result.get('tags', []))}")
                if 'related_weight' in result:
                    print(f"  Related Weight: {result['related_weight']:.2f}")
                print()
    else:
        # Print manifest
        manifest = index.get_manifest()
        if args.json:
            print(json.dumps(manifest, indent=2, ensure_ascii=False))
        else:
            print("Memory manifest:")
            for item in manifest:
                print(f"- {item['path']}")
                print(f"  Type: {item.get('type', 'unknown')}")
                print(f"  File Type: {item.get('file_type', 'text')}")
                print(f"  Title: {item.get('title', '-')}")
                print(f"  Tags: {', '.join(item.get('tags', []))}")
                print()
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
