import tkinter as tk
from tkinter import Frame, Canvas, Scrollbar

from openai import OpenAI
from dotenv import load_dotenv
import os

# =========================
# OpenAI 설정
# =========================

load_dotenv("/Users/leelaal/.env")

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

MODEL = "gpt-4o-mini"

# 대화 히스토리
messages = [
    {
        "role": "system",
        "content": "You are a assistant."
    }
]


# =========================
# GPT 함수
# =========================

def chat_with_gpt(user_input):

    messages.append({
        "role": "user",
        "content": user_input
    })

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    bot_response = completion.choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": bot_response
    })

    return bot_response


# =========================
# 말풍선 추가 함수
# =========================

def add_message(message, sender):

    bubble_frame = Frame(
        messages_frame,
        bg="#FFE4EC"
    )

    # 사용자 말풍선
    if sender == "user":

        bubble = tk.Label(
            bubble_frame,
            text=message,
            bg="#FFB6C1",
            fg="#5A2A3A",
            font=("맑은 고딕", 15),
            wraplength=550,
            justify="left",
            padx=15,
            pady=10
        )

        bubble.pack(
            anchor="e",
            padx=15,
            pady=5
        )

        bubble_frame.pack(
            fill="x",
            anchor="e"
        )

    # 봇 말풍선
    else:

        bubble = tk.Label(
            bubble_frame,
            text=message,
            bg="#FFFFFF",
            fg="#C2185B",
            font=("맑은 고딕", 15),
            wraplength=550,
            justify="left",
            padx=15,
            pady=10
        )

        bubble.pack(
            anchor="w",
            padx=15,
            pady=5
        )

        bubble_frame.pack(
            fill="x",
            anchor="w"
        )

    root.update_idletasks()

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )

    canvas.yview_moveto(1.0)


# =========================
# 메시지 전송
# =========================

def send_message(event=None):

    user_input = entry_box.get().strip()

    if not user_input:
        return

    # 사용자 메시지 표시
    add_message(user_input, "user")

    # 입력창 초기화
    entry_box.delete(0, tk.END)

    try:

        response = chat_with_gpt(user_input)

        # Bot 응답 표시
        add_message(response, "bot")

    except Exception as e:

        add_message(f"오류 발생: {e}", "bot")


# =========================
# GUI 생성
# =========================

root = tk.Tk()

root.title("🎀 AI Chat 🎀")
root.geometry("900x700")
root.configure(bg="#FFE4EC")


# =========================
# 상단 바
# =========================

top_bar = tk.Frame(
    root,
    bg="#FFB6C1",
    height=70
)

top_bar.pack(fill="x")

title_label = tk.Label(
    top_bar,
    text="🎀 AI Chat 🎀",
    bg="#FFB6C1",
    fg="white",
    font=("맑은 고딕", 18, "bold")
)

title_label.pack(pady=18)


# =========================
# 채팅 영역
# =========================

chat_container = Frame(
    root,
    bg="#FFE4EC"
)

chat_container.pack(
    fill="both",
    expand=True
)

canvas = Canvas(
    chat_container,
    bg="#FFE4EC",
    highlightthickness=0
)

scrollbar = Scrollbar(
    chat_container,
    orient="vertical",
    command=canvas.yview
)

messages_frame = Frame(
    canvas,
    bg="#FFE4EC"
)

messages_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas_window = canvas.create_window(
    (0, 0),
    window=messages_frame,
    anchor="nw"
)


# Canvas 폭 자동 조절
def resize_frame(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )

canvas.bind("<Configure>", resize_frame)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# =========================
# 입력 영역
# =========================

bottom_frame = tk.Frame(
    root,
    bg="#FFD1DC",
    height=90
)

bottom_frame.pack(fill="x")


# 입력창
entry_box = tk.Entry(
    bottom_frame,
    font=("맑은 고딕", 12),
    bg="white",
    fg="#C2185B",
    insertbackground="#C2185B",
    relief="flat",
    bd=0
)

entry_box.pack(
    side="left",
    fill="x",
    expand=True,
    padx=15,
    pady=18,
    ipady=12
)

# 엔터 입력 시 전송
entry_box.bind("<Return>", send_message)


# 전송 버튼
send_button = tk.Button(
    bottom_frame,
    text="💌",
    command=send_message,
    font=("Arial", 16),
    bg="#FF69B4",
    fg="white",
    activebackground="#FF85C1",
    relief="flat",
    width=4,
    cursor="hand2"
)

send_button.pack(
    side="right",
    padx=15,
    pady=15
)


# =========================
# 시작 메시지
# =========================

add_message(
    "안녕하세요! 무엇을 도와드릴까요?",
    "bot"
)


# =========================
# 실행
# =========================

root.mainloop()