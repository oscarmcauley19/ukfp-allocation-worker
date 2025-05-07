from fastapi import FastAPI
from pydantic import BaseModel

from celery_app import run_simulation

app = FastAPI()


class JobRequest(BaseModel):
    user_ranking: list[int]
    runs: int


@app.post("/start-job")
async def start_job(request: JobRequest):
    task = run_simulation.apply_async(args=[request.user_ranking, request.runs])
    print("Task created with ID: " + str(task.id))
    return {"task_id": task.id}
