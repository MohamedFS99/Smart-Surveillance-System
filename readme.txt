The project is to create a surveillance system using Raspberry Pi and motion sensors. When the motion sensor detects motion, the camera connected to the Raspberry Pi will take a picture of the object detected. If the picture taken by the camera does not match the database, the Raspberry Pi will send an SMS message to the property owner an intrusion alert.

The project is a further implementation of Adrian Rosebrock's face recognition and face alignment using OpenCV in Python.

#Requirements:
1) Raspberry Pi 4 or 3 (or any Raspberry Pi that has access to the internet and with a RAM at least 1 GB)
2) USB Webcam (The RPi camera module is more preferable)
3) At least 32 GB Micro SD card (OpenCV needs alot of space).
4) OpenCV 4 installed (if not installed, it can be installed by following this tutorial in https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/). Install using the long method.
5) PIR sensor
6) Vonage API account
7) Your own faces image datastores. More faces, better accuracy.

#Code Files:
1) extractEmdedding.py: The code is to detect then read the faces from the face image dataset using a face detector and embedder. Then store the detected faces using pickle.
2) faceAligner.py: The code imports the facial landmarks prediction model. Then initializes the face geometic variables that will align the faces using *faceAlignment.py*, and defines the aligning functions and parameters.
3) faceAlignment.py: The code is the implementation of the face aligner created in *faceAligner.py* which initializes the face detector, facial landmarks predictor, and face aligner. Next, loads the input image then reads and shows the image. Then detects the faces in the image; and detects and aligns the faces in the images using the face aligner. Finally, shows the original resized and aligned images.
4) faceRecognize.py: The code firstly loads the detector,  training model in *trainModel.py*, embedding model in *extractEmbedding*,  and the face recognizer. Then loads the images from the image datastore for face recognition. Recognizes the faces in the blobs, and then displays the names over the Region of Interest(RoI).
5) img.sh: The bash script used to take pictures for webcams using *fswebcam* library.
6) PIR.py: The code is for sending an SMS message to the registered mobile number in "Nexmo" SMS services after the detection of motion using the PIR Sensor.
7) trainModel.py: The code is for training the face recognizer by loading the pickled faces extracted by *extractEmbedding.py*, train the recognizer using Support Vector Machine (SVM), and finally store the face recognizer using pickle.

#Run Instructions (from command line/terminal):
1) extractEmbedding.py: python extractEmbedding.py --dataset dataset \
	--embeddings output/embeddings.pickle \
	--detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7

2) trainModel.py: python trainModel.py --embeddings output/embeddings.pickle \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle

3) faceRecognize.py: python faceRecognize.py --detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7 \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle \
	--image images/adrian.jpg

4) faceAlignment.py: python faceAlignment.py \
	--shape-predictor shape_predictor_68_face_landmarks.dat \
	--image images/example_01.jpg