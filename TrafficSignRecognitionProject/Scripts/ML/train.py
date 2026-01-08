# 4th module

import torch
import torch.optim as optim
from torch.utils.data import DataLoader
import os
import argparse
from tqdm import tqdm

torch.autograd.set_detect_anomaly(True) # detecteaza operatii care dau erori la backprop (pt debug)

from model import YoloV1
from loss import CostFunction
from dataset import GetData
import config
import gc

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_DIR = os.path.join(CURRENT_DIR, "weights")

def transfer_learning(model, path):
	oldWeights = torch.load(path, map_location=config.DEVICE) # load old weights for transfer learning

	if "state_dict" in oldWeights:
		oldWeights = oldWeights["state_dict"]

	model_dict = model.state_dict()
	pretrained_dict = {}
	for k, v in oldWeights.items():
		if k in model_dict and v.shape == model_dict[k].shape:
			pretrained_dict[k] = v

    # update the model
	model_dict.update(pretrained_dict)
	model.load_state_dict(model_dict, strict=False)


def train_fn(train_loader, model, optimizer, loss_fn, scaler):
	loop = tqdm(train_loader, leave=True)
	mean_loss = []

	for batch_idx, (x, y) in enumerate(loop):
		x, y = x.to(config.DEVICE), y.to(config.DEVICE)

		with torch.amp.autocast('cuda', enabled=torch.cuda.is_available()):
			out = model(x) # forward pass
			loss = loss_fn(out, y) # calculez loss-ul pt batchul curent

		loss_value = loss.item()
		mean_loss.append(loss_value)

		# 3. Backward pass
		optimizer.zero_grad()
		scaler.scale(loss).backward()
		scaler.step(optimizer)
		scaler.update()

		# loss.backward()
		# torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) # limiteaza gradientii sa nu explodeze
		# optimizer.step()

		# elibereaza memoria inutila
		del x, y, out, loss
		torch.cuda.empty_cache() # Curata VRAM

		# updateaza bara de progres
		loop.set_postfix(loss=loss_value)

	# facem media losului pe epoca
	mean_loss_val = sum(mean_loss) / len(mean_loss)
	print(f"Mean loss was {mean_loss_val}")
	return mean_loss_val

def get_num_classes_from_labels(label_dir):
	max_idx = -1
	files = []
	for f in os.listdir(label_dir):
		if f.endswith(".txt"):
			files.append(f)

	if not files:
		return 15 # default

	for file in files:
		path = os.path.join(label_dir, file)
		with open(path, 'r') as f:
			lines = f.readlines()
			for line in lines:
				class_id = int(line.split()[0])
				if class_id > max_idx:
					max_idx = class_id

	return max_idx + 1

def main():

	parser = argparse.ArgumentParser()

	parser.add_argument('--data_dir', type=str, required=True, help='Data directory path')

	args = parser.parse_args()

	current_img_dir = args.data_dir
	current_label_dir = args.data_dir

	detected_C = get_num_classes_from_labels(current_label_dir)

	base_weights = os.path.join(WEIGHTS_DIR, "yolov1_epoch100.pth")
	retrained_weights_path = os.path.join(WEIGHTS_DIR, "yolov1_custom.pth")

	if os.path.exists(retrained_weights_path):
		weights_to_load = retrained_weights_path
	else:
		weights_to_load = base_weights

	model = YoloV1(nrClasses=detected_C).to(config.DEVICE)
	loss_fn = CostFunction(C=detected_C)
	scaler = torch.amp.GradScaler('cuda', enabled=torch.cuda.is_available())

	transfer_learning(model, weights_to_load) # load old weights

	# freeze all blocks except the last layer
	for name, parameters in model.named_parameters():
		if "block_final" in name:
			parameters.requires_grad = True
		else:
			parameters.requires_grad = False


	# optimizer only for active parameters
	params_to_update = []
	for p in model.parameters():
		if p.requires_grad:
			params_to_update.append(p)

	optimizer = optim.Adam(params_to_update, lr=config.LEARNING_RATE, weight_decay=0.0005)
	scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.5, patience=5) # folosim un scheduler ca sa reduca learning rate-ul daca loss-ul stagneaza


	files = os.listdir(current_img_dir)
	img_files = []
	label_files = []

	for file in files:
		if file.endswith(".jpg") or file.endswith(".png"):
			img_path = os.path.join(current_img_dir, file)

            # adaugam labeluri imaginilor
			label_name = file.rsplit('.', 1)[0] + ".txt"
			label_path = os.path.join(current_label_dir, label_name)

			if os.path.exists(label_path):
				img_files.append(img_path)
				label_files.append(label_path)

	train_dataset = GetData(
        imgDir=img_files,
        labelsDir=label_files,
        S=config.S,
        B=config.B,
        C=detected_C
    )

	train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        pin_memory=False,
        drop_last=False,
        num_workers=0
    )

	for epoch in range(config.EPOCHS):
		torch.cuda.empty_cache()
		print(f"Epoch [{epoch+1}/{config.EPOCHS}]")
		model.train()

		mean_loss = train_fn(train_loader, model, optimizer, loss_fn, scaler) # antrenam o epoca
		scheduler.step(mean_loss) # ajustam learning rate-ul

		# salvam modelul
		if (epoch+1) % config.saveEvery == 0:
			#save_path = f"weights/yolov1_epoch{epoch+1}.pth"
			torch.save(model.state_dict(), retrained_weights_path)
			print(f"Model salvat: {retrained_weights_path}")
			print("Model saved!")

if __name__ == "__main__":
    main()