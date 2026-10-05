"""Validation and publication helpers for the NBA frontend snapshot contract."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


class SnapshotValidationError(ValueError):
    """Raised when an input snapshot cannot safely be published."""


MULTI_TEAM_CODE = re.compile(r"^\d+TM$")


def read_snapshot(inbox: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    metadata = _read_json(inbox / "metadata.json")
    teams_payload = _read_json(inbox / "teams.json")
    players_payload = _read_json(inbox / "active_players.json")
    teams = teams_payload.get("teams")
    players = players_payload.get("players")

    if not isinstance(teams, list) or not isinstance(players, list):
        raise SnapshotValidationError("teams.json and active_players.json must use the Angular envelope format")
    validate_snapshot(metadata, teams, players)
    return metadata, teams, players


def validate_snapshot(metadata: dict[str, Any], teams: list[dict[str, Any]], players: list[dict[str, Any]]) -> None:
    required_metadata = {"source_name", "source_url", "authorization_reference", "captured_at"}
    missing_metadata = required_metadata - metadata.keys()
    if missing_metadata:
        raise SnapshotValidationError(f"metadata is missing: {', '.join(sorted(missing_metadata))}")
    try:
        datetime.fromisoformat(str(metadata["captured_at"]).replace("Z", "+00:00"))
    except ValueError as error:
        raise SnapshotValidationError("captured_at must be ISO-8601") from error

    if len(teams) != 30:
        raise SnapshotValidationError("an NBA snapshot must contain exactly 30 teams")
    team_ids = [team.get("id") for team in teams]
    if len(set(team_ids)) != len(team_ids) or any(not isinstance(team_id, int) for team_id in team_ids):
        raise SnapshotValidationError("team IDs must be unique integers")
    for team in teams:
        if not all(isinstance(team.get(key), str) and team[key].strip() for key in ("Team", "name")):
            raise SnapshotValidationError("each team requires non-empty Team and name fields")

    if not players:
        raise SnapshotValidationError("a player snapshot cannot be empty")
    player_ids = [player.get("index") for player in players]
    if len(set(player_ids)) != len(player_ids) or any(not isinstance(player_id, int) for player_id in player_ids):
        raise SnapshotValidationError("player indexes must be unique integers")
    valid_team_codes = {team["Team"] for team in teams}
    for player in players:
        if not isinstance(player.get("name"), str) or not player["name"].strip():
            raise SnapshotValidationError("each player requires a non-empty name")
        team_code = player.get("Team")
        if team_code not in valid_team_codes and not (isinstance(team_code, str) and MULTI_TEAM_CODE.fullmatch(team_code)):
            raise SnapshotValidationError(f"player {player['name']} references an unknown team")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_frontend_snapshot(destination: Path, teams: list[dict[str, Any]], players: list[dict[str, Any]]) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "teams.json").write_text(json.dumps({"teams": teams}, indent=2) + "\n", encoding="utf-8")
    (destination / "active_players.json").write_text(
        json.dumps({"players": players}, indent=2) + "\n", encoding="utf-8",
    )


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SnapshotValidationError(f"required input file is absent: {path.name}") from error
    except json.JSONDecodeError as error:
        raise SnapshotValidationError(f"{path.name} is not valid JSON") from error
    if not isinstance(payload, dict):
        raise SnapshotValidationError(f"{path.name} must contain a JSON object")
    return payload
