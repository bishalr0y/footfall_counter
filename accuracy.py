import cv2 as cv
import numpy as np

def nonMaxSuppression(boxes, overlap_threshold):
    if len(boxes) == 0:
        return []

    # Convert the boxes to numpy array
    boxes = np.array(boxes)

    # Initialize the list of picked indexes
    picked_indexes = []

    # Get the coordinates of bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # Calculate the areas of bounding boxes
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    # Sort the bounding boxes by the bottom-right y-coordinate
    sorted_indexes = np.argsort(y2)

    # Iterate over the sorted indexes
    while len(sorted_indexes) > 0:
        # Get the index of the last bounding box in the sorted list
        last_index = len(sorted_indexes) - 1

        # Get the index with the largest confidence score
        index = sorted_indexes[last_index]
        picked_indexes.append(index)

        # Find the coordinates of intersection region
        xx1 = np.maximum(x1[index], x1[sorted_indexes[:last_index]])
        yy1 = np.maximum(y1[index], y1[sorted_indexes[:last_index]])
        xx2 = np.minimum(x2[index], x2[sorted_indexes[:last_index]])
        yy2 = np.minimum(y2[index], y2[sorted_indexes[:last_index]])

        # Calculate the width and height of the intersection region
        width = np.maximum(0, xx2 - xx1 + 1)
        height = np.maximum(0, yy2 - yy1 + 1)

        # Calculate the intersection area and union area
        intersection_area = width * height
        union_area = areas[index] + areas[sorted_indexes[:last_index]] - intersection_area

        # Calculate the overlap ratio
        overlap_ratio = intersection_area / union_area

        # Remove the indexes of bounding boxes with high overlap
        overlapping_indexes = np.where(overlap_ratio > overlap_threshold)[0]
        sorted_indexes = np.delete(sorted_indexes, np.concatenate(([last_index], overlapping_indexes)))

    # Return the picked bounding boxes
    return boxes[picked_indexes]

def motionDetection():
    cap = cv.VideoCapture('in_trimmed.avi')
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    count_array = []  # Array to store the count of people in each frame

    frame_count = 0
    while cap.isOpened() and frame_count < 100:
        if not ret:
            break

        diff = cv.absdiff(frame1, frame2)
        diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
        dilated = cv.dilate(thresh, None, iterations=3)
        contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        num_people = 0  # Counter for the number of people in the current frame
        boxes = []  # List to store the bounding boxes

        for contour in contours:
            (x, y, w, h) = cv.boundingRect(contour)
            if cv.contourArea(contour) < 500:
                continue
            boxes.append([x, y, x + w, y + h])

        # Apply non-maximum suppression to filter redundant bounding boxes
        boxes = nonMaxSuppression(boxes, 0.3)

        for (x, y, x2, y2) in boxes:
            cv.rectangle(frame1, (x, y), (x2, y2), (0, 255, 0), 2)
            cv.putText(frame1, "Pedestrian {}".format('Tracker'), (10, 20), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

            num_people += 1  # Increment the counter for each person detected in the current frame

        cv.putText(frame1, "People Count: {}".format(num_people), (10, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv.imshow("Video", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        count_array.append(num_people)  # Store the count in the array
        frame_count += 1

        if cv.waitKey(50) == 27 or cv.waitKey(1) & 0xFF == ord('q'):
            break

        # Reset the counter for the next frame
        num_people = 0

    cap.release()
    cv.destroyAllWindows()

    # Display the count of people in the first 100 frames
    print("Count of people in the first 100 frames:")
    for i, count in enumerate(count_array):
        print("Frame {}: {}".format(i+1, count))
    
    print("-----------------")
    print(count_array)

if __name__ == "__main__":
    motionDetection()
