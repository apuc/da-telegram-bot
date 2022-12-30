from bot.DaHandler import DaHandler
from telegram import ParseMode
import bot


class CopyFromMainChannelVideoHandler(DaHandler):

    def handler(self, update, context):
        if bot.config['TEST_CHANNEL_ID'] == str(update.effective_chat.id):
            if update.effective_message.caption is not None:
                text = "{text} \n\n {bot_link}".format(text=update.effective_message.caption,
                                                       bot_link="&#128073; <a href='https://t.me/prosmi_bot'>Предложить новость</a>")

                context.bot.send_message(chat_id=bot.config['NEW_MAIN_CHANNEL_ID'], text=text, parse_mode=ParseMode.HTML)