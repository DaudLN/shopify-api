#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Populate database"
python manage.py seed_db --no-input --clear

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
python manage.py collectstatic --no-input --clear
exec "$@"