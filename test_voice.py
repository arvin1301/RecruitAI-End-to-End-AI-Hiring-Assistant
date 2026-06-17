from agents.voice_agent import VoiceAgent


def main():

    agent = VoiceAgent()

    transcript = (
        agent.record_and_transcribe(
            duration=10
        )
    )

    print("\nTRANSCRIPT:\n")
    print(transcript)


if __name__ == "__main__":
    main()