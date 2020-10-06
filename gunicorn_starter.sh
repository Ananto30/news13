#!/bin/bash
gunicorn wsgi:app -b 0.0.0.0:5000 --access-logfile "-" --log-file "-" --log-level info