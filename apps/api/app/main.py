from fastapi import FastAPI
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.me import router as me_router

app = FastAPI(title="GARAG API", version="0.1.0")

app.include_router(auth_router)
app.include_router(me_router)

@app.get("/health")
def health():
    return {"ok": True}
