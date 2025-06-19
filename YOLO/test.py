import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2

model = torch.hub.load('C:/Users/dhruv/OneDrive/Documents/GitHub/Machine Learning/YOLO/yolov5/', 'yolov5s', source='local')

# Detections Using Images
# img = "./Car.jpg"
# results = model(img)
# results.print()

# plt.imshow(np.squeeze(results.render()))
# plt.savefig("render-car.png")
# plt.close()

#Real time Detection
cap = cv2.VideoCapture(0)
while cap.isOpened():
  ret, frame = cap.read()
  
  results = model(frame) #Make Detections

  cv2.imshow('YOLO', np.squeeze(results.render()))

  if cv2.waitKey(10) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()