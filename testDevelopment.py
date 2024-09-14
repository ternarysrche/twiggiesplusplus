import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
from mediapipe.tasks.python import BaseOptions

# Path to the model (Ensure this path is correct)
model_path = r'C:\Users\Hamza\OneDrive - Massachusetts Institute of Technology\Freshman Year\HackMIT 2024\hand_landmarker.task'

# Constants
mpDraw = mp.solutions.drawing_utils
mode = False
maxHands = 2
modelComplex = 1
detectionCon = .5
trackCon = .5

# Function to draw detected hands using the OpenCV frame
def drawHands(img, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(mode, maxHands, modelComplex, detectionCon, trackCon)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if draw:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

# Function to handle hand landmark results
def handle_result(result: vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    pass  # You can add functionality here if needed

# Initialize hand landmarker
try:
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=RunningMode.LIVE_STREAM,
        result_callback=handle_result  # Pass the callback function here
    )
except Exception as e:
    pass  # Handle exceptions silently if needed

# Open webcam using OpenCV
cap = cv2.VideoCapture(0)

# Create the hand landmarker
try:
    with HandLandmarker.create_from_options(options) as hand_landmarker:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue

            # Convert the frame to RGB (since OpenCV loads frames as BGR)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create a MediaPipe Image object
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Get current timestamp in milliseconds
            timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

            # Run hand landmark detection asynchronously
            hand_landmarker.detect_async(mp_image, timestamp)

            # Draw hands using the OpenCV frame (not the MediaPipe Image)
            drawHands(frame)

            # Display the frame with drawn hands
            cv2.imshow('Hand Landmarker', frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

except Exception as e:
    pass  # Handle exceptions silently if needed

# Release resources
# cap.release()
cv2.destroyAllWindows()
