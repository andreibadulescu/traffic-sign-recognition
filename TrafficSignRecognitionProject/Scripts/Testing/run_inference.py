import sys
import torch
import os
import torchvision.transforms as transforms
from utils import nonMaxSuppression, convert_cellboxes

# add ../ML to program Path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
ml_dir = os.path.join(parent_dir, 'ML')
weights_dir = os.path.join(ml_dir, 'weights')
sys.path.append(ml_dir)

from model import YoloV1
from utils import nonMaxSuppression
from PIL import Image
from PIL import ImageDraw

TRAINED_WEIGHTS_PATH = os.path.join(weights_dir, 'yolov1_epoch100.pth')
SIGN_LABELS_PATH = os.path.join(parent_dir, 'sign_labels.txt')
EXTRACTED_FRAMES_PATH = os.path.join(current_dir, 'extracted_frames')
DRAWN_IMAGES_PATH = os.path.join(current_dir, 'inference_results')

MODEL_INPUT_SIZE = (448, 448)
CONFIDENCE_THRESHOLD = 0.2

def create_sign_mapping(labels_path):
	# map numeric id equal to line number in the labels file to sign labels
	label_mapping = {}
	with open(labels_path, "r") as f:
		for id, label in enumerate(f):
			label = label.strip()  # remove the newline at the end
			label_mapping[id] = label
	return label_mapping

def run_inference():
	# load model and set it to evaluation mode
	model = YoloV1()
	model.load_state_dict(torch.load(TRAINED_WEIGHTS_PATH, weights_only=True))
	model.eval()

	# load sign classes labels and create (id, class_name) mapping
	label_mapping = create_sign_mapping(SIGN_LABELS_PATH)

	# iterate over all extracted frames
	for frame in sorted(os.listdir(EXTRACTED_FRAMES_PATH)):
		# open the frame and resize it to expected model input size
		frame_path = os.path.join(EXTRACTED_FRAMES_PATH, frame)
		image = Image.open(frame_path)
		resized_image = image.resize(MODEL_INPUT_SIZE)

		# define a transform to convert the image to torch tensor
		transform = transforms.Compose([transforms.ToTensor()])
		# convert the image to torch tensor
		tensor = transform(resized_image)

		# add new dimension for batch, model expects (1, C, H, W)
		tensor = tensor.unsqueeze(0)

		with torch.no_grad(): # disable gradient calculation for inference efficiency
			prediction = model(tensor) # run the model to calculate predictions

		# create a drawable version of the original image
		drawable = ImageDraw.Draw(image)

		# fetch list of bounding boxes from prediction
		#boxes = nonMaxSuppression(prediction)

		# the yolo model returns a tensor shaped (1, 7, 30), but NMS takes as input a list [x, y, w, h, scor, clasa]
		bboxes = convert_cellboxes(prediction)
		bboxes = bboxes[0].reshape(-1, 6).tolist()
		boxes = nonMaxSuppression(bboxes)

		for box in boxes:
			# x, y = center of box, all values are normalized
			x, y, width, height, confidence, class_id = box

			if confidence < CONFIDENCE_THRESHOLD:
				continue # skip poor predictions

			class_name = label_mapping[class_id]

			# print for frontend consumption
			print(f"{frame} {class_name}")

			# convert YOLO to pixel coordinates for drawing bounding boxes
			x_center = x * image.width
			y_center = y * image.height
			box_width = width * image.width
			box_height = height * image.height

			# calculate bounding box coordinates (top left and bottom right)
			x_min = x_center - box_width / 2
			y_min = y_center - box_height / 2
			x_max = x_center + box_width / 2
			y_max = y_center + box_height / 2

			# draw rectangle based on bounding box coordinates and write class name
			drawable.rectangle([x_min, y_min, x_max, y_max], outline = "green", width = 3)
			drawable.text((x_min, y_min - 10), class_name, fill = "green")

		# save the image with drawn bounding boxes
		os.makedirs(DRAWN_IMAGES_PATH, exist_ok=True)
		output_img_path = os.path.join(DRAWN_IMAGES_PATH, frame)
		image.save(output_img_path)

def main():
	if not os.path.isdir(EXTRACTED_FRAMES_PATH):
		print("Extracted frames path does not exist", file=sys.stderr)
		sys.exit(1)

	if not os.path.isfile(TRAINED_WEIGHTS_PATH):
		print(TRAINED_WEIGHTS_PATH, file=sys.stderr)
		print("Trained weights file does not exist", file=sys.stderr)
		sys.exit(1)

	run_inference()


if __name__ == "__main__":
	main()
