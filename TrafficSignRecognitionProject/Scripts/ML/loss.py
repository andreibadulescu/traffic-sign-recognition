# 3rd module

import torch
import torch.nn as nn
from utils import IoU


class CostFunction(nn.Module):

    # implementez 5 lossuri:
    # 1) no-object loss care ajuta sa reduca fals pozitivele
    # 2) object confidence loss care altereaza increderea pentru a face detectii reale
    # 3) localization loss pentru a penaliza cutiile imprecise
    # 4) loser loss care asigura o cutie per obiect
    # 5) classification loss care se asigura ca sunt etichetate corect obiectele


    def __init__(self, C=15):
        super(CostFunction, self).__init__()

        # yolo original foloseste Mean Squared Error
        # reduction="sum" inseamna ca toate erorile se aduna (erori mari => gradient mare => corectie puternica)
        self.mse = nn.MSELoss(reduction="sum")

        # hiperparametri
        self.S = 7   # grid 7x7
        self.B = 2   # 2 box-uri per celula
        self.C = C  # numar de clase

        self.lambda_noobj = 0.5   # fundalul conteaza mai putin (penalizare mica)
        self.lambda_coord = 5.0   # coordonatele conteaza mult (penalizare mare)


    def forward(self, predictions, target):

        # predictions = [x1,y1,w1,h1,conf1, x2,y2,w2,h2,conf2, class_probs]
        # target      = [x,y,w,h,obj, class_one_hot]

        # transform grid-ul 7x7 intr-o lista de celule
        predictions = predictions.reshape(-1, self.B * 5 + self.C)
        target = target.reshape(-1, 5 + self.C)

        # identificam celulele
        mask_obj = target[:, 4] == 1 # true unde exista obiect
        mask_noobj = target[:, 4] == 0 # true unde nu exista obiect

        # Object Loss
        # daca nu exista obiect in celula, confidence-ul ambelor box-uri trebuie sa fie 0
        no_object_loss = self.mse(predictions[mask_noobj][:, 4], target[mask_noobj][:, 4])
        no_object_loss += self.mse(predictions[mask_noobj][:, 9], target[mask_noobj][:, 4])

        # initializam lossurile
        box_loss = torch.tensor(0.0, device=predictions.device)
        object_loss = torch.tensor(0.0, device=predictions.device)
        class_loss = torch.tensor(0.0, device=predictions.device)
        loser_loss = torch.tensor(0.0, device=predictions.device)

        # pentru celulele cu obiect
        if mask_obj.sum() > 0:

            # luam doar celulele relevante
            pred_obj = predictions[mask_obj]
            target_obj = target[mask_obj]

            # IoU decide care box este responsabil de obiect. nu este folosit direct in loss, ci doar ca decizie.

            # Box 1
            box1 = pred_obj[:, 0:4].clone()
            box1[:, 2:4] *= self.S  # aducem w,h la aceeasi scara

            # Box 2
            box2 = pred_obj[:, 5:9].clone()
            box2[:, 2:4] *= self.S

            # Ground truth
            target_box = target_obj[:, 0:4].clone()
            target_box[:, 2:4] *= self.S

            iou1 = IoU(box1, target_box).detach()
            iou2 = IoU(box2, target_box).detach()

            # best_box = 1 daca box1 e mai bun, 0 daca box2 e mai bun
            best_box = (iou1 >= iou2).float()

            # Localization loss
            # doar boxul responsabil invata coordonatele, in timp ce a doua cutie nu este penalizata

            box_pred = (best_box * pred_obj[:, 0:4] + (1 - best_box) * pred_obj[:, 5:9])
            box_loss = self.mse(box_pred, target_obj[:, 0:4])

            # Object confidence Loss
            # Box-ul responsabil trebuie sa aiba confidence 1
            conf_pred = (best_box * pred_obj[:, 4:5] + (1 - best_box) * pred_obj[:, 9:10])
            object_loss = self.mse(conf_pred, target_obj[:, 4:5])

            # Loser confidence loss
            # cutia care nu e rasponsabila trebuie sa aiba increderea 0
            conf_loser = ((1 - best_box) * pred_obj[:, 4:5] + best_box * pred_obj[:, 9:10])
            loser_loss = self.mse(conf_loser, torch.zeros_like(conf_loser))

            # Classification loss
            # nu se clasifica fundalul
            class_loss = self.mse(pred_obj[:, 10:], target_obj[:, 5:])

        # penalizare totala
        total_loss = (self.lambda_coord * box_loss + object_loss + self.lambda_noobj * (no_object_loss + loser_loss) + class_loss)

        return total_loss
