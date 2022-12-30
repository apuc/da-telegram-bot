from telegram import Bot, ParseMode, Message

from dotenv import dotenv_values
from pathlib import Path  # Python 3.6+ only

env_path = Path('.') / '.env.local'

config = dotenv_values(dotenv_path=env_path)

if __name__ == '__main__':
    bot = Bot(config['TELEGRAM_TOKEN'])
    chat = bot.get_chat(chat_id=config['MAIN_CANNEL_ID'])
    msg = Message(chat=chat)

    print(123)