import sys
sys.path.append('./src')

import time
import json
import pandas as pd
import redis
from celery import Celery

from simulations import perform_simulations

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

def update_progress(task_id, progress):
    """
    Update the progress of the task in Redis.
    """
    redis_client.set(f"task_progress:{task_id}", progress)

@celery_app.task(bind=True)
def run_simulation(self, user_ranking, runs):
    task_id = self.request.id
    print(task_id)
    result = perform_simulations(user_ranking, runs, lambda progress : update_progress(task_id, progress))

    print("Simulation completed")
    print(result)

    # Ensure the result is JSON serializable before storing it in Redis
    redis_client.set(f"result:{task_id}", json.dumps(result))  # Store the result in Redis

    for i in range(1, 101):
        time.sleep(0.1)  # Simulate processing delay
        progress = i  # Update progress percentage
        redis_client.set(f"task_progress:{task_id}", progress)  # Store progress

    return {"status": "completed", "job_id": task_id}
