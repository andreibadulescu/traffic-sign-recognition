# 4th module

import torch
import torch.optim as optim
from torch.utils.data import DataLoader
import os
from tqdm import tqdm

torch.autograd.set_detect_anomaly(True) # detecteaza operatii care dau erori la backprop (pt debug)

from model import YoloV1
from loss import CostFunction
from dataset import GetData
import config
import gc

def train_fn(train_loader, model, optimizer, loss_fn):
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
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) # limiteaza gradientii sa nu explodeze
        optimizer.step()

        # elibereaza memoria inutila
        del x, y, out, loss
        torch.cuda.empty_cache() # Curata VRAM

        # updateaza bara de progres
        loop.set_postfix(loss=loss_value)

    # facem media losului pe epoca
    mean_loss_val = sum(mean_loss) / len(mean_loss)
    print(f"Mean loss was {mean_loss_val}")
    return mean_loss_val

def main():
    scaler = torch.amp.GradScaler('cuda', enabled=torch.cuda.is_available())
    model = YoloV1().to(config.DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.5, patience=5) # folosim un scheduler ca sa reduca learning rate-ul daca loss-ul stagneaza
    loss_fn = CostFunction()
    
    files = os.listdir(config.TRAIN_IMG_DIR)
    img_files = []
    label_files = []
    
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            img_path = os.path.join(config.TRAIN_IMG_DIR, file)

            # adaugam labeluri imaginilor
            label_name = file.rsplit('.', 1)[0] + ".txt"
            label_path = os.path.join(config.TRAIN_LABEL_DIR, label_name)
            
            if os.path.exists(label_path):
                img_files.append(img_path)
                label_files.append(label_path)

    train_dataset = GetData(
        imgDir=img_files, 
        labelsDir=label_files,
        S=config.S, 
        B=config.B, 
        C=config.C
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

        mean_loss = train_fn(train_loader, model, optimizer, loss_fn) # antrenam o epoca
        scheduler.step(mean_loss) # ajustam learning rate-ul
        
        # salvam modelul
        if (epoch+1) % config.saveEvery == 0:
          save_path = f"weights/yolov1_epoch{epoch+1}.pth"
          torch.save(model.state_dict(), save_path)
          print(f"Model salvat: {save_path}")
          print("Model saved!")

if __name__ == "__main__":
    main()