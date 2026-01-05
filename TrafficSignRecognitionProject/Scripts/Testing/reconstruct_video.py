import os
import sys
from PIL import Image
import numpy as np
from moviepy.editor import ImageSequenceClip
from moviepy.editor import VideoClip
from collections import defaultdict

DRAWN_IMAGES_PATH = "./inference_results"

SOURCE_FPS = 10
UPSCALE_RESOLUTION = (1920, 1080) # full HD resolution

def reconstruct_video(output_dir_path, target_fps):
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
        duration = num_frames / target_fps

		# function that returns the frame at a given time t
        def get_frame(t, files=files, num_frames=num_frames):
            # find corresponding source frame index for time t
            idx = min(int(t * target_fps), num_frames - 1)
            frame_path = os.path.join(DRAWN_IMAGES_PATH, files[idx])
            
			# open, upscale, and convert to numpy array
            with Image.open(frame_path) as img:
                img_resized = img.resize(UPSCALE_RESOLUTION, Image.LANCZOS)
                return np.array(img_resized)

		# create VideoClip object from the get_frame function
        video_clip = VideoClip(get_frame, duration=duration)
        
		# define output video path
        output_video_name = f"video_{prefix[-2:]}.mp4"
        output_video_path = os.path.join(output_dir_path, output_video_name)
        
		# write video to disk at target FPS with H.264 codec
        video_clip.write_videofile(output_video_path, fps=target_fps, codec="libx264")
        print(f"Created video {output_video_name} with {num_frames} frames")


def main():
	if len(sys.argv) < 3:
		print("Usage: python reconstruct_video.py <output_directory_path> <fps>", file=sys.stderr)
		sys.exit(1)

	output_dir_path = sys.argv[1]
	fps = int(sys.argv[2]) # convert argument to integer

	# validate fps number
	if fps <= 0 or not isinstance(fps, int):
		print("FPS must be a positive integer", file=sys.stderr)
		sys.exit(1)

	# create output directory for the final
	os.makedirs(output_dir_path, exist_ok=True)

	reconstruct_video(output_dir_path, fps)


if __name__ == "__main__":
	main()
