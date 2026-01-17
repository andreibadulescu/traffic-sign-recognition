# DEFINE CONSTANTS & PATHS

import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
PIN_MEMORY = False

S = 7
B = 2
C = 15

IMG_SIZE = 448

BATCH_SIZE = 16 #16 4 2
EPOCHS = 100
LEARNING_RATE = 1e-4
EPSILON = 1e-6

nmsThresh = 0.1
iouThresh = 0.5

trainImages = ""
trainLabels = ""

weightsDir = ""
evalEvery = 1
saveEvery = 5

TRAIN_IMG_DIR = "data/train/images"
TRAIN_LABEL_DIR = "data/train/labels"
TEST_IMG_DIR = "data/test/images"
TEST_LABEL_DIR = "data/test/labels"