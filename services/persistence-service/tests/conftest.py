import sys
from pathlib import Path

# add the service root to python path
SERVICE_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(SERVICE_ROOT))