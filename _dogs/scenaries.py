from .telegram_dogs import TelegramDogs
import time
import random


def dogs_daily_rewards(path):
    telegram_app = TelegramDogs(path)
    telegram_app.launch_dogs('https://t.me/dogshouse_bot/join?startapp')
    telegram_app.work_with_dogs()

    telegram_app.quit_telegram()


def dogs_accounts_create(path):
    with open('_dogs\\dogs_refs.txt', 'r', encoding='utf-8') as fileobj:
        refs_list = fileobj.readlines()
    ref_link =  random.choice(refs_list).strip()
    print(ref_link)


def set_nicknames(path):
    telegram_app = TelegramDogs(path)
    telegram_app.set_random_nicknames()
    telegram_app.quit_telegram()
    