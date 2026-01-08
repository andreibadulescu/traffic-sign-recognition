# # 5th module

import torch
from collections import Counter

def IoU(box1, box2):
    # box1, box2: [x, y, w, h]
    b1_x1 = box1[..., 0:1] - box1[..., 2:3] / 2
    b1_y1 = box1[..., 1:2] - box1[..., 3:4] / 2
    b1_x2 = box1[..., 0:1] + box1[..., 2:3] / 2
    b1_y2 = box1[..., 1:2] + box1[..., 3:4] / 2

    b2_x1 = box2[..., 0:1] - box2[..., 2:3] / 2
    b2_y1 = box2[..., 1:2] - box2[..., 3:4] / 2
    b2_x2 = box2[..., 0:1] + box2[..., 2:3] / 2
    b2_y2 = box2[..., 1:2] + box2[..., 3:4] / 2

    x1 = torch.max(b1_x1, b2_x1)
    y1 = torch.max(b1_y1, b2_y1)
    x2 = torch.min(b1_x2, b2_x2)
    y2 = torch.min(b1_y2, b2_y2)

    intersection = (x2 - x1).clamp(min=0) * (y2 - y1).clamp(min=0)

    box1_area = abs((b1_x2 - b1_x1) * (b1_y2 - b1_y1))
    box2_area = abs((b2_x2 - b2_x1) * (b2_y2 - b2_y1))

    return intersection / (box1_area + box2_area - intersection + 1e-6)

def nonMaxSuppression(bboxes, iou_threshold=0.5, threshold=0.4):
    bboxes = [box for box in bboxes if box[4] > threshold]
    bboxes = sorted(bboxes, key=lambda x: x[4], reverse=True)
    bboxes_after_nms = []

    while bboxes:
        chosen_box = bboxes.pop(0)
        bboxes = [
            box for box in bboxes
            if box[5] != chosen_box[5]
            or IoU(torch.tensor(chosen_box[:4]).unsqueeze(0),
                   torch.tensor(box[:4]).unsqueeze(0)) < iou_threshold
        ]
        bboxes_after_nms.append(chosen_box)
    return bboxes_after_nms

def convert_cellboxes(predictions, S=7):
    # Aceasta este functia CRITICA.
    # Trebuie sa returneze (x, y, w, h) globale, nu (x1, y1, x2, y2).

    predictions = predictions.to("cpu")
    batch_size = predictions.shape[0]
    predictions = predictions.reshape(batch_size, S, S, -1)

    bboxes1 = predictions[..., 0:4]
    bboxes2 = predictions[..., 5:9]
    scores = torch.cat((predictions[..., 4].unsqueeze(0), predictions[..., 9].unsqueeze(0)), dim=0)

    best_box = scores.argmax(0).unsqueeze(-1)
    best_boxes = bboxes1 * (1 - best_box) + bboxes2 * best_box

    cell_indices = torch.arange(S).repeat(batch_size, S, 1).unsqueeze(-1)

    # CALCUL CORECT:
    # x = (x_rel + index) / S
    x = (1 / S) * (best_boxes[..., :1] + cell_indices)
    y = (1 / S) * (best_boxes[..., 1:2] + cell_indices.permute(0, 2, 1, 3))

    # w si h sunt deja 0-1 (de la Sigmoid), NU le adunam cu nimic!
    w = best_boxes[..., 2:3]
    h = best_boxes[..., 3:4]

    # Returnam x, y, w, h concatenate
    converted_bboxes = torch.cat((x, y, w, h), dim=-1)

    predicted_class = predictions[..., 10:].argmax(-1).unsqueeze(-1).float()
    best_confidence = torch.max(predictions[..., 4], predictions[..., 9]).unsqueeze(-1)

    return torch.cat((converted_bboxes, best_confidence, predicted_class), dim=-1)

def get_bboxes(loader, model, iou_threshold, conf_threshold, device="cuda"):
    model.eval()
    all_pred_boxes = []
    all_true_boxes = []
    train_idx = 0

    for batch_idx, (x, labels) in enumerate(loader):
        x = x.to(device)
        labels = labels.to(device)

        with torch.no_grad():
            predictions = model(x)

        batch_size = x.shape[0]
        bboxes = convert_cellboxes(predictions, S=7)

        for idx in range(batch_size):
            nms_boxes = nonMaxSuppression(
                bboxes[idx].reshape(-1, 6).tolist(),
                iou_threshold=iou_threshold,
                threshold=conf_threshold,
            )

            for box in nms_boxes:
                all_pred_boxes.append([train_idx] + box)

            # Ground truth
            for i in range(7):
                for j in range(7):
                    if labels[idx, i, j, 4] == 1:
                        box_cell = labels[idx, i, j, 0:4]
                        class_label = torch.argmax(labels[idx, i, j, 5:])
                        global_x = (box_cell[0] + i) / 7
                        global_y = (box_cell[1] + j) / 7
                        global_w = box_cell[2]
                        global_h = box_cell[3]
                        all_true_boxes.append([train_idx, class_label.item(), 1.0,
                                               global_x.item(), global_y.item(),
                                               global_w.item(), global_h.item()])
            train_idx += 1

    model.train()
    return all_pred_boxes, all_true_boxes

# Functia mean_average_precision ramane neschimbata (dar acum primeste date corecte)
def mean_average_precision(pred_boxes, true_boxes, iou_threshold=0.5, num_classes=45):
    # ... (pastreaza codul tau sau cel vechi, e ok daca IoU e bun)
    average_precisions = []
    epsilon = 1e-6

    for c in range(num_classes):
        detections = [p for p in pred_boxes if p[1] == c]
        ground_truths = [t for t in true_boxes if t[1] == c]

        amount_bboxes = Counter([gt[0] for gt in ground_truths])
        for key, val in amount_bboxes.items():
            amount_bboxes[key] = torch.zeros(val)

        detections.sort(key=lambda x: x[2], reverse=True)
        TP = torch.zeros(len(detections))
        FP = torch.zeros(len(detections))
        total_true_bboxes = len(ground_truths)

        if total_true_bboxes == 0:
            continue

        for detection_idx, detection in enumerate(detections):
            ground_truth_img = [bbox for bbox in ground_truths if bbox[0] == detection[0]]
            best_iou = 0
            best_gt_idx = -1

            for idx, gt in enumerate(ground_truth_img):
                iou = IoU(torch.tensor(detection[3:]).unsqueeze(0),
                          torch.tensor(gt[3:]).unsqueeze(0))
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = idx

            if best_iou > iou_threshold:
                if amount_bboxes[detection[0]][best_gt_idx] == 0:
                    TP[detection_idx] = 1
                    amount_bboxes[detection[0]][best_gt_idx] = 1
                else:
                    FP[detection_idx] = 1
            else:
                FP[detection_idx] = 1

        TP_cumsum = torch.cumsum(TP, dim=0)
        FP_cumsum = torch.cumsum(FP, dim=0)
        recalls = TP_cumsum / (total_true_bboxes + epsilon)
        precisions = TP_cumsum / (TP_cumsum + FP_cumsum + epsilon)
        precisions = torch.cat((torch.tensor([1]), precisions))
        recalls = torch.cat((torch.tensor([0]), recalls))
        average_precisions.append(torch.trapz(precisions, recalls))

    return sum(average_precisions) / (len(average_precisions) + epsilon)