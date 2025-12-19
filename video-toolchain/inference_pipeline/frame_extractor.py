import os
import sys
import moviepy as mp
from PIL import Image

OUTPUT_DIR = "extracted_frames"
RESIZE_HEIGHT = 720
TARGET_FPS = 10

def main():
	# check command line arguments
	if len(sys.argv) != 2:
		print("Usage: python frame_extractor.py <input_video_path>")
		sys.exit(1)

	# fetch the command line argument
	input_video_path = sys.argv[1]

	# check if input files exist
	if not os.path.isfile(input_video_path):
		print("Input video file does not exist")
		sys.exit(1)

	video = mp.VideoFileClip(input_video_path)
	
	# resize the video to 720p
	video = video.resized(height=RESIZE_HEIGHT)
	
	# create or replace output directory
	os.makedirs(OUTPUT_DIR, exist_ok=True)
	
	# extract 10 equidistant individual frames per second save them as JPEG images
	frame_number = 1

	for frame in video.iter_frames(fps = TARGET_FPS, dtype = 'uint8'):
		# create the path for the output frame image with zero-padded numbering
		frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame_number:05d}.jpg")
		Image.fromarray(frame).save(frame_path, "JPEG")
		frame_number += 1

	video.close()


if __name__ == "__main__":
	main()
