#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py migrate

# Create the superuser ONLY when a password is supplied via the environment.
# There is deliberately no default — a public deployment must never ship with
# a password that is published in this repository.
if [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ['DJANGO_SUPERUSER_PASSWORD']

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created')
else:
    print('Superuser already exists')
PYEOF
else
  echo "DJANGO_SUPERUSER_PASSWORD not set - skipping superuser creation."
fi

# Demo data for the public showcase deployment (idempotent, safe to re-run).
if [ "${SEED_DEMO_DATA:-true}" = "true" ]; then
  python manage.py seed_data
fi
