#!/bin/bash
gunicorn backend_new:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
