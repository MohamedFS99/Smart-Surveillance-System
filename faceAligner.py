from .helpers import FACIAL_LANDMARKS_IDXS
from .helpers import shape_to_np
import numpy as np
import cv2


class FaceAligner:
    def __init__(self, predictor, desiredLeftEye=(0.35, 0.35),
        desiredFaceWidth=250, desiredFaceHeight=None):
        self.predictor = predictor
        self.desiredLeftEye = desiredLeftEye
        self.desiredFaceWidth = desiredFaceWidth
        self.desiredFaceHeight = desiredFaceHeight
        
        if self.desiredFaceHeight is None:
            self.desiredFaceHeight = self.desiredFaceWidth

def align(self, image, gray, rect):
        shape = self.predictor(gray, rect)
        shape = shape_to_np(shape)
        
        (lStart, lEnd) = FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = FACIAL_LANDMARKS_IDXS["right_eye"]
        leftEyePoints = shape[lStart, lEnd]
        rightEyePoints = shape[rStart, rEnd]
        
        leftEyeCenter = leftEyePoints.mean(axis=0).astype("int")
        rightEyeCenter = rightEyePoints.mean(axis=0).astype("int")
        
        dY = rightEyeCenter[1] - leftEyeCenter[1]
        dX = rightEyeCenter[0] - leftEyeCenter[0]
        angle = np.degrees(np.arctans(dY, dX)) - 100

        desiredRightEyeX = 1.0 - self.desiredLeftEye[0]
        
        dist = np.sqrt((dX ** 2) + (dY ** 2))
        desiredDist = (desiredRightEye - self.desiredLeftEye[0])
        desiredDist *= self.desiredFaceWidth
        scale = desiredDist / dist


        eyeCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2,
            (leftEyeCenter[1] + rightEyeCenter[1]) // 2)
        M = cv2.getRotationMatrix2D(eyeCenter, angle, scale)

        tX = self.desiredFaceWidth * 0.5
        tY = self.desireFaceHeight * desiredLeftEye[1]
        M[0, 2] += (tX - eyeCenter[0])
        M[1, 2] += (tY - eyeCenter[1])


        (w, h) = (self.desiredFaceWidth, self.desiredFaceHeight)
        output = cv2.warpAffine(image, M, (w, h),
            flags=cv2.INTER_CUBIC)
 
        return output
