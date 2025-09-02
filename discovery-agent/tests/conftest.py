"""
Pytest configuration and fixtures for discovery-agent tests
"""

import sys
import os
from pathlib import Path


def pytest_configure(config):
    """Configure pytest with proper import paths"""
    # Get the absolute path to the src directory
    # This works regardless of the current working directory
    tests_dir = Path(__file__).parent
    project_root = tests_dir.parent
    src_dir = project_root / 'src'

    # Add src directory to Python path if not already there
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    # Also add the project root for any other imports
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


def pytest_sessionstart(session):
    """Ensure imports are working at session start"""
    try:
        # Test that we can import from src
        import src.models
        import src.mcp.core.client
    except ImportError as e:
        raise ImportError(f"Failed to import src modules: {e}. "
                         f"Python path: {sys.path[:3]}...") from e
