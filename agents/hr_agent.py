import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class HRAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        self.model = os.getenv(
            "MODEL_NAME",
            "llama-3.3-70b-versatile"
        )

        os.makedirs(
            "data/hr_reports",
            exist_ok=True
        )

    def generate_hr_decision(
        self,
        report_data: dict
    ):

        prompt = f"""
You are a Senior HR Manager.

Analyze the candidate report and
provide a hiring recommendation.

Candidate Report:

{json.dumps(report_data, indent=2)}

Return ONLY JSON.

Format:

{{
    "candidate_name": "",
    "status": "",
    "next_round": "",
    "salary_band": "",
    "hr_summary": "",
    "joining_recommendation": ""
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

        result = (
            response
            .choices[0]
            .message
            .content
        )

        result = result.replace(
            "```json",
            ""
        )

        result = result.replace(
            "```",
            ""
        )

        result = result.strip()

        hr_decision = json.loads(
            result
        )

        candidate_name = report_data.get(
            "candidate_name",
            "candidate"
        )

        safe_candidate_name = (
            candidate_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        file_path = (
            f"data/hr_reports/"
            f"{safe_candidate_name}_hr_decision.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                hr_decision,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"\nHR Decision saved: "
            f"{file_path}"
        )

        return hr_decision