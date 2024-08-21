from pywinauto import Application
from telegram_core.img_detection import *
import time
import psutil
from loguru import logger
    

class WindowApp:
    x, y = 0, 0
    width, height = 800, 600
    delay = 0.2

    def __init__(self, exe_path):
        self.app = Application(backend="win32").start(exe_path)
        self.app.wait_cpu_usage_lower(threshold=5)

        self.main_window = self.app.top_window()

        self.main_window.move_window(x=self.x, y=self.y, width=self.width, height=self.height, repaint=True)


    def get_window_center_coords(self, window):
        rect = window.rectangle()
        x = rect.left
        y = rect.top
        width = rect.width()
        height = rect.height()

        x_center = int(x + width / 2)
        y_center = int(y + height / 2)

        return x_center, y_center


    def get_visible_windows(self):
        visible_windows = []
        for window in self.app.windows():
            if window.is_visible():
                visible_windows.append(window)
        return visible_windows
    

    def get_windows_except_main(self):
        windows = []
        for w in self.get_visible_windows():
            if w != self.main_window:
                windows.append(w)
        return windows
    

    def get_first_window_except_main(self, wait, ignore_windows_list = [], windows_pos=(0,0)):
        for i in range(wait*5):
            for w in self.get_visible_windows():
                if w != self.main_window and not w in ignore_windows_list:
                    w.move_window(*windows_pos)
                    return w
            time.sleep(0.2)


    def stop_all_windows_except_main(self):
        windows = self.get_windows_except_main()
        for w in windows:
            if w != self.main_window:
                w.close()


    
    @staticmethod
    def stop_processes(name):
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if name in process.info['name']:
                    p = psutil.Process(process.info['pid'])
                    p.terminate()
                    p.wait()
                    logger.warning(f"{name} process - PID {process.info['pid']} was stopped.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    
    @staticmethod
    def is_process_running(name):
        for process in psutil.process_iter(['name']):
            if process.info['name'] == name:
                return True
        return False
        

    @staticmethod
    def get_control_data(window):
        children = window.children()
        print()
        for control in children:
            control_text = control.window_text()
            control_rect = control.rectangle()
            control_width = control_rect.width()
            control_height = control_rect.height()
            control_class = control.class_name()
            print(f"Control text: {control_text}")
            print(f"Class name: {control_class}")
            print(f"Sizes: {control_width}x{control_height}")
            print()


    @staticmethod
    def print_window_info(window):
        window_title = window.window_text()
        window_class = window.class_name()
        window_rect = window.rectangle()
        window_position = (window_rect.left, window_rect.top)
        window_size = (window_rect.width(), window_rect.height())

        print(f"Title: {window_title}")
        print(f"Class: {window_class}")
        print(f"Pos: {window_position}")
        print(f"Sizes: {window_size}")

