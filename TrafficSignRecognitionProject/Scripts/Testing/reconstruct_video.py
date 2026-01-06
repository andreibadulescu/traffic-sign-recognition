import os
import sys
from PIL import Image
import numpy as np
from moviepy.editor import VideoClip
from collections import defaultdict

DRAWN_IMAGES_PATH = "./inference_results"

TARGET_FPS = 30
UPSCALE_RESOLUTION = (1920, 1080) # full HD resolution

def reconstruct_video(output_dir_path):
    # get sorted list of all drawn frame filenames
    frame_files = sorted(os.listdir(DRAWN_IMAGES_PATH))

    # group frames into single frames vs video groups
    frame_groups = defaultdict(list)
    single_frames = []

    for f in frame_files:
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            if f.startswith("frame_"):
                # regular single frame, not part of a video
                single_frames.append(f)
            elif f.startswith("v_"):
                # video frame, group by prefix v_
                prefix = "_".join(f.split("_")[:2])
                frame_groups[prefix].append(f)

    # copy single frames directly to output directory
    for f in single_frames:
        src_path = os.path.join(DRAWN_IMAGES_PATH, f)
        dst_path = os.path.join(output_dir_path, f)
        # keep original resolution (or optionally resize if desired)
        with Image.open(src_path) as img:
            img.save(dst_path)
    print(f"Copied {len(single_frames)} single frames to {output_dir_path}")

    # process each video frame group separately
    for prefix, files in frame_groups.items():
        files = sorted(files) # ensure temporal order
        num_frames = len(files)
        
        # calculate total duration in seconds
        duration = num_frames / TARGET_FPS

        # function that returns the frame at a given time t
        def get_frame(t, files=files, num_frames=num_frames):
            # find corresponding source frame index for time t
            idx = min(int(t * TARGET_FPS), num_frames - 1)
            frame_path = os.path.join(DRAWN_IMAGES_PATH, files[idx])
            
            # open, upscale, and convert to numpy array
            with Image.open(frame_path) as img:
                img_resized = img.resize(UPSCALE_RESOLUTION, Image.LANCZOS)
                return np.array(img_resized)

        # create VideoClip object from the get_frame function
        video_clip = VideoClip(get_frame, duration=duration)
        
        # define output video path
        video_id = prefix.split("_")[1]
        output_video_name = f"video_{video_id}.mp4"
        output_video_path = os.path.join(output_dir_path, output_video_name)
        
        # write video to disk at target FPS with H.264 codec
        video_clip.write_videofile(output_video_path, fps=TARGET_FPS, codec="libx264")
        print(f"Created video {output_video_name} with {num_frames} frames")


def main():
    if not os.path.isdir(DRAWN_IMAGES_PATH):
        print("Inference results directory does not exist", file=sys.stderr)
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage: python reconstruct_video.py <output_directory_path>", file=sys.stderr)
        sys.exit(1)

    output_dir_path = sys.argv[1]

    # create output directory for the final
    os.makedirs(output_dir_path, exist_ok=True)

    reconstruct_video(output_dir_path)


if __name__ == "__main__":
    main()
