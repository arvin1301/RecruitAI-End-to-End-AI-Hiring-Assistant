from fastapi import APIRouter

from agents.interview_agent import (
    InterviewAgent
)

router = APIRouter()


@router.get("/questions")
def get_questions():

    interview_agent = (
        InterviewAgent()
    )

    result = (
        interview_agent.generate_questions(
            candidate_profile={
                "strengths": [
                    "Machine Learning",
                    "NLP"
                ]
            },
            role="AI Engineer"
        )
    )

    return result