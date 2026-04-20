"""Configuration for ukfp-allocation-worker.

Expose connection URLs via environment variables with sensible defaults so
other modules (like `celery_app`) can import these settings.

This module will attempt to load a `.env` file located at the worker root
(`.. / .env` relative to this file) using `python-dotenv` if that package is
installed. Process environment variables (exported) always take precedence
over `.env` entries (override=False).
"""
import os
from pathlib import Path

# Try to load a .env file from the worker root if python-dotenv is available.
# This is optional — if python-dotenv isn't installed we simply read real
# environment variables as before.
try:
	from dotenv import load_dotenv
except Exception:
	load_dotenv = None

# Look for .env one level above src (i.e., the worker project root)
env_path = Path(__file__).resolve().parent.parent / ".env"
if load_dotenv:
	# Do not override already-set environment variables.
	load_dotenv(env_path, override=False)

# AMQP broker for Celery (RabbitMQ)
# Example: 'pyamqp://guest@localhost//'
BROKER_URL = os.getenv("BROKER_URL", "pyamqp://guest@localhost//")

# Redis connection settings. Prefer explicit host/port/db environment
# variables. We compute a REDIS_URL from these so callers that expect a URL
# (e.g. Celery backend) can still use it.
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
try:
	REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
except ValueError:
	REDIS_PORT = 6379
try:
	REDIS_DB = int(os.getenv("REDIS_DB", "0"))
except ValueError:
	REDIS_DB = 0

# Construct REDIS_URL from host/port/db so Celery/backend code can use a URL
# while the rest of the code can use host/port directly.
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
