from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.me import router as me_router
from app.api.v1.routes.cars import router as cars_router

app = FastAPI(title="GARAG API", version="0.1.0")

app.include_router(auth_router, prefix="/v1")
app.include_router(me_router, prefix="/v1")
app.include_router(cars_router, prefix="/v1")

ui_dir = Path(__file__).resolve().parent / "ui"
if ui_dir.exists():
    app.mount(
        "/ui",
        StaticFiles(directory=ui_dir, html=True),
        name="ui",
    )

@app.get("/health")
def health():
    return {"ok": True}
