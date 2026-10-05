# Traceability

## Scope and provenance boundary

The Git remote and imported revision are the source authority for application
code and existing sports-data artifacts. PIOS Registry stores only structural
metadata; it does not ingest source, datasets, notebooks, or scraped pages.

## Authoritative records

| Concern | Authority |
| --- | --- |
| Product identity and boundary | `manifest.yaml` |
| Runtime and data flow | `SYSTEM.md` |
| Development behavior | `BEHAVIOR.md` and `AGENTS.md` |
| Repository ownership | Root `registry/repositories.yaml` |
| Architecture and boundary decisions | `DECISIONS.md` |
| Verification evidence | `AUDIT.md` |
| Active priorities | `ROADMAP.md` and `TASKS.md` |
| Pipeline design and operation | `nba-tests/pipeline/README.md` and `nba-tests/pipeline/sql/001_nba_schema.sql` |

## Imported source

- Repository: `https://github.com/isaiapedro/nba-app.git`
- Imported branch: `main`
- Imported revision: `043fed7105c4a7d8818edc77d4a458be717cdf2b`
- Import date: 2026-09-18

Future data-source refreshes must identify the source, date, transformation,
usage constraints, and verification result without copying credentials or
authenticated session material into this record.

## Verification baseline

The 2026-09-21 verification record in `AUDIT.md` is authoritative for the
repaired dependency tree, production build, and deterministic browser tests.
Puppeteer is a development-only test dependency; its managed browser processes
bundled application data locally and does not add a remote data service,
telemetry, credentials, or Personal-data flow.

## Pipeline source boundary

The restored local pipeline records a source URL, authorization reference,
capture time, row count, and SHA-256 checksum for every approved snapshot.
Its raw artifacts and curated database rows remain in local Docker volumes.
The recovered Basketball Reference extraction code is provenance evidence, not
an approved source adapter; no scheduled collection or automatic publication is
authorized.

## Development dashboard boundary

The local Airflow dashboard uses root-designated development port `8765`.
It is deliberately credential-free for this prototype; the Compose mapping and
`webserver_config.py` are the enforcement points. Local-network exposure was
explicitly approved for browser access; authentication is mandatory before any
public exposure.

## Local access boundary

The Compose stack is credential-free only because its PostgreSQL services are
reachable exclusively on the internal Docker network and no Airflow webserver
is started. Scheduler CLI commands are the operational interface. A new stack
initialization will create fresh trust-only database volumes; the prior
password-era Airflow and NBA database volumes were intentionally deleted on
2026-09-21.
