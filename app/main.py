import json
from uuid import uuid4

import pika
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .queue_config import get_connection, QUEUE_NAME
from .image_analysis import detect_people_from_url
from .result_store import get_result

app = FastAPI(title="API + Kolejkowanie")


# --- MODELE ---
class AnalyzeImageRequest(BaseModel):
    url: str


class AnalyzeImageResponse(BaseModel):
    people_count: int


class AnalyzeImageQueuedResponse(BaseModel):
    job_id: str
    status: str = "queued"


# --- ENDPOINTY ---

@app.get("/")
def healthcheck():
    return {"hello": "world"}


@app.post("/analyze_img_sync", response_model=AnalyzeImageResponse)
def analyze_img_sync(body: AnalyzeImageRequest):
    try:
        count = detect_people_from_url(body.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analyze error: {e}")
    return AnalyzeImageResponse(people_count=count)


@app.post("/analyze_img", response_model=AnalyzeImageQueuedResponse, status_code=202)
def analyze_img(body: AnalyzeImageRequest):
    job_id = str(uuid4())
    message = json.dumps({"job_id": job_id, "url": body.url})

    conn = None
    try:
        conn = get_connection()
        ch = conn.channel()
        ch.queue_declare(queue=QUEUE_NAME, durable=True)

        ch.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),  # persistent
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Queue publish error: {e}")
    finally:
        try:
            if conn:
                conn.close()
        except Exception:
            pass

    return AnalyzeImageQueuedResponse(job_id=job_id)


@app.get("/analyze_img/{job_id}")
def analyze_img_result(job_id: str):
    res = get_result(job_id)
    if res is None:
        return {"job_id": job_id, "status": "pending"}
    return res
