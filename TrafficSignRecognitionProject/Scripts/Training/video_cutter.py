import os
import sys
import pandas as pd
import moviepy as mp
from PIL import Image

OUTPUT_DIR = "./extracted_frames"
RESIZE_HEIGHT = 720
RESIZE_RESOLUTION = (1280, 720) # 720p resolution
TARGET_FPS = 10

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov"]

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


def process_video(input_video_path, timestamps_csv_path, frame_id):
    video = mp.VideoFileClip(input_video_path)

    # create a list of valid (start, end) timestamp tuplets
    timestamps = extract_timestamps(timestamps_csv_path, video.duration)

    # extract and save frames from subclips based on the timestamps
    for (start, end) in timestamps:
        subclip = video.subclipped(start, end)

        # resize to 720p for smaller file size and smaller ML model input size
        subclip = subclip.resized(height=RESIZE_HEIGHT)

        # extract 10 equidistant individual frames per second save them as JPEG images 
        for frame in subclip.iter_frames(fps = TARGET_FPS, dtype = 'uint8'):
            # create the path for the output frame image with zero-padded numbering
            frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame_id:05d}.jpg")
            Image.fromarray(frame).save(frame_path, "JPEG")
            frame_id += 1

        subclip.close()

    video.close()
    return frame_id


def process_frame(frame_path, frame_id):
    # open the image file
    with Image.open(frame_path) as image:
        # resize image to 720p using lanczos resampling
        image = image.resize(RESIZE_RESOLUTION, Image.LANCZOS)
         # save the resized image to the frames directory
        output_frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame_id:05d}.jpg")
        image.save(output_frame_path, "JPEG")

def main():
    # check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python video_cutter.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    # fetch the command line argument
    input_dir_path = sys.argv[1]

    # check if input files exist
    if not os.path.isdir(input_dir_path):
        print("Input directory does not exist", file=sys.stderr)
        sys.exit(1)

    # create or replace output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    frame_id = 0

    # go through all the files in directory
    for filename in os.listdir(input_dir_path):
        file_path = os.path.join(input_dir_path, filename)

        # check if the file is a video or image by its extension
        split_filename = os.path.splitext(filename)
        file_extension = split_filename[1].lower()

        if file_extension in VIDEO_EXTENSIONS:
            # video file
            input_video_path = file_path
            timestamps_csv_path = os.path.join(input_dir_path, split_filename[0] + ".csv")
            
            if not os.path.isfile(timestamps_csv_path):
                print(f"Corresponding CSV file {timestamps_csv_path} not found for video: {input_video_path}", file=sys.stderr)
            else:
                frame_id = process_video(input_video_path, timestamps_csv_path, frame_id)
        elif file_extension in IMAGE_EXTENSIONS:
            # image file
            process_frame(file_path, frame_id)
            frame_id += 1
        else:
            # invalid file type
            print(f"Invalid file type: {file_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
