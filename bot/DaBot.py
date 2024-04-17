from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, ChatMemberHandler
from exchange.Cbr import Cbr
from bot.msg.ExchangeMsg import ExchangeMsg
from bot.msg.CryptocurrencyMsg import CryptocurrencyMsg
from smtp.Mailer import Mailer
from pycoingecko import CoinGeckoAPI
from urllib.parse import urlparse
import re

from bot import config, text_msg_handlers, photo_msg_handlers, video_msg_handlers, da_text_msg_scenario


class DaBot:

    def __init__(self):
        self.FIRST, self.SECOND = range(2)
        self.add_new_flag = 0
        self.add_photo_flag = 0
        self.add_new_pool = []
        self.add_photo_pool = []
        self.add_video_pool = []
        self.event_pool = {}

    def run(self):
        TOKEN = config['TELEGRAM_TOKEN']
        # получаем экземпляр `Updater`
        updater = Updater(token=TOKEN, use_context=True)
        # получаем экземпляр `Dispatcher`
        dispatcher = updater.dispatcher

        # reaply_k = [['/mune', '/some']]
        # markup = ReplyKeyboardMarkup(reaply_k, one_time_keyboard=False)

        caps_handler = CommandHandler('caps', self.caps)
        close_keyboard = CommandHandler('close_keyboard', self.close_keyboard)
        text_handler = MessageHandler(Filters.text & (~Filters.command), self.text_msg)
        photo_handler = MessageHandler(Filters.photo, self.photo)
        video_handler = MessageHandler(Filters.video, self.video)
        dispatcher.add_handler(text_handler)
        dispatcher.add_handler(photo_handler)
        dispatcher.add_handler(video_handler)
        # dispatcher.add_handler(ChatMemberHandler(self.welcome, ChatMemberHandler.CHAT_MEMBER))
        # добавляем этот обработчик в `dispatcher`
        dispatcher.add_handler(caps_handler)
        dispatcher.add_handler(close_keyboard)

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start), CommandHandler('menu', self.show_menu)],
            states={  # словарь состояний разговора, возвращаемых callback функциями
                self.FIRST: [
                    CallbackQueryHandler(self.add_video, pattern='^add_video$'),
                    CallbackQueryHandler(self.add_new, pattern='^add_new$'),
                    CallbackQueryHandler(self.add_photo, pattern='^add_photo$'),
                    CallbackQueryHandler(self.exchange_rates, pattern='^exchange_rates$'),
                    CallbackQueryHandler(self.cryptocurrency_exchange_rates, pattern='^cryptocurrency_exchange_rates$'),
                ],
                self.SECOND: [
                    CallbackQueryHandler(self.start_over, pattern='^start_menu'),
                    CallbackQueryHandler(self.thx, pattern='^thx$'),
                ],
            },
            fallbacks=[CommandHandler('start', self.start)],
        )

        dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()

    def welcome(self, update, context):
        update.message.reply_text("""Привет. Это новостной бот канала "проСМИсь» Присылайте фото, видео, сводки и любую информацию, о которой хотите рассказать. Мы все обязательно изучим.""")

    def start(self, update, context):
        # `bot.send_message` это метод Telegram API
        # `update.effective_chat.id` - определяем `id` чата,
        # откуда прилетело сообщение
        keyboard = self.get_first_step()
        print(update.effective_chat.id)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)

        # reaply_k = [['/menu', '/some']]
        # markup = ReplyKeyboardMarkup(reaply_k, one_time_keyboard=False)
        # update.message.reply_text('Пожалуйста, выберите:', reply_markup=markup)

        return self.FIRST

    def start_over(self, update, context):
        """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
        # Получаем `CallbackQuery` из обновления `update`
        query = update.callback_query
        # На запросы обратного вызова необходимо ответить,
        # даже если уведомление для пользователя не требуется.
        # В противном случае у некоторых клиентов могут возникнуть проблемы.
        query.answer()
        keyboard = self.get_first_step()
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Отредактируем сообщение, вызвавшее обратный вызов.
        # Это создает ощущение интерактивного меню.
        query.edit_message_text(
            'Пожалуйста, выберите:', reply_markup=reply_markup
        )
        # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
        return self.FIRST

    def show_menu(self, update, context):
        keyboard = self.get_first_step()
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)

        return self.FIRST

    def caps(self, update, context):
        # если аргументы присутствуют
        if context.args:
            # объединяем список в строку и
            # переводим ее в верхний регистр
            text_caps = ' '.join(context.args).upper()
            # `update.effective_chat.id` - определяем `id` чата,
            # откуда прилетело сообщение
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=text_caps)
        else:
            # если в команде не указан аргумент
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='No command argument')
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='send: /caps argument')

    def close_keyboard(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Закрыто', reply_markup=ReplyKeyboardRemove())

    def add_new(self, update, context):
        query = update.callback_query
        query.answer()
        self.add_to_event_pool(key='new_pool', value=update.effective_chat.id)
        query.edit_message_text(text=f"Введите текст новости")

        return self.SECOND

    def add_photo(self, update, context):
        query = update.callback_query
        query.answer()
        self.add_to_event_pool(key='photo_pool', value=update.effective_chat.id)
        query.edit_message_text(text=f"Загрузите фотографии")

        return self.SECOND

    def add_video(self, update, context):
        query = update.callback_query
        query.answer()
        self.add_to_event_pool(key='video_pool', value=update.effective_chat.id)
        query.edit_message_text(text=f"Загрузите видео")

        return self.SECOND

    def exchange_rates(self, update, context):
        print("Курс валют")
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=ExchangeMsg.get_msg(), parse_mode=ParseMode.HTML)

        keyboard = self.get_last_step()
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            'Опции: ', reply_markup=reply_markup
        )

        return self.SECOND

    @staticmethod
    def get_exchange_msg():
        cbr = Cbr()
        currencies = cbr.get_by_codes()
        msg = ''
        for currency in currencies:
            msg = msg + currency['Name'] + ": " + str(currency['Value']) + ", Ранее: " + str(currency['Previous']) + "\n\n"

        return msg

    def cryptocurrency_exchange_rates(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=CryptocurrencyMsg.get_msg(), parse_mode=ParseMode.HTML)

        keyboard = self.get_last_step()
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            'Опции: ', reply_markup=reply_markup
        )

        return self.SECOND

    @staticmethod
    def get_cryptocurrency_exchange_msg():
        cg = CoinGeckoAPI()
        codes = config['CRYPTO_CHARCODES'].split(" ")
        res = cg.get_price(ids=codes, vs_currencies=['usd'])
        msg = ''
        for currency in codes:
            msg = msg + currency + ": " + str(res[currency]['usd']) + "$\n\n"

        return msg

    def thx(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Спасибо!")
        return ConversationHandler.END

    def text_msg(self, update, context):
        self.run_text_handlers(update, context)
        print("Текстовое сообщение из чата {id}".format(id=update.effective_chat.id))
        if self.has_in_event_pool(key='new_pool', value=update.effective_chat.id):
            print('Добавляем новость', update.effective_user)
            self.remove_from_event_pool(key='new_pool', value=update.effective_chat.id)

            keyboard = self.get_last_step()
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'Опции: ', reply_markup=reply_markup
            )

            # Информируем админа
            txt = "Пользователь {user} добавил новость через бота\n\n{text}".format(user=update.effective_user.first_name,
                                                                                                          text=update.message.text)
            self.send_admins_notif(context, text=txt)

            return self.SECOND

        if self.has_in_event_pool(key='photo_descr_pool', value=update.effective_chat.id):
            self.remove_from_event_pool(key='photo_descr_pool', value=update.effective_chat.id)

            keyboard = self.get_last_step()
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'Опции: ', reply_markup=reply_markup
            )

            # Информируем админа
            txt = "Пользователь {user} добавил описание фото\n\n{text}".format(
                user=update.effective_user.first_name,
                text=update.message.text)
            self.send_admins_notif(context, text=txt)

            return self.SECOND

    def run_text_handlers(self, update, context):
        for handler in self.get_scenario(update, context):
            handler.handler(update, context)

    def get_scenario(self, update, context):
        text = update.effective_message.text
        s = re.search("(?P<url>https?://[^\s]+)", text)
        if s is not None:
            link = s.group("url")
            domain = urlparse(link).netloc
            if domain == config['MAP_DOMAIN']:
                return da_text_msg_scenario

        return text_msg_handlers

    def run_photo_handlers(self, update, context):
        for handler in photo_msg_handlers:
            handler.handler(update, context)

    def run_video_handlers(self, update, context):
        for handler in video_msg_handlers:
            handler.handler(update, context)

    def photo(self, update, context):
        self.run_photo_handlers(update, context)
        if self.has_in_event_pool(key='photo_pool', value=update.effective_chat.id):
            print('Добавляем фото')
            self.remove_from_event_pool(key='photo_pool', value=update.effective_chat.id)

            # Добавление описания фото
            context.bot.send_message(text="Описание фотографии:", chat_id=update.effective_chat.id)
            self.add_to_event_pool(key="photo_descr_pool", value=update.effective_chat.id)

            # Информируем админа
            photo_count = len(update.message.photo)
            file_size = update.message.photo[photo_count - 1]
            self.send_admins_notif(context,
                                   text='Пользователь {user} добавил фото через бота'.format(user=update.effective_user.first_name),
                                   photo=file_size)

            return self.SECOND

    def video(self, update, context):
        self.run_video_handlers(update, context)
        if self.has_in_event_pool(key='video_pool', value=update.effective_chat.id):
            print('Добавляем видео')
            self.remove_from_event_pool(key='video_pool', value=update.effective_chat.id)

            keyboard = self.get_last_step()
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'Опции: ', reply_markup=reply_markup
            )

            # Информируем админа
            self.send_admins_notif(context,
                                   text='Пользователь добавил видео через бота',
                                   video=update.message.video)

            return self.SECOND

    def add_to_event_pool(self, key, value):
        if key not in self.event_pool:
            self.event_pool[key] = []

        self.event_pool[key].append(value)

    def remove_from_event_pool(self, key, value):
        if key in self.event_pool:
            self.event_pool[key].remove(value)

    def has_in_event_pool(self, key, value):
        if key in self.event_pool:
            if value in self.event_pool[key]:
                return True

        return False

    @staticmethod
    def get_last_step():
        keyboard = [
            [
                InlineKeyboardButton("Меню", callback_data='start_menu'),
                InlineKeyboardButton("Завершить", callback_data='thx')
            ],
        ]
        return keyboard

    @staticmethod
    def get_first_step():
        keyboard = [
            [
                InlineKeyboardButton("Добавить видео", callback_data='add_video')
            ],
            [
                InlineKeyboardButton("Добавить фото", callback_data='add_photo')
            ],
            [
                InlineKeyboardButton("Добавить новость", callback_data='add_new')
            ],
            [
                InlineKeyboardButton("Курс валют", callback_data='exchange_rates'),
            ],
            [
                InlineKeyboardButton("Курс криптовалют", callback_data='cryptocurrency_exchange_rates'),
            ],
        ]
        return keyboard

    @staticmethod
    def send_admins_notif(context, text, photo=None, video=None):
        admins = config['ADMINS'].split(" ")

        for admin in admins:
            context.bot.send_message(chat_id=admin, text=text)
            if photo:
                context.bot.send_photo(chat_id=admin, photo=photo)
            if video:
                context.bot.send_video(chat_id=admin, video=video)

    def button(self, update, context):
        query = update.callback_query
        variant = query.data

        # `CallbackQueries` требует ответа, даже если
        # уведомление для пользователя не требуется, в противном
        #  случае у некоторых клиентов могут возникнуть проблемы.
        # смотри https://core.telegram.org/bots/api#callbackquery.
        query.answer()
        # редактируем сообщение, тем самым кнопки
        # в чате заменятся на этот ответ.
        query.edit_message_text(text=f"Выбранный вариант: {variant}")