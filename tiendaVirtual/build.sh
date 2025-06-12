#!/usr/bin/env bash

# Build commands for Render
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
