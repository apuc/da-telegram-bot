from bot.DaMsg import DaMsg
from exchange.Cbr import Cbr


class ExchangeMsg(DaMsg):

    @staticmethod
    def get_msg(data=None) -> str:
        if data is None:
            data = {}
        cbr = Cbr()
        currencies = cbr.get_by_codes()
        msg = '&#128200; Курс валют ЦБ РФ на сегодня:\n\n'
        for currency in currencies:
            circle = ExchangeMsg.get_circle(currency['Value'], currency['Previous'])
            arrow = ExchangeMsg.get_arrow(currency['Value'], currency['Previous'])
            msg = msg + "{n}: {c} <b>{v}</b> {a}\n\n".format(n=currency['Name'], c=circle, v=currency['Value'], a=arrow)

        msg = msg + "&#128073; <a href='https://t.me/prosmi_bot'>Предложить новость</a>"

        return msg

    @staticmethod
    def get_arrow(value, previous) -> str:
        if value > previous:
            return "&#11014;"

        return "&#11015;"

    @staticmethod
    def get_circle(value, previous) -> str:
        if value > previous:
            return "&#128994;"

        return "&#128308;"
