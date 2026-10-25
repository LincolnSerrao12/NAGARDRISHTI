#!/usr/bin/env python3
"""
Cleanup script to remove old processed videos
Prevents uploads folder from growing too large
"""

import os
import time
from pathlib import Path
from datetime import datetime, timedelta

UPLOADS_FOLDER = 'uploads'
MAX_AGE_HOURS = 24  # Delete videos older than 24 hours
MAX_FOLDER_SIZE_MB = 1000  # Keep folder under 1GB

def get_file_age_hours(file_path):
    """Get age of file in hours"""
    mtime = os.path.getmtime(file_path)
    age_seconds = time.time() - mtime
    return age_seconds / 3600

def get_folder_size_mb():
    """Get total size of uploads folder in MB"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(UPLOADS_FOLDER):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total += os.path.getsize(filepath)
    return total / (1024 * 1024)

def cleanup_old_videos():
    """Remove videos older than MAX_AGE_HOURS"""
    if not os.path.exists(UPLOADS_FOLDER):
        print(f"📁 Folder not found: {UPLOADS_FOLDER}")
        return

    videos = [f for f in os.listdir(UPLOADS_FOLDER) if f.startswith('output_') and f.endswith('.mp4')]

    if not videos:
        print("✅ No videos to clean up")
        return

    deleted_count = 0
    freed_space = 0

    for video in videos:
        video_path = os.path.join(UPLOADS_FOLDER, video)
        age_hours = get_file_age_hours(video_path)
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)

        if age_hours > MAX_AGE_HOURS:
            try:
                os.remove(video_path)
                deleted_count += 1
                freed_space += file_size_mb
                print(f"🗑️  Deleted: {video} ({file_size_mb:.2f}MB, age: {age_hours:.1f}h)")
            except Exception as e:
                print(f"⚠️  Failed to delete {video}: {e}")

    if deleted_count > 0:
        print(f"\n✅ Cleanup complete!")
        print(f"   Deleted: {deleted_count} files")
        print(f"   Freed: {freed_space:.2f}MB")
    else:
        print("✅ All videos are recent, nothing to delete")

def cleanup_by_size():
    """Remove oldest videos if folder exceeds MAX_FOLDER_SIZE_MB"""
    if not os.path.exists(UPLOADS_FOLDER):
        return

    current_size = get_folder_size_mb()

    if current_size <= MAX_FOLDER_SIZE_MB:
        print(f"✅ Folder size OK: {current_size:.2f}MB / {MAX_FOLDER_SIZE_MB}MB")
        return

    print(f"⚠️  Folder size exceeded: {current_size:.2f}MB / {MAX_FOLDER_SIZE_MB}MB")
    print(f"🧹 Removing oldest videos...")

    videos = []
    for f in os.listdir(UPLOADS_FOLDER):
        if f.startswith('output_') and f.endswith('.mp4'):
            path = os.path.join(UPLOADS_FOLDER, f)
            mtime = os.path.getmtime(path)
            size = os.path.getsize(path)
            videos.append((path, mtime, size))

    # Sort by modification time (oldest first)
    videos.sort(key=lambda x: x[1])

    deleted_count = 0
    freed_space = 0

    for video_path, mtime, size in videos:
        if current_size <= MAX_FOLDER_SIZE_MB:
            break

        try:
            os.remove(video_path)
            deleted_count += 1
            freed_space += size / (1024 * 1024)
            current_size -= size / (1024 * 1024)
            print(f"🗑️  Deleted: {os.path.basename(video_path)} ({size / (1024 * 1024):.2f}MB)")
        except Exception as e:
            print(f"⚠️  Failed to delete {video_path}: {e}")

    print(f"\n✅ Cleanup by size complete!")
    print(f"   Deleted: {deleted_count} files")
    print(f"   Freed: {freed_space:.2f}MB")
    print(f"   New folder size: {current_size:.2f}MB")

def show_stats():
    """Show statistics about uploads folder"""
    if not os.path.exists(UPLOADS_FOLDER):
        print(f"📁 Folder not found: {UPLOADS_FOLDER}")
        return

    videos = [f for f in os.listdir(UPLOADS_FOLDER) if f.startswith('output_') and f.endswith('.mp4')]

    if not videos:
        print("✅ No videos in uploads folder")
        return

    print(f"\n📊 Uploads Folder Statistics")
    print(f"{'=' * 60}")
    print(f"Total videos: {len(videos)}")
    print(f"Folder size: {get_folder_size_mb():.2f}MB")
    print(f"\nVideo Files:")
    print(f"{'=' * 60}")

    total_size = 0
    for video in sorted(videos):
        path = os.path.join(UPLOADS_FOLDER, video)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        age_hours = get_file_age_hours(path)
        created = datetime.fromtimestamp(os.path.getmtime(path))
        total_size += size_mb

        print(f"📹 {video}")
        print(f"   Size: {size_mb:.2f}MB | Age: {age_hours:.1f}h | Created: {created.strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"{'=' * 60}")
    print(f"Total size: {total_size:.2f}MB")

if __name__ == '__main__':
    import sys

    print("\n🧹 Pothole Detection - Video Cleanup Tool")
    print("=" * 60)

    if len(sys.argv) > 1:
        if sys.argv[1] == 'stats':
            show_stats()
        elif sys.argv[1] == 'clean-old':
            cleanup_old_videos()
        elif sys.argv[1] == 'clean-size':
            cleanup_by_size()
        elif sys.argv[1] == 'clean-all':
            cleanup_old_videos()
            cleanup_by_size()
        else:
            print(f"Usage: python cleanup_videos.py [stats|clean-old|clean-size|clean-all]")
    else:
        # Default: show stats and cleanup old videos
        show_stats()
        print()
        cleanup_old_videos()
        print()
        cleanup_by_size()
