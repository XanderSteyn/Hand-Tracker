---

# 🖐️ HandTracker

A Python-based hand tracking and cursor control application using OpenCV, MediaPipe, and PyAutoGUI.

## 🚀 Features
- Tracks hand movements through webcam using MediaPipe.
- Controls the mouse cursor with your hand's position.
- Clicks when a pinch gesture is detected.
- Smooth cursor movement with adjustable sensitivity.
- Lightweight and easy to use.

## ⚙️ Installation

### Prerequisites

To run this project, you need Python 3.x installed on your system. You'll also need to install the following dependencies :

```bash
pip install opencv-python mediapipe numpy pyautogui
```

### 🛠️ Setup

1. Clone the repository to your local machine :

   ```bash
   git clone https://github.com/XanderSteyn/Hand-Tracker.git
   cd Hand-Tracker
   ```

3. Run the script :

   ```bash
   python HandTracker.py
   ```

### 📦 Dependencies

- `opencv-python` : For accessing the webcam and processing video frames.
- `mediapipe` : For detecting and tracking hand landmarks.
- `numpy` : For numerical operations on hand position data.
- `pyautogui` : For controlling the mouse cursor and clicking.

## 📸 How It Works

1. The script initializes the webcam using OpenCV.
2. MediaPipe is used to detect and track hand landmarks in real-time.
3. The thumb and index finger are tracked, and the distance between them is calculated to detect a pinch.
4. When the pinch value exceeds a threshold, a mouse click is simulated.
5. The cursor is moved based on the hand's position, and smooth cursor movement is implemented to reduce jitter.

## 🎮 Usage

- **Pinch Gesture** : When the thumb and index finger are close enough, it simulates a mouse click.
- **Hand Movement** : Move your hand to control the mouse cursor on the screen.
- **Exit** : Press `q` to close the application.

## 🧰 Configuration

- **Sensitivity Factor** : Controls the speed of cursor movement. Modify `SensitivityFactor` for faster or slower movement.
- **Pinch Threshold** : Adjusts how sensitive the pinch detection is. Modify `PinchThreshold` to change the required pinch distance.
- **Smooth Factor** : Adjusts the smoothness of the cursor movement. Higher values make the movement smoother.

---
