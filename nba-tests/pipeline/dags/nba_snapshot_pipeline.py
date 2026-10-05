"""Airflow DAG for approved NBA snapshot ingestion; no web scraping is performed."""

from __future__ import annotations

import json
import os
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path

import psycopg2
from airflow import DAG
from airflow.exceptions import AirflowSkipException
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow/lib")
from snapshot import read_snapshot, sha256_file, write_frontend_snapshot  # noqa: E402

INBOX = Path("/data/inbox")
RAW = Path("/data/raw")
PUBLISH = Path("/data/publish")


def require_approved_input(**context: object) -> str:
    if os.environ.get("NBA_SOURCE_MODE") != "approved_manual_snapshot":
        raise AirflowSkipException("No approved source adapter is configured; scheduled collection is disabled.")
    metadata, teams, players = read_snapshot(INBOX)
    run_id = str(uuid.uuid4())
    context["ti"].xcom_push(key="metadata", value=metadata)
    context["ti"].xcom_push(key="teams", value=teams)
    context["ti"].xcom_push(key="players", value=players)
    return run_id


def persist_and_materialize(**context: object) -> None:
    ti = context["ti"]
    run_id = ti.xcom_pull(task_ids="validate_input")
    metadata = ti.xcom_pull(task_ids="validate_input", key="metadata")
    teams = ti.xcom_pull(task_ids="validate_input", key="teams")
    players = ti.xcom_pull(task_ids="validate_input", key="players")
    raw_run = RAW / run_id
    raw_run.mkdir(parents=True, exist_ok=False)
    for name in ("metadata.json", "teams.json", "active_players.json"):
        shutil.copy2(INBOX / name, raw_run / name)

    with psycopg2.connect(os.environ["NBA_DATABASE_URL"]) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO ingestion_runs
                   (run_id, source_name, source_url, authorization_reference, captured_at, status)
                   VALUES (%s, %s, %s, %s, %s, 'validated')""",
                (run_id, metadata["source_name"], metadata["source_url"], metadata["authorization_reference"], metadata["captured_at"]),
            )
            for name, rows in (("teams", teams), ("players", players)):
                path = raw_run / ("active_players.json" if name == "players" else "teams.json")
                cursor.execute(
                    """INSERT INTO source_artifacts (run_id, dataset_name, storage_path, sha256, row_count)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (run_id, name, str(path), sha256_file(path), len(rows)),
                )
            cursor.executemany(
                "INSERT INTO teams (run_id, team_id, team_code, name) VALUES (%s, %s, %s, %s)",
                [(run_id, team["id"], team["Team"], team["name"]) for team in teams],
            )
            cursor.executemany(
                """INSERT INTO player_snapshots (run_id, player_index, name, team_code, position, age, stats)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                [
                    (run_id, player["index"], player["name"], player["Team"], player.get("Pos"), player.get("Age"), json.dumps(player))
                    for player in players
                ],
            )
    write_frontend_snapshot(PUBLISH / run_id, teams, players)


with DAG(
    dag_id="nba_approved_snapshot_to_postgres",
    description="Validates approved NBA snapshots, stores provenance, and materializes Angular-compatible candidates.",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["nba", "postgres", "provenance", "manual-approval"],
) as dag:
    validate_input = PythonOperator(task_id="validate_input", python_callable=require_approved_input)
    persist_candidate = PythonOperator(task_id="persist_candidate", python_callable=persist_and_materialize)
    validate_input >> persist_candidate
