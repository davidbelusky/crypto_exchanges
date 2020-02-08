from models.others import Get_currency_api

class Trade_validate_model:
    def __init__(self,fiat_list = None,crypto_list = None):
        self.fiat_list = fiat_list
        self.crypto_list = crypto_list

    def trade_validate_json(self,json):

        #Check if json have keys (amount,currency_in,currency_out)
        if (('amount' not in json) or ('currency_in' not in json) or ('currency_out' not in json)):
            return {'message':'Wrong keys in json. Keys (amount,currency_in,currency_out)'}
        #Check if amount is number and convert it to float type
        try:
            json['amount'] = float(json['amount'])
        except ValueError:
            return {'message':'Amount must be number'}

        if not (isinstance(json['currency_in'], str)) or not (isinstance(json['currency_out'], str)): return {'message':'currency_in / currency_out must be string'}

        if (len(json['currency_in']) != 3) or (len(json['currency_out']) != 3): return {'message':'Currencies must be 3 characters length'}

        #Upper currency values
        json['currency_in'] = json['currency_in'].upper()
        json['currency_out'] = json['currency_out'].upper()

        if json['currency_in'] == json['currency_out']: return {'message': 'cannot trade same currencies'}

        currency_in_crypto,currency_out_crypto = self.get_currencies_type(json)

        # If None then currency was not founded in crypto list or fiat list
        if (currency_in_crypto == None) and (currency_out_crypto == None): return {'message': 'currency_in and currency_out doesnt exist'}
        elif currency_in_crypto == None: return {'message':'currency_in doesnt exist'}
        elif currency_out_crypto == None: return {'message':'currency_out doesnt exist'}

        if currency_out_crypto == currency_in_crypto: return {'message': 'Cannot trade same type currency (fiat to fiat or crypto to crypto)'}
        currency_types = {"currency_in":currency_in_crypto,"currency_out":currency_out_crypto}
        return currency_types,json


    def get_currencies_type(self,json):
        """
        Check if currency is FIAT or CRYPTO
        FIAT = FALSE
        CRYPTO = TRUE
        :param currency_in_crypto: 3 letter shortcut of currency fiat/crypto
        :param currency_out_crypto: 3 letter shortcut of currency fiat/crypto
        :return: tupple of types currency_in,currency_out Ex. currency_in_crypto = True,currency_out_crypto = False
        """
        # currency_in/currency_out IF FALSE then its fiat IF TRUE then crypto currency
        currency_in_crypto = None
        currency_out_crypto = None

        #IF currency_in/currency_out in crypto list then SET TRUE
        for asset in self.crypto_list:
            if asset['asset_id'] == json['currency_in']:
                currency_in_crypto = True
            if asset['asset_id'] == json['currency_out']:
                currency_out_crypto = True
        # currency_in/currency_out in fiat list then SET FALSE
        if json['currency_in'] in self.fiat_list:
            currency_in_crypto = False
        if json['currency_out'] in self.fiat_list:
            currency_out_crypto = False

        return currency_in_crypto,currency_out_crypto

class Convert_currency_trade():
    @staticmethod
    def convert_currency(currency_in,currency_out,amount):
        """
        Convert amount from currency in to currency out
        :param currency_in:
        :param currency_out:
        :param amount: inputted amount in currency in
        :return: converted amount as float or error message if currency_in or currency_out was not founded in API for exchange rates
        """
        exchange_rate = Get_currency_api.get_crypto_rate(currency_in,currency_out)
        #If API not return float exchange rate then return error message. One or both currencies was not founded
        if 'rate' not in exchange_rate: return {'message':'One or both currencies was not founded in API'}
        converted_amount = float(exchange_rate['rate'] * float(amount))
        return converted_amount

#dics = {'amount':52,"currency_in":"EUR","currency_out":"BTC"}
#print(Trade_validate_model().trade_validate_json(dics))
