import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1] / "lib"))
from snapshot import SnapshotValidationError, read_snapshot, write_frontend_snapshot


def metadata() -> dict[str, str]:
    return {
        "source_name": "approved fixture",
        "source_url": "https://example.invalid/nba",
        "authorization_reference": "fixture-only",
        "captured_at": "2026-09-21T00:00:00Z",
    }


def teams() -> list[dict[str, object]]:
    return [{"id": index, "Team": f"T{index}", "name": f"Team {index}"} for index in range(30)]


def players() -> list[dict[str, object]]:
    return [{"index": 1, "name": "Example Player", "Team": "T0", "Pos": "G", "Age": 25}]


class SnapshotContractTests(unittest.TestCase):
    def test_reads_and_rewrites_the_angular_envelopes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inbox = Path(directory) / "inbox"
            inbox.mkdir()
            (inbox / "metadata.json").write_text(json.dumps(metadata()), encoding="utf-8")
            (inbox / "teams.json").write_text(json.dumps({"teams": teams()}), encoding="utf-8")
            (inbox / "active_players.json").write_text(json.dumps({"players": players()}), encoding="utf-8")

            _, loaded_teams, loaded_players = read_snapshot(inbox)
            output = Path(directory) / "output"
            write_frontend_snapshot(output, loaded_teams, loaded_players)

            self.assertEqual(json.loads((output / "teams.json").read_text())["teams"], teams())
            self.assertEqual(json.loads((output / "active_players.json").read_text())["players"], players())

    def test_rejects_players_for_unknown_teams(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inbox = Path(directory)
            (inbox / "metadata.json").write_text(json.dumps(metadata()), encoding="utf-8")
            (inbox / "teams.json").write_text(json.dumps({"teams": teams()}), encoding="utf-8")
            (inbox / "active_players.json").write_text(
                json.dumps({"players": [{**players()[0], "Team": "UNKNOWN"}]}), encoding="utf-8",
            )

            with self.assertRaises(SnapshotValidationError):
                read_snapshot(inbox)

    def test_accepts_a_source_multi_team_aggregate_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inbox = Path(directory)
            (inbox / "metadata.json").write_text(json.dumps(metadata()), encoding="utf-8")
            (inbox / "teams.json").write_text(json.dumps({"teams": teams()}), encoding="utf-8")
            (inbox / "active_players.json").write_text(
                json.dumps({"players": [{**players()[0], "Team": "2TM"}]}), encoding="utf-8",
            )

            _, _, loaded_players = read_snapshot(inbox)

            self.assertEqual(loaded_players[0]["Team"], "2TM")
