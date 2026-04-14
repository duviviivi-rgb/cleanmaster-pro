#!/usr/bin/env python3
"""Memory management web interface using Flask."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, render_template_string, request, jsonify

from memory_index import MemoryIndex
from memory_quality import MemoryQualityEvaluator
from memory_optimizer import MemoryOptimizer
from memory_compressor import MemoryCompressor
from memory_context_compressor import MemoryContextCompressor
from memory_graph import MemoryGraph
from memory_multimodal import MultiModalProcessor
from memory_recommender import MemoryRecommender, MemoryContextAnalyzer
from memory_ml import MemoryML
from memory_tracker import RealTimeRecommender
from memory_personalizer import MemoryPersonalizer
from memory_lifecycle import MemoryLifecycleManager


app = Flask(__name__)
memory_root: Path | None = None


@app.route('/')
def index():
    """Home page."""
    if not memory_root:
        return "Memory root not set. Please run with --memory-root option."
    
    # Get memory manifest
    indexer = MemoryIndex(memory_root)
    manifest = indexer.get_manifest()
    
    # Get memory quality evaluations
    evaluator = MemoryQualityEvaluator(memory_root)
    evaluations = evaluator.evaluate_all_memories()
    
    # Get optimization report
    optimizer = MemoryOptimizer(memory_root)
    optimization_report = optimizer.generate_optimization_report()
    
    # Get compression report
    compressor = MemoryCompressor(memory_root)
    compression_report = compressor.generate_compression_report()
    
    # Get memory graph
    graph = MemoryGraph(memory_root)
    
    # Calculate file type distribution
    file_type_distribution = {}
    for memory in manifest:
        file_type = memory.get('file_type', 'text')
        file_type_distribution[file_type] = file_type_distribution.get(file_type, 0) + 1
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WorkBuddy Memory Manager</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #333;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        .memory-item {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #f0f0f0;
            border-radius: 4px;
        }
        .memory-item h4 {
            margin-top: 0;
            color: #555;
        }
        .memory-item .meta {
            font-size: 12px;
            color: #888;
            margin-bottom: 5px;
        }
        .memory-item .content {
            font-size: 14px;
            color: #333;
        }
        .memory-item .thumbnail {
            max-width: 200px;
            margin-top: 10px;
            border-radius: 4px;
        }
        .quality-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        .quality-high {
            background-color: #d4edda;
            color: #155724;
        }
        .quality-medium {
            background-color: #fff3cd;
            color: #856404;
        }
        .quality-low {
            background-color: #f8d7da;
            color: #721c24;
        }
        .file-type-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            background-color: #e3f2fd;
            color: #1976d2;
        }
        .search-form {
            margin-bottom: 20px;
        }
        .search-form input {
            padding: 8px;
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .search-form button {
            padding: 8px 16px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .search-form button:hover {
            background-color: #0069d9;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .stat-card {
            flex: 1;
            min-width: 150px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 14px;
            cursor: pointer;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-primary:hover {
            background-color: #0069d9;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background-color: #5a6268;
        }
        .btn-danger {
            background-color: #dc3545;
            color: white;
        }
        .btn-danger:hover {
            background-color: #c82333;
        }
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        .btn-success:hover {
            background-color: #218838;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        .graph-container {
            width: 100%;
            height: 500px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            margin-top: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        .form-group input[type="text"],
        .form-group textarea {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            width: 100%;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }
        .form-group input[type="text"]:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .form-group input[type="file"] {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            width: 100%;
            background-color: white;
        }
        .form-group button {
            padding: 10px 20px;
            background-color: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .form-group button:hover {
            background-color: #5a6fd8;
            transform: translateY(-2px);
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }
        /* Stats Cards */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
        /* Search Form */
        .search-form {
            display: flex;
            gap: 10px;
        }
        .search-form input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
        }
        .search-form button {
            padding: 10px 20px;
            background-color: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }
        /* Memory Item Enhancements */
        .memory-item {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .memory-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .memory-item .meta {
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .file-type-badge {
            background-color: #e9ecef;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }
        .quality-badge {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }
        .quality-high {
            background-color: #d4edda;
            color: #155724;
        }
        .quality-medium {
            background-color: #fff3cd;
            color: #856404;
        }
        .quality-low {
            background-color: #f8d7da;
            color: #721c24;
        }
        .memory-item h4 {
            margin-bottom: 10px;
            color: #333;
            font-size: 16px;
        }
        .memory-item .content {
            margin-bottom: 10px;
            color: #555;
            line-height: 1.5;
        }
        .thumbnail {
            margin-top: 10px;
        }
        .thumbnail img {
            max-width: 100%;
            max-height: 200px;
            border-radius: 4px;
            object-fit: cover;
        }
        /* Graph Container */
        .graph-container {
            width: 100%;
            height: 500px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
        /* Table Styles */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
    </style>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>WorkBuddy Memory Manager</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{{ total_memories }}</div>
                <div class="stat-label">Total Memories</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ total_size }} bytes</div>
                <div class="stat-label">Total Size</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ high_quality_count }}</div>
                <div class="stat-label">High Quality</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ compression_ratio }}%</div>
                <div class="stat-label">Compression Ratio</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Search Memories</h2>
            <form class="search-form" action="/search" method="post">
                <input type="text" name="query" placeholder="Enter search query... (e.g., tag:important, type:image, related:memory.md)">
                <button type="submit">Search</button>
            </form>
        </div>
        
        <div class="section">
            <h2>Process Multi-Modal Content</h2>
            <form action="/process_multimodal" method="post" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="file">Select File (Image, Audio, or Video):</label>
                    <input type="file" id="file" name="file" accept="image/*,audio/*,video/*">
                </div>
                <div class="form-group">
                    <button type="submit">Process and Create Memory</button>
                </div>
            </form>
        </div>
        
        <div class="section">
            <h2>Intelligent Memory Recommendations</h2>
            <form action="/recommend" method="post">
                <div class="form-group">
                    <label for="context">Enter Context for Recommendations:</label>
                    <textarea id="context" name="context" rows="4" cols="50" placeholder="Describe your current task or topic..."></textarea>
                </div>
                <div class="form-group">
                    <button type="submit">Get Recommendations</button>
                </div>
            </form>
        </div>
        
        <div class="section">
            <h2>Machine Learning Recommendations</h2>
            <form action="/ml_recommend" method="post">
                <div class="form-group">
                    <label for="ml_context">Enter Context for ML Recommendations:</label>
                    <textarea id="ml_context" name="context" rows="4" cols="50" placeholder="Describe your current task or topic..."></textarea>
                </div>
                <div class="form-group">
                    <button type="submit">Get ML Recommendations</button>
                </div>
            </form>
        </div>
        
        <div class="section">
            <h2>Personalized Recommendations</h2>
            <form action="/personalized_recommend" method="post">
                <div class="form-group">
                    <label for="user_id">User ID:</label>
                    <input type="text" id="user_id" name="user_id" placeholder="Enter user ID">
                </div>
                <div class="form-group">
                    <label for="personalized_context">Enter Context:</label>
                    <textarea id="personalized_context" name="context" rows="4" cols="50" placeholder="Describe your current task or topic..."></textarea>
                </div>
                <div class="form-group">
                    <button type="submit">Get Personalized Recommendations</button>
                </div>
            </form>
        </div>
        
        <div class="section">
            <h2>Memory Lifecycle Management</h2>
            <a href="/lifecycle_report" class="btn btn-primary">View Lifecycle Report</a>
            <a href="/run_lifecycle" class="btn btn-secondary">Run Lifecycle Management</a>
        </div>
        
        <div class="section">
            <h2>Memory List</h2>
            {% for memory in memories %}
            <div class="memory-item">
                <div class="meta">
                    Type: {{ memory.type or 'unknown' }} | 
                    <span class="file-type-badge">{{ memory.file_type or 'text' }}</span> | 
                    Tags: {{ ', '.join(memory.tags) if memory.tags else 'none' }}
                    {% if evaluations[memory.path.split('\\')[-1]] %}
                    | <span class="quality-badge {% if evaluations[memory.path.split('\\')[-1]].overall > 0.8 %}quality-high{% elif evaluations[memory.path.split('\\')[-1]].overall > 0.5 %}quality-medium{% else %}quality-low{% endif %}">
                        Quality: {{ "%.2f"|format(evaluations[memory.path.split('\\')[-1]].overall) }}
                    </span>
                    {% endif %}
                </div>
                <h4>{{ memory.title or 'Untitled' }}</h4>
                <div class="content">{{ memory.description or 'No description' }}</div>
                {% if memory.file_type == 'image' %}
                <div class="thumbnail">
                    <img src="{{ memory.path }}" alt="Thumbnail" class="thumbnail">
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>Memory Type Distribution</h2>
            <table>
                <tr>
                    <th>Type</th>
                    <th>Count</th>
                </tr>
                {% for type, count in optimization_report.type_distribution.items() %}
                <tr>
                    <td>{{ type }}</td>
                    <td>{{ count }}</td>
                </tr>
                {% endfor %}
            </table>
            
            <h3>File Type Distribution</h3>
            <table>
                <tr>
                    <th>File Type</th>
                    <th>Count</th>
                </tr>
                {% for file_type, count in file_type_distribution.items() %}
                <tr>
                    <td>{{ file_type }}</td>
                    <td>{{ count }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div class="section">
            <h2>Memory Association Graph</h2>
            <div class="graph-container" id="memoryGraph"></div>
            <script>
                // Simple graph visualization using D3.js
                const graphData = {{
                    nodes: [
                        {% for memory in memories %}
                        {{ "{" }}id: "{{ memory.path.split('\\')[-1] }}", title: "{{ memory.title or memory.path.split('\\')[-1] }}", type: "{{ memory.file_type or 'text' }}"{{ "}," }}
                        {% endfor %}
                    ],
                    links: [
                        {% for memory in memories %}
                        {% set related = graph.get_related_memories(memory.path.split('\\')[-1], 3) %}
                        {% for rel_memory, weight in related %}
                        {{ "{" }}source: "{{ memory.path.split('\\')[-1] }}", target: "{{ rel_memory }}", weight: {{ weight }}{{ "}," }}
                        {% endfor %}
                        {% endfor %}
                    ]
                }};
                
                const width = document.getElementById('memoryGraph').clientWidth;
                const height = document.getElementById('memoryGraph').clientHeight;
                
                const svg = d3.select('#memoryGraph')
                    .append('svg')
                    .attr('width', width)
                    .attr('height', height);
                
                const simulation = d3.forceSimulation(graphData.nodes)
                    .force('link', d3.forceLink(graphData.links).id(d => d.id).distance(100))
                    .force('charge', d3.forceManyBody().strength(-300))
                    .force('center', d3.forceCenter(width / 2, height / 2));
                
                const link = svg.append('g')
                    .selectAll('line')
                    .data(graphData.links)
                    .enter()
                    .append('line')
                    .attr('stroke', '#999')
                    .attr('stroke-width', d => Math.sqrt(d.weight) * 2);
                
                const node = svg.append('g')
                    .selectAll('circle')
                    .data(graphData.nodes)
                    .enter()
                    .append('circle')
                    .attr('r', 10)
                    .attr('fill', d => d.type === 'image' ? '#ff7f0e' : d.type === 'audio' ? '#2ca02c' : d.type === 'video' ? '#d62728' : '#1f77b4')
                    .call(d3.drag()
                        .on('start', dragstarted)
                        .on('drag', dragged)
                        .on('end', dragended));
                
                const label = svg.append('g')
                    .selectAll('text')
                    .data(graphData.nodes)
                    .enter()
                    .append('text')
                    .text(d => d.title.substring(0, 10) + '...')
                    .attr('font-size', 10)
                    .attr('dx', 12)
                    .attr('dy', 4);
                
                simulation.on('tick', () => {
                    link
                        .attr('x1', d => d.source.x)
                        .attr('y1', d => d.source.y)
                        .attr('x2', d => d.target.x)
                        .attr('y2', d => d.target.y);
                    
                    node
                        .attr('cx', d => d.x = Math.max(10, Math.min(width - 10, d.x)))
                        .attr('cy', d => d.y = Math.max(10, Math.min(height - 10, d.y)));
                    
                    label
                        .attr('x', d => d.x)
                        .attr('y', d => d.y);
                });
                
                function dragstarted(event, d) {
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }
                
                function dragged(event, d) {
                    d.fx = event.x;
                    d.fy = event.y;
                }
                
                function dragended(event, d) {
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }
            </script>
        </div>
        
        <div class="section">
            <h2>Compression Report</h2>
            <p>Compressible memories: {{ compression_report.compressible_count }}</p>
            <p>Estimated compression ratio: {{ "%.2f"|format(compression_report.compression_ratio) }}%</p>
        </div>
        
        <div class="section">
            <h2>Actions</h2>
            <a href="/optimize" class="btn btn-primary">Optimize Memory Structure</a>
            <a href="/compress" class="btn btn-secondary">Compress Memories</a>
            <a href="/context_compress" class="btn btn-info">Compress Context</a>
            <a href="/refresh" class="btn btn-danger">Refresh Index</a>
            <a href="/graph" class="btn btn-success">View Detailed Graph</a>
        </div>
    </div>
</body>
</html>
''',
        total_memories=len(manifest),
        total_size=sum(m['size_bytes'] for m in manifest),
        high_quality_count=sum(1 for e in evaluations.values() if e['overall'] > 0.8),
        compression_ratio=compression_report['compression_ratio'],
        memories=manifest,
        evaluations=evaluations,
        optimization_report=optimization_report,
        compression_report=compression_report,
        graph=graph,
        file_type_distribution=file_type_distribution
    )


@app.route('/search', methods=['POST'])
def search():
    """Search memories."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    query = request.form.get('query', '')
    indexer = MemoryIndex(memory_root)
    results = indexer.search(query)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .memory-item {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #f0f0f0;
            border-radius: 4px;
        }
        .memory-item h4 {
            margin-top: 0;
            color: #555;
        }
        .memory-item .meta {
            font-size: 12px;
            color: #888;
            margin-bottom: 5px;
        }
        .memory-item .content {
            font-size: 14px;
            color: #333;
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Search Results for "{{ query }}"</h1>
        
        {% if results %}
        {% for result in results %}
        <div class="memory-item">
            <div class="meta">
                Type: {{ result.type or 'unknown' }} | Tags: {{ ', '.join(result.tags) if result.tags else 'none' }}
            </div>
            <h4>{{ result.title or 'Untitled' }}</h4>
            <div class="content">{{ result.description or 'No description' }}</div>
        </div>
        {% endfor %}
        {% else %}
        <p>No results found.</p>
        {% endif %}
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', query=query, results=results)


@app.route('/optimize')
def optimize():
    """Optimize memory structure."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    optimizer = MemoryOptimizer(memory_root)
    output_dir = memory_root / "optimized"
    report = optimizer.optimize_memory_structure(output_dir)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Optimization Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Memory Optimization Results</h1>
        
        <p>Total memories: {{ report.total_memories }}</p>
        <p>Duplicate groups: {{ report.duplicate_groups|length }}</p>
        <p>Similar groups: {{ report.similar_groups|length }}</p>
        
        <h2>Optimization Suggestions</h2>
        <ul>
            {% for suggestion in report.optimization_suggestions %}
            <li>{{ suggestion }}</li>
            {% endfor %}
        </ul>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', report=report)


@app.route('/compress')
def compress():
    """Compress memories."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    compressor = MemoryCompressor(memory_root)
    output_dir = memory_root / "compressed"
    report = compressor.compress_all_memories(output_dir)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compression Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Memory Compression Results</h1>
        
        <p>Total memories: {{ report.total_memories }}</p>
        <p>Compressed memories: {{ report.compressed_count }}</p>
        <p>Kept memories: {{ report.kept_count }}</p>
        <p>Size before: {{ report.total_size_before }} bytes</p>
        <p>Size after: {{ report.total_size_after }} bytes</p>
        <p>Compression ratio: {{ "%.2f"|format(report.compression_ratio) }}%</p>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', report=report)


@app.route('/context_compress')
def context_compress():
    """Compress memory context."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    compressor = MemoryContextCompressor(memory_root)
    report = compressor.compress_all_memories()
    stats = compressor.get_compression_stats()
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Context Compression Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Context Compression Results</h1>
        
        <p>Total files: {{ report.total }}</p>
        <p>Compressed files: {{ report.compressed }}</p>
        <p>Skipped files: {{ report.skipped }}</p>
        <p>Error files: {{ report.errors }}</p>
        
        <h2>Compression Statistics</h2>
        <p>Total original size: {{ stats.total_original_size }} bytes</p>
        <p>Total compressed size: {{ stats.total_compressed_size }} bytes</p>
        <p>Overall compression ratio: {{ "%.2f"|format(stats.overall_compression_ratio * 100) }}%</p>
        
        <h2>Detailed Results</h2>
        <table>
            <tr>
                <th>File</th>
                <th>Status</th>
                <th>Original Size</th>
                <th>Compressed Size</th>
                <th>Compression Ratio</th>
            </tr>
            {% for file, result in report.details.items() %}
            <tr>
                <td>{{ file }}</td>
                <td>{{ result.status }}</td>
                <td>{{ result.original_size|default(0) }}</td>
                <td>{{ result.compressed_size|default(0) }}</td>
                <td>{{ "%.2f"|format(result.compression_ratio * 100 if result.compression_ratio else 0) }}%</td>
            </tr>
            {% endfor %}
        </table>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', report=report, stats=stats)


@app.route('/refresh')
def refresh():
    """Refresh memory index."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    # Rebuild index
    indexer = MemoryIndex(memory_root)
    index_path = memory_root / ".memory_index.json"
    indexer.save_index(index_path)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index Refreshed</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Memory Index Refreshed</h1>
        <p>The memory index has been successfully refreshed.</p>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''')


@app.route('/process_multimodal', methods=['POST'])
def process_multimodal():
    """Process multi-modal content and create a memory."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    if 'file' not in request.files:
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Error</h1>
        <p>No file uploaded.</p>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''')
    
    file = request.files['file']
    if file.filename == '':
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Error</h1>
        <p>No file selected.</p>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''')
    
    # Save the uploaded file
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(file.filename)[1], delete=False) as tmp:
        file.save(tmp)
        temp_file_path = tmp.name
    
    try:
        # Process the file
        processor = MultiModalProcessor()
        memory_content = processor.create_memory_from_multimodal(temp_file_path)
        
        # Save the memory
        memory_file_name = f"{os.path.splitext(file.filename)[0]}_memory.md"
        memory_path = memory_root / memory_file_name
        memory_path.write_text(memory_content, encoding="utf-8")
        
        # Clean up
        os.unlink(temp_file_path)
        
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Success</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Success</h1>
        <p>Multi-modal content processed and memory created successfully.</p>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''')
    except Exception as e:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Error</h1>
        <p>Error processing file: {{ error }}</p>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', error=str(e))


@app.route('/graph')
def graph_view():
    """View detailed memory association graph."""
    if not memory_root:
        return "Memory root not set. Please run with --memory-root option."
    
    # Get memory graph
    graph = MemoryGraph(memory_root)
    
    # Get memory manifest
    indexer = MemoryIndex(memory_root)
    manifest = indexer.get_manifest()
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memory Association Graph</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .graph-container {
            width: 100%;
            height: 700px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            margin-top: 20px;
        }
        .back-link {
            margin-top: 20px;
        }
        .legend {
            margin-top: 20px;
            display: flex;
            gap: 20px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }
    </style>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>Memory Association Graph</h1>
        
        <div class="graph-container" id="memoryGraph"></div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background-color: #1f77b4;"></div>
                <span>Text</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #ff7f0e;"></div>
                <span>Image</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #2ca02c;"></div>
                <span>Audio</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #d62728;"></div>
                <span>Video</span>
            </div>
        </div>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
    
    <script>
        // Detailed graph visualization using D3.js
        const graphData = {{
            nodes: [
                {% for memory in manifest %}
                {{ "{" }}id: "{{ memory.path.split('\\')[-1] }}", title: "{{ memory.title or memory.path.split('\\')[-1] }}", type: "{{ memory.file_type or 'text' }}"{{ "}," }}
                {% endfor %}
            ],
            links: [
                {% for memory in manifest %}
                {% set related = graph.get_related_memories(memory.path.split('\\')[-1], 5) %}
                {% for rel_memory, weight in related %}
                {{ "{" }}source: "{{ memory.path.split('\\')[-1] }}", target: "{{ rel_memory }}", weight: {{ weight }}{{ "}," }}
                {% endfor %}
                {% endfor %}
            ]
        }};
        
        const width = document.getElementById('memoryGraph').clientWidth;
        const height = document.getElementById('memoryGraph').clientHeight;
        
        const svg = d3.select('#memoryGraph')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        const simulation = d3.forceSimulation(graphData.nodes)
            .force('link', d3.forceLink(graphData.links).id(d => d.id).distance(120))
            .force('charge', d3.forceManyBody().strength(-400))
            .force('center', d3.forceCenter(width / 2, height / 2));
        
        const link = svg.append('g')
            .selectAll('line')
            .data(graphData.links)
            .enter()
            .append('line')
            .attr('stroke', '#999')
            .attr('stroke-width', d => Math.sqrt(d.weight) * 2);
        
        const node = svg.append('g')
            .selectAll('circle')
            .data(graphData.nodes)
            .enter()
            .append('circle')
            .attr('r', 12)
            .attr('fill', d => d.type === 'image' ? '#ff7f0e' : d.type === 'audio' ? '#2ca02c' : d.type === 'video' ? '#d62728' : '#1f77b4')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        const label = svg.append('g')
            .selectAll('text')
            .data(graphData.nodes)
            .enter()
            .append('text')
            .text(d => d.title.substring(0, 15) + '...')
            .attr('font-size', 12)
            .attr('dx', 15)
            .attr('dy', 5);
        
        // Add tooltips
        node.append('title')
            .text(d => d.title);
        
        simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node
                .attr('cx', d => d.x = Math.max(15, Math.min(width - 15, d.x)))
                .attr('cy', d => d.y = Math.max(15, Math.min(height - 15, d.y)));
            
            label
                .attr('x', d => d.x)
                .attr('y', d => d.y);
        });
        
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    </script>
</body>
</html>
''', graph=graph, manifest=manifest)


@app.route('/recommend', methods=['POST'])
def recommend():
    """Get memory recommendations based on context."""
    if not memory_root:
        return "Memory root not set. Please run with --memory-root option."
    
    context = request.form.get('context', '')
    
    # Initialize recommender
    behavior_db_path = memory_root / ".behavior_db.json"
    recommender = MemoryRecommender(memory_root, behavior_db_path)
    
    # Get recommendations
    recommendations = recommender.get_recommended_memories(context, 5)
    
    # Analyze context
    analyzer = MemoryContextAnalyzer()
    context_analysis = analyzer.analyze_text_context(context)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memory Recommendations</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        .memory-item {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #f0f0f0;
            border-radius: 4px;
        }
        .memory-item h4 {
            margin-top: 0;
            color: #555;
        }
        .memory-item .meta {
            font-size: 12px;
            color: #888;
            margin-bottom: 5px;
        }
        .memory-item .content {
            font-size: 14px;
            color: #333;
        }
        .score-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            background-color: #d1ecf1;
            color: #0c5460;
        }
        .context-analysis {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Memory Recommendations</h1>
        
        <div class="section">
            <h2>Context Analysis</h2>
            <div class="context-analysis">
                <p><strong>Keywords:</strong> {{ context_analysis.keywords|join(', ') }}</p>
                <p><strong>Entities:</strong> {{ context_analysis.entities|join(', ') }}</p>
                <p><strong>Context Length:</strong> {{ context_analysis.context_length }} characters</p>
            </div>
        </div>
        
        <div class="section">
            <h2>Recommended Memories</h2>
            {% if recommendations %}
                {% for memory in recommendations %}
                <div class="memory-item">
                    <div class="meta">
                        Type: {{ memory.type or 'unknown' }} | 
                        File Type: {{ memory.file_type or 'text' }} | 
                        <span class="score-badge">Score: {{ "%.2f"|format(memory.recommendation_score) }}</span>
                    </div>
                    <h4>{{ memory.title or 'Untitled' }}</h4>
                    <div class="content">{{ memory.description or 'No description' }}</div>
                </div>
                {% endfor %}
            {% else %}
                <p>No recommendations found for the given context.</p>
            {% endif %}
        </div>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', recommendations=recommendations, context_analysis=context_analysis)


@app.route('/ml_recommend', methods=['POST'])
def ml_recommend():
    """Get machine learning based recommendations."""
    if not memory_root:
        return "Memory root not set. Please run with --memory-root option."
    
    context = request.form.get('context', '')
    
    # Initialize ML recommender
    model_path = memory_root / ".memory_ml_model.pkl"
    memory_ml = MemoryML(memory_root, model_path)
    
    # Get recommendations
    recommendations = memory_ml.get_recommended_memories(context, 5)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Machine Learning Recommendations</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        .memory-item {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #f0f0f0;
            border-radius: 4px;
        }
        .memory-item h4 {
            margin-top: 0;
            color: #555;
        }
        .memory-item .meta {
            font-size: 12px;
            color: #888;
            margin-bottom: 5px;
        }
        .memory-item .content {
            font-size: 14px;
            color: #333;
        }
        .score-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            background-color: #d1ecf1;
            color: #0c5460;
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Machine Learning Recommendations</h1>
        
        <div class="section">
            <h2>Recommended Memories</h2>
            {% if recommendations %}
                {% for memory in recommendations %}
                <div class="memory-item">
                    <div class="meta">
                        Type: {{ memory.type or 'unknown' }} | 
                        File Type: {{ memory.file_type or 'text' }} | 
                        <span class="score-badge">Score: {{ "%.2f"|format(memory.recommendation_score) }}</span>
                        {% if memory.recommendation_method %}
                        | Method: {{ memory.recommendation_method }}
                        {% endif %}
                    </div>
                    <h4>{{ memory.title or 'Untitled' }}</h4>
                    <div class="content">{{ memory.description or 'No description' }}</div>
                </div>
                {% endfor %}
            {% else %}
                <p>No recommendations found for the given context.</p>
            {% endif %}
        </div>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', recommendations=recommendations)


@app.route('/personalized_recommend', methods=['POST'])
def personalized_recommend():
    """Get personalized recommendations."""
    if not memory_root:
        return "Memory root not set. Please run with --memory-root option."
    
    user_id = request.form.get('user_id', '')
    context = request.form.get('context', '')
    
    if not user_id:
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Error</h1>
        <p>Please enter a user ID.</p>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''')
    
    # Initialize personalizer
    profiles_dir = memory_root / ".user_profiles"
    behavior_db_path = memory_root / ".behavior_db.json"
    model_path = memory_root / ".memory_ml_model.pkl"
    personalizer = MemoryPersonalizer(memory_root, profiles_dir, behavior_db_path, model_path)
    
    # Get personalized recommendations
    recommendations = personalizer.get_personalized_recommendations(user_id, context, 5)
    
    # Get user insights
    insights = personalizer.get_user_insights(user_id)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personalized Recommendations</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        .memory-item {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #f0f0f0;
            border-radius: 4px;
        }
        .memory-item h4 {
            margin-top: 0;
            color: #555;
        }
        .memory-item .meta {
            font-size: 12px;
            color: #888;
            margin-bottom: 5px;
        }
        .memory-item .content {
            font-size: 14px;
            color: #333;
        }
        .score-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            background-color: #d1ecf1;
            color: #0c5460;
        }
        .user-insights {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Personalized Recommendations</h1>
        
        <div class="section">
            <h2>User Insights</h2>
            <div class="user-insights">
                <p><strong>User ID:</strong> {{ insights.user_id }}</p>
                <p><strong>Total Interactions:</strong> {{ insights.total_interactions }}</p>
                <p><strong>Most Common Actions:</strong> {{ insights.action_counts | items | list | join(', ') }}</p>
                <p><strong>Preferences:</strong> {{ insights.preferences | items | list | join(', ') }}</p>
            </div>
        </div>
        
        <div class="section">
            <h2>Recommended Memories</h2>
            {% if recommendations %}
                {% for memory in recommendations %}
                <div class="memory-item">
                    <div class="meta">
                        Type: {{ memory.type or 'unknown' }} | 
                        File Type: {{ memory.file_type or 'text' }} | 
                        <span class="score-badge">Score: {{ "%.2f"|format(memory.personalized_score) }}</span>
                    </div>
                    <h4>{{ memory.title or 'Untitled' }}</h4>
                    <div class="content">{{ memory.description or 'No description' }}</div>
                </div>
                {% endfor %}
            {% else %}
                <p>No personalized recommendations found for the given context.</p>
            {% endif %}
        </div>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', recommendations=recommendations, insights=insights)


@app.route('/lifecycle_report')
def lifecycle_report():
    """Get memory lifecycle report."""
    if not memory_root:
        return "Memory root not set. Please run with --memory-root option."
    
    # Initialize lifecycle manager
    archive_dir = memory_root / ".archive"
    config_path = memory_root / ".lifecycle_config.json"
    manager = MemoryLifecycleManager(memory_root, archive_dir, config_path)
    
    # Get lifecycle report
    report = manager.get_lifecycle_report()
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memory Lifecycle Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        .status-breakdown {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .status-card {
            flex: 1;
            min-width: 150px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
            text-align: center;
        }
        .status-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .status-label {
            font-size: 14px;
            color: #666;
        }
        .config-section {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Memory Lifecycle Report</h1>
        
        <div class="section">
            <h2>Memory Status Breakdown</h2>
            <div class="status-breakdown">
                {% for status, count in report.status_breakdown.items() %}
                <div class="status-card">
                    <div class="status-value">{{ count }}</div>
                    <div class="status-label">{{ status }}</div>
                </div>
                {% endfor %}
            </div>
            <p><strong>Total Memories:</strong> {{ report.total_memories }}</p>
            <p><strong>Archive Size:</strong> {{ report.archive_size }} bytes</p>
        </div>
        
        <div class="section">
            <h2>Configuration</h2>
            <div class="config-section">
                <p><strong>Active Days:</strong> {{ report.config.active_days }}</p>
                <p><strong>Archive Days:</strong> {{ report.config.archive_days }}</p>
                <p><strong>Delete Days:</strong> {{ report.config.delete_days }}</p>
                <p><strong>Auto Archive:</strong> {{ report.config.auto_archive }}</p>
                <p><strong>Auto Delete:</strong> {{ report.config.auto_delete }}</p>
            </div>
        </div>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', report=report)


@app.route('/run_lifecycle')
def run_lifecycle():
    """Run memory lifecycle management."""
    if not memory_root:
        return "Memory root not set. Please run with --memory-root option."
    
    # Initialize lifecycle manager
    archive_dir = memory_root / ".archive"
    config_path = memory_root / ".lifecycle_config.json"
    manager = MemoryLifecycleManager(memory_root, archive_dir, config_path)
    
    # Run lifecycle management
    results = manager.run_lifecycle()
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lifecycle Management Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        .results {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .result-card {
            flex: 1;
            min-width: 150px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
            text-align: center;
        }
        .result-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .result-label {
            font-size: 14px;
            color: #666;
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lifecycle Management Results</h1>
        
        <div class="section">
            <h2>Results</h2>
            <div class="results">
                <div class="result-card">
                    <div class="result-value">{{ results.archived }}</div>
                    <div class="result-label">Archived</div>
                </div>
                <div class="result-card">
                    <div class="result-value">{{ results.deleted }}</div>
                    <div class="result-label">Deleted</div>
                </div>
                <div class="result-card">
                    <div class="result-value">{{ results.errors }}</div>
                    <div class="result-label">Errors</div>
                </div>
            </div>
        </div>
        
        <div class="back-link">
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
''', results=results)


@app.route('/api/memories')
def api_memories():
    """API endpoint for memories."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    indexer = MemoryIndex(memory_root)
    manifest = indexer.get_manifest()
    return jsonify(manifest)


@app.route('/api/search')
def api_search():
    """API endpoint for search."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    query = request.args.get('q', '')
    indexer = MemoryIndex(memory_root)
    results = indexer.search(query)
    return jsonify(results)


@app.route('/api/quality')
def api_quality():
    """API endpoint for memory quality."""
    if not memory_root:
        return jsonify({"error": "Memory root not set"}), 400
    
    evaluator = MemoryQualityEvaluator(memory_root)
    evaluations = evaluator.evaluate_all_memories()
    return jsonify(evaluations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True)
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    global memory_root
    memory_root = Path(args.memory_root).expanduser()

    print(f"Starting Memory Manager on port {args.port}...")
    print(f"Memory root: {memory_root}")
    print(f"Access the web interface at: http://localhost:{args.port}")

    app.run(host='0.0.0.0', port=args.port, debug=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
