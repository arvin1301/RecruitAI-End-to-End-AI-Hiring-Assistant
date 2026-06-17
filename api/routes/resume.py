from fastapi import APIRouter
from agents.resume_parser import ResumeParser
from agents.recruiter_agent import RecruiterAgent

router = APIRouter()


@router.post("/evaluate")
def evaluate_resume():

    resume_path = (
        "resumes/candidate1.pdf"
    )

    job_description = """
    AI Engineer

    Skills:
    Python
    FastAPI
    LangChain
    LLMs
    """

    resume_text = (
        ResumeParser.extract_text(
            resume_path
        )
    )

    recruiter = RecruiterAgent()

    result = (
        recruiter.evaluate_candidate(
            resume_text,
            job_description
        )
    )

    return result