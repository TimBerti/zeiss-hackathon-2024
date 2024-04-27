import numpy as np
import cv2 as cv
import os

PTS = np.float32([[500,250],[1546,250],[0,2040],[2046,2040]])

def transform(img, size=(2000,2000)):
    img = np.rot90(img, 1)
    corner_pts = np.float32([[0,0], [size[0],0], [0,size[1]], [size[0],size[1]]])
    M = cv.getPerspectiveTransform(PTS,corner_pts)
    return cv.warpPerspective(img, M, size)

def split_image(img):
    h, w, _ = img.shape
    h = h // 4
    w = w // 2
    parts = []
    for i in range(4):
        for j in range(2):
            part = img[i*h:(i+1)*h, j*w:(j+1)*w]
            parts.append(part)
    return parts

def process_image(img, path='.', filename='img'):
    img = transform(img)
    parts = split_image(img)
    for i, part in enumerate(parts):
        part = cv.resize(part, (240,240))
        cv.imwrite(os.path.join(path, f'{filename}_place{i}.png'), part)

def process_folder(folder_path, output_path):
    for file in os.listdir(folder_path):
        if file.endswith('.png'):
            img = cv.imread(os.path.join(folder_path, file))
            process_image(img, output_path, file.split('.')[0])
