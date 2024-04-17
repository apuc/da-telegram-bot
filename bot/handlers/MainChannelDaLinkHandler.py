from bot.DaHandler import DaHandler
from telegram import ParseMode
import bot
import re
from urllib.parse import urlparse


class MainChannelDaLinkHandler(DaHandler):

    def handler(self, update, context):
        if bot.config['MAIN_CANNEL_ID'] == str(update.effective_chat.id):
            if update.effective_message.text is not None:
                text = update.effective_message.text
                s = re.search("(?P<url>https?://[^\s]+)", text)
                if s is not None:
                    link = s.group("url")
                    domain = urlparse(link).netloc
                    if domain == bot.config['MAP_DOMAIN']:
                        final_text = "{text}".format(
                            text="<a href='{link}'>&#128506; Смотреть на карте</a>".format(link=link))
                        update.effective_message.text = final_text

                        context.bot.editMessageText(chat_id=update.effective_chat.id,
                                                    message_id=update.effective_message.message_id,
                                                    text=final_text, parse_mode=ParseMode.HTML)
