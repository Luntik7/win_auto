import random
from config import CHECK_WEBVIEW_INSPECTIOIN
from .telegram_blum import TelegramAppBlum
import time


def blum_data_collect(path, counter, proxies_path) -> None:           #need proxies
    telegram_app = TelegramAppBlum(path)
    if CHECK_WEBVIEW_INSPECTIOIN:
        telegram_app.turn_on_webview_inspecting()
    telegram_app.launch_blum('https://t.me/BlumCryptoBot/app?startapp')
    telegram_app.work_with_blum()
    telegram_app.open_devtools()

    data = telegram_app.collect_data()
    
    with open(proxies_path, 'r', encoding='utf-8') as fileobj:
        proxies_list = fileobj.readlines()
    number = TelegramAppBlum.get_account_number_from_path(path)
    if number:
        proxy = proxies_list[number].strip()
    else:
        proxy = proxies_list[counter].strip()
    data['proxy'] = proxy
    telegram_app.append_to_json_file('_blum\\blum.json', data)  

    telegram_app.quit_telegram()
    time.sleep(0.5)


def blum_wallet_connect(path):
    telegram_app = TelegramAppBlum(path)
    telegram_app.launch_blum('https://t.me/BlumCryptoBot/app?startapp')
    telegram_app.work_with_blum()
    if telegram_app.connect_wallet():
        telegram_app.launch_blum('https://t.me/BlumCryptoBot/app?startapp')
        telegram_app.connect_wallet()
    telegram_app.quit_telegram()
    

def blum_daily_rewards(path):
    telegram_app = TelegramAppBlum(path)
    telegram_app.launch_blum('https://t.me/BlumCryptoBot/app?startapp')
    telegram_app.work_with_blum()

    telegram_app.quit_telegram()


def blum_register(path, ref_path):
    telegram_app = TelegramAppBlum(path)

    with open(ref_path, 'r', encoding='utf-8') as fileobj:
        ref_link = random.choice(fileobj.readlines()).strip()

    telegram_app.launch_blum(ref_link)
    telegram_app.work_with_blum()

    telegram_app.quit_telegram()