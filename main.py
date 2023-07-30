import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import Tracker

model = YOLO('yolov8s.pt')
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# Initialize video capture
cap = cv2.VideoCapture('in.avi')

# Create the tracker
tracker = Tracker()

# Initialize variables
count = 0
list_of_people = []
confidence_threshold = -0.5  # Adjust this threshold as needed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Skip frames to reduce YOLO predictions
    count += 1
    if count % 3 != 0:
        continue

    # Detect people using YOLO
    results = model.predict(frame)
    boxes_data = results[0].boxes.data
    px = pd.DataFrame(boxes_data).astype("float")

    list_of_people = []
    for index, row in px.iterrows():
        x1, y1, x2, y2 = map(int, row[0:4])
        d = int(row[5])
        c = class_list[d]
        confidence = row[5]

        if confidence >= confidence_threshold and 'person' in c:
            # Calculate the center coordinates of the person
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Calculate the width and height of the bounding box
            w = x2 - x1
            h = y2 - y1

            # Reduce the size of the bounding box to cover only the person
            padding = 20  # Adjust this padding as needed
            x1 = max(0, cx - w // 2 - padding)
            x2 = min(frame.shape[1], cx + w // 2 + padding)
            y1 = max(0, cy - h // 2 - padding)
            y2 = min(frame.shape[0], cy + h // 2 + padding)

            list_of_people.append([x1, y1, x2, y2])

    # Update the tracker
    bbox_id = tracker.update(list_of_people)

    # Draw bounding boxes and display count
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = (x3 + x4) // 2
        cy = (y3 + y4) // 2
        cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)
        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 1)
        cv2.putText(frame, "People Count: {}".format(len(bbox_id)), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

    # Display the frame
    cv2.imshow("RGB", frame)

    # Exit on 'Esc' key press
    if cv2.waitKey(2) & 0xFF == 27:
        break

# Release video capture and close the window
cap.release()
cv2.destroyAllWindows()
