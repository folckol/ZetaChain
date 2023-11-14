import time
import concurrent.futures

from logger import logger
from network.galxe import Galxe
from config import *


def create_lst(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def connect_twitter(index, galxe):
    logger.info(f'{index}: Executing...')
    galxe.delete_twitter()
    galxe.connect_twitter()
    time.sleep(delay)


def connect_discord(index, galxe):
    logger.info(f'{index}: Executing...')
    galxe.connect_discord()
    time.sleep(delay)


def claimer(index, galxe):
    logger.info(f'{index}: Executing...')
    for campaig_data in data:
        galxe.verif(campaign_id=campaig_data[0], credentials=campaig_data[1])
        # galxe.claim(campaig_data[0])


if __name__ == '__main__':

    keys = create_lst('files/private_keys.txt')
    addresses = create_lst('files/addresses.txt')
    proxy = create_lst('files/proxy.txt')
    tw_auth_tokens = create_lst('files/tw_auth_tokens.txt')
    tw_csrf_tokens = create_lst('files/tw_csrf_tokens.txt')
    discord_tokens = create_lst('files/discord_tokens.txt')
    cap_key = create_lst('files/cap_key.txt')[0]

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(len(keys)):

            try:
                galxe = Galxe(
                    index=i + 1,
                    proxy=proxy[i],
                    address=addresses[i],
                    private=keys[i],
                    auth_token=tw_auth_tokens[i],
                    csrf=tw_csrf_tokens[i],
                    discord_token=discord_tokens[i],
                    cap_key=cap_key,
                    acc_id=i
                )

                if func == 'claimer':
                    executor.submit(claimer, i + 1, galxe)
                elif func == 'connect_twitter':
                    executor.submit(connect_twitter, i + 1, galxe)
                elif func == 'connect_discord':
                    executor.submit(connect_discord, i + 1, galxe)
            except:
                logger.error(f'{i + 1}: Unknown error')
