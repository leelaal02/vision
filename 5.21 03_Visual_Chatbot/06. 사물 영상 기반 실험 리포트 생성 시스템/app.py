from flask import Flask, render_template, Response, request
import cv2
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv
import base64

# encode the image
def encode_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
        
# .env 파일의 내용 불러오기
load_dotenv("C:/env/.env")

# 환경 변수 가져오기
API_KEY = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=API_KEY)

# 카메라 초기화
cap = cv2.VideoCapture(0)

app = Flask(__name__)


# 전역 상태
latest_image_path = None
latest_report = ""

# 실시간 영상 스트리밍 생성기
def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# AI 리포트 생성 함수
def generate_experiment_report(base64_image):
    prompt = (
        '''
        당신은 실험 관찰 리포트를 작성하는 AI입니다.
        아래는 사용자가 보여준 장면 사진입니다
        이 장면에서 어떤 실험을 진행한 것처럼 보이며, 그 결과는 어떤지 과학적으로 상상해서 설명해 주세요
        '''
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            # {"role": "system", "content": "당신은 과학적 실험 보고서를 작성하는 AI입니다."},
            {
                "role": "user", 
                "content" : [
                    { "type": "text","text": prompt },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content

# 웹 루트 라우트
@app.route('/')
def index():
    return render_template('index.html', image_url=latest_image_path, report=latest_report)

# 실시간 영상 스트림 라우트
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 현재 프레임을 캡처하고 분석하는 라우트
@app.route('/capture', methods=['POST'])
def capture():
    global latest_image_path, latest_report

    success, frame = cap.read()
    if not success:
        return "카메라 캡처 실패", 500

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join("static", "captured")
    os.makedirs(save_path, exist_ok=True)
    filename = f"{timestamp}.jpg"
    image_path = os.path.join(save_path, filename)
    cv2.imwrite(image_path, frame)

    latest_image_path = '/' + image_path  # 웹에서 접근 가능한 경로로 저장
    base64_image = encode_image(image_path)
    latest_report = generate_experiment_report(base64_image)

    return render_template('index.html', image_url=latest_image_path, report=latest_report)

if __name__ == '__main__':
    app.run(debug=False)