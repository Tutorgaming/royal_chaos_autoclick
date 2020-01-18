import threading 
import win32gui
import time

class WindowGuiDetector(threading.Thread):
    """ 
    A Thread Class To Look for Game Window
    and Report that the game window is ready or not
    """
    # Constructor
    def __init__(self, window_title):
        # Super 
        threading.Thread.__init__(self)
        # Variables
        self.daemon = True
        self.hwnd = None
        self.window_title = window_title
        self.is_focused = False
        self.is_running = True
        self.width = self.height = 0
        self.pos = (0 , 0)
        self.loop_rate = 10 # Hz

    def get_focus_status(self):
        foreground_window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return foreground_window_name == self.window_title
    
    def get_window_detail(self):
        if self.hwnd:
            rect = win32gui.GetWindowRect(self.hwnd)
            x = rect[0]
            y = rect[1] + 29
            w = rect[2] - x
            h = rect[3] - y
            return (x, y), w , h
        return (0,0), 0 ,0

    def is_okay(self):
        if not self.is_focused:
            return False
        return self.pos[0] >= 0 and self.pos[1] >=0 #  and self.width == 558 and self.height == 1020

    def run(self):
        # Updating the status of the NoxPlayer Focusing !
        while True:
            self.is_focused = self.get_focus_status()
            if self.is_focused:
                try:
                    self.hwnd = win32gui.FindWindow(None, self.window_title)
                    self.pos, self.width , self.height = self.get_window_detail()
                    # print self.pos, self.width, self.height
                except Exception:
                    print "hwnd ?"
                    continue
            if self.is_running is False:
                break
            # Delayed 
            time.sleep(float(1/self.loop_rate))
        print("WindowGui Thread has Ended !")

