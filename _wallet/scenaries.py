from .telegram_wallet import TelegramWallet
import time


def wallet_main(path, counter):
    telegram_app = TelegramWallet(path)
    telegram_app.launch_wallet('https://t.me/wallet?startapp')

    with open('_wallet\\secrets.txt', 'r', encoding='utf-8') as fileobj:
        phrases_list = fileobj.readlines()
    secret = phrases_list[counter].strip()

    telegram_app.work_with_wallet(secret)

    telegram_app.quit_telegram()
    

def secret_collect(path):
    telegram_app = TelegramWallet(path)
    telegram_app.launch_wallet('https://t.me/wallet?startapp', window_pos=(0, 0))
    telegram_app.collect_adresses('_wallet\\adresses.txt')

    telegram_app.quit_telegram()


def wallet_send_manual(path, counter):
    telegram_app = TelegramWallet(path)
    telegram_app.launch_wallet('https://t.me/wallet?startapp', window_pos=(0, 0))

    data = None
    with open('_wallet\\adresses.txt', 'r', encoding='utf-8') as fileobj:
        data = fileobj.readlines()

    address = data[(counter+1)].strip()
    telegram_app.manual_send(address, counter)

    telegram_app.quit_telegram()