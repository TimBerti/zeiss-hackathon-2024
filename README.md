# Zeiss Hackathon 2024 - Team 13

Our Topic:

Desk seat occupancy monitoring with CeilNet: Find your spot, fast – discover available seats at your library.

## Table of Contents
1. [Problem](#problem)
2. [Our Solution](#our-solution)
   - [Idea](#idea)
   - [Technical Implementation Overview](#technical-implementation-overview)
   - [Dataset](#dataset)
   - [Training Process](#training-process)
   - [Hardware Design](#hardware-design)
   - [Web App](#web-app)
3. [Event Info](#event-info)

## Problem
- Never enough seats at the Bib
    - In the exam phase time is precious
- Technical problems:
    - Camera Position
    - Different seating arrangements
    - Light conditions
    - Data Privacy
    - Overlapping people and objects
    - Cost efficiency
    - User Experience

## Our Solution

### Idea:
Implement a system that monitors seating availability from above, classifying each spot as free, absent, or occupied. This information is then conveniently made accessible through a web application.

### Technical Implementation Overview:
- **Camera Monitoring**: A camera set up above the area to monitor the seats, connected to a Jetson Nano via USB.
- **Image Classification**: A ResNet-18 classifier runs on the Jetson Nano, which we have fine-tuned with our custom-recorded dataset.
- **Data Handling**: The image classification process occurs locally on the Jetson Nano. Only the classification results, indicating whether seats are free, absent, or occupied, are transmitted to the web app. This ensures user privacy is maintained.

With this approach, we aim to enhance user experience and manage seating capacity effectively, all while upholding data privacy standards.

![Solution Architecture](readme_images\solution.png "image showing the architecture of our solution")

### Dataset
To optimize our ResNet-18 classifier, we dedicated to create our own dataset tailored to the specific usecase. This dataset includes a collection of 1.120 images, capturing a table with eight seats under a multitude of scenarios, showcasing a diverse range of combinations where seats are either occupied, vacant, or marked as absent by leaving things on the table or a jacket on the chair. An exemplary sample of our sample can be seen below.

![Dataset Sample](readme_images\dataset_example.png "image showing an example of our own dataset")

### Training Process

The graphic below illustrates the training process we employed to develop our seating monitoring system:

1. The initial step involves recording the images. Following this, we apply a series of image transformations and split the images to isolate each seat into a separate data point.
2. Subsequently, each seat image undergoes a manual labeling process. During this phase, we categorize them into three distinct statuses: occupied, absent, and free.
3. With the dataset prepared and labeled, it then serves as the input for the fine-tuning of our ResNet-18 classifier. Through this fine-tuning process, we refine the classifier with our specific dataset, ultimately producing a set of new model weights.

![Training Process](readme_images\train_process.png "image showing our training process")

### Hardware Design
To seamlessly integrate the hardware components, such as the Jetson Nano and camera, into a single device, we designed our own casing utilizing 3D printing techniques. In the process we incorporated the flexibility to adjust the camera angle, allowing for optimal field-of-view adjustments to suit various monitoring environments. This customizable feature ensures our system can adapt to different seating arrangements and room layouts with ease.

![Custom Hardware Design](readme_images\hardware.png "image showing our devices hardware with custom 3d printed casing")

### Web App
Our web application presents a real-time overview of seating arrangements, providing updates on the occupancy status with clear indicators for seats that are occupied (red), absent (orange), or free (green). Below is a screenshot demonstrating the app's interface and functionality.

![Web App Screenshot](readme_images\web_app.png "image showing a screenshot of our web app")

Command to start the Web App:
```sh
flask --app webapp run
```

## Event Info

Reveal the Invisible -
ZEISS Computer Vision Hackathon

https://www.zeiss.com/corporate/en/about-zeiss/present/events/zeiss-hackathon.html
