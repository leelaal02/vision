import cv2
import mediapipe as mp

class GestureDetector:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(static_image_mode=False,
                                               max_num_hands=1,
                                               min_detection_confidence=0.7)
        self.drawing = mp.solutions.drawing_utils

    def count_fingers(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)

        if not results.multi_hand_landmarks:
            return 0

        hand_landmarks = results.multi_hand_landmarks[0]
        
        # 엄지를 제외한 4개 손가락의 tip 번호
        finger_tips = [8, 12, 16, 20]  # index, middle, ring, pinky
        finger_count = 0

        for tip in finger_tips:
            # 손가락이 펴졌는지 판단 (tip이 아래 joint보다 위에 있으면 편 상태)
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                finger_count += 1

        return finger_count
