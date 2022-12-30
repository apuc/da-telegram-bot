from telegram import Bot, ParseMode
from bot.msg.ExchangeMsg import ExchangeMsg
from bot.msg.CryptocurrencyMsg import CryptocurrencyMsg
import argparse

from dotenv import dotenv_values
from pathlib import Path  # Python 3.6+ only

env_path = Path('.') / '.env.local'

config = dotenv_values(dotenv_path=env_path)

parser = argparse.ArgumentParser()

# add arguments to the parser
parser.add_argument("-m", "--mode", default="prod", type=str, help="Mode type")
parser.add_argument("-t", "--type", default="main", type=str, help="Exchange type")

args = parser.parse_args()

if __name__ == '__main__':
    bot = Bot(config['TELEGRAM_TOKEN'])
    if args.mode == "test":
        channel_id = config['TEST_CHANNEL_ID']
    else:
        channel_id = config['MAIN_CANNEL_ID']

    if args.type == "crypto":
        msg_text = CryptocurrencyMsg.get_msg()
    else:
        msg_text = ExchangeMsg.get_msg()
    # print(channel_id)
    bot.send_message(chat_id=channel_id, text=msg_text, parse_mode=ParseMode.HTML)
