import cv2
import os

# Path to the input video file
video_path = "in_trimmed.avi"

# Create the "frames" folder if it doesn't exist
output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)

# Open the video file
video = cv2.VideoCapture(video_path)

# Iterate through the first 100 frames
for frame_count in range(100):
    # Read the current frame
    ret, frame = video.read()

    # Break the loop if there are no more frames
    if not ret:
        break

    # Save the frame as an image file
    frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
    cv2.imwrite(frame_path, frame)

    # Display the frame (optional)
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)

# Release the video file and close any open windows
video.release()
cv2.destroyAllWindows()
