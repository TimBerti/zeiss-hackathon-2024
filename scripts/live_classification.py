'''
Script for capturing video from a Basler camera and converting it to OpenCV-compatible images for processing.

This script is specifically designed to work with the Basler acA1300-200uc camera model and has been tested on a Nvidia Jetson Nano with the camera connected via USB.
It utilizes the Pypylon interface for camera operations and OpenCV for image processing.

Key Features:
- Continuously captures video frames from the Basler camera.
- Uses the Classifier class to analyze and classify the content of each captured frame into predefined categories such as 'occupied', 'absent', or 'free'.
- Applies color overlays (red, orange, and green) to the captured frames based on the classification results to visually denote the state of different segments of the image.
The image is divided into a 2x4 grid, and each segment is marked according to its classified state:
  - Red overlay for 'occupied'
  - Orange overlay for 'absent'
  - Green overlay for 'free'
- Sends the classification results to a remote web server using an HTTPS POST request, allowing for remote monitoring or further processing.
- Displays the processed images in real-time, providing a visual interface for immediate feedback.
'''

import cv2
import numpy as np
from pypylon import pylon
from classifier import Classifier
import requests

def classify_to_states(classification_results):
    """ Convert classification results to a dictionary of grid coordinates marking different states.
    The grid is 2x4 (rows x cols).
    Start at the top right, then bottom right, moving to the left in a zigzag.
    """
    states = {'occupied': [], 'absent': [], 'free': []}

    # Define custom index mapping
    conditions = {
        0: (0, 3),
        1: (1, 3),
        2: (0, 2),
        3: (1, 2),
        4: (0, 1),
        5: (1, 1),
        6: (0, 0),
        7: (1, 0)
    }

    for index, result in enumerate(classification_results):
        row, col = conditions[index]
        if "occupied" in result.lower():
            states['occupied'].append((row, col))
        elif "absent" in result.lower():
            states['absent'].append((row, col))
        elif "free" in result.lower():
            states['free'].append((row, col))

    return states

def apply_red_overlay(image, alpha=0.4):
    """ Apply a red color overlay to an image with a given alpha transparency. """
    color=(0, 0, 255) # BGR for red
    overlay = np.full(image.shape, color, dtype=np.uint8)
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def apply_green_overlay(image, alpha=0.4):
    """ Apply a green color overlay to an image with a given alpha transparency. """
    color = (0, 255, 0)  # BGR for green
    overlay = np.full(image.shape, color, dtype=np.uint8)
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def apply_orange_overlay(image, alpha=0.4):
    """ Apply an orange color overlay to an image with a given alpha transparency. """
    color = (0, 165, 255)  # BGR for orange
    overlay = np.full(image.shape, color, dtype=np.uint8)
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def split_and_mark(img, states):
    """ Split the image into parts and mark each one based on its state with different overlays. """
    rows, cols = 2, 4  # Grid size
    h, w = img.shape[:2]
    part_height, part_width = h // rows, w // cols

    # Apply overlays for each state
    for state, positions in states.items():
        for (r, c) in positions:
            y_start = r * part_height
            y_end = y_start + part_height
            x_start = c * part_width
            x_end = x_start + part_width
            part_img = img[y_start:y_end, x_start:x_end]
            if state == 'occupied':
                img[y_start:y_end, x_start:x_end] = apply_red_overlay(part_img)
            elif state == 'absent':
                img[y_start:y_end, x_start:x_end] = apply_orange_overlay(part_img)
            elif state == 'free':
                img[y_start:y_end, x_start:x_end] = apply_green_overlay(part_img)

    return img

if __name__ == '__main__':

    #Initialize classifier
    classifier = Classifier('../models/ResNet18_pretrained-accuracy0.9226.pt')

    # conect to camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    # Grab Continuous video with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()
    # convert to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img = image.GetArray()
            results = classifier.classify(img)  # Assume classify function exists

            # Send results to webserver
            print(results)
            try:
                response = requests.post('https://thomas-holder.de:1313/statusmask', json={"data": results})
                print("Response from server:", response.text)
            except Exception as e:
                print("Failed to send data to server:", e)


            states = classify_to_states(results)
            marked_img = split_and_mark(img, states)
            
            # Display captured and marked image
            cv2.namedWindow('Marked Image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Marked Image', 800, 600)
            cv2.imshow('Marked Image', marked_img)
            k = cv2.waitKey(1)
            if k == 27:  # ESC key to break the loop
                break

        grabResult.Release()

    camera.StopGrabbing()
    cv2.destroyAllWindows()

