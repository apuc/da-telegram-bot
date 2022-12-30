from bot.DaHandler import DaHandler
from telegram import ParseMode
import bot


class TestChannelPhotoHandler(DaHandler):

    def handler(self, update, context):
        if bot.config['TEST_CHANNEL_ID'] == str(update.effective_chat.id):
            if update.effective_message.caption is not None:
                text = "{text} \n\n {bot_link}".format(text=update.effective_message.caption,
                                                       bot_link="&#128073; <a href='https://t.me/prosmi_bot'>Предложить новость</a>")

                context.bot.editMessageCaption(chat_id=update.effective_chat.id,
                                            message_id=update.effective_message.message_id,
                                            caption=text, parse_mode=ParseMode.HTML)