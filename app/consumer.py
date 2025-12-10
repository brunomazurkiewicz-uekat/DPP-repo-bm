from pathlib import Path
import csv
import time
import os
from contextlib import contextmanager

QUEUE_FILE = Path("jobs.csv")
LOCK_FILE = Path("jobs.lock")

CHECK_INTERVAL = 5
JOB_DURATION = 15


@contextmanager
def acquire_lock():
    fd = None
    while True:
        try:
            fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            break
        except FileExistsError:
            time.sleep(0.05)  # krótki sleep i próbujemy ponownie

    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            LOCK_FILE.unlink()
        except FileNotFoundError:
            pass


def read_jobs():
    if not QUEUE_FILE.exists():
        return None, None

    with QUEUE_FILE.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        return None, None

    header = rows[0]
    data_rows = rows[1:]
    return header, data_rows


def write_jobs(header, rows):
    with QUEUE_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def take_next_pending_job():
    with acquire_lock():
        header, rows = read_jobs()

        if header is None:
            return None, None

        for row in rows:
            job_id, status, description = row
            if status == "pending":
                row[1] = "in_progress"
                write_jobs(header, rows)
                return job_id, description

        # nie znaleziono pending
        return None, None


def mark_job_done(job_id: str):
    with acquire_lock():
        header, rows = read_jobs()

        if header is None:
            return

        for row in rows:
            if row[0] == job_id:
                row[1] = "done"
                break

        write_jobs(header, rows)


def main():
    consumer_name = f"PID-{os.getpid()}"
    print(f"[{consumer_name}] Consumer uruchomiony.")

    while True:
        job_id, description = take_next_pending_job()

        if job_id is None:
            print(f"[{consumer_name}] Brak zadań – czekam {CHECK_INTERVAL}s.")
            time.sleep(CHECK_INTERVAL)
            continue

        print(f"[{consumer_name}] Zaczynam zadanie {job_id}: {description}")
        time.sleep(JOB_DURATION)
        mark_job_done(job_id)
        print(f"[{consumer_name}] Zakończono zadanie {job_id}: {description}")


if __name__ == "__main__":
    main()
