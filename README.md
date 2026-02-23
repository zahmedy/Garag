# GARAG
Market Place for Apartments

```
shiqah/
  apps/
    web/                # Next.js
    api/                # FastAPI
       app/
            main.py
            core/
                config.py
                security.py
                deps.py
            models/
            schemas/
            api/
                v1/
                routes/
                    auth.py
                    listings.py
                    search.py
                    leads.py
                    admin.py
            services/
                search_index.py
                media.py
                notifications.py
            db/
                session.py
                migrations/   # Alembic
    worker/             # celery/rq worker
  packages/
    shared/             # shared types (optional)
  infra/
    docker/
    compose.yaml
  docs/

```
