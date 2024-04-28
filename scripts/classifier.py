import torch
import cv2 as cv
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

    def __init__(self, model_path, root_dir):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.load(model_path)
        self.model.to(self.device)
        self.model.eval()
        self.root_dir = root_dir

    def classify(self, filename):
        img = cv.imread(os.path.join(self.root_dir, filename))
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
    
if __name__ == '__main__':
    classifier = Classifier('../models/ResNet18_pretrained-accuracy0.9226.pt', '../data/raw_data/')
    classifications = classifier.classify('saved_pypylon_img_1714253425.png')
    for i in range(4):
        print(classifications[2*i], classifications[2*i+1])
