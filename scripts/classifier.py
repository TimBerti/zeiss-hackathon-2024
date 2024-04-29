import torch
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
from torchvision.transforms import v2
from transform_split import transform, split_image

torch_transform = v2.Compose([
    v2.Resize((224, 224)),
    v2.ToImage(),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

class Classifier:
    classes = {0: 'absent', 1: 'free', 2: 'occupied'}

    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.load(model_path)
        self.model.to(self.device)
        self.model.eval()

    def classify(self, img):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = self.adjust_lighting(img)
        img = transform(img)
        parts = split_image(img)
        classifications = []
        for part in parts:
            part = cv.resize(part, (240,240))
            part = torch_transform(part)
            part = part.unsqueeze(0).to(self.device)
            with torch.no_grad():
                output = self.model(part)
            label = torch.argmax(output).item()
            classifications.append(self.classes[label])
        return classifications
    
    def adjust_lighting(self, img, target_brightness=86.031, target_color=[98.981, 95.423, 62.651]):
        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        current_brightness = gray_image.mean()

        brightness_offset = target_brightness - current_brightness
        img = cv.add(img, np.array([brightness_offset]))

        average_color_per_row = np.average(img, axis=0)
        current_color = np.average(average_color_per_row, axis=0)

        color_diff = target_color - current_color

        adjusted_image = cv.add(img, np.array([color_diff]))
        return adjusted_image
    
if __name__ == '__main__':
    root_dir = '../images'
    img = cv.imread(root_dir + 'saved_pypylon_img_1714289587.png')
    classifier = Classifier('../models/ResNet18_pretrained-accuracy0.9226.pt')
    classifications = classifier.classify(img)
    for i in range(4):
        print(classifications[2*i], classifications[2*i+1])
