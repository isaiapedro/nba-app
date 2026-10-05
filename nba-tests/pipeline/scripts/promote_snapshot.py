"""Copy one reviewed pipeline candidate into the Angular application's static-data contract."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: promote_snapshot.py <run-id>")
    run_id = sys.argv[1]
    candidate = Path("/data/publish") / run_id
    target = Path("/workspace/src/app/data")
    for filename in ("teams.json", "active_players.json"):
        source = candidate / filename
        if not source.is_file():
            raise SystemExit(f"candidate is incomplete: {source}")
        shutil.copy2(source, target / filename)


if __name__ == "__main__":
    main()
