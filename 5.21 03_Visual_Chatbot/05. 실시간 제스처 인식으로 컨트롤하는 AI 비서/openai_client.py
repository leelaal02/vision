# openai_client.py
from dotenv import load_dotenv
import os

# .env 파일의 내용 불러오기
load_dotenv("C:/env/.env")

# 환경 변수 가져오기
API_KEY = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
client = OpenAI(api_key=API_KEY)

gesture_map = {
    1: "오늘 뉴스를 알려줘",
    2: "오늘 날씨 어때?",
    3: "유명한 명언 하나 알려줘",
    4: "간단한 운동 루틴 알려줘",
    5: "나에게 인사해줘"
}

# gesture_map = {
#     1: "Tell me today's news.",
#     2: "How's the weather today?",
#     3: "Give me a famous quote.",
#     4: "Suggest a simple workout routine.",
#     5: "Greet me."
# }

# gesture_map = {
#     1: "Tell me an interesting fact.",
#     2: "Describe a beautiful place in the world.",
#     3: "Give me a motivational quote.",
#     4: "Recommend a simple exercise I can do at home.",
#     5: "Say something nice to cheer me up."
# }

def get_ai_response(finger_count):
    prompt = gesture_map.get(finger_count, "인식되지 않는 제스처입니다.")
    if "인식되지 않는" in prompt:
        return prompt

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 친절한 AI 비서입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
