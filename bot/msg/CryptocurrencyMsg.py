from bot.DaMsg import DaMsg
from pycoingecko import CoinGeckoAPI

from bot import config


class CryptocurrencyMsg(DaMsg):

    @staticmethod
    def get_msg(data=None) -> str:
        if data is None:
            data = {}
        cg = CoinGeckoAPI()
        codes = config['CRYPTO_CHARCODES'].split(" ")
        res = cg.get_price(ids=codes, vs_currencies=['usd'])
        msg = '&#128200; Курс криптовалют на сегодня:\n\n'
        for currency in codes:
            msg = msg + "<b>" + currency + "</b>: " + str(res[currency]['usd']) + "$\n\n"

        msg = msg + "&#128073; <a href='https://t.me/prosmi_bot'>Предложить новость</a>"

        return msg