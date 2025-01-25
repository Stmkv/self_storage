#!/bin/bash

if [ "$1" == "web" ]; then
  python manage.py migrate --noinput

  exec python manage.py runserver 0.0.0.0:8000
else
  echo "Неизвестный параметр: $1. Используйте 'web' или 'bot'."
  exit 1
fi
