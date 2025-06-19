from matplotlib import pyplot as plt
import numpy as np
import torch
import uuid
import time
import cv2
import os

# model = torch.hub.load('C:/Users/dhruv/OneDrive/Documents/GitHub/Machine Learning/YOLO/yolov5/', 'yolov5s', source='local')

# IMAGES_PATH = os.path.join('data','images')
# labels = ['awake', 'drowsy']
# number_imgs = 20

# cap = cv2.VideoCapture(0)
# for label in labels:
#   print('Collecting images for {}'.format(label))
#   time.sleep(5)

#   for img_num in range( number_imgs):
#     print('Collecting images for {}, image number {}'.format(label, img_num))
    
#     #Webcam feed
#     ret, frame  =cap.read()

#     #Naming out image path
#     imgname = os.path.join(IMAGES_PATH, label+'.'+str(uuid.uuid1())+'.jpg')
    
#     #Writes out image to file
#     cv2.imwrite(imgname, frame)
    
#     #Render to the screen
#     cv2.imshow('Image Collection', frame)
#     time.sleep(2)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/dhruv/OneDrive/Documents/GitHub/Machine Learning/YOLO/yolov5/runs/train/exp8/weights/last.pt', force_reload=True)

# img = os.path.join('data', 'images', 'awake.9fb90069-4c6f-11f0-840d-e46017965dce.jpg')

# results = model(img)
# print(results)

# plt.imshow(np.squeeze(results.render()))
# plt.savefig('results_custom.png') 
# plt.close()

cap = cv2.VideoCapture(0)
while cap.isOpened():
  ret, frame = cap.read()
  
  results = model(frame) #Make Detections

  cv2.imshow('YOLO', np.squeeze(results.render()))

  if cv2.waitKey(10) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()