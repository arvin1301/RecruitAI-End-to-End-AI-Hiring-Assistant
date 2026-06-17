import os
import cv2
import requests

from ultralytics import YOLO


class ProctoringAgent:

    def __init__(self):

        self.model_path = "models/yolov10n.pt"

        self.download_model()

        print(
            "Loading YOLOv10 model..."
        )

        self.model = YOLO(
            self.model_path
        )

        self.suspicion_score = 0

        self.monitoring = False

        self.phone_events = 0
        self.multiple_person_events = 0
        self.missing_person_events = 0

    def download_model(self):

        os.makedirs(
            "models",
            exist_ok=True
        )

        if os.path.exists(
            self.model_path
        ):

            return

        url = (
            "https://github.com/THU-MIG/yolov10/"
            "releases/download/v1.1/yolov10n.pt"
        )

        response = requests.get(
            url,
            stream=True
        )

        response.raise_for_status()

        with open(
            self.model_path,
            "wb"
        ) as file:

            for chunk in response.iter_content(
                chunk_size=8192
            ):

                if chunk:

                    file.write(
                        chunk
                    )

    def analyze_frame(
        self,
        frame
    ):

        frame = cv2.resize(
            frame,
            (640, 480)
        )

        results = self.model(
            frame,
            verbose=False,
            imgsz=320
        )

        person_count = 0
        phone_detected = False

        for result in results:

            for box in result.boxes:

                cls_id = int(
                    box.cls[0]
                )

                class_name = (
                    self.model.names[
                        cls_id
                    ]
                )

                if class_name == "person":

                    person_count += 1

                elif class_name == "cell phone":

                    phone_detected = True

        if person_count == 0:

            self.suspicion_score += 5
            self.missing_person_events += 1

        if person_count > 1:

            self.suspicion_score += 10
            self.multiple_person_events += 1

        if phone_detected:

            self.suspicion_score += 15
            self.phone_events += 1

        return {

            "persons_detected":
                person_count,

            "phone_detected":
                phone_detected,

            "candidate_missing":
                person_count == 0,

            "multiple_people":
                person_count > 1,

            "suspicion_score":
                self.suspicion_score
        }

    def start_monitoring(self):

        self.monitoring = True

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():

            print(
                "Camera not available."
            )

            return

        frame_count = 0

        analysis = {}

        while self.monitoring:

            success, frame = cap.read()

            if not success:

                continue

            frame_count += 1

            if frame_count % 10 == 0:

                analysis = (
                    self.analyze_frame(
                        frame
                    )
                )

                print(
                    analysis
                )

            cv2.imshow(
                "AI Proctoring",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):

                self.stop_monitoring()

        cap.release()

        cv2.destroyAllWindows()

    def stop_monitoring(self):

        self.monitoring = False

    def get_risk_score(self):

        return {

            "risk_score":
                self.suspicion_score,

            "phone_events":
                self.phone_events,

            "multiple_person_events":
                self.multiple_person_events,

            "missing_person_events":
                self.missing_person_events
        }