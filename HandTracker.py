import cv2
import mediapipe as mp
import numpy as np
import pyautogui

MP_Hands = mp.solutions.hands
Hands = MP_Hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
MP_Draw = mp.solutions.drawing_utils
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not access the camera.")
    exit()

SensitivityFactor = 4.0

InitialCursorSet = False
InitialCursorX, InitialCursorY = None, None
PinchThreshold = 0.8
MovementThreshold = 5

SmoothFactor = 0.5
LastCursorX, LastCursorY = None, None

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Frame", cv2.WND_PROP_TOPMOST, 1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    FrameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    Result = Hands.process(FrameRGB)

    if Result.multi_hand_landmarks:
        hand_landmarks = Result.multi_hand_landmarks[0]

        ThumbTip = hand_landmarks.landmark[4]
        PointerTip = hand_landmarks.landmark[8]

        ThumbPosition = np.array([ThumbTip.x, ThumbTip.y])
        PointerPosition = np.array([PointerTip.x, PointerTip.y])

        Distance = np.linalg.norm(ThumbPosition - PointerPosition)
        PinchValue = np.clip(1.0 - Distance * 5, 0, 1)

        h, w, _ = frame.shape
        LabelX = int((ThumbTip.x + PointerTip.x) / 2 * w)
        LabelY = int((ThumbTip.y + PointerTip.y) / 2 * h)

        cv2.putText(frame, f"{PinchValue:.2f}", (LabelX, LabelY),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        CubeSize = 10
        if PinchValue > PinchThreshold:
            cv2.drawContours(frame, [np.array([[LabelX - CubeSize, LabelY - CubeSize],
                                               [LabelX + CubeSize, LabelY - CubeSize],
                                               [LabelX + CubeSize, LabelY + CubeSize],
                                               [LabelX - CubeSize, LabelY + CubeSize]])], 0, (255, 0, 0), -1)
            pyautogui.click()

            if not InitialCursorSet:
                ScreenWidth, ScreenHeight = pyautogui.size()
                InitialCursorX = int(PointerTip.x * w * SensitivityFactor)
                InitialCursorY = int(PointerTip.y * h * SensitivityFactor)
                pyautogui.moveTo(ScreenWidth / 2, ScreenHeight / 2)
                InitialCursorSet = True

        if InitialCursorX is not None and InitialCursorY is not None:
            NewCursorX = int(PointerTip.x * w * SensitivityFactor)
            NewCursorY = int(PointerTip.y * h * SensitivityFactor)

            if abs(NewCursorX - InitialCursorX) > MovementThreshold or abs(NewCursorY - InitialCursorY) > MovementThreshold:
                if LastCursorX is not None and LastCursorY is not None:
                    NewCursorX = int(LastCursorX * (1 - SmoothFactor) + NewCursorX * SmoothFactor)
                    NewCursorY = int(LastCursorY * (1 - SmoothFactor) + NewCursorY * SmoothFactor)

                OffsetX = -(NewCursorX - InitialCursorX)
                OffsetY = NewCursorY - InitialCursorY
                pyautogui.moveRel(OffsetX, OffsetY)

                InitialCursorX = NewCursorX
                InitialCursorY = NewCursorY

                LastCursorX, LastCursorY = NewCursorX, NewCursorY

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()