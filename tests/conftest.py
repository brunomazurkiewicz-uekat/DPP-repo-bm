import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Bruno"}

@pytest.fixture
def config_tmp(tmp_path):
    p = tmp_path / "config.ini"
    p.write_text("[app]\nmode=dev\n")
    return p
