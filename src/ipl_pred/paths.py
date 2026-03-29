"""Repository-root-relative paths. Wire up YAML loading here when you add PyYAML."""

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

RAW_DATA_DIR = _REPO_ROOT / "raw-data"
PROCESSED_DATA_DIR = _REPO_ROOT / "processed-data"
CONFIGS_DIR = _REPO_ROOT / "configs"
DEFAULT_CONFIG_PATH = CONFIGS_DIR / "default.yaml"
