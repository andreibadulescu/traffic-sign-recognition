import os
import sys
import pandas as pd
import moviepy as mp

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
    entries_count = df['start'].size
    
    # create a list of tuplets from the timestamps CSV
    timestamps = []
    
    for (start, end) in zip(df['start'], df['end']):
        # transform the timestamps to seconds and add them to the list
        start_sec = timestamp_to_seconds(start)
        end_sec = timestamp_to_seconds(end)
        # validate timestamps
        if timestamp_isvalid(start_sec, end_sec, video_duration):
            timestamps.append((start_sec, end_sec))
        else:
            print(f"Invalid timestamp: {start} - {end}")

    return timestamps

def main():
    # check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python video_cutter.py <input_video> <timestamps_csv>")
        sys.exit(1)

    # fetch the command line arguments
    input_video_path = sys.argv[1]
    timestamps_csv_path = sys.argv[2]

    # check if input files exist
    if not os.path.isfile(input_video_path):
        print("Input video file does not exist")
        sys.exit(1)

    if not os.path.isfile(timestamps_csv_path):
        print("Timestamps CSV file does not exist")
        sys.exit(1)

    video = mp.VideoFileClip(input_video_path)

    # create a list of valid (start, end) timestamp tuplets
    timestamps = extract_timestamps(timestamps_csv_path, video.duration)

    # create or replace output directory
    output_dir = "extracted_clips"
    os.makedirs(output_dir, exist_ok=True)

    # extract and save video clips based on the timestamps
    clip_number = 1
    for (start, end) in timestamps:
        subclip = video.subclipped(start, end)

        # resize to 720p for smaller file size and smaller ML model input size
        subclip = subclip.resized(height=720)

        # create a file in the output directory and write the subclip to it
        subclip_path = os.path.join(output_dir, f"clip_{clip_number}.mp4")
        subclip.write_videofile(subclip_path)
        subclip.close()
        clip_number += 1

    video.close()


if __name__ == "__main__":
    main()
