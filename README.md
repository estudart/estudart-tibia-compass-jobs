# estudart-tibia-compass-jobs

Python batch jobs that feed the Tibia Compass Postgres database (the same one `estudart-tibia-compass-be` reads from). Each job is a standalone script pulling from the public [TibiaData API](https://api.tibiadata.com) and writing normalized rows via SQLAlchemy, packaged as a Docker image and run as a **Cloud Run Job** (not a long-running Service — it runs to completion and exits).

## Jobs

| Job | Entry point | What it does |
|---|---|---|
| `killstatistics` | `src/jobs/killstatistics/main.py` | For each world in `settings.world_list`, calls `GET /v4/killstatistics/{world}`, upserts one row per creature race into `kill_statistics` |

## Project layout

```
src/
  config.py                                # pydantic-settings: world/town/character lists, database_url
  infrastructure/
    adapters/tibia_api_adapter.py           # thin requests wrapper over api.tibiadata.com
    database/database.py                   # SQLAlchemy engine + session factory + declarative Base
    database/tables/kill_statistics.py      # ORM table (snake_case columns, matches Postgres directly)
    database/repositories/kill_statistics.py # save() — insert + commit
  jobs/killstatistics/
    main.py                                 # create_tables() then KillStatisticsSync.sync_db()
    Dockerfile                              # entrypoint: python -m src.jobs.killstatistics.main
```

Note the columns in `kill_statistics.py` are snake_case (`last_day_players_killed`, etc.) on purpose — this table is written here in Python and read by the NestJS backend's TypeORM entity, so the entity on that side maps explicit snake_case columns rather than relying on camelCase auto-mapping.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

Loaded via `pydantic-settings` (`Settings.Config.env_file = ".env"`, see `src/config.py`).

| Var | Default if unset | Notes |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres@localhost:5432/test_db` | Full SQLAlchemy DSN. Currently commented out in `.env` — uncomment and point at Cloud SQL for a real run. |

## Run locally

```bash
python -m src.jobs.killstatistics.main
```

This creates the `kill_statistics` table if it doesn't exist (`Base.metadata.create_all`), then syncs every configured world.

## Deployment (Cloud Run Jobs)

```bash
make deploy
```

`deploy.sh`:

1. Builds `src/jobs/killstatistics/Dockerfile` for `linux/amd64`.
2. Tags the image with a unix timestamp (override with `TAG=... make deploy` for a reproducible tag).
3. Pushes to `us-central1-docker.pkg.dev/estudart-tibia-compass/tibia-compass/killstatistics-job`.
4. Runs `gcloud run jobs deploy killstatistics-job`, attached to the `tibia-vpc` network/subnet with `--vpc-egress=private-ranges-only` — required so the job can reach Cloud SQL over its private IP, same as the backend.

This only builds and deploys the Job definition; it does **not** execute it. Trigger a run manually with:

```bash
gcloud run jobs execute killstatistics-job --region=us-central1 --project=estudart-tibia-compass
```

or set up a Cloud Scheduler trigger for recurring syncs. Env vars (`DATABASE_URL`) must be set on the Job itself via `gcloud run jobs update killstatistics-job --update-env-vars DATABASE_URL=...` — `deploy.sh` doesn't touch job config, only the image.
