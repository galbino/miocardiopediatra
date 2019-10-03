#!/bin/bash
gunicorn -t 7200 -w 1 --threads 8 --bind 0.0.0.0:8080 app:app
