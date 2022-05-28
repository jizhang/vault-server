# Vault

> Vault 687 in Gringotts Wizarding Bank
>
> "Inside were mounds of gold coins. Columns of silver. Heaps of little bronze Knuts."
>
> -- Description of the interior of the Potter vault

## Quick Start

```
python3.8 -m venv venv
source venv/bin/activate
make dev
make web
```

Run job:

```
python scripts/job.py user_count
```

## Production

Set environment variables, or create `.env` file:

```
FLASK_ENV=production
APP_CONFIG=/path/to/production_settings.py
```

Start WSGI server:

```
waitress-serve --port=5050 scripts.web:app
```
