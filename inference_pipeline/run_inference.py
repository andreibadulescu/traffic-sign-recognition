import torch
import os
import torchvision.transforms as transforms
from model import YoloV1
from PIL import Image

TRAINED_WEIGHTS_PATH = "./weights/yolov1_epoch100.pth"
SIGN_LABELS_PATH = "../sign_labels.txt"
EXTRACTED_FRAMES_PATH = "extracted_frames"

MODEL_INPUT_SIZE = (448, 448)

def create_sign_mapping(labels_path):
	# map sign labels to a numeric id equal to their line number in the labels file
	label_mapping = {}
	
	with open(labels_path, 'r') as f:
		for id, label in enumerate(f):
			label = label.strip()  # remove the newline at the end
			label_mapping[label] = id
			
	return label_mapping

def main():
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
		image = image.resize(MODEL_INPUT_SIZE)

		# define a transform to convert the image to torch tensor
		transform = transforms.Compose([transforms.ToTensor()])
		# convert the image to torch tensor
		tensor = transform(image)

		# add new dimension for batch, model expects (1, C, H, W)
		tensor = tensor.unsqueeze(0)

		prediction = model(tensor) # run the model to calculate predictions


if __name__ == "__main__":
	main()