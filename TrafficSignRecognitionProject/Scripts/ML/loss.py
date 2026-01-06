# 3rd module

# import torch
# import torch.nn as nn
# from utils import IoU

# class CostFunction(nn.Module):
#     # implement 3 functions
#     # 1 confidence error
#     # 2 localization error (SSE)
#     # 3 classification error (Categorical Cross Entropy Loss)

#     # each vector has the following structrure [x, y, w, h, C, class1, .... classC], where:
#     #  x = coordonata x a centrului relativa la celula
#     #  y = coordonata y a centrului relativa la celula
#     #  w = latimea w a boxului
#     #  h = inaltimea h a boxului
#     #  C = confidence score
#     #  vectorul one hot encoding al clasei [0 .. 0 .. 1 ... 0]

#     def __init__(self):
#         super().__init__()

#     def forward(self, predictions, target):

#         # predictions are forma (N, 7, 7, 55), N = nr de imagini
#         # structura ultimului vector de 55x1 e asa:
#         # [0:4] coordonatele primei cutii,
#         # [4] - scorul de confidenta
#         # [5:9] - coordonatele cutiei 2,
#         # [9] - confidenta scor 2
#         # [10:55] - logits (per celula, nu per box) [-2.1, 0.5 ...]

#         # target are forma (N, 7, 7, 50)
#         # [0] - coordonata x bounding box-ului
#         # [1] - coordonata y
#         # [2] - latimea
#         # [3] - inaltimea
#         # [4] - masca (iObj) 1.0 daca exista obiect in celula, 0 altfel
#         # [5:50] - one hot encoding

#         lossConf, b1RespTrue, b2RespTrue = self.confidenceError(predictions, target)
#         lossLoc = self.localizationError(target, predictions, b1RespTrue, b2RespTrue)
#         lossCross = self.categoricalCrossEntropyLoss(target, predictions)

#         totalLoss = lossLoc + lossConf + lossCross
#         return totalLoss / predictions.shape[0]


#     # the probability that an object exists in that box and how well does the box matches the real object
#     def confidenceError(self, predictions, target):
#         # setting the weights
#         lambdaNoobj = 0.5
#         lambdaObj = 1.0

#         box1Coords = predictions[..., 0:4] # pun ... sa ia si dimensiunile de dinainte
#         box1Conf = predictions[..., 4:5]

#         box2Coords = predictions[..., 5:9]
#         box2Conf = predictions[..., 9:10] # pun 9:10 ca sa imi adauge ultima dimensiune 1 sa pot aplica mai departe calculele

#         targetBoxCoords = target[..., 0:4]

#         iouScore1 = IoU(box1Coords, targetBoxCoords)
#         iouScore2 = IoU(box2Coords, targetBoxCoords)

#         # one of the masks is responsible for the object (1 / 0)
#         b1Responsible = (iouScore1 >= iouScore2).float()
#         b2Responsible = 1.0 - b1Responsible

#         # another mask; (1 / 0) value if the box is responsible and the object is there
#         b1RespTrue = target[..., 4:5] * b1Responsible
#         b2RespTrue = target[..., 4:5] * b2Responsible

#         # now each box is penalized differently
#         lossObj = torch.sum(b1RespTrue * (box1Conf - iouScore1) ** 2) + torch.sum(b2RespTrue * (box2Conf - iouScore2) ** 2)

#         b1Noobj = 1.0 - b1RespTrue
#         b2Noobj = 1.0 - b2RespTrue

#         lossNoobj = torch.sum(b1Noobj * (box1Conf - 0.0) ** 2) + torch.sum(b2Noobj * (box2Conf - 0.0) ** 2)

#         return (lambdaObj * lossObj + lambdaNoobj * lossNoobj), b1RespTrue, b2RespTrue

#     # penalizes the model if the position and dimension are wrongly predicted
#     # we are using the Error Sum of Squares
#     def localizationError(self, target, predictions, b1RespTrue, b2RespTrue):
#         # weight to penalize the wrong position or dimension of the box
#         lambdaCoord = 5.0

#         # to measure the difference between the predicted box and the real box we measure on coordinates:
#         # x difference for Box1
#         firstBoxXY = (predictions[..., 0:2] - target[..., 0:2]) ** 2
#         secondBoxXY = (predictions[..., 5:7] - target[..., 0:2]) ** 2
#         L1 = torch.sum(b1RespTrue * firstBoxXY + b2RespTrue * secondBoxXY)

#         firstBoxWH = (torch.sqrt(torch.abs(predictions[..., 2:4]) + 1e-6) - torch.sqrt(torch.abs(target[..., 2:4]) + 1e-6)) ** 2
#         secondBoxWH = (torch.sqrt(torch.abs(predictions[..., 7:9]) + 1e-6) - torch.sqrt(torch.abs(target[..., 2:4]) + 1e-6)) ** 2
#         L2 = torch.sum(b1RespTrue * firstBoxWH + b2RespTrue * secondBoxWH)

#         return lambdaCoord * (L1 + L2)

#     # penalizes the model if it makes a wrong guess regarding the object class
#     def categoricalCrossEntropyLoss(self, target, predictions):
#         lambdaObj = 1.0
#         isObj = target[..., 4].unsqueeze(-1) # adauga ultima dimensiune
#         L = target[..., 5:50] * torch.log(torch.softmax(predictions[..., 10:55], dim=-1) + 1e-6) # softmax makes sure the numbers are probabilities
#         L = torch.sum(L * isObj)

#         return (-1) * L * lambdaObj





# import torch
# import torch.nn as nn
# from utils import IoU

# class CostFunction(nn.Module):
#     def __init__(self):
#         super(CostFunction, self).__init__()
#         self.mse = nn.MSELoss(reduction="sum") # yolo foloseste mse, nu cross entropy (loss mai mare => gradient mai puternic)
#         self.S = 7
#         self.B = 2
#         self.C = 45
#         self.lambda_noobj = 0.5 # penalizare mica pentru fundal
#         self.lambda_coord = 5.0 # si penalizare mare pentru coordonate

#     def forward(self, predictions, target):
#         # predictions: (N, 7, 7, 30)
#         # target: (N, 7, 7, 25)

#         # transformam pentru a putea lucra celula cu celula
#         predictions = predictions.reshape(-1, self.B * 5 + self.C)
#         target = target.reshape(-1, 5 + self.C)


#         mask_obj = (target[:, 4] == 1) # masca pentru celule cu obiect
#         mask_noobj = (target[:, 4] == 0) # masca pentru celule fara obiect

#         # =======================
#         #    LOSS NO OBJECT
#         # =======================
#         # Penalizam ambele cutii daca prezic ceva in fundal (unde conf trebuie sa fie 0)
#         no_object_loss = self.mse(predictions[mask_noobj][:, 4], target[mask_noobj][:, 4])
#         no_object_loss += self.mse(predictions[mask_noobj][:, 9], target[mask_noobj][:, 4])

#         # =======================
#         #    LOSS OBJECT
#         # =======================
#         box_loss = torch.tensor(0.0, device=predictions.device)
#         object_loss = torch.tensor(0.0, device=predictions.device)
#         class_loss = torch.tensor(0.0, device=predictions.device)
#         loser_loss = torch.tensor(0.0, device=predictions.device)

#         if torch.sum(mask_obj) > 0:
#             pred_obj = predictions[mask_obj]
#             target_obj = target[mask_obj]

#             # --- CALCUL IoU CORECT ---
#             # Problema geometrica: x,y sunt relative la celula (0-1), w,h sunt relative la imagine (0-1).
#             # Pentru IoU corect, trebuie sa le aducem pe aceeasi scara. Inmultim w,h cu S (7).

#             box1_iou = pred_obj[:, 0:4].clone()
#             box1_iou[:, 2:4] *= self.S

#             box2_iou = pred_obj[:, 5:9].clone()
#             box2_iou[:, 2:4] *= self.S

#             target_iou = target_obj[:, 0:4].clone()
#             target_iou[:, 2:4] *= self.S

#             # Calculam IoU folosind dimensiunile ajustate
#             ious1 = IoU(box1_iou, target_iou).detach()
#             ious2 = IoU(box2_iou, target_iou).detach()

#             # --- FIX CRITIC PENTRU EROAREA TA ---
#             # ious1 are forma (N, 1). NU folosi unsqueeze(1) aici, altfel devine (N, 1, 1)
#             # si inmultirea cu (N, 4) va produce (N, N, 4) -> Eroarea ta de broadcasting.
#             best_box = (ious1 >= ious2).float()

#             # -- Coordonate (Doar cutia castigatoare) --
#             # (N, 1) * (N, 4) -> (N, 4). Corect.
#             box_pred = best_box * pred_obj[:, 0:4] + (1 - best_box) * pred_obj[:, 5:9]
#             box_loss = self.mse(box_pred, target_obj[:, 0:4])

#             # -- Confidenta Obiect (Doar cutia castigatoare -> Target 1) --
#             conf_pred = best_box * pred_obj[:, 4:5] + (1 - best_box) * pred_obj[:, 9:10]
#             object_loss = self.mse(conf_pred, target_obj[:, 4:5])

#             # -- Confidenta Pierzatoare (Cutia proasta -> Target 0) --
#             conf_loser = (1 - best_box) * pred_obj[:, 4:5] + best_box * pred_obj[:, 9:10]
#             loser_loss = self.mse(conf_loser, torch.zeros_like(conf_loser))

#             # -- Clase --
#             class_loss = self.mse(pred_obj[:, 10:], target_obj[:, 5:])

#         # Total Loss
#         loss = (
#             self.lambda_coord * box_loss
#             + object_loss
#             + self.lambda_noobj * (no_object_loss + loser_loss)
#             + class_loss
#         )

#         return loss


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


    def __init__(self, C=45):
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
