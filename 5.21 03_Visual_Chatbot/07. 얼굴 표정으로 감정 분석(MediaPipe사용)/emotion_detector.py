import mediapipe as mp
import cv2
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 전역 감정 저장
current_emotion = "neutral"

def detect_emotion(frame):
    global current_emotion

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    img_h, img_w, _ = frame.shape

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            def get_point(idx):
                lm = landmarks[idx]
                x, y = int(lm.x * img_w), int(lm.y * img_h)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # 녹색 점 찍기
                return np.array([x, y])

            # 주요 포인트 추출
            mouth_left = get_point(61)
            mouth_right = get_point(291)
            mouth_top = get_point(13)
            mouth_bottom = get_point(14)

            left_eye_top = get_point(159)
            left_eye_bottom = get_point(145)
            right_eye_top = get_point(386)
            right_eye_bottom = get_point(374)

            left_eyebrow = get_point(65)
            right_eyebrow = get_point(295)

            forehead = get_point(10)
            chin = get_point(152)

            # 얼굴 전체 높이 계산
            face_height = np.linalg.norm(forehead - chin)

            # 분석 값 계산
            mouth_open = np.linalg.norm(mouth_top - mouth_bottom) / face_height
            mouth_curve = ((mouth_left[1] + mouth_right[1]) / 2 - mouth_top[1]) / face_height
            left_eye_open = np.linalg.norm(left_eye_top - left_eye_bottom) / face_height
            right_eye_open = np.linalg.norm(right_eye_top - right_eye_bottom) / face_height
            avg_eye_open = (left_eye_open + right_eye_open) / 2
            eyebrow_distance = np.linalg.norm(left_eyebrow - right_eyebrow) / face_height

            # 디버깅용 출력
            # print(f"mouth_open={mouth_open:.4f}, mouth_curve={mouth_curve:.4f}, avg_eye_open={avg_eye_open:.4f}, eyebrow_distance={eyebrow_distance:.4f}")

            MOUTH_OPEN_THRESH = 0.015        # 입 아주 약간만 열려도 happy로
            MOUTH_CURVE_THRESH = -0.005      # 입꼬리 살짝만 올라가도 happy로
            EYE_OPEN_THRESH = 0.05           # 놀람은 유지
            EYEBROW_DISTANCE_THRESH = 0.25   # 눈썹 거리 약간 넓게
            

            # 감정 판정 (우선순위 happy -> angry -> surprised)
            if mouth_curve < MOUTH_CURVE_THRESH and mouth_open > MOUTH_OPEN_THRESH:
                emotion = "happy"
            elif eyebrow_distance < EYEBROW_DISTANCE_THRESH and avg_eye_open < 0.035:
                emotion = "angry"
            elif avg_eye_open > EYE_OPEN_THRESH:
                emotion = "surprised"
            else:
                emotion = "neutral"

            current_emotion = emotion

            # 감정 텍스트 영상에 표시
            cv2.putText(frame, f"Emotion: {emotion}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            return emotion

    # 얼굴이 안 잡히면 기본 neutral
    current_emotion = "neutral"
    return "neutral"

def get_current_emotion():
    return current_emotion
