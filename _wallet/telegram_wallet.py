from telegram_core.telegram import TelegramApp
from telegram_core.img_detection import *
from loguru import logger
import pyperclip
from pywinauto.keyboard import send_keys
import pyautogui
from config import TON_COUNT, TON_SEND


class TelegramWallet(TelegramApp):
    def __init__(self, exe_path):
        super().__init__(exe_path)
        self.wallet_window = None


    def launch_wallet(self, link, tries_count=30, window_pos=None):
        self.wallet_window = self.launch_app(
            '_wallet\\templates\\launch.png',
            '_wallet\\templates\\allow_msg.png',
            '_wallet\\templates\\OK.png',
            link,
            'Wallet',
            window_pos=window_pos
        )


    def work_with_wallet(self, phrase=None):
        time.sleep(0.4)
        self.start_wallet()        
        self.check_ton_space()

        click_on_img(self.wallet_window, '_wallet\\templates\\ton_space_main.png', 0.2, 20, 0.9)

        self.manual_add_wallet_phrase(phrase)


    def start_wallet(self):
        res = find_first_image(
            [
                [self.wallet_window, '_wallet\\templates\\start_wallet.png', 0.2, 1, 0.8],
                [self.wallet_window, '_wallet\\templates\\main_page.png', 0.2, 1, 0.8],
            ]
        )
        if 'start_wallet' in res:
           click_on_img(self.wallet_window, '_wallet\\templates\\start_wallet.png', 0.2, 25, 0.8)
        elif 'main_page' in res:
           logger.info("Wallet already register")
        else:
            raise Exception("Wallet start not found.")
        

    def manual_send(self, receive_address, counter):
        click_on_img(self.wallet_window, '_wallet\\templates\\ton_space_main.png', 0.2, 40, 0.9)
        time.sleep(1)
        if not wait_while_img_dissapear(self.wallet_window, '_wallet\\templates\\zero.png', 0.2, 80, 0.9,):
            raise Exception('Zero balance')
        click_on_img(self.wallet_window, '_wallet\\templates\\ton_send.png', 0.2, 40, 0.9)
        if not click_on_img(self.wallet_window, '_wallet\\templates\\ton_send_2.png', 0.2, 40, 0.9):
            raise Exception('Send not loaded')
        pyperclip.copy(receive_address)
        time.sleep(0.5)
        send_keys('^v')
        print(receive_address)
        click_on_img(self.wallet_window, '_wallet\\templates\\continue.png', 0.2, 60, 0.9)
        time.sleep(0.5)
        current_count = round(TON_COUNT - (counter + 1) * TON_SEND + random.uniform(0.000, 0.015), 4)
        send_keys(str(current_count))
        click_on_img(self.wallet_window, '_wallet\\templates\\continue.png', 0.2, 60, 0.9)
        time.sleep(2)
        if not click_on_img(self.wallet_window, '_wallet\\templates\\confirm_send.png', 0.2, 60, 0.9):
            raise Exception('Confirm Send not loaded')
        time.sleep(0.5)
        click_on_img(self.wallet_window, '_wallet\\templates\\ready.png', 0.2, 60, 0.9)


    def collect_adresses(self, adresses_path):
        click_on_img(self.wallet_window, '_wallet\\templates\\ton_space_main.png', 0.2, 40, 0.9)
        pyautogui.moveTo(200, 220)
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.3)
        clipboard_data = pyperclip.paste()
        with open(adresses_path, 'a', encoding='utf-8') as fileobj:
            fileobj.write(clipboard_data+'\n')
        print(clipboard_data)


    def check_ton_space(self):
        get_img_coords(self.wallet_window, '_wallet\\templates\\main_page.png', 0.2, 20, 0.9)
        if get_img_coords(self.wallet_window, '_wallet\\templates\\ton_space_main.png', 0.2, 3, 0.9):
            logger.info("Ton Space already ON(main page)")
            return True
        
        click_on_img(self.wallet_window, '_wallet\\templates\\wallet_settings.png', 0.2, 20, 0.8)
        click_on_img(self.wallet_window, '_wallet\\templates\\wallet_settings2.png', 0.2, 20, 0.9)
        
        beta_wallet = find_first_image(
           [
              [self.wallet_window, '_wallet\\templates\\ton_space_beta_off.png', 0.2, 1, 0.75, False, None, True, False],
              [self.wallet_window, '_wallet\\templates\\ton_space_beta_on.png', 0.2, 1, 0.75, False, None, True, False],
           ]
        )
        
        if 'ton_space_beta_off' in beta_wallet:
            click_on_img(self.wallet_window, '_wallet\\templates\\ton_space_beta_off.png', 0.2, 20, 0.75)
            logger.info("Ton Space turned ON")
        elif 'ton_space_beta_on' in beta_wallet:
            logger.info("Ton Space already ON")
        else:
            raise Exception('Ton Space radiobutton not found.')
        
        if not click_on_img(self.wallet_window, '_wallet\\templates\\back.png', 0.2, 20, 0.9):
            raise Exception('Check ton space error.')
        

    def manual_add_wallet_phrase(self, phrase):
        res = find_first_image([
            [self.wallet_window, '_wallet\\templates\\ton_space_wallet_ready.png', 0.2, 1, 0.8],
            [self.wallet_window, '_wallet\\templates\\add_existing_wallet.png', 0.2, 1, 0.8],
        ])
        
        if 'ton_space_wallet_ready' in res:
            logger.info("Ton Wallet already logged in")
            return True
        elif 'add_existing_wallet' in res:
            if not phrase:
                raise Exception("Secret phrase not found!")
            click_on_img(self.wallet_window, '_wallet\\templates\\add_existing_wallet.png', 0.2, 20, 0.9)
            click_on_img(self.wallet_window, '_wallet\\templates\\manual_add.png', 0.2, 20, 0.9)
            if get_img_coords(self.wallet_window, '_wallet\\templates\\phrase_field.png', 0.2, 20, 0.8):
                pyperclip.copy(phrase)
                time.sleep(0.2)
                send_keys("^v")

            click_on_img(self.wallet_window, '_wallet\\templates\\next.png', 0.2, 20, 0.8)
            if not click_on_img(self.wallet_window, '_wallet\\templates\\finish_wallet.png', 0.2, 80, 0.8):
                raise Exception('Add existing address error.')
        else:
            raise Exception('Ton wallet status error.')
        