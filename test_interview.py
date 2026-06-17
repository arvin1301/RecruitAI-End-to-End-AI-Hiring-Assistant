from agents.interview_agent import InterviewAgent


def main():

    candidate_profile = {

        "candidate_name": "PH ARVIND SHARMA",

        "strengths": [
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "Real-time AI Assistant"
        ]
    }

    agent = InterviewAgent()

    questions = agent.generate_questions(
        candidate_profile=candidate_profile,
        role="AI Engineer",
        num_questions=3
    )

    print("\nGenerated Interview Questions\n")

    evaluations = []

    for index, question in enumerate(
            questions["questions"],
            start=1
    ):

        print("\n" + "=" * 60)
        print(f"Question {index}")
        print("=" * 60)

        print(question)

        answer = input(
            "\nEnter Candidate Answer:\n"
        )

        evaluation = agent.evaluate_answer(
            question=question,
            answer=answer
        )

        evaluations.append(
            evaluation
        )

        print("\nEvaluation\n")
        print(evaluation)

    report = agent.generate_interview_report(
        evaluations
    )

    print("\n" + "=" * 60)
    print("FINAL INTERVIEW REPORT")
    print("=" * 60)

    print(report)


if __name__ == "__main__":
    main()