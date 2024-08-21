from pyautogui import click
from telegram_core.telegram import TelegramApp
import time
from telegram_core.img_detection import *
from loguru import logger
from pywinauto.keyboard import send_keys
from pywinauto import mouse
import pyperclip


class TelegramDogs(TelegramApp):
    def __init__(self, exe_path):
        super().__init__(exe_path)
        self.dogs_window = None


    def set_random_nicknames(self, tries_count=5, delay=0.2):
        for i in range(tries_count):
            if self.set_nickname(TelegramDogs.get_nickname(),delay):
                break

    
    def launch_dogs(self, link, sleep_before_launch=3, tries_count=30, window_pos=None):
        self.dogs_window = self.launch_app(
            '_dogs\\templates\\launch.png',
            '_dogs\\templates\\allow_msg.png',
            '_dogs\\templates\\OK.png',
            link,
            'Blum',
            window_pos=window_pos
        )
    

    def work_with_dogs(self):
        account_status = find_first_image([
            [self.dogs_window, '_dogs\\templates\\start_dogs.png', 0.2, 1, 0.8],
            [self.dogs_window, '_dogs\\templates\\daily_reward.png', 0.2, 1, 0.65],
            [self.dogs_window, '_dogs\\templates\\main_page.png', 0.2, 1, 0.75],
        ], 200)

        if 'start_dogs' in account_status:
            click_on_img(self.dogs_window, '_dogs\\templates\\start_dogs.png', 0.5, 60, 0.9)
            time.sleep(8)
            click_on_img(self.dogs_window, '_dogs\\templates\\continue_blue.png', 0.5, 40, 0.9)
            click_on_img(self.dogs_window, '_dogs\\templates\\continue_white.png', 0.5, 40, 0.9)
            if not click_on_img(self.dogs_window, '_dogs\\templates\\continue_white.png', 0.5, 40, 0.9):
                raise Exception('Last button on Dogs registration not found!')
            logger.info('Dogs account created and claimed!')
        elif 'daily_reward' in account_status:
            logger.info('Dogs daily reward claimed!')
            time.sleep(6)
        elif 'main_page' in account_status:
            logger.info('Dogs already claimed!')
        else:
            raise Exception("Account status not defined.")
        

    def add_bone_in_name(self):
        self.open_name_settings()
        time.sleep(0.2)
        send_keys("{END}")
        pyperclip.copy("🦴")
        time.sleep(0.2)
        send_keys("^v")
        time.sleep(0.2)
        click_on_img(self.main_window, 'telegram_core\\templates\\save.png', 0.5, 5, 0.8)
        time.sleep(1)
        self.key_cycle(self.main_window, '{ESC}', 4, 0.05)
        logger.info('Bone added to name!')
