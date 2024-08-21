from telegram_core.telegram import TelegramApp
from telegram_core.devtools import DevTools
from telegram_core.img_detection import *
import time
from loguru import logger
from pywinauto.keyboard import send_keys
import json


class TelegramAppBlum(TelegramApp):
    def __init__(self, exe_path):
        super().__init__(exe_path)
        self.blum_window = None
        self.devtools = None


    def launch_blum(self, link):    
        self.blum_window = self.launch_app(
            '_blum\\templates\\launch.png',
            '_blum\\templates\\allow_msg.png',
            '_blum\\templates\\OK.png',
            link,
            'Blum',
            window_pos=(0, 0)
        )


    def work_with_blum(self, create_account=False):
        res = find_first_image([
            [self.blum_window, '_blum\\templates\\create_account.png', 0.2, 1, 0.9],
            [self.blum_window, '_blum\\templates\\start_farming.png', 0.2, 1, 0.8],
            [self.blum_window, '_blum\\templates\\currently_farming.png', 0.2, 1, 0.6],
            [self.blum_window, '_blum\\templates\\claim.png', 0.2, 1, 0.6],
            [self.blum_window, '_blum\\templates\\continue.png', 0.2, 1, 0.6],
        ])
        if 'continue' in res:
            click_on_img(self.blum_window, '_blum\\templates\\continue.png', 0.5, 5, 0.6)
            res = find_first_image([
                [self.blum_window, '_blum\\templates\\create_account.png', 0.2, 1, 0.9],
                [self.blum_window, '_blum\\templates\\start_farming.png', 0.2, 1, 0.8],
                [self.blum_window, '_blum\\templates\\currently_farming.png', 0.2, 1, 0.6],
                [self.blum_window, '_blum\\templates\\claim.png', 0.2, 1, 0.6],
            ])
        if 'currently_farming' in res:
            logger.info('Account is currently farming!')
        elif 'start_farming' in res:
            click_on_img(self.blum_window, '_blum\\templates\\start_farming.png', 0.2, 1, 0.8)
            logger.info('Account start farming!')
            time.sleep(2)
        elif 'claim' in res:
            click_on_img(self.blum_window, '_blum\\templates\\claim.png', 0.5, 5, 0.6)
            click_on_img(self.blum_window, '_blum\\templates\\start_farming.png', 0.5, 10, 0.8)
            logger.info('Account claim earnings!')
            time.sleep(2)
        elif 'create_account' in res:
            if create_account:
                logger.info('Account start to create!')
                self.create_account()
            else:
                raise Exception("Account not created!")
        else: 
            raise Exception("Account status not found!")
    

    def open_devtools(self):
        if click_on_img(self.blum_window, '_blum\\templates\\logo.png', 0.5, 5, 0.7):
            time.sleep(0.3)
            send_keys("{F12}")
            time.sleep(1)
            self.devtools = DevTools()
        else:
            raise Exception('Blum logo not found!')


    def create_account(self):
        click_on_img(self.blum_window, '_blum\\templates\\create_account.png', 0.5, 10, 0.9)
        if get_img_coords(self.blum_window, '_blum\\templates\\blum_nickname_available.png', 0.5, 20, 0.8):
            click_on_img(self.blum_window, '_blum\\templates\\continue.png', 0.5, 10, 0.9)
        time.sleep(13)
        click_on_img(self.blum_window, '_blum\\templates\\continue.png', 0.5, 50, 0.9)
        click_on_img(self.blum_window, '_blum\\templates\\continue.png', 0.5, 20, 0.9)
        click_on_img(self.blum_window, '_blum\\templates\\start_farming.png', 0.5, 5, 0.8)
        time.sleep(2)

        logger.info('Account successfully created!')


    def connect_wallet(self):
        #blum app
        if get_img_coords(self.blum_window, '_blum\\templates\\home.png', 0.2, 40, 0.7):
            click_on_img(self.blum_window, '_blum\\templates\\wallet.png', 0.5, 40, 0.7)
            time.sleep(1)
            if not click_on_img(self.blum_window, '_blum\\templates\\wallet.png', 0.5, 40, 0.7):
                raise Exception('Wallet button not found')
            if not click_on_img(self.blum_window, '_blum\\templates\\connect_wallet.png', 0.2, 4, 0.8):
                logger.info("Wallet already connected")
                return False
        else:
            raise Exception("Problem with blum window")
        

        time.sleep(0.5)
        click_on_img(self.blum_window, '_blum\\templates\\wallet_telegram.png', 0.5, 40, 0.8)

        #wallet app
        wallet_window = self.get_first_window_except_main(40, [self.blum_window])
        if wallet_window:
            logger.info("Wallet successfully launch")
        else:
            raise Exception('Wallet do not launch')
            
        time.sleep(1)
        if click_on_img(wallet_window, '_blum\\templates\\connect_app_wallet.png', 0.5, 40, 0.9):
            logger.info("Wallet connected")
            new_blum_window = self.get_first_window_except_main(40, [wallet_window])
            time.sleep(8)
            if new_blum_window:
                self.blum_window = new_blum_window
                return True
            else:
                raise Exception('New blum window not found.')
        raise Exception('No wallet connection button')
        

    def collect_data(self, proxy=''):
        session_data = self.devtools.prepare_and_get_tgWebAppData()
        local_data = self.devtools.prepare_and_get_localdata()
        end_data = {
            'proxy': proxy,
            'Token':'',
            'distinct_id': local_data['distinct_id'],
            'device_id': local_data['device_id'],
            'user_id': local_data['user_id'],
            'tok': 'a663ec3881444e996e51121d5a98ce4d',
            'queid': session_data,
        }

        logger.info("Devtools data successfully collected!")
        return end_data
    

    def append_to_json_file(self, file_path, new_dict):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []

        if not isinstance(data, list):
            data = []

        data.append(new_dict)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


    @staticmethod
    def test_devtools():
        devtools = DevTools()
        
        session_data = devtools.prepare_and_get_tgWebAppData()
        local_data = devtools.prepare_and_get_localdata()
        end_data = {
            'proxy':'---',
            'Token':'',
            'distinct_id': local_data['distinct_id'],
            'device_id': local_data['device_id'],
            'user_id': local_data['user_id'],
            'tok': 'a663ec3881444e996e51121d5a98ce4d',
            'queid': session_data,
        }

        for i,j in end_data.items():
            print(f"{i}: {j}")