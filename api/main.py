from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Bank Retention API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/clients/{client_id}/recommend")
def recommend(client_id: str):
    raise HTTPException(status_code=501, detail="not implemented")
