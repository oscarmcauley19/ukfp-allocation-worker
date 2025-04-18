from fastapi import FastAPI
from pydantic import BaseModel

from celery_app import run_simulation

app = FastAPI()


class JobRequest(BaseModel):
    job_id: str


@app.post("/start-job")
async def start_job(request: JobRequest):
    task = run_simulation.apply_async(args=[request.job_id])
    return {"task_id": task.id}
