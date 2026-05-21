const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const chatHistoryDiv = document.getElementById("chatHistory");
let chatHistory = [];

// 웹캠 활성화
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => console.error("웹캠을 사용할 수 없습니다.", err));


function captureImage() {
    const ctx = canvas.getContext("2d");

    // 캔버스 크기를 비디오 크기와 맞추기 
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // 캔버스에 현재 프레임 그리기
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // 이미지 데이터를 Base64 형식으로 변환
    const imageData = canvas.toDataURL("image/png");

    // Base64 데이터에서 "data:image/png;base64," 부분 제거
    const base64Image = imageData.split(",")[1];

    // 서버로 데이터 전송
    fetch("/upload_image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64Image })
    })
    .then(response => response.json())
    .then(data => {
        if (data.extracted_text) {
            document.getElementById("textInput").value = data.extracted_text;
        } else {
            alert("⚠️ 이미지에서 텍스트를 추출할 수 없습니다. 더 명확한 이미지를 사용해 주세요.");
        }
    })
    .catch(error => {
        console.error("이미지 업로드 오류:", error);
        alert("🚨 서버와의 연결 중 오류가 발생했습니다.");
    });
}

// 질문 전송
function sendQuestion() {
    const userInput = document.getElementById("textInput").value;
    if (!userInput) {
        alert("질문을 입력하세요!");
        return;
    }

    chatHistory.push({ role: "user", content: userInput });
    updateChatHistory();

    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userInput, history: chatHistory })
    })
    .then(response => response.json())
    .then(data => {
        chatHistory = data.history;
        updateChatHistory();
    });
}

// 채팅 내역 갱신
function updateChatHistory() {
    chatHistoryDiv.innerHTML = chatHistory.map(entry => 
        `<p><strong>${entry.role === "user" ? "👤 사용자" : "🤖 챗봇"}:</strong> ${entry.content}</p>`
    ).join("");
}

// 채팅 초기화
function clearChat() {
    fetch("/clear", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        chatHistory = data.history;
        updateChatHistory();
        textInput.value = ""; // 입력란 초기화
    });
}
