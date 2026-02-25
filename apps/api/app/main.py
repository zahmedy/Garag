from fastapi import FastAPI

app = FastAPI(title="GARAG API")

@app.get("/health")
def health():
    return {"ok": True}