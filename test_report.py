from agents.report_agent import ReportAgent


def main():

    resume_result = {

        "candidate_score": 70,

        "strengths": [
            "Machine Learning",
            "Deep Learning",
            "NLP"
        ],

        "missing_skills": [
            "FastAPI",
            "Vector Databases"
        ]
    }

    interview_report = {

        "overall_score": 75
    }

    proctoring_result = {

        "risk_score": 10
    }

    report_agent = ReportAgent()

    report = (
        report_agent.generate_report(
            candidate_name=
            "PH ARVIND SHARMA",

            resume_result=
            resume_result,

            interview_report=
            interview_report,

            proctoring_result=
            proctoring_result
        )
    )

    print("\nFINAL REPORT:\n")
    print(report)


if __name__ == "__main__":
    main()