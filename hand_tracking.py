# New version of the hand tracking module

import cv2
from flask import Flask, Response
# def generate_frames():
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             # Encode frame to JPEG
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             # Yield frame as byte stream in the format of a multipart response
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# # Video feed route
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(debug=True)

import mediapipe as mp
import time 

class handDetector():
  def __init__(self, mode = False, maxHands = 2, modelComplex = 1,detectionCon = .5, trackCon = .5):
    self.mode = mode
    self.maxHands = maxHands
    self.detectionCon = detectionCon
    self.trackCon = trackCon
    self.modelComplex = modelComplex

    self.mpHands =  mp.solutions.hands
    self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
    self.mpDraw = mp.solutions.drawing_utils
  
  def findHands(self, img, draw = True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.results = self.hands.process(imgRGB)

    if self.results.multi_hand_landmarks:
      for handLms in self.results.multi_hand_landmarks:
        if draw:
          self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
    return img
  def findPosition(self, img, handNo = 0, draw =  True):
    lmlist = []
    if self.results.multi_hand_landmarks:
      myHand = self.results.multi_hand_landmarks[handNo]
      for id, lm in enumerate(myHand.landmark):
        h, w, cc = img.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        lmlist.append([id, cx, cy])
        if draw: 
          cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
    return lmlist

def main():
  pTime = 0
  cTime = 0
  cap = cv2.VideoCapture(0)
  detector = handDetector()
  frame = None

  while True:
    success, frame = cap.read()
    if not success:
            break
    else:
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield frame as byte stream in the format of a multipart response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    img = frame
    try:
      img = detector.findHands(img)
      lmlist = detector.findPosition(img)
    except:
       continue
    if len(lmlist) != 0:
      print(lmlist[4])
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(main(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
  app.run(debug=True)
  # main()






