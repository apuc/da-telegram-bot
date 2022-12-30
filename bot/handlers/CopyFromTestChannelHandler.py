from bot.DaHandler import DaHandler
from telegram import ParseMode
import bot


class CopyFromTestChannelHandler(DaHandler):

    def handler(self, update, context):
        if bot.config['TEST_CHANNEL_ID'] == str(update.effective_chat.id):
            print(update)
            print(context)
            context.bot.copy_message(from_chat_id=update.effective_chat.id,
                                     chat_id=1078162189,
                                     message_id=update.effective_message.message_id,
                                     parse_mode=ParseMode.HTML)
