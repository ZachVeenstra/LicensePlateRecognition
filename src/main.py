"""This file is unused."""

import torch
import torch.nn as nn
import numpy as np
import cv2
import matplotlib.pyplot as plt
from MTCNN import create_mtcnn_net
from LPRNet import LPRNet, small_basic_block, STNet, decode

# Load pre-trained models
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# MTCNN
image = cv2.imread('test/7.jpg')
input_image = np.copy(image)
bboxes = create_mtcnn_net(input_image, (50, 15), device, p_model_path='MTCNN/weights/pnet_Weights', o_model_path='MTCNN/weights/onet_Weights')

# STN
STN = STNet()
STN.to(device)
STN.load_state_dict(torch.load('LPRNet/weights/Final_STN_model.pth', map_location=lambda storage, loc: storage))
STN.eval()

bbox = bboxes[0, :4]
x1, y1, x2, y2 = [int(bbox[j]) for j in range(4)]
w = int(x2 - x1 + 1.0)
h = int(y2 - y1 + 1.0)
img_box = np.zeros((h, w, 3))
img_box = image[y1:y2+1, x1:x2+1, :]
im = cv2.resize(img_box, (94, 24), interpolation=cv2.INTER_CUBIC)
im = (np.transpose(np.float32(im), (2, 0, 1)) - 127.5) * 0.0078125
data = torch.from_numpy(im).float().unsqueeze(0).to(device)
transfer = STN(data)

# LPRNet
CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
         'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
         'Y', 'Z', 'I', 'O', '-'
]

lprnet = LPRNet(class_num=len(CHARS), dropout_rate=0)
lprnet.to(device)
lprnet.load_state_dict(torch.load('LPRNet/weights/Final_LPRNet_model.pth', map_location=lambda storage, loc: storage))
lprnet.eval()

# Inference
preds = lprnet(transfer)

# Decoding
preds = preds.cpu().detach().numpy()  # (1, 68, 18)
labels, pred_labels = decode(preds, CHARS)
print("label is", labels)
print("pred_labels is", pred_labels)

# Visualization
plt.imshow(input_image[:, :, ::-1])
plt.title(f'Predicted License Plate: {labels[0]}')
plt.show()