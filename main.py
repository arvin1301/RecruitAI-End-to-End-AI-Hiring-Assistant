from agents.resume_parser import ResumeParser
from agents.recruiter_agent import RecruiterAgent
from agents.qdrant_agent import QdrantAgent


def main():

    resume_path = "resumes/Arvind_Sharma_ATS_Resume.pdf"

    job_description = """
AI Engineer

Required:
Python
FastAPI
LangChain
Vector Databases
LLMs
"""

    resume_text = ResumeParser.extract_text(
        resume_path
    )

    recruiter = RecruiterAgent()

    result = recruiter.evaluate_candidate(
        resume_text=resume_text,
        job_description=job_description
    )

    print(result)

    qdrant = QdrantAgent()

    qdrant.store_candidate(
        candidate_id=1,
        resume_text=resume_text,
        candidate_data=result
    )


if __name__ == "__main__":
    main()