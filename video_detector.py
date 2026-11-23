
import cv2
import os


def extract_video_frames(video_path, output_folder="uploads/frames"):
    os.makedirs(output_folder, exist_ok=True)

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise ValueError("Unable to open the uploaded video.")

    frames = []
    frame_interval = 30
    frame_count = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        if frame_count % frame_interval == 0:
            frame_name = f"frame_{len(frames)}.jpg"
            frame_path = os.path.join(output_folder, frame_name)

            cv2.imwrite(frame_path, frame)

            frames.append(frame_path)

        frame_count += 1

    video.release()

    return {
        "total_frames": frame_count,
        "extracted_frames": len(frames),
        "frame_paths": frames
    }
