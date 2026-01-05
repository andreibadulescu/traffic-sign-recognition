import os
import sys
from PIL import Image
import numpy as np
from moviepy.editor import ImageSequenceClip
from moviepy.editor import VideoClip

DRAWN_IMAGES_PATH = "inference_results"
OUTPUT_VIDEO_NAME = "output_video.mp4"

SOURCE_FPS = 10
UPSCALE_RESOLUTION = (1920, 1080) # full HD resolution


def reconstruct_video(output_video_path, target_fps):
	# get string list of drawn frames names
	frame_files = sorted(os.listdir(DRAWN_IMAGES_PATH))
	num_frames = len(frame_files)

	# calculate final video duration in seconds
	duration = num_frames / SOURCE_FPS

	# function that returns the frame at a given time t
	def get_frame(t):
		# compute the index of the source frame corresponding to time t
		src_frame_idx = min(int(t * SOURCE_FPS), num_frames - 1)

		# load the drawn frame image
		frame_path = os.path.join(DRAWN_IMAGES_PATH, frame_files[src_frame_idx])
		frame_img = Image.open(frame_path)

		# upscale frame to target resolution using lanczos interpolation
		frame_img = frame_img.resize(UPSCALE_RESOLUTION, Image.LANCZOS)
		return np.array(frame_img) # convert image to numpy array

	# create the video clip object using the make_frame function
	video_clip = VideoClip(get_frame, duration = duration)

	# write video clip to output file path
	video_clip.write_videofile(
		os.path.join(output_video_path, OUTPUT_VIDEO_NAME),
		fps = target_fps,
		codec = 'libx264'
	)


def main():
	if len(sys.argv) < 3:
		print("Usage: python reconstruct_video.py <output_video_path> <fps>")
		sys.exit(1)

	output_video_path = sys.argv[1]
	fps = int(sys.argv[2]) # convert argument to integer

	# check if provided path is a valid directory
	if not os.path.isdir(output_video_path):
		print("Output video path does not exist")
		sys.exit(1)

	# validate fps number
	if fps <= 0 or not isinstance(fps, int):
		print("FPS must be a positive integer")
		sys.exit(1)

	reconstruct_video(output_video_path, fps)


if __name__ == "__main__":
	main()
