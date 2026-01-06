# Traffic Sign Recognition Application

## About our project <br>
This project focuses on the end-to-end development of a custom object detection system designed for traffic scenarios. At the core of our solution is the YOLOv1 (You Only Look Once) architecture, which we implemented and built entirely from scratch without relying on pre-trained "black box" libraries. The model was trained on a custom dataset created by processing raw traffic video footage. We sliced the video into individual frames to build a dataset that challenges the model to recognize vehicles and traffic elements in real-time environments. To make the technology accessible, we integrated the training and inference scripts into a fully functional application. This wrapper allows users to easily interact with the model and visualize the detection results on new data.

## GitHub Link <br>
[Github Repository Link](https://github.com/andreibadulescu/traffic-sign-recognition)

## Used languages / technologies <br>
The Windows application that controls the processing pipelines and the ML model is written in C# and XAML (where C# is used for program logic flow and XAML describes what and how elements should be shown on screen). It was built using methods and structures defined in the Windows and Windows APP SDKs, the latter including also the UI elements that form WinUI3. In order to enforce the ModelView-View Model design pattern, the MVVM Toolkit library maintained by the .NET community was used, which offers special attributes for various properties and classes that should be observable in order to dynamically update the graphical interface when any change occurs.
<br> <br>
The implementation of this detection subsystem relies on Python as the primary language, utilizing the PyTorch framework for building and training the deep neural network. Essential libraries include NumPy for high-performance matrix operations and linear algebra, particularly for IoU calculations, and OpenCV for image pre-processing and visualization. Additionally, Torchvision is used for data augmentation, while Matplotlib handles the plotting of loss metrics to monitor training convergence.

# How to run the application <br>

To install the application, the user must either download the packaged executable from GitHub or install Visual Studio in order to compile the application, as well as install Python and the dependencies of the Python scripts by consulting the requirements.txt file. From that point, the user simply starts the app, either by starting it in Visual Studio or by launching the installed executable and uses the application in accordance with the indications given in-app and the guidelines and suggestions mentioned in this README. The user can also opt to directly interact with the pipelines or the ML model for rapidity and scalability.

# How to use the application <br>

This application supports **two main workflows**:

1. **Further training the ML model**
2. **Detecting traffic signs**

Both workflows rely on **strict file naming conventions and directory structures**. These must be respected for the application to function correctly.

---

## 1. Further Training the ML Model

This workflow allows you to extend or retrain the traffic sign detection model using your own data.

### 1.1 Input Data Preparation

You must provide a **directory path** containing any combination of:

#### Supported video formats

* `.mp4`
* `.avi`
* `.mov`

#### Supported image formats

* `.jpg`
* `.jpeg`
* `.png`

### 1.2 Video–CSV Naming Convention (Mandatory)

For **each video file**, the same directory **must also contain a CSV file with the same base name**.

#### Example

```
video1.mp4
video1.csv
```

or

```
highway_scene.avi
highway_scene.csv
```

#### CSV timestamp format

Each associated CSV file **must contain timestamps defining subclips** from which frames will be extracted.

**Format:**

```
start,end
HH:MM:SS,HH:MM:SS
```

**Example:**

```
start,end
00:01:10,00:01:25
00:02:40,00:03:00
```

Each row defines a time range in the video where traffic signs appear. Frames extracted from these ranges will be used for training.

### 1.3 Annotation Options

After frames are extracted, you must choose **one of the following annotation paths**.


#### Option A: You already have YOLO annotation files

If you already have YOLO-format annotations:

* Each image frame must have a corresponding `.txt` file
* The `.txt` file name **must exactly match** the image name
* Annotation format must follow YOLO convention:

```
<class_id> <center_x> <center_y> <width> <height>
```

The model will then be further trained with the provided dataset.

#### Option B: You have a single CSV and want to convert it to YOLO

If you **do not have YOLO `.txt` files**, but instead have bounding boxes stored in a CSV:

1. Choose a directory path containing a file named **exactly**:

   ```
   annotations.csv
   ```

2. The CSV **must use the following column format**:

   ```
   frame_id, x_min, y_min, x_max, y_max, class_label
   ```

   The app will then convert these csv annotations to YOLO format and model will then be further trained with the provided dataset.

---

## 2. Detecting Traffic Signs

This workflow runs the trained ML model on new data and produces visual outputs.

### 2.1 Input Data

You must choose a **directory path** containing videos and/or images.

#### Supported formats

**Videos**

* `.mp4`
* `.avi`
* `.mov`

**Images**

* `.jpg`
* `.jpeg`
* `.png`

All supported files found in the directory will be processed automatically.

### 2.2 Output Directory Selection

You must choose a **separate output directory path** where final results will be saved.

The application will generate:

#### Reconstructed videos

* Frames originating from videos are recombined into videos
* Output naming format:

  ```
  video_<id>.mp4
  ```

  where `<id>` is derived from the original video identifier

#### Output images

* Frames originating from standalone images are saved directly
* Original filenames are preserved
* These images are **not included in any video**, since they weren't originally extracted from a video

### 2.4 Final Output Summary

| Input Type      | Output                                           |
| --------------- | ------------------------------------------------ |
| Video           | Reconstructed `.mp4` with drawn boxes and labels |
| Image           | Annotated image saved directly                   |
| Multiple videos | One output video per input video                 |
| Mixed inputs    | Videos + images handled independently            |


## Team members and individual responsibilities <br>
Karina Antoniu was tasked with creating the ML model and writing the training / inference logic. Andrei Bădulescu was responsible with writing the Windows application that functions over the ML model and the processing pipelines and offers an easy-to-learn, intuitive interface for users that do not have a technology-oriented background. Ștefan Mărășescu was responsible with obtaining the data necessary to train the ML model and create the processing pipelines that enable an easier interaction with the ML model.

## Difficulties and Fixes <br>
### Building the YOLO model
A primary challenge encountered during the development phase was the precise tuning of hyperparameters. Achieving model stability required an iterative process of training validation. By consistently monitoring inference results on raw images, I was able to fine-tune these parameters to ensure optimal convergence and detection accuracy.
Initially, I attempted to implement the full YOLOv1 architecture. However, due to computational constraints and hardware limitations, the original model proved too resource-intensive for training. Consequently, I optimized the network by pruning specific layers and reducing filter dimensions to create a lightweight variant that ensures stable execution.

### Developing the Windows Application <br>
There were several problems identifying learning materials in order to understand how to make use of the SDKs, how the interaction between XAML and C# logic works and how to implement correctly a codebase that follows the MVVM design pattern. The documentation regarding UI elements is well-written, but the articles about the interaction with the MVVM toolkit is not beginner-friendly. Not only that, but there is not any demo or follow-through media that learns newcomers how to start developing apps using the Windows App SDK. However, there is a plug-in for Visual Studio that builds a template from which you can further expand, which offers some code examples. There is also a Windows application made by Microsoft that displays all UI elements (with code snippets included) in a catalogue.

### Developing the Traffic Sign Recognition Pipeline <br>

Implementing the full end-to-end pipeline posed several challenges. A major difficulty was understanding how the machine learning model itself operates, as the pipeline needed to interact directly with it and provide inputs in the exact format expected by the network. This required learning the model’s input conventions, annotation formats, preprocessing steps, and inference behavior, which was time-consuming and required repeated experimentation and validation. Additionally, adapting the pipeline scripts to align with the frontend’s requirements introduced further complexity. The pipeline outputs had to match specific naming conventions, resolutions, and directory structures expected by the frontend application, making tight coordination between backend processing and frontend integration necessary. Another issue was managing memory efficiently during video reconstruction, since trying to load all frames at once could quickly overwhelm the available RAM. To solve this, the code was restructured to process frames on-the-fly using generator-style functions, which allowed each frame to be loaded, processed, and discarded immediately.

# About the ML Model

<html>
<body>

<h2> <strong> YOLO for Traffic Sign Detection </strong> </h2>

<p style="text-indent: 2em;">
    This document provides a technical overview and implementation guide for the YOLOv1 detection subsystem, developed as my primary contribution to the Applied Informatics group project on traffic sign recognition.
</p>

<p style="text-indent: 2em;">
    The scope of this README is exclusively limited to the YOLO component, which functions as the core computer vision engine for our team's larger system. My responsibility encompassed the complete pipeline for this module:
    
<ul>
  <li> The adaptation and configuration of the YOLOv1 architecture. </li>
  <li> Model training and hyperparameter tuning. </li>
  <li> The final implementation script that provides an API for the main application. </li>
</ul>
</p>
    
<p style="text-indent: 2em;">
    This component's primary function is to ingest a video frame and output a vector of bounding box coordinates, class labels, and confidence scores for any detected traffic signs.
</p>

<p style="text-indent: 2em;">
    The subsequent sections provide a detailed delineation of each implemented module.
</p>

<h2> <strong> Model Architecture </strong> </h2>

<p style="text-indent: 2em;">
    The network's architecture is divided into a "backbone" and a "head". The backbone consists of six sequential blocks primarily composed of Convolutional Layers and MaxPool Layers. The convolutional layers function as sophisticated feature extractors; each layer's kernel, or filter, is a small, learnable matrix trained to recognize a specific low-level pattern, such as a distinct edge, corner, or texture. As the kernel scans the input, it produces a feature map that indicates the locations and strength of these detected patterns. Following these layers, MaxPooling is applied to progressively downsample the spatial dimensions of the representation and to select only the maximum feature activation from a local vicinity. After this deep feature extraction, the final block (head) is responsible for interpreting these features and generating the final prediction. This transition begins as the 3D feature map is flattened into a 1D vector. This vector is then processed by fully-connected layers, which learn complex combinations of the extracted features. To enable the learning of non-linear relationships, a LeakyReLU activation is applied. A Dropout layer is also included as a regularization technique, active only during training, to mitigate overfitting by randomly deactivating neurons. Finally, a Sigmoid function is applied to the output tensor, scaling every value to a standardized range between 0 and 1.This error is down-weighted to mitigate the class imbalance caused by the preponderance of background cells in any given image.
</p>

<h2> <strong> Data Pipeline </strong> </h2>
<p style="text-indent: 2em;">
    This module is responsible for translating raw input images into structured tensors with a specific format requested by the neural network. The image undergoes essential pre-processing procedure such as resizing to the 448x448 dimensional space, followed by normalization and instantiation as a torch tensor. We then process the coresponding annotation file which outlines the ground truth for any present traffic sign. For each bounding box, we determine the responsible grid cell. This localization necessitates transforming the absolut coordinates into localized offsets which represent the object's center position relative to the cell's top left corner. We then create a tensor with theese coordinated and a one-hot encoding vector to specify the class of the object.
</p>

<h2> <strong> Loss Function </strong> </h2>
<p style="text-indent: 2em;">
    The model's optimization is composed by 3 components: the Localization Error, the Confidence Error and the Categorical Cross Entropy. This function is a weighted summ of these 3 errors, with scaling factors to balance their relevance on the final gradient. 
</p>
<p style="text-indent: 2em;">
    Confidence Error:
        This error's main task is to distinguish object presence from background. For each grid cell, our model proposes 2 bounding boxes and computes the Intersection Over Union between each of this boxes and the ground truth. The prediction with the highest IoU score becomes the responsible box. The the loss is applied acordingly:
</p>
<p style="text-indent: 2em;">
<ul>
  <li> Object Presence Loss: </li>
<p>
    If the confidence score (IoU) is low for this box then we penalize it to force the model to produce better scores where the object is present.
</p>
  <li> No Object Loss: </li>
<p>
    If there is no object in the box the model is being penalized severely and the confidence scores are regressed towards zero. This error is down-weighted to mitigate the class imbalance caused by the preponderance of background cells in any given image.
</p>
</ul>
</p>
<p style="text-indent: 2em;">
    Localization Error:
        This error is applied only to the bounding box that is responsible for the object in the cell and quantifies the geometric inaccuracy. Basically, we measure how far away is the predicted box from the real box and we penalize the model for both wrongly guessed postion or dimension. I used SSE (Error of Sum Squares) and applied the root function over the weight and height to ensure this dimensional errors contribue more to the loss improving sensibility.
</p>
<p style="text-indent: 2em;">
    Cross Entropy Error:
        Evaluates the model's ability to correctly identify the class of the detected object and is computed only on the responsible boxes containing a ground truth object. The divergence between the probability distribution for the current box and the one hot encoding ground truth vector penalizing incorect class guesses and forces the model to better understand what it is "seeing".
</p>

<h2> <strong> Training Script </strong> </h2>
<p style="text-indent: 2em;">
    Within the Training Script, all of the modules come together to achieve model convergence through iterative parameter refinement. Initially, we split the data set into a nested loop of epochs and batch iterations. For every batch processed we apply the 3 step cycle which defines the model: the inference, the loss calculations and the backward pass. The model predicts the positions of the objects, then computes the loss function to quantify the discrepancies between its response and the ground truth. With the backward pass (the learning step) calculates the gradients of the loss with respect to all the model parameters thereby determining the optimal direction for parameter adjustment. The Adam optimizer applies these gradients, refining the model's internal weights to minimize the calculated error in the next iteration. This module is responsible for model stability and that the performance metrics are logged, assuring convergence.
</p>

<h2> <strong> Non-Maximum Suppresion </strong> </h2>
<p style="text-indent: 2em;">
    This technique is used in object detection to remove the extra boxes that are detected around the same object. When an object is detected multiple times NMS comes in handy to keep the best one acording to a threshold and eliminates the rest. This helps us to make sure we only count the object once improving accuracy (reduce the number of false positives).

</p>

<h2> <strong> Accuracy Metrics & Performance </strong> </h2>
<p style="text-indent: 2em;">
    To evaluate the performance of the model, I will use Mean Average Precision (mAP) which serves as a rigorous and comprehensive metric that measures both the accuracy of object recognition and the precision of geometric localization. For every class, predictions are ordered by confidence and used to generate de precision-recall curve that captures performance across varying confidence thresholds. The average precision corresponds to the area under this curve for a single class which gives us the final metric: the mean of all values.
</p>

<h2> <strong> Technologies used </strong> </h2>
<p style="text-indent: 2em;">
    The implementation of this detection subsystem relies on Python as the primary language, utilizing the PyTorch framework for building and training the deep neural network. Essential libraries include NumPy for high-performance matrix operations and linear algebra, particularly for IoU calculations, and OpenCV for image pre-processing and visualization. Additionally, Torchvision is used for data augmentation, while Matplotlib handles the plotting of loss metrics to monitor training convergence.
</p>

<h2> <strong> Instructions </strong> </h2>
<p style="text-indent: 2em;">
    To operate this module, first ensure all dependencies are installed. The training phase can be initiated by executing the training script, which processes the dataset and optimizes the model parameters over a specified number of epochs. Once converged, the system saves the weights, which can then be loaded by the inference script to generate bounding box predictions and class labels for any input image or video frame provided by the main application. <br> To evaluate the model's inference capabilities, I implemented a prediction script that accepts a raw input image. The network localizes the objects and outputs their relative bounding box coordinates, which are subsequently visualized on the frame using OpenCV.
</p>

<h2> <strong> Implementation Challenges </strong> </h2>
<p style="text-indent: 2em;">
    A primary challenge encountered during the development phase was the precise tuning of hyperparameters. Achieving model stability required an iterative process of training validation. By consistently monitoring inference results on raw images, I was able to fine-tune these parameters to ensure optimal convergence and detection accuracy. <br> Initially, I attempted to implement the full YOLOv1 architecture. However, due to computational constraints and hardware limitations, the original model proved too resource-intensive for training. Consequently, I optimized the network by pruning specific layers and reducing filter dimensions to create a lightweight variant that ensures stable execution." 
</p>

</body>
</html>

---

# About the Windows Application

## Sign Catalogue

This section of the app includes all traffic signs that are recognised by the model. Each individual entry has a name and a picture associated with it in order to allow easier identification and cross-matching between detection labels and signs. 

The traffic signs are saved within the application in a service as a static list of Sign items. The application also supports persistent storage, with the help of a JSON loader / saver service.

## Detect Section

In this section, the user shall provide the application a folder which contains footage that the ML model should process in order to identify traffic signs. After pressing the "Browse" button, the user is shown a system dialogue, which asks for a directory of the data entries.

If there are any errors, the execution stops and a specific error message is shown. Otherwise, a list with filenames and identified labels is shown. The user can then opt to start again the detection process with a different folder.

## Train Section

The user can choose to provide a folder with a video and a .csv file with the annotations in order to refine the model / add new signs that can be identified. If there are no errors, a success message will be shown on screen. Otherwise, an error message that states the specific problem with the script or with the input data will be shown.

## Home Section

This section is the default section of the app, it is visible on start-up and its purpose is to explain to the user in a succint format available operations that can be carried out using the app.

## Design Patterns and Resources Catalog

The Windows Application follows all of the Design Guidelines imposed by the ModelView - View Model pattern. Every view has a view model associated with it, which is responsible for data fetching, asynchronous calls towards services and interface updates.

All of the static strings are localized with the help of a string resources catalog, which eases identification of various messages, titles and other text snippets.

---

# About the Data and Inference Pipelines

## Dataset Preparation Pipeline

### `video_cutter.py`

This script is responsible for segmenting long dashcam recordings into shorter video clips suitable for dataset creation and annotation. The primary motivation for this step is to improve manageability and efficiency when working with raw video data, as well as to isolate relevant temporal segments containing traffic signs.

The input videos were collected from personal dashcam recordings, providing realistic driving scenarios for training and evaluation.

### `dataset_preparator.py`

The dataset preparation script manages the transformation of raw video data into a structured dataset suitable for annotation and training. It enforces consistent directory layouts and naming conventions, which are critical for downstream compatibility with annotation tools, training scripts, and inference pipelines.

This script ensures that extracted frames are organized deterministically, reducing the likelihood of errors caused by mismatched filenames or directory structures.

## Manual Annotation with Label Studio

To generate ground truth annotations, the extracted frames were manually labeled using **Label Studio**. Frames produced by the dataset preparation pipeline were imported into the tool and annotated with bounding boxes corresponding to traffic signs.

Annotations were exported in **YOLO format**, ensuring direct compatibility with the training pipeline. Particular attention was given to label configuration, coordinate normalization, and class indexing, as these aspects must strictly align with the model’s expected input format.

The resulting annotated dataset was used to train and validate the YOLO model developed in the machine learning subsystem.

## Inference Pipeline

### `frame_extractor.py`

This script serves as the entry point for the inference pipeline. It processes directories containing a mixture of videos and standalone images, extracting frames at a fixed target frame rate and resizing them to a standardized resolution.

Frames originating from videos are grouped using deterministic filename prefixes, preserving temporal ordering and enabling later reconstruction into full video sequences. This approach allows batch processing while maintaining clear separation between different input sources.

### `run_inference.py`

The inference script interfaces directly with the YOLO model. It loads preprocessed frames, converts them into the tensor format required by the network, and executes forward passes to obtain detection outputs.

These outputs include bounding box coordinates, class predictions, and confidence scores, which are then serialized for use in downstream post-processing steps. The script acts as a strict intermediary between raw image data and structured detection results.

### `reconstruct_video.py`

The final stage of the pipeline reconstructs annotated videos from inference results. To avoid excessive memory usage, frames are loaded and processed on demand using a generator-style approach rather than being stored entirely in memory.

Each frame is optionally upscaled to Full HD resolution before being encoded into an H.264 video file. Standalone images that are not part of a video sequence are copied directly to the output directory, allowing the pipeline to support both image-based and video-based inference seamlessly.

## Pipeline Integration and Design Considerations

A central challenge during development was ensuring consistent interoperability between all pipeline stages. This required strict standardization of file formats, naming conventions, and directory structures so that outputs from one stage could be reliably consumed by the next.

Additionally, close coordination with the machine learning subsystem was necessary to correctly format model inputs and interpret outputs. The final result is a modular yet cohesive pipeline that supports dataset creation, manual annotation, automated inference, and video reconstruction in a reproducible and scalable manner.

