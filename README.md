# FastAPI + SQLAlchemy + RabbitMQ (Image Analysis Queue)

Projekt składa się z dwóch głównych części:

1. **API w FastAPI**, które obsługuje:
   - CRUD dla `movies`, `links`, `ratings`, `tags`
   - endpoint `/analyze_img`, który przyjmuje URL obrazka i przekazuje zadanie na kolejkę

2. **Kolejkowanie (RabbitMQ)**:
   - **producer** – działa w API i wrzuca zadania na kolejkę
   - **consumer** – osobny proces, pobiera zadania z kolejki i wykonuje analizę zdjęcia (wykrywanie osób)

---

## 📌 Wymagania

- Python 3.10+
- Virtualenv (`python -m venv`)
- FastAPI + SQLAlchemy (instalowane z `requirements.txt`)
- RabbitMQ (Docker lub lokalnie)

---

## 🔧 Instalacja

### 1. Klonowanie repo

```bash
git clone <repo-url>
cd repo
