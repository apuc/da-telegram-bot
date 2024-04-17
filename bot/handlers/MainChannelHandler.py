from bot.DaHandler import DaHandler
from telegram import ParseMode
import bot
from bot.DaMsg import DaMsg


class MainChannelHandler(DaHandler):

    def handler(self, update, context):
        if bot.config['MAIN_CANNEL_ID'] == str(update.effective_chat.id):
            da_msg = DaMsg(update.effective_message)
            text = "{text} \n\n {bot_link}".format(text=da_msg.stylizedText,
                                                   bot_link="&#128073; <a href='https://t.me/prosmi_bot'>Предложить новость</a>")

            context.bot.editMessageText(chat_id=update.effective_chat.id,
                                        message_id=update.effective_message.message_id,
                                        text=text, parse_mode=ParseMode.HTML)
