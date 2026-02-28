\"\"\"FastAPI application entrypoint for Desert Rule.\"\"\"
from fastapi import FastAPI
from .api import router
from .config import settings

app = FastAPI(title=settings.app_name)
app.include_router(router)
