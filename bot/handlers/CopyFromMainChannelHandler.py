from bot.DaHandler import DaHandler
from telegram import ParseMode
import bot


class CopyFromMainChannelHandler(DaHandler):

    def handler(self, update, context):
        if bot.config['MAIN_CANNEL_ID'] == str(update.effective_chat.id):
            text = "{text} \n\n {bot_link}".format(text=update.effective_message.text,
                                                   bot_link="&#128073; <a href='https://t.me/prosmi_bot'>Предложить новость</a>")

            context.bot.send_message(chat_id=bot.config['NEW_MAIN_CHANNEL_ID'], text=text, parse_mode=ParseMode.HTML)