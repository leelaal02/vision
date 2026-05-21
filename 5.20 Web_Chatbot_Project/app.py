from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 로드
load_dotenv()

# OpenAI API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key)

app = Flask(__name__)

# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")


# 챗봇 API
@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        bot_reply = response.choices[0].message.content

        return jsonify({
            "reply": bot_reply
        })

    except Exception as e:
        return jsonify({
            "reply": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)