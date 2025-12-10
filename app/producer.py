# producer.py
from queue_storage import init_db, add_job


def main():
    init_db()  # upewnia się, że baza i tabela istnieją

    count = int(input("Ile zadań dodać do kolejki? "))

    for i in range(count):
        description = f"Rozmowa telefoniczna #{i + 1}"
        add_job(description)
        print(f"Dodano zadanie: {description}")


if __name__ == "__main__":
    main()
