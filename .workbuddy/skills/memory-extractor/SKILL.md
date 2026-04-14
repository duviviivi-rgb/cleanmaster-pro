---
name: memory-extractor
description: Extract durable memories from recent conversation turns into user, feedback, project, and reference categories while avoiding stale code-state facts.
---

# Memory Extractor

Use this skill when you want to persist durable collaboration context from the latest conversation turns.

## Use It For

- capturing user preferences
- saving feedback about how to work
- recording non-code project constraints or deadlines
- storing pointers to external systems
- extracting information from images, audio, and video files

## Avoid It For

- storing code structure or file locations
- saving short-lived task state that belongs in a plan
- duplicating an existing memory topic without checking first

## Quick Start

Build a manifest of existing memories:

```bash
python3 {baseDir}/scripts/memory_manifest.py --memory-root /path/to/memory
```

Build and search memory index:

```bash
# Build index and search by keyword
python3 {baseDir}/scripts/memory_index.py --memory-root /path/to/memory --search "project deadline"

# Search by tag
python3 {baseDir}/scripts/memory_index.py --memory-root /path/to/memory --search "tag:important"

# Search by file type (for multimodal content)
python3 {baseDir}/scripts/memory_index.py --memory-root /path/to/memory --search "type:image"

# Search for related memories
python3 {baseDir}/scripts/memory_index.py --memory-root /path/to/memory --search "related:test_user_memory.md"
```

## Process multi-modal content

```bash
# Process an image and create a memory
python3 {baseDir}/scripts/memory_multimodal.py --file /path/to/image.jpg --output /path/to/memory/image_memory.md

# Process an audio file and create a memory
python3 {baseDir}/scripts/memory_multimodal.py --file /path/to/audio.mp3 --output /path/to/memory/audio_memory.md

# Process a video file and create a memory
python3 {baseDir}/scripts/memory_multimodal.py --file /path/to/video.mp4 --output /path/to/memory/video_memory.md
```

Then use the portable prompt in [references/prompt-template.md](./references/prompt-template.md).

## Four Types

- `user`
- `feedback`
- `project`
- `reference`

## Rules

- save only durable signals
- avoid code-state facts that can drift
- prefer updating an existing topic file
- organize by topic, not chronology

## Supporting Files

- Prompt template: [references/prompt-template.md](./references/prompt-template.md)
- Source notes: [references/source-notes.md](./references/source-notes.md)
- Helper script: `python3 {baseDir}/scripts/memory_manifest.py ...`
- Memory index script: `python3 {baseDir}/scripts/memory_index.py ...`
- Memory quality script: `python3 {baseDir}/scripts/memory_quality.py ...`
- Memory optimizer script: `python3 {baseDir}/scripts/memory_optimizer.py ...`
- Memory compressor script: `python3 {baseDir}/scripts/memory_compressor.py ...`
- Memory manager script: `python3 {baseDir}/scripts/memory_manager.py ...`
- Memory updater script: `python3 {baseDir}/scripts/memory_updater.py ...`
- Memory recommender script: `python3 {baseDir}/scripts/memory_recommender.py ...`
