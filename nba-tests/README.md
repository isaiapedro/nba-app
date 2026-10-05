# NBA data pipeline

This directory preserves the recovered legacy extraction material and adds a
local-first Airflow/PostgreSQL replacement under `pipeline/`.

The historical `python_to_postgres_dag.py` is evidence of the original design,
not an executable deployment: its imported ETL functions, PostgreSQL schema,
container configuration, and dependency lock were absent.

## Safety boundary

The legacy code accesses Basketball Reference with `cloudscraper`. It is not
enabled by the restored pipeline. Sports Reference's data-use policy must be
reviewed and explicit permission obtained before any automated collection from
that source. The implemented DAG accepts only an approved, manually supplied
snapshot until an authorized source adapter is introduced and documented.

See [pipeline/README.md](pipeline/README.md) for setup, storage, operation,
and the approval gate.
