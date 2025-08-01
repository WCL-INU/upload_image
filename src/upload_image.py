#!/usr/bin/python

import io, time
from datetime import datetime
import requests
from picamera2 import Picamera2
import os

TYPE_ID = os.getenv("CAMERA_TYPE_ID")
DEVICE_ID = os.getenv("CAMERA_DEVICE_ID")
URL = os.getenv("SERVER_URL")

print("TYPE_ID:", TYPE_ID)
print("DEVICE_ID:", DEVICE_ID)

# 카메라 초기화
picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.configure(capture_config)
picam2.start()
time.sleep(1)  # 카메라 안정화 대기

while True:
    # 이미지 캡처
    buffer = io.BytesIO()
    picam2.capture_file(buffer, format="jpeg")
    buffer.seek(0)

    # 현재 시간 포맷팅
    now = datetime.now()
    if now.hour < 4 or now.hour >= 22:
        time.sleep(300)
        continue  # 새벽 4시 이전 또는 밤 10시 이후에는 캡처하지 않음

    file_name = f"image_{now.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    formatted_datetime = now.isoformat()  # ex. "2025-06-18T22:30:05.123456"

    # multipart/form-data 구성
    files = {
        "file1": (file_name, buffer, "image/jpeg"),
        "file1_id": (None, str(DEVICE_ID)),
        "file1_time": (None, formatted_datetime),
    }
    data = {"type": TYPE_ID}

    # POST 요청
    response = requests.post(URL, files=files, data=data)

    # 결과 확인
    print("Formatted datetime:", formatted_datetime)
    print(response.status_code)
    print(response.text, flush=True)

    time.sleep(300)  # 10초 대기 후 다음 캡처

# 카메라 종료
picam2.stop()
