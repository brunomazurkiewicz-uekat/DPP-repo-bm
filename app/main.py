from fastapi import FastAPI

app = FastAPI(title="Projekt Zaliczeniowy - Zadanie X")

@app.get("/")
def root():
    return {"status": "OK", "message": "Backend działa – można zaczynać kolejne zadanie."}
