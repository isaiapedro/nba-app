# Local Airflow and PostgreSQL pipeline

## What it does

The DAG `nba_approved_snapshot_to_postgres` accepts an approved local snapshot,
validates the Angular JSON contract, stores immutable raw copies plus checksums,
loads curated records into PostgreSQL, and writes a publish candidate. It does
not fetch the web, use credentials, expose a host port, or modify the Angular
application automatically.

## Storage

| Storage | Contents | Retention |
| --- | --- | --- |
| `airflow_db` Docker volume | Airflow metadata and task state | operational; delete only with the stack |
| `nba_db` Docker volume | validated runs, provenance, teams, player snapshots | retained until an intentional dataset purge |
| `nba_raw` Docker volume | immutable supplied JSON per run | retained with its matching curated run |
| `nba_publish` Docker volume | Angular-compatible candidate per run | retained until superseded/reviewed |
| Angular `src/app/data/` | manually promoted public browser snapshot | versioned in the application repository |

## Setup

```bash
cd nba-tests/pipeline
cp .env.example .env
# set AIRFLOW_UID to `id -u` if files promoted to the app should be owned by your user
docker compose build
docker compose up airflow-init
docker compose up -d airflow-webserver airflow-scheduler
```

The Airflow dashboard is available without a login at
`http://localhost:8765`. It is published on the development network so a
browser/port-forwarding layer can reach it. Its two PostgreSQL instances use
`trust` authentication only on Docker's internal network. Do not use this
unauthenticated mapping for a public deployment. Use
`docker compose exec airflow-scheduler airflow dags list` for CLI operations.

## Ingest an approved snapshot

Copy three files into the `nba_inbox` volume at `/data/inbox`:

```text
metadata.json
teams.json
active_players.json
```

`teams.json` must be `{ "teams": [...] }`, and `active_players.json` must be
`{ "players": [...] }`. `metadata.json` must declare `source_name`,
`source_url`, `authorization_reference`, and an ISO-8601 `captured_at` time.
The authorization reference is mandatory: it is the record of the data owner's
permission or licence.

Player records must reference one of the 30 team codes. Source-level aggregate
codes such as `2TM` are retained as multi-team season rows and are not assigned
to a roster page.

Run the DAG manually only after source approval. It writes the candidate into
`nba_publish/<run-id>/`. Review its row counts, provenance, and frontend build.
Promotion is a separate, human-controlled repository change.

After review, promote only the selected run:

```bash
docker compose exec airflow-scheduler \
  python /opt/airflow/pipeline/scripts/promote_snapshot.py <run-id>
```

The command mounts only `src/app/data/` and replaces its two generated JSON
snapshots. Run the Angular build and tests afterward, then review the Git diff
before committing.

## Source policy

The recovered Basketball Reference/`cloudscraper` extractor is intentionally
not connected to this DAG. Sports Reference's published policy restricts
automated access and use of scraped data for websites/tools. Add an automated
adapter only for a source with documented permission or licence, and update the
project's `DECISIONS.md`, `AUDIT.md`, and `TRACEABILITY.md` before enabling a
schedule.
