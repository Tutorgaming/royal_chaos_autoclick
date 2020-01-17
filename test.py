import threading 
import win32gui
import time

class WindowGui(threading.Thread):
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
        self.window_title = window_title
        self.is_focused = False
        self.is_running = True
        self.loop_rate = 10 # Hz

    def get_focus_status(self):
        foreground_window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return foreground_window_name == self.window_title

    def run(self):
        # Updating the status of the NoxPlayer Focusing !
        while self.is_running:
            self.is_focused = self.get_focus_status()
            time.sleep(float(1/self.loop_rate))
        print("WindowGui Thread has Ended !")
    
    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    WIN = WindowGui("NoxPlayer")
    WIN.start()
    try:
        while True:
            print "Win is Focused =", WIN.is_focused 
    except KeyboardInterrupt:
        print "Ctrl-c received! Sending kill to threads..."
        WIN.is_running = False