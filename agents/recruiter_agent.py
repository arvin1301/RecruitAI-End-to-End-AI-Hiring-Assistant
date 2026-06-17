import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class RecruiterAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("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")
        )

        self.model = os.getenv(
            "MODEL_NAME",
            "llama-3.3-70b-versatile"
        )

    def evaluate_candidate(
        self,
        resume_text: str,
        job_description: str
    ):

        prompt = f"""
You are an expert AI recruiter.

Analyze the candidate resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

IMPORTANT:
Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not provide explanations.

JSON Format:

{{
    "candidate_name": "",
    "candidate_score": 0,
    "skills_match": 0,
    "experience_match": 0,
    "education_match": 0,
    "strengths": [],
    "missing_skills": [],
    "recommendation": ""
}}
"""

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.2,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior technical recruiter."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.choices[0].message.content.strip()

            # Remove markdown code blocks if model adds them
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            return json.loads(result)

        except json.JSONDecodeError:

            return {
                "error": "Failed to parse JSON response",
                "raw_response": result
            }

        except Exception as e:

            return {
                "error": str(e)
            }