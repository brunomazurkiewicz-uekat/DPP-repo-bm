import json
from datetime import datetime

import pika

from .queue_config import get_connection, QUEUE_NAME
from .image_analysis import detect_people_from_url
from .result_store import append_result


def callback(ch, method, properties, body: bytes):
    data = json.loads(body.decode("utf-8"))
    job_id = data["job_id"]
    url = data["url"]

    print(f"[consumer] Start job_id={job_id}")

    try:
        people_count = detect_people_from_url(url)
        status = "done"
        error = None
    except Exception as e:
        people_count = None
        status = "error"
        error = str(e)

    record = {
        "job_id": job_id,
        "url": url,
        "people_count": people_count,
        "status": status,
        "error": error,
        "timestamp": datetime.utcnow().isoformat(),
    }

    append_result(record)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[consumer] Done job_id={job_id} status={status}")


def main():
    conn = get_connection()
    channel = conn.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print("[consumer] Waiting for tasks. Ctrl+C to exit.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
