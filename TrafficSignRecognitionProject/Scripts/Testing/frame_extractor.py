import os
import sys
import moviepy as mp
from PIL import Image

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRACTED_FRAMES_PATH = os.path.join(CURRENT_DIR, 'extracted_frames')
RESIZE_HEIGHT = 720
RESIZE_RESOLUTION = (1280, 720) # 720p resolution
TARGET_FPS = 10

def process_video(video_path, video_id):
	video = mp.VideoFileClip(video_path)

	# resize the video to 720p
	video = video.resized(height=RESIZE_HEIGHT)

	# extract 10 equidistant individual frames per second save them as JPEG images
	frame_number = 1

	for frame in video.iter_frames(fps = TARGET_FPS, dtype = 'uint8'):
		# create the path for the output frame image with zero-padded numbering
		frame_path = os.path.join(EXTRACTED_FRAMES_PATH, f"v_{video_id:02d}_frame_{frame_number:05d}.jpg")
		Image.fromarray(frame).save(frame_path, "JPEG")
		frame_number += 1

	video.close()

def process_frame(frame_path, frame_id):
	# open the image file
	image = Image.open(frame_path)

	# resize the frame to 720p using lanczos resampling
	image = image.resize(RESIZE_RESOLUTION, resample=Image.LANCZOS)

	# save the resized image to the frames directory
	output_frame_path = os.path.join(EXTRACTED_FRAMES_PATH, f"frame_{frame_id:05d}.jpg")
	image.save(output_frame_path, "JPEG")

def extract_frames(input_directory_path):
	video_id = 0
	frame_id = 0
	# go thorugh all the files in directory
	for filename in os.listdir(input_directory_path):
		file_path = os.path.join(input_directory_path, filename)

		# check if the file is a video or image by its extension
		file_extension = os.path.splitext(filename)[1].lower()

		if file_extension in [".mp4", ".avi", ".mov"]:
			# video file
			process_video(file_path, video_id)
			video_id += 1
		elif file_extension in [".jpg", ".jpeg", ".png"]:
			# image file
			process_frame(file_path, frame_id)
			frame_id += 1
		else:
			# invalid file type
			print(f"Invalid file type: {file_path}")


def main():
	# check command line arguments
	if len(sys.argv) != 2:
		print("Usage: python frame_extractor.py <input_directory_path>", file=sys.stderr)
		sys.exit(1)

	# fetch the command line argument
	input_directory_path = sys.argv[1]

	# check if input files exist
	if not os.path.isdir(input_directory_path):
		print("Input directory does not exist", file=sys.stderr)
		sys.exit(1)

	# create directory for all individual frames
	os.makedirs(EXTRACTED_FRAMES_PATH, exist_ok=True)

	extract_frames(input_directory_path)


if __name__ == "__main__":
	main()
