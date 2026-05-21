document.addEventListener("DOMContentLoaded", function () {
    const infoButton = document.getElementById("getInfoButton");
    const infoBox = document.getElementById("infoBox");

    infoButton.addEventListener("click", function () {
        fetch("/get_latest_info")
            .then(response => response.json())
            .then(data => {
                infoBox.innerText = `손가락 수: ${data.fingers}\nAI 응답: ${data.response}`;
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                infoBox.innerText = "오류가 발생했습니다.";
            });
    });
});
