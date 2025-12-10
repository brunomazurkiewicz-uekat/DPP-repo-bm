from pathlib import Path
import csv
import uuid

QUEUE_FILE = Path("jobs.csv")


def ensure_file_exists():
    if not QUEUE_FILE.exists():
        with QUEUE_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "status", "description"])


def main():
    ensure_file_exists()

    count = 100

    with QUEUE_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i in range(count):
            job_id = str(uuid.uuid4())
            description = f"Rozmowa telefoniczna #{i + 1}"
            writer.writerow([job_id, "pending", description])
            print(f"Dodano zadanie {job_id}: {description}")


if __name__ == "__main__":
    main()
