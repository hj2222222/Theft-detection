import math
from ultralytics import YOLO
import cv2
# import ultralytics
import torch

if torch.cuda.is_available():
    device = torch.device('cuda')
    print("GPU를 사용", torch.cuda.get_device_name(0))
else:
    device = torch.device('cpu')
    print("GPU를 사용할 수 없습니다, CPU를 사용합니다.")

# ultralytics.checks()


model = YOLO('./best.pt')
# model = torch.load('./best.pt')

cap = cv2.VideoCapture('./test2.mp4')

thief = False
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        result = model.predict(frame,save=False,conf=0.35)
        boxes = result[0].boxes
        box_coordinates = boxes.xyxy
        print(len(boxes))
        if len(boxes) == 2:
            print('손2개 인식!')
            xmin1, ymin1, xmax1, ymax1 = box_coordinates[0]
            xmin2, ymin2, xmax2, ymax2 = box_coordinates[1]
            centerx1 = (xmin1+xmax1)/2
            centery1 = (ymin1+ymax1)/2
            centerx2 = (xmin2+xmax2)/2
            centery2 = (ymin2+ymax2)/2
            distance = math.sqrt((centerx2 - centerx1) ** 2 + (centery2 - centery1) ** 2)
            print(distance)
            if distance <= 150:
                thief = True
                print(thief)
        if thief:
            height, width = frame.shape[:2]
            text = "caution!"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_color = (0, 0, 255)  # 빨강색
            font_thickness = 2
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
            x = (width - text_width) // 2
            y = (height + text_height) // 2
            cv2.putText(frame, text, (x, y), font, font_scale, font_color, font_thickness)
        cv2.imshow('frame', frame)
        if cv2.waitKey(3) & 0xFF == ord('q'):
            break
print(thief)