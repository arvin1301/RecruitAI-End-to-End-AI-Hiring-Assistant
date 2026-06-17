import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class InterviewAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = os.getenv(
            "MODEL_NAME",
            "llama-3.3-70b-versatile"
        )

    def generate_questions(
        self,
        candidate_profile: dict,
        role: str,
        num_questions: int = 5
    ):

        prompt = f"""
You are a senior technical interviewer.

Role:
{role}

Candidate Profile:
{candidate_profile}

Generate {num_questions} interview questions.

Requirements:
- Mix easy, medium and hard questions
- Focus on candidate strengths
- Focus on role requirements
- Return ONLY JSON

Format:

{{
    "questions": [
        "Question 1",
        "Question 2",
        "Question 3"
    ]
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        return json.loads(result)

    def evaluate_answer(
        self,
        question: str,
        answer: str
    ):

        prompt = f"""
You are a senior technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate:

1. Technical Knowledge (0-100)
2. Communication Skills (0-100)
3. Accuracy (0-100)

Return ONLY JSON.

Format:

{{
    "technical_score": 0,
    "communication_score": 0,
    "accuracy_score": 0,
    "overall_score": 0,
    "feedback": "",
    "recommendation": ""
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        return json.loads(result)

    def generate_interview_report(
        self,
        evaluations: list
    ):

        total_technical = 0
        total_communication = 0
        total_accuracy = 0

        for evaluation in evaluations:

            total_technical += evaluation["technical_score"]
            total_communication += evaluation["communication_score"]
            total_accuracy += evaluation["accuracy_score"]

        count = len(evaluations)

        report = {

            "average_technical_score":
                round(total_technical / count, 2),

            "average_communication_score":
                round(total_communication / count, 2),

            "average_accuracy_score":
                round(total_accuracy / count, 2),

            "overall_score":
                round(
                    (
                        total_technical +
                        total_communication +
                        total_accuracy
                    ) / (count * 3),
                    2
                ),

            "recommendation":
                "Proceed"
                if (
                    (
                        total_technical +
                        total_communication +
                        total_accuracy
                    ) / (count * 3)
                ) >= 70
                else "Reject"
        }

        return report