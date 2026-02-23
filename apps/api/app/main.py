from fastapi import FastAPI
from app.api.v1.routes import auth, cars, admin, media

app = FastAPI(title="GARAG API", version="0.1.0")

app.include_router(auth.router, prefix="/v1")
app.include_router(cars.router, prefix="/v1")
app.include_router(admin.router, prefix="/v1")
app.include_router(media.router, prefix="/v1")

@app.get("/health")
def health():
    return {"ok": True}