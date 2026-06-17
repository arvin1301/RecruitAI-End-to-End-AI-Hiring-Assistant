from agents.tts_agent import TTSAgent


def main():

    tts = TTSAgent()

    tts.speak(
        "Welcome to the AI interview."
    )

    tts.speak(
        "What is machine learning?"
    )


if __name__ == "__main__":
    main()