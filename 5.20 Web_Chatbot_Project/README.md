# Web_Chatbot_Project

## 기능 소개 및 사용 설명서

---

# 1. 프로젝트 개요

Web_Chatbot_Project는 Flask 기반으로 제작된 AI 웹 챗봇 프로젝트입니다.

OpenAI API를 활용하여 사용자의 질문에 대해 자연스러운 대화를 제공하며, 웹 브라우저에서 실시간 채팅 형태로 사용할 수 있습니다.

본 프로젝트는:

* Flask 웹 서버
* OpenAI GPT 모델 연동
* 비동기(Fetch API) 통신
* 채팅 UI
* 환경변수 기반 API 키 관리

를 포함하고 있습니다.

---

# 2. 주요 기능

## 2.1 AI 챗봇 기능

사용자가 입력한 질문을 OpenAI GPT 모델에 전달하여 응답을 생성합니다.

사용 모델:

```python
model="gpt-4o-mini"
```

지원 가능 기능 예시:

* 일반 대화
* 코딩 질문
* 문서 요약
* 번역
* 학습 보조
* 아이디어 생성
* 고객 응대
* FAQ 챗봇
* AI 비서 기능

---

## 2.2 실시간 비동기 채팅

Fetch API 기반 비동기 통신을 사용하여:

* 새로고침 없이 채팅 가능
* 빠른 응답 처리
* 자연스러운 UX 제공

을 지원합니다.

---

## 2.3 말풍선 UI 제공

사용자와 챗봇 메시지를 구분하여 표시합니다.

### 사용자 메시지

* 오른쪽 정렬
* 파란색 말풍선
* “You:” 표시

### 챗봇 메시지

* 왼쪽 정렬
* 회색 말풍선
* “Bot:” 표시

---

## 2.4 OpenAI API 연동

최신 OpenAI Python SDK 스타일을 사용합니다.

예시:

```python
from openai import OpenAI

client = OpenAI(api_key=api_key)
```

---

## 2.5 환경변수(.env) 기반 API 키 관리

API 키를 코드에 직접 작성하지 않고 `.env` 파일에서 관리합니다.

장점:

* 보안 향상
* GitHub 업로드 시 안전성 증가
* 유지보수 편리

예시:

```env
OPENAI_API_KEY=YOUR_API_KEY
```

---

# 3. 프로젝트 구조

```text
Web_Chatbot_Project/
│
├── app.py
├── requirements.txt
├── .env
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

---

# 4. 파일 설명

## 4.1 app.py

Flask 서버 메인 파일입니다.

주요 역할:

* 웹 서버 실행
* OpenAI API 호출
* 사용자 메시지 처리
* 챗봇 응답 반환

---

## 4.2 templates/index.html

챗봇 화면(UI)을 구성합니다.

포함 기능:

* 채팅창
* 입력창
* 전송 버튼
* Fetch API 비동기 통신

---

## 4.3 static/style.css

채팅 UI 디자인 파일입니다.

포함 내용:

* 말풍선 디자인
* 채팅창 스타일
* 버튼 스타일
* 반응형 레이아웃

---

## 4.4 requirements.txt

프로젝트 실행에 필요한 Python 패키지 목록입니다.

예시:

```text
flask
openai
python-dotenv
```

---

# 5. 설치 방법

## 5.1 Python 설치

Python 3.10 이상 권장.

공식 사이트:

[https://www.python.org/](https://www.python.org/)

---

## 5.2 프로젝트 폴더 이동

```bash
cd Web_Chatbot_Project
```

---

## 5.3 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

---

## 5.4 .env 파일 생성

프로젝트 루트 폴더에 `.env` 파일 생성 후 API 키 입력:

```env
OPENAI_API_KEY=YOUR_API_KEY
```

---

# 6. 실행 방법

## Flask 서버 실행

```bash
python app.py
```

---

## 브라우저 접속

```text
http://127.0.0.1:5000
```

접속 시 웹 챗봇 화면이 표시됩니다.

---

# 7. 사용 방법

## 7.1 질문 입력

입력창에 질문을 입력합니다.

예시:

```text
안녕하세요
파이썬 코드를 알려줘
오늘 날씨 어때?
```

---

## 7.2 전송 버튼 클릭

전송 버튼을 누르면:

1. Flask 서버로 메시지 전달
2. OpenAI API 요청
3. GPT 응답 생성
4. 채팅창 출력

순서로 동작합니다.

---

## 7.3 응답 확인

사용자 메시지:

```text
You: 안녕하세요
```

챗봇 응답:

```text
Bot: 안녕하세요! 무엇을 도와드릴까요?
```

형태로 출력됩니다.

---

# 8. 동작 흐름

```text
사용자 입력
    ↓
Fetch API 요청
    ↓
Flask 서버
    ↓
OpenAI API 호출
    ↓
GPT 응답 생성
    ↓
JSON 응답 반환
    ↓
브라우저 채팅창 출력
```

---

# 9. 확장 가능 기능

본 프로젝트는 다양한 기능으로 확장 가능합니다.

---

## 9.1 로그인 기능

추가 가능 기술:

* Flask-Login
* JWT 인증
* OAuth 로그인

---

## 9.2 대화 저장 기능

추천 DB:

* SQLite
* MySQL
* PostgreSQL
* MongoDB

---

## 9.3 음성 입력 기능

추가 가능 기능:

* Speech-to-Text
* 음성 챗봇
* 음성 비서

---

## 9.4 이미지 업로드 기능

활용 가능 예시:

* 이미지 분석
* OCR
* 객체 탐지
* AI Vision

---

## 9.5 스트리밍 응답

ChatGPT 스타일의:

* 한 글자씩 출력
* 실시간 생성 효과

구현 가능.

---

## 9.6 모바일 앱 연동

연동 가능 플랫폼:

* Flutter
* React Native
* Android
* iOS

---

# 10. 배포 방법

추천 배포 플랫폼:

* Render
* Railway
* Vercel
* AWS
* Azure
* Google Cloud

배포 후:

```text
https://your-chatbot.com
```

형태로 서비스 가능.

---

# 11. 보안 주의사항

## API 키 공개 금지

`.env` 파일은 GitHub에 업로드하지 않는 것을 권장합니다.

`.gitignore` 추가 예시:

```text
.env
```

---

## HTTPS 사용 권장

실서비스 환경에서는 HTTPS 사용 권장.

---

# 12. 추천 업그레이드 방향

## 초급 단계

* 기본 챗봇 구현
* UI 개선
* 채팅 저장

---

## 중급 단계

* 사용자 인증
* DB 연동
* 스트리밍 응답
* 파일 업로드

---

## 고급 단계

* RAG 시스템
* 벡터 DB
* LangChain
* 멀티모달 AI
* 음성 AI
* AI 에이전트

---

# 13. 프로젝트 활용 예시

본 프로젝트는 다양한 서비스에 활용 가능합니다.

예시:

* 고객 상담 챗봇
* 학교 학습 보조 챗봇
* 코딩 도우미
* AI 비서
* 병원 안내 챗봇
* 쇼핑몰 FAQ
* 사내 업무 챗봇
* OCR/YOLO 연동 AI 시스템

---

# 14. 결론

Web_Chatbot_Project는:

* Flask 기반
* OpenAI GPT 연동
* 실시간 채팅 UI
* 비동기 통신
* 확장 가능한 구조

를 갖춘 AI 챗봇 프로젝트입니다.

현재 구조만으로도:

* 웹 서비스
* 모바일 앱 백엔드
* AI API 서버

역할 수행이 가능하며, 향후 다양한 AI 기능과 연동하여 확장할 수 있습니다.
