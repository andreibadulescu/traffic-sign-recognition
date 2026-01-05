About our project
TODO

GitHub Link
https://github.com/andreibadulescu/traffic-sign-recognition

Used languages / technologies
The Windows application that controls the processing pipelines and the ML model is written in C# and XAML (where C# is used for program logic flow and XAML describes what and how elements should be shown on screen). It was built using methods and structures defined in the Windows and Windows APP SDKs, the latter including also the UI elements that form WinUI3. In order to enforce the ModelView-View Model design pattern, the MVVM Toolkit library maintained by the .NET community was used, which offers special attributes for various properties and classes that should be observable in order to dynamically update the graphical interface when any change occurs.

How to run and use the application
TODO

Team members and individual responsibilities
Karina Antoniu was tasked with creating the ML model and writing the training / inference logic. Andrei Bădulescu was responsible with writing the Windows application that functions over the ML model and the processing pipelines and offers an easy-to-learn, intuitive interface for users that do not have a technology-oriented background. Ștefan Mărășescu was responsible with obtaining the data necessary to train the ML model and create the processing pipelines that enable an easier interaction with the ML model.

Difficulties and fixes
A primary challenge encountered during the development phase was the precise tuning of hyperparameters. Achieving model stability required an iterative process of training validation. By consistently monitoring inference results on raw images, I was able to fine-tune these parameters to ensure optimal convergence and detection accuracy.
Initially, I attempted to implement the full YOLOv1 architecture. However, due to computational constraints and hardware limitations, the original model proved too resource-intensive for training. Consequently, I optimized the network by pruning specific layers and reducing filter dimensions to create a lightweight variant that ensures stable execution.

Developing the Windows Application
There were several problems identifying learning materials in order to understand how to make use of the SDKs, how the interaction between XAML and C# logic works and how to implement correctly a codebase that follows the MVVM design pattern. The documentation regarding UI elements is well-written, but the articles about the interaction with the MVVM toolkit is not beginner-friendly. Not only that, but there is not any demo or follow-through media that learns newcomers how to start developing apps using the Windows App SDK. However, there is a plug-in for Visual Studio that builds a template from which you can further expand, which offers some code examples. There is also a Windows application made by Microsoft that displays all UI elements (with code snippets included) in a catalogue.