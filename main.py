"""
ROYAL CHAOS AUTO PLAYER :)
Author : c3mx 
For Educational Purpose only , not for sale :)
"""
###################################################
# Imports
###################################################
from GameImageGrabber import GameImageGrabber
from SceneDetector import SceneDetector
import cv2 as cv
###################################################
# Class
###################################################
class RoyalChaosBot(object):
    """
    Main Application of the bot 
    """
    def __init__(self):
        print "INITIALIZED !"
        self.game_image_grabber = GameImageGrabber()
        self.scene_detector = SceneDetector()
        self.is_running = True
    
    def scale_frame(self, frame, scale=1):
        """
        Given the frame , return the scaled version of the frame
        """
        height, width = frame.shape[:2]
        result = cv.resize(frame, (width/2, height/2), interpolation = cv.INTER_CUBIC)
        return result

    def create_preview(self, frame, scene_text):
        """
        Create Preview Mat
        """
        new_mat = frame.copy()
        # font 
        font = cv.FONT_HERSHEY_SIMPLEX 
        # org 
        org = (0, 50) 
        # fontScale 
        fontScale = 1
        # Blue color in BGR 
        color = (255, 255, 255) 
        # Line thickness of 2 px 
        thickness = 2
        # Using cv2.putText() method 
        new_mat = cv.putText(new_mat, scene_text, org, font,  
                        fontScale, color, thickness, cv.LINE_AA) 
        return new_mat

    def start(self):
        """
        Start the Whole Process
        """
        try:
            while self.is_running:
                # Grabber is working 
                frame_full = self.game_image_grabber.read()
                if frame_full is None:
                    continue
                # Scaler
                frame_half = self.scale_frame(frame_full, 2)
                frame_quater = self.scale_frame(frame_half, 2)
                # Scene Detection
                scene_text = self.scene_detector.detect_scene(frame_quater)
                # State Machine (Receive State , Button)
                # self.state_machine.tick(scene_text, button, player_profile)
                # Show
                preview = self.create_preview(frame_half, scene_text)
                cv.imshow('BOT_VIEW', preview)
                # End Condition
                if cv.waitKey(1) & 0xFF == ord('q') :
                    self.is_running = False
                    break
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            self.is_running = False
            self.game_image_grabber.stop()            

        self.game_image_grabber.stop()  
        print "BOT IS END !"
    
    def stop(self):
        """
        Stop and Cleanup
        """
        self.is_running = False

###################################################
# Main
###################################################
if __name__ == "__main__":
    BOT_INSTANCE = RoyalChaosBot()
    try:
        BOT_INSTANCE.start()
    except KeyboardInterrupt:
        print "Ctrl-c received! Sending kill to threads..."
        BOT_INSTANCE.stop()
    

