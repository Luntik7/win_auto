from linecache import cache
import time
from telegram_core.telegram import TelegramApp
from loguru import logger
import traceback
from config import TRIES_COUNT
from _dogs.scenaries import dogs_daily_rewards, set_nicknames
from _blum.scenaries import blum_data_collect, blum_wallet_connect, blum_daily_rewards, blum_register
from _wallet.scenaries import wallet_main, secret_collect, wallet_send_manual


def scenary_selection(path, counter):
    # dogs_daily_rewards(path)
    set_nicknames(path)
    
    # blum_daily_rewards(path)
    # blum_data_collect(path, counter, 'all_proxies.txt')            #PROXY needed
    # blum_wallet_connect(path)
    # blum_register(path, '_blum\\blum_refs.txt')                      #REFS needed

    # wallet_main(path, counter)                                      #SECRETS needed       NEED UPDATE!
    # secret_collect(path)
    # wallet_send_manual(path, counter)



def main():
    # logger.add("file.log", level="DEBUG")

    with open('all_pathes.txt', 'r', encoding='utf-8') as fileobj:
        pathes_list = fileobj.readlines()

    for counter, path in enumerate(pathes_list):
        for i in range(TRIES_COUNT):
            try:
                if path.find('all_telegrams') != -1:
                    short_path = path[path.index('all_telegrams')+13:].strip()
                else:
                    short_path = path[-40:]

                if TelegramApp.is_proxifier_running():
                    TelegramApp.stop_telegram_processes()
                    time.sleep(1)
                    logger.info(f"Start account ...{short_path}")

                    scenary_selection(path.strip(), counter)
                    break
                else:
                    logger.warning('Launch proxyfier firstly')
                    return 0
            except Exception as e:
                error_message = f'Error: {str(e).strip()}'
                error_traceback = traceback.format_exc().strip()
                logger.error(f'{error_message}\n{error_traceback}')
                logger.warning(f"TRY {i+1}/{TRIES_COUNT}")
                if i+1 < TRIES_COUNT:
                    continue
                else:
                    with open('bad_accounts.txt', 'a', encoding='utf-8') as fileobj:
                        fileobj.write(path.strip() + '\n')
            finally:
                logger.info(f"Finish account ...{short_path}\n")


if __name__ == '__main__':
    main()
    input('Press any key to exit...')
