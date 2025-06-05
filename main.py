from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict
import uuid
import time
import asyncio

app = FastAPI()

# Storage for all jobs
all_jobs: Dict[str, dict] = {}
job_list = []  # Each job = (priority, time_created, job_id, batch_id, ids)
is_processing = False

# Priority levels for sorting
priority_levels = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}

# Request body structure
class JobInput(BaseModel):
    ids: List[int]
    priority: str

@app.post("/ingest")
async def ingest_data(data: JobInput, background: BackgroundTasks):
    job_id = str(uuid.uuid4())
    time_created = time.time()

    # Break into groups of 3 ids
    batches = []
    for i in range(0, len(data.ids), 3):
        group = data.ids[i:i+3]
        batch_id = str(uuid.uuid4())
        batches.append({
            "batch_id": batch_id,
            "ids": group,
            "status": "yet_to_start"
        })
        job_list.append((data.priority.upper(), time_created, job_id, batch_id, group))

    # Save job
    all_jobs[job_id] = {
        "created_time": time_created,
        "priority": data.priority.upper(),
        "batches": batches,
        "status": "yet_to_start"
    }

    if not is_processing:
        background.add_task(start_processing)

    return {"ingestion_id": job_id}

@app.get("/status/{job_id}")
def get_job_status(job_id: str):
    job = all_jobs.get(job_id)
    if not job:
        return {"error": "Job not found"}

    # Calculate overall status
    batch_states = [b["status"] for b in job["batches"]]
    if all(state == "completed" for state in batch_states):
        job["status"] = "completed"
    elif any(state == "triggered" for state in batch_states):
        job["status"] = "triggered"
    else:
        job["status"] = "yet_to_start"

    return {
        "ingestion_id": job_id,
        "status": job["status"],
        "batches": job["batches"]
    }

async def start_processing():
    global is_processing
    is_processing = True

    while job_list:
        # Sort by priority and creation time
        job_list.sort(key=lambda x: (priority_levels[x[0]], x[1]))
        prio, created, job_id, batch_id, ids = job_list.pop(0)

        # Mark batch as triggered
        for batch in all_jobs[job_id]["batches"]:
            if batch["batch_id"] == batch_id:
                batch["status"] = "triggered"

        await asyncio.sleep(2)  # simulate external API delay

        # Mark batch as completed
        for batch in all_jobs[job_id]["batches"]:
            if batch["batch_id"] == batch_id:
                batch["status"] = "completed"

        await asyncio.sleep(5)  # rate limit (1 batch per 5 sec)

    is_processing = False
