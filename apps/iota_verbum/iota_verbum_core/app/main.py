from fastapi import FastAPI
from .db import engine, Base
from . import models  # noqa: F401
from .routers import ivb
from web.iv_maps_api import router as iv_maps_router  # ← this line is crucial

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Iota Verbum Pilot")

app.include_router(ivb.router)
app.include_router(iv_maps_router)  # ← now this name exists


@app.get("/")
def root():
    return {"message": "Iota Verbum pilot running"}
