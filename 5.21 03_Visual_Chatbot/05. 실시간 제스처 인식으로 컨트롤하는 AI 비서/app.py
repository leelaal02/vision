from flask import Flask, render_template, Response
import cv2
from gesture_detector import GestureDetector
from openai_client import get_ai_response
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import os

app = Flask(__name__)
cap = cv2.VideoCapture(1)
detector = GestureDetector()

latest_fingers = 0
latest_response = ""

# 한글 텍스트를 프레임에 표시하는 함수
def draw_korean_text(frame, text, position=(10, 30), font_size=24, font_path=None):
    if font_path is None:
        font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 기준
        # Linux일 경우 예: '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

    image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=(255, 255, 255, 255))
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

def gen_frames():
    global latest_fingers, latest_response
    while True:
        success, frame = cap.read()
        if not success:
            break

        fingers = detector.count_fingers(frame)
        if fingers != latest_fingers and fingers > 0:
            latest_fingers = fingers
            latest_response = get_ai_response(fingers)

        # 한글 텍스트 표시
        frame = draw_korean_text(frame, f'손가락 수: {latest_fingers}', (10, 30), font_size=28)
        frame = draw_korean_text(frame, latest_response, (10, 70), font_size=24)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False)