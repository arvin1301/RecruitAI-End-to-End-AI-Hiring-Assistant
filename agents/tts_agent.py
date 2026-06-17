import pyttsx3


class TTSAgent:

    def speak(
        self,
        text
    ):

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            160
        )

        engine.setProperty(
            "volume",
            1.0
        )

        print(
            f"\nAI Interviewer: {text}"
        )

        engine.say(
            str(text)
        )

        engine.runAndWait()

        engine.stop()