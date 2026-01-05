# Traffic Sign Recognition Application

## About our project <br>
This project focuses on the end-to-end development of a custom object detection system designed for traffic scenarios. At the core of our solution is the YOLOv1 (You Only Look Once) architecture, which we implemented and built entirely from scratch without relying on pre-trained "black box" libraries. The model was trained on a custom dataset created by processing raw traffic video footage. We sliced the video into individual frames to build a dataset that challenges the model to recognize vehicles and traffic elements in real-time environments. To make the technology accessible, we integrated the training and inference scripts into a fully functional application. This wrapper allows users to easily interact with the model and visualize the detection results on new data.

## GitHub Link <br>
[Github Repository Link](https://github.com/andreibadulescu/traffic-sign-recognition)

## Used languages / technologies <br>
The Windows application that controls the processing pipelines and the ML model is written in C# and XAML (where C# is used for program logic flow and XAML describes what and how elements should be shown on screen). It was built using methods and structures defined in the Windows and Windows APP SDKs, the latter including also the UI elements that form WinUI3. In order to enforce the ModelView-View Model design pattern, the MVVM Toolkit library maintained by the .NET community was used, which offers special attributes for various properties and classes that should be observable in order to dynamically update the graphical interface when any change occurs.
<br> <br>
The implementation of this detection subsystem relies on Python as the primary language, utilizing the PyTorch framework for building and training the deep neural network. Essential libraries include NumPy for high-performance matrix operations and linear algebra, particularly for IoU calculations, and OpenCV for image pre-processing and visualization. Additionally, Torchvision is used for data augmentation, while Matplotlib handles the plotting of loss metrics to monitor training convergence.

## How to run and use the application <br>
TODO

## Team members and individual responsibilities <br>
Karina Antoniu was tasked with creating the ML model and writing the training / inference logic. Andrei Bădulescu was responsible with writing the Windows application that functions over the ML model and the processing pipelines and offers an easy-to-learn, intuitive interface for users that do not have a technology-oriented background. Ștefan Mărășescu was responsible with obtaining the data necessary to train the ML model and create the processing pipelines that enable an easier interaction with the ML model.

## Difficulties and Fixes <br>
### Building the YOLO model
A primary challenge encountered during the development phase was the precise tuning of hyperparameters. Achieving model stability required an iterative process of training validation. By consistently monitoring inference results on raw images, I was able to fine-tune these parameters to ensure optimal convergence and detection accuracy.
Initially, I attempted to implement the full YOLOv1 architecture. However, due to computational constraints and hardware limitations, the original model proved too resource-intensive for training. Consequently, I optimized the network by pruning specific layers and reducing filter dimensions to create a lightweight variant that ensures stable execution.

### Developing the Windows Application <br>
There were several problems identifying learning materials in order to understand how to make use of the SDKs, how the interaction between XAML and C# logic works and how to implement correctly a codebase that follows the MVVM design pattern. The documentation regarding UI elements is well-written, but the articles about the interaction with the MVVM toolkit is not beginner-friendly. Not only that, but there is not any demo or follow-through media that learns newcomers how to start developing apps using the Windows App SDK. However, there is a plug-in for Visual Studio that builds a template from which you can further expand, which offers some code examples. There is also a Windows application made by Microsoft that displays all UI elements (with code snippets included) in a catalogue.
<html>
<body>

<h1> <strong> YOLO for Traffic Sign Detection </strong> </h1>

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

<h1> <strong> Model Architecture </strong> </h1>

<p style="text-indent: 2em;">
    The network's architecture is divided into a "backbone" and a "head". The backbone consists of six sequential blocks primarily composed of Convolutional Layers and MaxPool Layers. The convolutional layers function as sophisticated feature extractors; each layer's kernel, or filter, is a small, learnable matrix trained to recognize a specific low-level pattern, such as a distinct edge, corner, or texture. As the kernel scans the input, it produces a feature map that indicates the locations and strength of these detected patterns. Following these layers, MaxPooling is applied to progressively downsample the spatial dimensions of the representation and to select only the maximum feature activation from a local vicinity. After this deep feature extraction, the final block (head) is responsible for interpreting these features and generating the final prediction. This transition begins as the 3D feature map is flattened into a 1D vector. This vector is then processed by fully-connected layers, which learn complex combinations of the extracted features. To enable the learning of non-linear relationships, a LeakyReLU activation is applied. A Dropout layer is also included as a regularization technique, active only during training, to mitigate overfitting by randomly deactivating neurons. Finally, a Sigmoid function is applied to the output tensor, scaling every value to a standardized range between 0 and 1.This error is down-weighted to mitigate the class imbalance caused by the preponderance of background cells in any given image.
</p>

<h1> <strong> Data Pipeline </strong> </h1>
<p style="text-indent: 2em;">
    This module is responsible for translating raw input images into structured tensors with a specific format requested by the neural network. The image undergoes essential pre-processing procedure such as resizing to the 448x448 dimensional space, followed by normalization and instantiation as a torch tensor. We then process the coresponding annotation file which outlines the ground truth for any present traffic sign. For each bounding box, we determine the responsible grid cell. This localization necessitates transforming the absolut coordinates into localized offsets which represent the object's center position relative to the cell's top left corner. We then create a tensor with theese coordinated and a one-hot encoding vector to specify the class of the object.
</p>

<h1> <strong> Loss Function </strong> </h1>
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

<h1> <strong> Training Script </strong> </h1>
<p style="text-indent: 2em;">
    Within the Training Script, all of the modules come together to achieve model convergence through iterative parameter refinement. Initially, we split the data set into a nested loop of epochs and batch iterations. For every batch processed we apply the 3 step cycle which defines the model: the inference, the loss calculations and the backward pass. The model predicts the positions of the objects, then computes the loss function to quantify the discrepancies between its response and the ground truth. With the backward pass (the learning step) calculates the gradients of the loss with respect to all the model parameters thereby determining the optimal direction for parameter adjustment. The Adam optimizer applies these gradients, refining the model's internal weights to minimize the calculated error in the next iteration. This module is responsible for model stability and that the performance metrics are logged, assuring convergence.
</p>

<h1> <strong> Non-Maximum Suppresion </strong> </h1>
<p style="text-indent: 2em;">
    This technique is used in object detection to remove the extra boxes that are detected around the same object. When an object is detected multiple times NMS comes in handy to keep the best one acording to a threshold and eliminates the rest. This helps us to make sure we only count the object once improving accuracy (reduce the number of false positives).

</p>

<h1> <strong> Accuracy Metrics & Performance </strong> </h1>
<p style="text-indent: 2em;">
    To evaluate the performance of the model, I will use Mean Average Precision (mAP) which serves as a rigorous and comprehensive metric that measures both the accuracy of object recognition and the precision of geometric localization. For every class, predictions are ordered by confidence and used to generate de precision-recall curve that captures performance across varying confidence thresholds. The average precision corresponds to the area under this curve for a single class which gives us the final metric: the mean of all values.
</p>

<h1> <strong> Technologies used </strong> </h1>
<p style="text-indent: 2em;">
    The implementation of this detection subsystem relies on Python as the primary language, utilizing the PyTorch framework for building and training the deep neural network. Essential libraries include NumPy for high-performance matrix operations and linear algebra, particularly for IoU calculations, and OpenCV for image pre-processing and visualization. Additionally, Torchvision is used for data augmentation, while Matplotlib handles the plotting of loss metrics to monitor training convergence.
</p>

<h1> <strong> Instructions </strong> </h1>
<p style="text-indent: 2em;">
    To operate this module, first ensure all dependencies are installed. The training phase can be initiated by executing the training script, which processes the dataset and optimizes the model parameters over a specified number of epochs. Once converged, the system saves the weights, which can then be loaded by the inference script to generate bounding box predictions and class labels for any input image or video frame provided by the main application. <br> To evaluate the model's inference capabilities, I implemented a prediction script that accepts a raw input image. The network localizes the objects and outputs their relative bounding box coordinates, which are subsequently visualized on the frame using OpenCV.
</p>

<h1> <strong> Implementation Challenges </strong> </h1>
<p style="text-indent: 2em;">
    A primary challenge encountered during the development phase was the precise tuning of hyperparameters. Achieving model stability required an iterative process of training validation. By consistently monitoring inference results on raw images, I was able to fine-tune these parameters to ensure optimal convergence and detection accuracy. <br> Initially, I attempted to implement the full YOLOv1 architecture. However, due to computational constraints and hardware limitations, the original model proved too resource-intensive for training. Consequently, I optimized the network by pruning specific layers and reducing filter dimensions to create a lightweight variant that ensures stable execution." 
</p>

</body>
</html>
