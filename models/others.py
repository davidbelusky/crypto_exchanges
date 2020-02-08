import re
import requests
import json
import decimal
from psycopg2.extras import RealDictRow
from decimal import Decimal

class Correct_string:
    @staticmethod
    def string_corrections(text):
        """
        Check if text contains any special character exclude 'underscore'
        Min length of text is 1
        If text contain special character return None
        Else clean all
        :param text:
        :return: None or validated string
        """
        string_check = re.compile('[@!#$%^&*()<>?/\|}{~:]')
        if (string_check.search(text) == None):
            text = text.strip().capitalize()
            if len(text) > 0:
                return text
        else:
            return None

class Get_currency_api:
    @staticmethod
    def get_all_assets():
        """
        Get all assets for fiat and crypto currencies.
        Use for validate user input
        :return: fiat currency list, crypto currency list
        """
        url = 'https://rest.coinapi.io/v1/assets'
        headers = {'X-CoinAPI-Key': '4ED760E9-11CC-4B1D-A423-A263D6BF8FDC'}
        response = requests.get(url, headers=headers).json()

        fiat_list = []
        crypto_list = []
        for asset in response:
            if asset['type_is_crypto'] == 0:
                fiat_list.append(asset['asset_id'])
            elif asset['type_is_crypto'] == 1:
                try:
                    crypto_list.append({'asset_id': asset['asset_id'], 'name': asset['name']})
                except KeyError:
                    crypto_list.append({'asset_id': asset['asset_id'], 'name': 'N/A'})

        return fiat_list, crypto_list

    @staticmethod
    def get_crypto_rate(base,quote):
        # Return rate of crypto currencies
        url = 'https://rest.coinapi.io/v1/exchangerate/{}/{}'.format(base,quote)
        headers = {'X-CoinAPI-Key': '4ED760E9-11CC-4B1D-A423-A263D6BF8FDC'}
        response = requests.get(url, headers=headers)
        json = response.json()
        return json


    # @staticmethod
    # def get_fiat_rate(base,quote):
    #     """
    #     :param base: base currency
    #     :param quote: quote
    #     :return: specific rate
    #     """
    #     fiat_currency_request = requests.get('https://api.exchangeratesapi.io/latest?base={}'.format(base))
    #     # Return rate
    #     fiat_currency_rate = fiat_currency_request.json()
    #     return fiat_currency_rate['rates'][quote]

class DecimalEncoder(json.JSONEncoder):
    """
    Convert returned decimal type from DB to float. (json cannot obtain decimal type)
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

