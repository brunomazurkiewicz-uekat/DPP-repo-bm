# consumer.py
import os
import time
from queue_storage import init_db, take_next_pending_job, mark_job_done

CHECK_INTERVAL = 5
JOB_DURATION = 30


def main():
    init_db()
    consumer_name = f"PID-{os.getpid()}"
    print(f"[{consumer_name}] Consumer uruchomiony.")

    while True:
        # TODO: pobierz zadanie z bazy
        # job_id, description = ...

        # TODO: jeśli brak zadania -> sleep(CHECK_INTERVAL) i continue

        # TODO: jeśli jest zadanie:
        #   - wypisz log "Zaczynam zadanie ..."
        #   - time.sleep(JOB_DURATION)
        #   - mark_job_done(job_id)
        #   - wypisz log "Zakończono zadanie ..."

        # pamiętaj o użyciu consumer_name w logach, żeby odróżnić procesy
        pass


if __name__ == "__main__":
    main()
