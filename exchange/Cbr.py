import requests
import json


class Cbr:

    def __init__(self):
        from exchange import config
        self.config = config
        self.exchanges = None

    def get_exchanges(self):
        res = requests.get(self.config['CBR_URL'])
        self.exchanges = json.loads(res.text)['Valute']

        return self.exchanges

    def get_by_codes(self, codes=None):
        if self.exchanges is None:
            self.get_exchanges()

        if codes is None:
            codes = self.config['CBR_CHARCODES'].split(" ")

        res = []
        for currency in codes:
            if currency in self.exchanges:
                res.append(self.exchanges[currency])

        return res

    def get_by_char_code(self, char_code):
        if self.exchanges is None:
            self.get_exchanges()

        if char_code in self.exchanges:
            return self.exchanges[char_code]

        return None
