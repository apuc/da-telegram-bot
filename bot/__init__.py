from dotenv import dotenv_values
from bot.handlers.MainChannelHandler import MainChannelHandler
from bot.handlers.TestChannelHandler import TestChannelHandler
from bot.handlers.TestChannelPhotoHandler import TestChannelPhotoHandler
from bot.handlers.MainChannelPhotoHandler import MainChannelPhotoHandler
from bot.handlers.TestChannelVideoHandler import TestChannelVideoHandler
from bot.handlers.MainChannelVideoHandler import MainChannelVideoHandler
from bot.handlers.CopyFromMainChannelHandler import CopyFromMainChannelHandler
from bot.handlers.CopyFromMainChannelPhotoHandler import CopyFromMainChannelPhotoHandler
from bot.handlers.CopyFromMainChannelVideoHandler import CopyFromMainChannelVideoHandler
from bot.handlers.CopyFromTestChannelHandler import CopyFromTestChannelHandler
from bot.handlers.TestChannelDaLinkHandler import TestChannelDaLinkHandler
from bot.handlers.MainChannelDaLinkHandler import MainChannelDaLinkHandler

config = dotenv_values(".env.local")

text_msg_handlers = [
    MainChannelHandler(),
    TestChannelHandler(),
    CopyFromMainChannelHandler(),
    CopyFromTestChannelHandler()
]

da_text_msg_scenario = [
    MainChannelDaLinkHandler(),
    TestChannelDaLinkHandler()
]

photo_msg_handlers = [
    TestChannelPhotoHandler(),
    MainChannelPhotoHandler(),
    # CopyFromMainChannelPhotoHandler(),
    CopyFromTestChannelHandler()
]

video_msg_handlers = [
    TestChannelVideoHandler(),
    MainChannelVideoHandler(),
    # CopyFromMainChannelVideoHandler()
]
