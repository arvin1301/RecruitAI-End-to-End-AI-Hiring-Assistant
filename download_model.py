import os
import requests


def download_yolov10():

    os.makedirs("models", exist_ok=True)

    model_path = "models/yolov10n.pt"

    if os.path.exists(model_path):
        print("YOLOv10 model already exists.")
        return

    url = (
        "https://github.com/THU-MIG/yolov10/releases/download/"
        "v1.1/yolov10n.pt"
    )

    print("Downloading YOLOv10n...")

    response = requests.get(
        url,
        stream=True
    )

    response.raise_for_status()

    with open(model_path, "wb") as file:

        for chunk in response.iter_content(
            chunk_size=8192
        ):

            if chunk:
                file.write(chunk)

    print(
        f"Model saved to {model_path}"
    )


if __name__ == "__main__":
    download_yolov10()