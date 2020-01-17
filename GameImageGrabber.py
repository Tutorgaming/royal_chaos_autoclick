import threading 
import win32gui
from PIL import ImageGrab
from utils.WindowGuiDetector import WindowGuiDetector
import cv2 as cv
import time
import numpy as np

class GameImageGrabber(object):
    """
    Class To Grab The Game Image From a window
    """
    def __init__(self):
        # Threads
        self.game_window_detector = WindowGuiDetector("NoxPlayer") # Is Window Focused ?
        self.grab_thread = None
        self.read_lock = threading.Lock() # Read Lock
        # Variables
        self.grabbed = None # Frame which already grabbed 
        self.running = False # Flag to Run or Stop 
        self.started = False # To Maintain only one starting operation 
        self.frame = None
        
        # Start Image Grabbing if Window is Detect !
        self.start()
    
    def start(self):
        # Check if the thread is started ?
        if self.started:
            print "Already Started !"
            return None
        # Start Window Detection Thread 
        self.game_window_detector.start()
        # Start the Grabbing Thread
        self.started = True
        self.grab_thread = threading.Thread(target=self.update, args=())
        self.grab_thread.start()
        return self

    def capture_game(self):
        """
        Capture Game by its Location !
        """
        (x, y), width, height = self.game_window_detector.get_window_detail()
        if width is 0 and height is 0:
            return None
        result = np.array(ImageGrab.grab(bbox=(x, y, x+width, y+height)))
        result = cv.cvtColor(result, cv.COLOR_BGR2RGB)
        return result
    
    def update(self):
        """
        Update the Grabber Tick !
        """
        while self.started:
            # Check if the detector is okay (size, title is match)
            if self.game_window_detector.is_okay():
                self.read_lock.acquire()
                frame = self.capture_game()
                # Lock First - To Update
                self.frame = frame
                # Update Complete - Release Lock
                self.read_lock.release()

        print "Game Image Grabber Thread is Ended !"
    
    def read(self) :
        if self.frame is not None:
            self.read_lock.acquire()
            frame = self.frame.copy()
            self.read_lock.release()
            return frame

    def stop(self) :
        # Stop Image Detection
        self.started = False
        if self.grab_thread.is_alive():
            self.grab_thread.join()
        # Stop Window Detection
        self.game_window_detector.is_running = False
 
if __name__ == "__main__":
    GRAB = GameImageGrabber()
    try:
        while True:
            frame = GRAB.read()
            if frame is None:
                continue
            else:
                height, width = frame.shape[:2]
                show = cv.resize(frame, (width/2, height/2), interpolation = cv.INTER_CUBIC)
                cv.imshow('Detection Result', show)
            if cv.waitKey(1) & 0xFF == ord('q') :
                GRAB.stop()
                break
    except KeyboardInterrupt:
        print "Ctrl-c received! Sending kill to threads..."
        GRAB.stop()

