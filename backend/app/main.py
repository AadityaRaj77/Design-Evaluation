from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analyze import router as analyze_router
from app.core.database import init_db
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="AI Design Reviewer",
    version="1.0.0"
)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "AI Design Reviewer API"
    }

@app.on_event("startup")
def on_startup():

    init_db()