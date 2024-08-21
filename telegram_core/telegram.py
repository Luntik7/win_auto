from pywinauto import Application
from pywinauto import mouse
from pywinauto.keyboard import send_keys
from telegram_core.img_detection import *
import time
from random_word import RandomWords
import pyperclip
import psutil
from loguru import logger
from telegram_core.base_app import WindowApp


class TelegramApp(WindowApp):
    def __init__(self, exe_path, wait_network_loading=True, time_to_wait=60):
        super().__init__(exe_path)
        
        if wait_network_loading:
            time.sleep(0.5)
            if not wait_while_img_dissapear(self.main_window, 'telegram_core\\templates\\network_loading.png', 0.25, time_to_wait*4, 0.95):
                raise Exception(f'Telegram not loaded in {time_to_wait} sec')
            logger.info('Telegram loaded successfully!')


    
    def scroll_to_click(self, dist, window, template_path, delay, tries_count, threshold, click=True, return_random=False, roi=None, show_rect=False, return_rect=False):
        window.set_focus()
        time.sleep(0.1)
        x, y = self.get_window_center_coords(window)

        time.sleep(0.2)
        mouse.move(coords=(x, y))
        time.sleep(0.2)

        for i in range(dist):
            if i % 5 == 0:
                if click:
                    if click_on_img(window, template_path, delay, tries_count, threshold, return_random=return_random, roi=roi, show_rect=show_rect):
                        return True
                else:
                    coords = get_img_coords(window, template_path, delay, tries_count, threshold,return_random=return_random, roi=roi, show_rect=show_rect, return_rect=return_rect)
                    if coords:
                        return coords
            send_keys('{DOWN}')
            time.sleep(0.01)
        return False


    def key_cycle(self, window, key, count, delay):
        window.set_focus()
        for i in range(count):
            send_keys(key)
            time.sleep(delay)


    def turn_on_webview_inspecting(self):
        click_on_img(self.main_window, 'telegram_core\\templates\\burger_menu.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'telegram_core\\templates\\settings.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'telegram_core\\templates\\advanced.png', 0.5, 5, 0.9)

        self.scroll_to_click(60, self.main_window, 'telegram_core\\templates\\exp_settings.png', 0, 1, 0.9)

        if self.scroll_to_click(50, self.main_window, 'telegram_core\\templates\\inspection.png', 0, 1, 0.9, click=False):
            if click_on_img(self.main_window, 'telegram_core\\templates\\inspection_off.png', 0.5, 5, 0.9):
                logger.info('Webview inspecction ON!')
            elif get_img_coords(self.main_window, 'telegram_core\\templates\\inspection_on.png', 0.5, 5, 0.9):
                logger.info('Webview inspecction already ON!')
            else:
                logger.info('Inspection not found!')

        self.key_cycle(self.main_window, '{ESC}', 4, 0.05)


    def enter_new_text(self, nickname, delay=0.2):
        time.sleep(delay)
        send_keys("^a")
        time.sleep(delay)
        send_keys("{BACKSPACE}")
        time.sleep(delay)
        send_keys(nickname)


    def open_username_settings(self):
        click_on_img(self.main_window, 'telegram_core\\templates\\burger_menu.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'telegram_core\\templates\\settings.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'telegram_core\\templates\\my_account.png', 0.5, 5, 0.9)
        click_on_img(self.main_window, 'telegram_core\\templates\\change_username.png', 0.5, 5, 0.9)

    
    def open_name_settings(self):
        click_on_img(self.main_window, 'telegram_core\\templates\\burger_menu.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'telegram_core\\templates\\settings.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'telegram_core\\templates\\my_account.png', 0.5, 5, 0.9)
        click_on_img(self.main_window, 'telegram_core\\templates\\change_name.png', 0.5, 5, 0.9)


    def set_nickname(self, nickname, delay=0.2, change_if_already_set=False):
        self.open_username_settings()

        if not change_if_already_set and not get_img_coords(self.main_window, 'telegram_core\\templates\\empty_username.png', 0.5, 5, 0.9):
            logger.info('Username already setted!')
            self.key_cycle(self.main_window, '{ESC}', 4, 0.05)
            return True

        self.enter_new_text(nickname, delay)
        time.sleep(delay * 3)

        if get_img_coords(self.main_window, 'telegram_core\\templates\\username_available.png', 0.5, 10, 0.9):
            if click_on_img(self.main_window, 'telegram_core\\templates\\save.png', 0.5, 5, 0.8):
                logger.info('Username successfully setted!')
                self.key_cycle(self.main_window, '{ESC}', 4, 0.05)
                return True
        
        raise Exception('Username do not setted!')
    

    def launch_app(self, launch_path, allow_msg_path, ok_path, link, app_name='App', message_load_timeout=60, message_resend_timeout=10, app_load_timeout=80, app_restart_timeout=20, window_pos=None):
        self.stop_all_windows_except_main()

        roi_rect = (660, 370, 770, 525)

        for i in range(int(message_load_timeout/message_resend_timeout)):
            self.write_to_saved_messages(link)
            if get_img_coords(self.main_window, launch_path, self.delay, int(message_resend_timeout/self.delay), 0.9, roi=roi_rect):
                break

        for i in range(int(app_load_timeout/app_restart_timeout)):
            click_on_img(self.main_window, launch_path, self.delay, 20, 0.9, roi=roi_rect)
            if click_on_img(self.main_window, allow_msg_path, self.delay, 5, 0.9):
                click_on_img(self.main_window, ok_path, self.delay, 10, 0.8)

            new_window = self.get_first_window_except_main(app_restart_timeout)
            if new_window:
                if window_pos:
                    new_window.move_window(*window_pos)
                logger.info(f'{app_name} window successfully launched!')
                return new_window

        raise Exception(f'{app_name} window do not launched.')
    

    def open_dev_tools(self, app, focus_control_path, app_name='App', wait=30):
        if app is None:
            raise Exception(f'{app_name} window not found!')

        if not click_on_img(app, focus_control_path, 0.2, wait*5, 0.9):
            raise Exception('Focus control not found!')
        time.sleep(0.3)
        send_keys("{F12}")
        time.sleep(0.2)
    

    def write_to_saved_messages(self, message, delay=0.2):
        time.sleep(delay)
        self.main_window.set_focus()
        send_keys('^0')
        pyperclip.copy(message)
        time.sleep(delay)
        self.main_window.set_focus()
        send_keys('^v')
        time.sleep(delay)
        self.main_window.set_focus()
        send_keys("{ENTER}")


    def quit_telegram(self, quit_delay=0.5):
        process_id = self.main_window.process_id()
        process = psutil.Process(process_id)
        process.terminate()
        logger.info("Telegram closed")
        time.sleep(0.5)


    @staticmethod
    def get_random_word_with_length( min_length, max_length):
        r = RandomWords()
        while True:
            word = r.get_random_word()
            if min_length <= len(word) <= max_length:
                return word


    @staticmethod
    def get_nickname():
        word1 = TelegramApp.get_random_word_with_length(3,5)
        word2 = TelegramApp.get_random_word_with_length(3,5)
        nickname = f"{word1}{word2}"
        return nickname

    
    @staticmethod
    def stop_telegram_processes():
        TelegramApp.stop_processes('Telegram')

    
    @staticmethod
    def is_proxifier_running():
        return TelegramApp.is_process_running('Proxifier.exe')
    

    @staticmethod
    def get_account_number_from_path(path):
        try:
            formatted_str = path[path.index('all_telegrams')+14:].strip()
            end_str = formatted_str[:formatted_str.index("\\")]
            return int(end_str)
        except:
            return None
        
        