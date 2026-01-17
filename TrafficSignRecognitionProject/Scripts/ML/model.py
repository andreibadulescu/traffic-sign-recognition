# 1st module 

# When creating a new neural network, you would usually go about creating a new class and inheriting from nn.Module, and defining two methods:
# __init__ (the initializer, where you define your layers) and forward (the inference code of your module, where you use your layers).
# That's all you need, since PyTorch will handle backward pass with Autograd. 


import torch
import torch.nn as nn


class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs):
        super(CNNBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.batchnorm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU(0.1)

    def forward(self, x):
        return self.leakyrelu(self.batchnorm(self.conv(x)))

class YoloV1(nn.Module):
    def __init__(self, split_size=7, num_boxes=2, num_classes=15):
        super(YoloV1, self).__init__()
        self.S = split_size
        self.B = num_boxes
        self.C = num_classes
        self.outputDim = self.B * 5 + self.C

        self.darknet = nn.Sequential(
            # Block 1
            CNNBlock(3, 64, kernel_size=7, stride=2, padding=3),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 2
            CNNBlock(64, 192, kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 3
            CNNBlock(192, 128, kernel_size=1),
            CNNBlock(128, 256, kernel_size=3, padding=1),
            CNNBlock(256, 256, kernel_size=1),
            CNNBlock(256, 512, kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 4
            CNNBlock(512, 256, kernel_size=1),
            CNNBlock(256, 512, kernel_size=3, padding=1),
            CNNBlock(512, 256, kernel_size=1),
            CNNBlock(256, 512, kernel_size=3, padding=1),
            CNNBlock(512, 256, kernel_size=1),
            CNNBlock(256, 512, kernel_size=3, padding=1),
            CNNBlock(512, 256, kernel_size=1),
            CNNBlock(256, 512, kernel_size=3, padding=1),
            CNNBlock(512, 512, kernel_size=1),
            CNNBlock(512, 1024, kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 5
            CNNBlock(1024, 512, kernel_size=1),
            CNNBlock(512, 1024, kernel_size=3, padding=1),
            CNNBlock(1024, 512, kernel_size=1),
            CNNBlock(512, 1024, kernel_size=3, padding=1),
            CNNBlock(1024, 1024, kernel_size=3, padding=1),
            CNNBlock(1024, 1024, kernel_size=3, stride=2, padding=1),

            CNNBlock(1024, 1024, kernel_size=3, padding=1),
            CNNBlock(1024, 1024, kernel_size=3, padding=1),
        )

        # fully conected 
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * self.S * self.S, 4096),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.5),
            nn.Linear(4096, self.S * self.S * self.outputDim) 
        )

    def forward(self, x):
        x = self.darknet(x)
        x = self.fcs(x)
        return x.reshape(-1, self.S, self.S, self.outputDim)

# import torch
# import torch.nn as nn
# import config

# class YoloV1(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.S = config.S  # 7
#         self.C = config.C
#         self.B = config.B
#         self.outputDim = self.B * 5 + self.C

#         def conv_block(in_c, out_c, kernel, stride, padding):
#             return nn.Sequential(
#                 nn.Conv2d(in_c, out_c, kernel, stride, padding, bias=False),
#                 nn.BatchNorm2d(out_c),
#                 nn.LeakyReLU(0.1)
#             )

#         self.features = nn.Sequential(
#             conv_block(3, 32, 3, 1, 1), 
#             nn.MaxPool2d(2, 2), 

#             conv_block(32, 64, 3, 1, 1),
#             nn.MaxPool2d(2, 2), 

#             conv_block(64, 128, 3, 1, 1),
#             conv_block(128, 128, 3, 1, 1),
#             nn.MaxPool2d(2, 2), 

#             conv_block(128, 256, 3, 1, 1),
#             conv_block(256, 256, 3, 1, 1),
#             nn.MaxPool2d(2, 2), 

#             conv_block(256, 512, 3, 1, 1),
#             conv_block(512, 512, 3, 1, 1),
#             nn.MaxPool2d(2, 2), 
            
#             conv_block(512, 1024, 3, stride=2, padding=1), 
#             conv_block(1024, 1024, 3, stride=1, padding=1),
#         )

#         self.fcs = nn.Sequential(
#             nn.Flatten(),
#             nn.Linear(1024 * 7 * 7, 4096), 
#             nn.LeakyReLU(0.1),
#             nn.Dropout(0.5),
#             nn.Linear(4096, self.S * self.S * self.outputDim),
#         )

#     def forward(self, x):
#         x = self.features(x)
#         x = self.fcs(x)
#         x = x.reshape(-1, self.S, self.S, self.outputDim)
#         return x
