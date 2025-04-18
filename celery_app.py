import time

import pandas as pd
import redis
from celery import Celery

# Set up Celery with RabbitMQ as the broker and Redis as the result backend
celery_app = Celery(
    "tasks",
    broker="pyamqp://guest@localhost//",
    backend="redis://localhost:6379/0",  # TODO make this configurable
)

# Store progress in Redis
redis_client = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


@celery_app.task(bind=True)
def run_simulation(self, job_id):
    """Simulates a long-running data processing task and tracks progress."""
    df = pd.DataFrame({"value": range(1, 101)})  # Sample DataFrame

    for i in range(1, 101):
        time.sleep(0.1)  # Simulate processing delay
        progress = i  # Update progress percentage
        redis_client.set(f"task_progress:{job_id}", progress)  # Store progress

    return {"status": "completed", "job_id": job_id}
