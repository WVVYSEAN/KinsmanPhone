web: /app/.venv/bin/python manage.py migrate --noinput && /app/.venv/bin/python manage.py collectstatic --noinput && /app/.venv/bin/gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file - --access-logfile -
worker: /app/.venv/bin/celery -A config worker --loglevel=info --concurrency=4
