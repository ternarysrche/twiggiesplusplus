# New version of the hand tracking module
import cv2
import mediapipe as mp
import time 
import threading

from midi_synth import check

flags = [True, True, True, True]
newFlags = [True, True, True, True]

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

def dist(point1, point2):
  return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

def compute(vec):
  if (vec[0] == []):
    return []
  base_scale = dist(vec[17], vec[5])
  fingers = [dist(vec[4], vec[8]), dist(vec[4], vec[12]), dist(vec[4], vec[16]), dist(vec[4], vec[20])]
  ratios = [fingers[i] / base_scale for i in range(len(fingers))]
  return ratios

def computeDiff(ratio1, ratio2):
  res = 0
  for i in range(len(ratio1)):
    res += (ratio1[i] - ratio2[i])**2
  return res**0.5

def convert(list):
  vec = [[] for i in range(21)]
  for x in list:
    vec[x[0]] = (x[1], x[2])
  return vec

def main():
  pTime = 0
  cTime = 0
  cap = cv2.VideoCapture(0)
  detector = handDetector()

  #CALIBRATION
  
  count = 0
  last = []
  inconsistency = 0
  ar_valid = []
  while (len(ar_valid) <= 20):
    success, img = cap.read()
    cv2.putText(img, "PLACE YOUR HANDS OUT IN FRONT OF YOU FOR CALIBRATION", (200,500), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    print(len(ar_valid))
    
    if (last != []):
      # print(computeDiff(compute(convert(lmlist)), last))
      # print(compute(convert(lmlist)))
      if (len(ar_valid) == 0):
        ar_valid.append(compute(convert(lmlist)))
      elif (computeDiff(compute(convert(lmlist)), ar_valid[0]) > 0.1):
          inconsistency += 1
          cv2.putText(img, "DON'T MOVE YOUR HANDS!!", (200,600), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
      else:
        ar_valid.append(compute(convert(lmlist)))
    if (inconsistency >= 20):
      ar_valid = []
      inconsistency = 0
    last = compute(convert(lmlist))
    # if len(lmlist) != 0:
    #   print(lmlist[4])
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime


    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
  defaultratios = [0 for i in range(len(ar_valid[0]))]
  print(defaultratios)
  for i in range(len(ar_valid[0])):
    for j in range(len(ar_valid)):
      defaultratios[i] += ar_valid[j][i]
    defaultratios[i] /= len(ar_valid)
  
  while (True):
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)

    if (compute(convert(lmlist)) != []):
      currentratios = compute(convert(lmlist))
      print(currentratios)
      fingers = []
      flag = False
      for i in range(len(currentratios)):
        if currentratios[i]/defaultratios[i] < 0.3:
          fingers.append(i)
          thread = threading.Thread(target=check, args=(fingers,i, flags, newFlags))
          thread.daemon = True
          thread.start()

      cv2.putText(img, str(fingers), (200,500), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    # if len(lmlist) != 0:
    #   print(lmlist[4])
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

if __name__ == "__main__":
  main()




