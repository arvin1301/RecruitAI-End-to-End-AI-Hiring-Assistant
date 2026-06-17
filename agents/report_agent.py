import os
import json


class ReportAgent:

    def __init__(self):

        os.makedirs(
            "data/reports",
            exist_ok=True
        )

    def generate_report(
        self,
        candidate_name,
        resume_result,
        interview_report,
        proctoring_result=None
    ):

        resume_score = (
            resume_result.get(
                "candidate_score",
                0
            )
        )

        interview_score = (
            interview_report.get(
                "overall_score",
                0
            )
        )

        risk_score = 0

        if proctoring_result:

            risk_score = (
                proctoring_result.get(
                    "risk_score",
                    0
                )
            )

        final_score = round(
            (
                resume_score * 0.4
                +
                interview_score * 0.5
                +
                (100 - risk_score) * 0.1
            ),
            2
        )

        if final_score >= 80:

            recommendation = (
                "Strong Hire"
            )

        elif final_score >= 70:

            recommendation = (
                "Hire"
            )

        elif final_score >= 60:

            recommendation = (
                "Consider"
            )

        else:

            recommendation = (
                "Reject"
            )

        report = {

            "candidate_name":
                candidate_name,

            "resume_score":
                resume_score,

            "interview_score":
                interview_score,

            "risk_score":
                risk_score,

            "final_score":
                final_score,

            "resume_strengths":
                resume_result.get(
                    "strengths",
                    []
                ),

            "missing_skills":
                resume_result.get(
                    "missing_skills",
                    []
                ),

            "recommendation":
                recommendation
        }

        safe_candidate_name = (
            candidate_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        report_path = (
            f"data/reports/"
            f"{safe_candidate_name}_report.json"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"\nReport saved: "
            f"{report_path}"
        )

        return report