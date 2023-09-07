import cv2
import os
from time import time

def time_lapse_video(input_path, output_path, frame_step, current, total):
    start_time = time()
    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1

        if ret:
            if frame_count % frame_step == 0:
                out.write(frame)
        else:
            break

    cap.release()
    out.release()

    # Calculate processing time and file sizes
    process_time = time() - start_time
    original_size = os.path.getsize(input_path) / (1024 * 1024)  # Convert bytes to megabytes
    new_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert bytes to megabytes
    print(f"Finished processing '{input_path}' ({current} of {total}). Original size: {original_size:.2f} MB, New size: {new_size:.2f} MB, Processing time: {process_time:.2f} seconds")

def combine_videos(video_paths, output_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None

    for video_path in video_paths:
        if os.path.getsize(video_path) > 102400:  # Skip files smaller than 100 KB
            cap = cv2.VideoCapture(video_path)

            if out is None:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                out = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    break

            cap.release()

    if out is not None:
        out.release()

if __name__ == "__main__":
    directory = '.'
    output_videos = []

    mp4_files = [filename for filename in sorted(os.listdir(directory), reverse=False) if filename.endswith(".mp4")]
    total_files = len(mp4_files)

    for index, filename in enumerate(mp4_files, start=1):
        input_path = os.path.join(directory, filename)
        output_path = "time_lapsed_" + filename
        output_videos.append(output_path)
        # hey you can change the '150" in the next line to change how many frames it should drop
        # before it picks up a frame to include. So for instance, 
        # if you set it to 1, it will drop 1 frame, and pick up one. (faster)
        # if you set it to 10, it will drop 10 frames, and pick up one. (much faster)
        # if you set it to 150, it will drop 150 frames and pick up one. (super turbo faster)
        time_lapse_video(input_path, output_path, 150, index, total_files)

    combine_videos(output_videos, "combined_time_lapse.mp4")
