from fastapi import FastAPI

from api.routes.resume import router as resume_router
from api.routes.interview import router as interview_router
from api.routes.report import router as report_router
from api.routes.hr import router as hr_router
from api.routes.search import router as search_router

app = FastAPI(
    title="AI Recruitment Agent",
    version="1.0.0"
)

app.include_router(
    resume_router,
    prefix="/resume",
    tags=["Resume"]
)

app.include_router(
    interview_router,
    prefix="/interview",
    tags=["Interview"]
)

app.include_router(
    report_router,
    prefix="/report",
    tags=["Report"]
)

app.include_router(
    hr_router,
    prefix="/hr",
    tags=["HR"]
)

app.include_router(
    search_router,
    prefix="/search",
    tags=["Search"]
)


@app.get("/")
def home():

    return {
        "message":
        "AI Recruitment Platform Running"
    }