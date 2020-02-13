import re
import requests
import json
import decimal


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
        # json = None
        # if base == 'EUR' and quote == 'BTC':
        #     json = {'rate': 0.0001116596551742244}
        # elif base == 'BTC' and quote == 'EUR':
        #     json = {'rate': 8958.385661352231}

        return json

class DecimalEncoder(json.JSONEncoder):
    """
    Convert returned decimal type from DB to float. (json cannot obtain decimal type)
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

class Trade_history_sql_generate():
    @staticmethod
    def generate_sql_history_filter(json):
        """
        Generate SQL to SELECT * data and filter based on inputted parameters
        :param json:
        :return: SQL in str format
        """

        sql = "SELECT * FROM trades WHERE "
        # List of parameters to use in WHERE clause
        where_conditions_list = ['exchange_id', 'search', 'date_from', 'date_to']
        # List of parameters use for paginate
        paginate_conditions_list = ['limit', 'offset']
        paginate_actual_lst = []
        for k, v in json.items():
            if v == None:
                continue
            if k in where_conditions_list:
                if k == 'date_from':
                    sql += 'trade_date' + " >= '" + str(v.date()) + "' AND "
                elif k == 'date_to':
                    sql += 'trade_date' + " <= '" + str(v.date()) + "' AND "
                elif k == 'search':
                    sql += 'name' + " LIKE '%" + str(v) + "%' AND "
                else:
                    sql += k + " = '" + str(v) + "' AND "
            elif k in paginate_conditions_list:
                paginate_actual_lst.append(k + ' ' + str(v))
        # sort paginate condition list first Limit second Offset
        paginate_actual_lst.sort()
        paginate_string = ' '.join(paginate_actual_lst)

        # Delete last AND
        sql = sql[:-4] + paginate_string
        return sql

#print(Get_currency_api.get_crypto_rate('usd','btc'))