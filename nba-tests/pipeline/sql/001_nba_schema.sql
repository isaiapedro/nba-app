CREATE TABLE IF NOT EXISTS ingestion_runs (
  run_id UUID PRIMARY KEY,
  source_name TEXT NOT NULL,
  source_url TEXT NOT NULL,
  authorization_reference TEXT NOT NULL,
  captured_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('validated', 'published', 'rejected')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS source_artifacts (
  artifact_id BIGSERIAL PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES ingestion_runs(run_id),
  dataset_name TEXT NOT NULL CHECK (dataset_name IN ('teams', 'players')),
  storage_path TEXT NOT NULL,
  sha256 CHAR(64) NOT NULL,
  row_count INTEGER NOT NULL CHECK (row_count >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (run_id, dataset_name)
);

CREATE TABLE IF NOT EXISTS teams (
  run_id UUID NOT NULL REFERENCES ingestion_runs(run_id),
  team_id INTEGER NOT NULL,
  team_code TEXT NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY (run_id, team_id)
);

CREATE TABLE IF NOT EXISTS player_snapshots (
  run_id UUID NOT NULL REFERENCES ingestion_runs(run_id),
  player_index INTEGER NOT NULL,
  name TEXT NOT NULL,
  team_code TEXT NOT NULL,
  position TEXT,
  age NUMERIC,
  stats JSONB NOT NULL,
  PRIMARY KEY (run_id, player_index)
);

CREATE INDEX IF NOT EXISTS player_snapshots_run_team_idx
  ON player_snapshots (run_id, team_code);
