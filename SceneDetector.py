from skimage import measure
import numpy as np
import cv2 as cv
import os

current_path = os.path.dirname(os.path.abspath(__file__))
asset_path = current_path + "\\assets\\scenes\\"

class SceneDetector(object):
    """
    Given a frame 
    Determines the state of game !
    """
    def __init__(self):
        print "Hello"

    def load_image(self, path):
        """
        Given a path 
        Load Image to CVMAT
        """
        full_path = asset_path + path
        cvmat = cv.imread(full_path, cv.IMREAD_COLOR)
        cvmat = cv.cvtColor(cvmat, cv.COLOR_BGR2GRAY)
        return cvmat

    def detect_scene(self, frame):
        """
        Receive a frame 
        """
        # Load Image
        # text = "first_screen"
        text = "battle_home"
        first_screen = self.load_image(text+".png")
        first_screen = cv.resize(first_screen, (558/4, 991/4), interpolation = cv.INTER_CUBIC)
        # Prepare Incoming
        incoming_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Compare ! 
        result = self.compare(incoming_frame, first_screen)
        print result
        if result <= 800:
            return text

    def compare(self, imageA, imageB):
        result = self.compare_mse(imageA, imageB)
        # result = self.compare_ssim(imageA, imageB)
        return result 

    def compare_ssim(self, imageA, imageB):
        result = measure.compare_ssim(incoming_frame, first_screen)
        return result
    
    def compare_mse(self, imageA, imageB):
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err
