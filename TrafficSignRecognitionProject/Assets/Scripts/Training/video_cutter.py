import os
import sys
import pandas as pd
import moviepy as mp
from PIL import Image

OUTPUT_DIR = "extracted_frames"
RESIZE_HEIGHT = 720
RESIZE_RESOLUTION = (1280, 720) # 720p resolution
TARGET_FPS = 10

def timestamp_to_seconds(timestamp):
    hours = int(timestamp[0:2])
    minutes = int(timestamp[3:5])
    seconds = int(timestamp[6:8])
    return hours * 3600 + minutes * 60 + seconds


def timestamp_isvalid(start, end, video_duration):
    # negative timestamps not allowed
    if start < 0 or end < 0:
        return False
    
    # start timestamp must be before end timestamp
    if start >= end:
        return False

    if end > video_duration:
        return False

    return True


def extract_timestamps(csv_path, video_duration):
    df = pd.read_csv(csv_path)
    
    # create a list of bounding box coordinate tuples from the CSV
    timestamps = []
    
    for (start, end) in zip(df['start'], df['end']):
        # transform the timestamps to seconds and add them to the list
        start_sec = timestamp_to_seconds(start)
        end_sec = timestamp_to_seconds(end)
        # only add valid timestamps
        if timestamp_isvalid(start_sec, end_sec, video_duration):
            timestamps.append((start_sec, end_sec))
        else:
            print(f"Invalid timestamp: {start} - {end}", file=sys.stderr)

    return timestamps


def main():
    # check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python video_cutter.py <input_video_path> <timestamps_csv_path>", file=sys.stderr)
        sys.exit(1)

    # fetch the command line arguments
    input_video_path = sys.argv[1]
    timestamps_csv_path = sys.argv[2]

    # check if input files exist
    if not os.path.isfile(input_video_path):
        print("Input video file does not exist", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(timestamps_csv_path):
        print("Timestamps CSV file does not exist", file=sys.stderr)
        sys.exit(1)

    video = mp.VideoFileClip(input_video_path)

    # create a list of valid (start, end) timestamp tuplets
    timestamps = extract_timestamps(timestamps_csv_path, video.duration)

    # create or replace output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    frame_number = 0

    # extract and save frames from subclips based on the timestamps
    for (start, end) in timestamps:
        subclip = video.subclipped(start, end)

        # resize to 720p for smaller file size and smaller ML model input size
        subclip = subclip.resized(height=RESIZE_HEIGHT)

        # extract 10 equidistant individual frames per second save them as JPEG images 
        for frame in subclip.iter_frames(fps = TARGET_FPS, dtype = 'uint8'):
            # create the path for the output frame image with zero-padded numbering
            frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame_number:05d}.jpg")
            Image.fromarray(frame).save(frame_path, "JPEG")
            frame_number += 1

        subclip.close()

    video.close()


if __name__ == "__main__":
    main()
