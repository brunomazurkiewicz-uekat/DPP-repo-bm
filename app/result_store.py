import json
from pathlib import Path
from typing import Optional, Dict, Any

RESULTS_FILE = Path("image_results.jsonl")

def append_result(record: Dict[str, Any]) -> None:
    with RESULTS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def get_result(job_id: str) -> Optional[Dict[str, Any]]:
    if not RESULTS_FILE.exists():
        return None

    # czytamy od końca (najszybciej znajdzie świeże wyniki)
    lines = RESULTS_FILE.read_text(encoding="utf-8").splitlines()
    for line in reversed(lines):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("job_id") == job_id:
            return obj
    return None
