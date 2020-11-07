import numpy as np
import argparse
from imutils import paths
import imutils
import pickle
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,
	help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

print("[INFO] loading the face detector model...")
protPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protPath, modelPath)

print("[INFO] loading face recognizer embedding model...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

print("[INFO] quantifying faces from dataset...")
imagePaths = list(paths.list_images(args["dataset"]))

known_embeddings = []
known_names = []

total = 0

for (i, imagePath) in enumerate(imagePaths):

	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	image = cv2.imread(imagePath)
	image = imutils.resize(image, width=600)
	(h, w) = image.shape[:2]

	image_blob = cv2.dnn.blobFromImage(
		cv2.resize(image, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)

detector.setInput(image_blob)
detections = detector.forward()

if len(detections) > 0:
		i = np.argmax(detections[0, 0, :, 2])
		confidence = detections[0, 0, i, 2]

		if confidence > args["confidence"]:
		
			bbox = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = bbox.astype("int")

			face = image[startY:endY, startX:endX]
			(faceHeight, faceWidth) = face.shape[:2]
			
			if faceWidth < 20 or faceHeight < 20:
				continue

            face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255,
            				(96, 96), (0, 0, 0), swapRB=True, crop=False)
            			embedder.setInput(face_blob)
            			vec = embedder.forward()

            known_names.append(name)
            			known_embeddings.append(vec.flatten())
            			total += 1

print("[INFO] serializing {} encodings...".format(total))
data = {"embeddings": known_embeddings, "names": known_names}
f = open(args["embeddings"], "wb")
f.write(pickle.dumps(data))
f.close()

