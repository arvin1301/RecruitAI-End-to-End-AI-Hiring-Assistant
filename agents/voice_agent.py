import os
import time
import numpy as np
import sounddevice as sd

from scipy.io.wavfile import write
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class VoiceAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        os.makedirs(
            "audio",
            exist_ok=True
        )

        os.makedirs(
            "transcripts",
            exist_ok=True
        )

    def record_until_silence(
        self,
        silence_duration=10,
        sample_rate=16000,
        threshold=0.003,
        minimum_answer_time=20
    ):

        print("\nRecording started...")
        print(
            f"Recording will stop after "
            f"{silence_duration} seconds "
            f"of silence."
        )

        audio_chunks = []
        silence_start = None

        block_duration = 0.5
        start_time = time.time()

        while True:

            chunk = sd.rec(
                int(
                    block_duration *
                    sample_rate
                ),
                samplerate=sample_rate,
                channels=1,
                dtype="float32"
            )

            sd.wait()

            audio_chunks.append(
                chunk
            )

            volume = np.abs(
                chunk
            ).mean()

            if volume < threshold:

                if silence_start is None:

                    silence_start = time.time()

                elif (
                    (time.time() - silence_start)
                    >= silence_duration
                    and
                    (time.time() - start_time)
                    >= minimum_answer_time
                ):

                    print(
                        "\nSilence detected. Moving to next question..."
                    )

                    break

            else:

                silence_start = None

        audio = np.concatenate(
            audio_chunks,
            axis=0
        )

        audio_int16 = (
            audio * 32767
        ).astype(
            np.int16
        )

        timestamp = int(
            time.time()
        )

        audio_path = (
            f"audio/answer_{timestamp}.wav"
        )

        write(
            audio_path,
            sample_rate,
            audio_int16
        )

        print(
            f"Audio saved: {audio_path}"
        )

        return audio_path

    def transcribe_audio(
        self,
        audio_path
    ):

        with open(
            audio_path,
            "rb"
        ) as audio_file:

            transcription = (
                self.client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3-turbo"
                )
            )

        transcript = (
            transcription.text
        )

        timestamp = int(
            time.time()
        )

        transcript_path = (
            f"transcripts/answer_{timestamp}.txt"
        )

        with open(
            transcript_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                transcript
            )

        print(
            f"Transcript saved: "
            f"{transcript_path}"
        )

        return transcript

    def record_and_transcribe(
        self
    ):

        audio_path = (
            self.record_until_silence()
        )

        transcript = (
            self.transcribe_audio(
                audio_path
            )
        )

        return transcript