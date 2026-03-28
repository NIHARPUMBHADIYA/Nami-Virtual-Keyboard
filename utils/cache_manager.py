"""
Cache Manager Utility
Handles cache directory creation and management for the gesture keyboard system.
"""

import os
import shutil
from pathlib import Path

class CacheManager:
    """Manages cache directory and files for the gesture keyboard system."""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.ensure_cache_dir()
    
    def ensure_cache_dir(self):
        """Ensure the cache directory exists."""
        self.cache_dir.mkdir(exist_ok=True)
        print(f"✓ Cache directory ready: {self.cache_dir}")
    
    def get_cache_path(self, filename: str) -> str:
        """Get the full path for a cache file."""
        return str(self.cache_dir / filename)
    
    def clear_cache(self):
        """Clear all cache files."""
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.ensure_cache_dir()
            print("✓ Cache cleared")
    
    def list_cache_files(self):
        """List all files in the cache directory."""
        if not self.cache_dir.exists():
            return []
        
        files = list(self.cache_dir.glob("*"))
        return [f.name for f in files if f.is_file()]
    
    def get_cache_size(self) -> int:
        """Get total size of cache directory in bytes."""
        if not self.cache_dir.exists():
            return 0
        
        total_size = 0
        for file_path in self.cache_dir.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size

# Global cache manager instance
cache_manager = CacheManager()

def get_cache_path(filename: str) -> str:
    """Convenience function to get cache file path."""
    return cache_manager.get_cache_path(filename)

def ensure_cache_dir():
    """Convenience function to ensure cache directory exists."""
    cache_manager.ensure_cache_dir()