import cv2 as cv

def motionDetection():
    # cap = cv.VideoCapture('in.avi')
    cap = cv.VideoCapture('crowd.mp4')
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():
        if not ret:
            break

        diff = cv.absdiff(frame1, frame2)
        diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
        dilated = cv.dilate(thresh, None, iterations=3)
        contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        num_people = 0  # Counter for the number of people in the current frame

        for contour in contours:
            (x, y, w, h) = cv.boundingRect(contour)
            if cv.contourArea(contour) < 800: #900 -> initial
                continue
            cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv.putText(frame1, "Pedestrian {}".format('Tracker'), (10, 20), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

            num_people += 1  # Increment the counter for each person detected in the current frame

        cv.putText(frame1, "People Count: {}".format(num_people), (10, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv.imshow("Video", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv.waitKey(50) == 27 or cv.waitKey(1) & 0xFF == ord('q'):
            break

        # Reset the counter for the next frame
        num_people = 0

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    motionDetection()
