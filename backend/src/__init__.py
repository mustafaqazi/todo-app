"""Todo backend application."""

import sys
from pathlib import Path

# Add parent directory to path so we can import config and db
sys.path.insert(0, str(Path(__file__).parent.parent))
