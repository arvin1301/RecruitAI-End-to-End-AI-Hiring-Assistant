from agents.voice_agent import VoiceAgent
from agents.interview_agent import InterviewAgent
from agents.tts_agent import TTSAgent

import time
import json
import os


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

    role = "AI Engineer"

    voice_agent = VoiceAgent()
    interview_agent = InterviewAgent()
    tts_agent = TTSAgent()

    os.makedirs(
        "data/interview_logs",
        exist_ok=True
    )

    print("\n" + "=" * 60)
    print("AI VOICE INTERVIEW STARTED")
    print("=" * 60)

    tts_agent.speak(
        "Welcome to the AI interview."
    )

    time.sleep(3)

    print(
        "\nGenerating Interview Questions..."
    )

    questions_response = (
        interview_agent.generate_questions(
            candidate_profile=candidate_profile,
            role=role,
            num_questions=3
        )
    )

    questions = questions_response.get(
        "questions",
        []
    )

    if not questions:

        print(
            "No questions generated."
        )

        return

    evaluations = []
    interview_logs = []

    for index, question in enumerate(
        questions,
        start=1
    ):

        print("\n" + "=" * 60)
        print(f"QUESTION {index}")
        print("=" * 60)

        print(question)

        tts_agent.speak(
            f"Question {index}"
        )

        time.sleep(2)

        tts_agent.speak(
            question
        )

        time.sleep(2)

        tts_agent.speak(
            "Please answer now."
        )

        time.sleep(3)

        transcript = (
            voice_agent.record_and_transcribe()
        )

        print("\n" + "-" * 60)
        print("TRANSCRIPT")
        print("-" * 60)

        print(transcript)

        if not transcript.strip():

            print(
                "Empty answer detected."
            )

            continue

        evaluation = (
            interview_agent.evaluate_answer(
                question=question,
                answer=transcript
            )
        )

        evaluations.append(
            evaluation
        )

        interview_logs.append(
            {
                "question": question,
                "answer": transcript,
                "evaluation": evaluation
            }
        )

        print(
            "\nAnswer evaluated successfully."
        )

        if index < len(questions):

            tts_agent.speak(
                "Moving to the next question."
            )

            time.sleep(3)

    log_file = (
        "data/interview_logs/"
        "interview_log.json"
    )

    with open(
        log_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            interview_logs,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nInterview log saved: {log_file}"
    )

    if not evaluations:

        print(
            "No interview evaluations found."
        )

        return

    report = (
        interview_agent.generate_interview_report(
            evaluations
        )
    )

    print("\n" + "=" * 60)
    print("FINAL INTERVIEW REPORT")
    print("=" * 60)

    print(report)

    tts_agent.speak(
        "Interview completed. Thank you for your time."
    )


if __name__ == "__main__":
    main()