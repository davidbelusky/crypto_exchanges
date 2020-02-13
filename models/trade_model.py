from models.others import Get_currency_api
from db.db_exchanges import DB_exchanges
from db.db_crypto_currencies import DB_crypto_currencies
from db.db_trades import DB_trades
from datetime import datetime as dt

class Trade_validate_model:
    def __init__(self,fiat_list = None,crypto_list = None):
        self.fiat_list = fiat_list
        self.crypto_list = crypto_list

    def trade_validate_json(self,json):
        #Check if json have keys (amount,currency_in,currency_out)
        if (('amount' not in json) or ('currency_in' not in json) or ('currency_out' not in json)):
            return {'message':'Wrong keys in json. Keys (amount,currency_in,currency_out)'},400
        #Check if amount is number and convert it to float type
        try:
            json['amount'] = float(json['amount'])
        except ValueError:
            return {'message':'Amount must be number'},400

        if not (isinstance(json['currency_in'], str)) or not (isinstance(json['currency_out'], str)): return {'message':'currency_in / currency_out must be string'},400

        if (len(json['currency_in']) != 3) or (len(json['currency_out']) != 3): return {'message':'Currencies must be 3 characters length'},400

        #Upper currency values
        json['currency_in'] = json['currency_in'].upper()
        json['currency_out'] = json['currency_out'].upper()

        if json['currency_in'] == json['currency_out']: return {'message': 'cannot trade same currencies'},400

        currency_in_crypto,currency_out_crypto = self.get_currencies_type(json)

        # If None then currency was not founded in crypto list or fiat list
        if (currency_in_crypto == None) and (currency_out_crypto == None): return {'message': 'currency_in and currency_out doesnt exist'},400
        elif currency_in_crypto == None: return {'message':'currency_in doesnt exist'},400
        elif currency_out_crypto == None: return {'message':'currency_out doesnt exist'},400

        if currency_out_crypto == currency_in_crypto: return {'message': 'Cannot trade same type currency (fiat to fiat or crypto to crypto)'},400
        currency_types = {"currency_in_crypto":currency_in_crypto,"currency_out_crypto":currency_out_crypto}
        return [currency_types,json]

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
    def convert_currency(currency_in,currency_out,amount,exchange_id,currency_types=None):
        """
        Convert amount from currency in to currency out
        :param currency_in:
        :param currency_out:
        :param amount: inputted amount in currency in
        :return: converted amount as float or error message if currency_in or currency_out was not founded in API for exchange rates
        """
        #If trade from crypto to fiat and trade fiat != exchange fiat convert it to exchange fiat


        exchange_rate = Get_currency_api.get_crypto_rate(currency_in,currency_out)
        #If API not return float exchange rate then return error message.
        if 'rate' not in exchange_rate: return {'message':'One or both currencies was not founded in API'},400
        converted_amount = float(exchange_rate['rate'] * float(amount))

        if currency_types['currency_in_crypto'] == True:
            exchange_currency = DB_exchanges().select_check_exchange(exchange_id)[0]
            #print(currency_out,exchange_currency)
            if currency_out != exchange_currency:
                #trade fiat to exchange fiat rate
                fiat_rate = Get_currency_api.get_crypto_rate(currency_out,exchange_currency)
                converted_amount = float(fiat_rate['rate'] * converted_amount)

        return converted_amount

class Check_balance():
    @staticmethod
    def check_balance(exchange_id,json,currency_types):
        """
        Check if crypto currency exist for exchange_id
        Check if balance_amount >= trade_amount
        :param exchange_id:
        :param json:
        :param currency_types: Type = bool, True = crypto, False = fiat
        :return: None if ok Else error message
        """
        # Get currencies list for specific exchange id. For check if crypto currency in trade exist for this exchange id
        currencies_list = DB_crypto_currencies().select_check_currencies_for_exchange_id(exchange_id)

        # If currency in == fiat currency, check if balance amount >= trade amount
        if currency_types['currency_in_crypto'] == False:
            if json['currency_out'] not in currencies_list: return {'message': 'Crypto currency_out doesnt exist in exchange_id: '.format(exchange_id)}, 400
            #balance_check = true/false,converted_amount = trade_amount converted to exchange_id amount

            balance_list = Check_balance.get_compare_balance_amount(exchange_id, json['currency_in'], json['amount'],'fiat')
            #If check balance return tuple with error message and http error return this error
            if isinstance(balance_list,tuple): return balance_list
            #If balance is type list save elements to variables
            balance_check,balance_amount,balance_currency,converted_amount = balance_list

            # If exchange rate was not founded return error message
            if not isinstance(balance_check, bool): return balance_check
            if balance_check == False: return {'message': 'balance amount < trade amount'},400
        # If currency_out == crypto currency, check if balance-amount >= trade amount
        else:
            if json['currency_in'] not in currencies_list: return {'message': 'Crypto currency_in doesnt exist in exchange_id'}, 400
            # balance_check = true/false,converted_amount = trade_amount converted to exchange_id amount
            balance_check,balance_amount,balance_currency,converted_amount = Check_balance.get_compare_balance_amount(exchange_id, json['currency_in'], json['amount'], 'crypto')
            if not isinstance(balance_check, bool): return balance_check
            if balance_check == False: return {'message': 'balance amount < trade amount'},400

        return [balance_check,balance_amount,balance_currency,converted_amount]


    @staticmethod
    def get_compare_balance_amount(exchange_id,currency_in,amount,type):
        """
        Check if amount of fiat currency is bigger than trade amount
        :param exchange_id:
        :param currency_in:
        :param amount: trade amount
        :param type: Type of currency balance check. 'fiat' or 'crypto'
        :return: If amount of trade <= balance_amount return True else False
        """
        if type == 'fiat':
            currency_balance,amount_balance = DB_exchanges().select_check_exchange(exchange_id)
        else: # 'crypto'
            currency_balance, amount_balance = DB_crypto_currencies().select_check_balance_amount(exchange_id,currency_in)
            exchange_currency = DB_exchanges().select_check_exchange(exchange_id)[0]
            #If fiat currency out != exchange currency then convert it to exchange currency

        #IF exchange_currency != trade_currency convert amount to exchange_currency
        if currency_balance != currency_in:
            try:
                exchange_rate = Get_currency_api.get_crypto_rate(currency_in,currency_balance)['rate']
            except KeyError:
                return {'message': 'exchange rate was not founded'}, 400
            converted_amount = float(float(amount) * exchange_rate)
            result = True if converted_amount <= amount_balance else False
        #If exchange_currency == trade_currency
        else:
            converted_amount = amount
            result = True if amount <= amount_balance else False
        #convert amount_balance from decimal to float (json cannot obtain decimal type)
        return [result,float(amount_balance),currency_balance,converted_amount]

class Trade_update_DB():

    @staticmethod
    def trade_update(json,type_currency_crypto,converted_amount,exchanged_amount):
        """
        Update DB based on trade subtract/add ammount to DB crypto amount and exchange amount

        :param json: Posted json + exchange_id
        :param type_currency_crypto: IF currency_in == crypto then True ELIF currency_in == fiat then False
        :param converted_amount: converted currency_in amount to exchange currency amount
        :param exchanged_amount: converted currency_out amount
        :return:
        """

        #If currency in = Fiat currency then subtract converted fiat amount from DB exchanges AND add crypto amount to crypto currency for specific exchange id
        if type_currency_crypto['currency_in_crypto'] == False:
            DB_trades().update_amount_trade_exchange(json['exchange_id'],converted_amount,'-')
            DB_trades().update_amount_trade_crypto(json['exchange_id'],json['currency_out'],exchanged_amount,'+')
        #If currency in = Crypto then subtract crypto amount from DB crypto_currencies AND add fiat converted fiat amount to DB exchanges for specific exchange id
        else:
            DB_trades().update_amount_trade_exchange(json['exchange_id'],exchanged_amount,'+')
            DB_trades().update_amount_trade_crypto(json['exchange_id'],json['currency_in'],converted_amount,'-')

class Trade_history_model:
    @staticmethod
    def validate_parameters(json):
        #convert offset,limit,exchange_id to int
        try:
            if json['offset'] != None: json['offset'] = int(json['offset'])
            if json['limit'] != None: json['limit'] = int(json['limit'])
            if json['exchange_id'] != None: json['exchange_id'] = int(json['exchange_id'])
        except ValueError:
            return {'message':'offset,limit,exchange_id must be integer'},400

        #Validate date parameters. If correct convert date parameters from str to datetime
        json = Trade_history_model.validate_date_parameters(json)
        #If returned tuple with error message and http error return this error message
        if isinstance(json,tuple): return json

        json_values = [value for value in json.values()]
        if (len(set(json_values)) == 1) and (None in set(json_values)):
            data_history = DB_trades().select_all_trade_history()
        else:
            data_history = DB_trades().select_trade_history(json)

        return data_history

    @staticmethod
    def validate_date_parameters(json):
        """
        Validate date_to and date_from parameters
        Convert date_to and date_from from str to datetime type
        Date format allowed: d.m.Y or d/m/Y

        :param json:
        :return: json with converted date parameters to datetime or error message + http error 400
        """
        # Convert date_from and date_to to datetime format
        try:
            if json['date_from'] != None:
                json['date_from'] = dt.strptime(json['date_from'], '%d.%m.%Y')
            if json['date_to'] != None:
                json['date_to'] = dt.strptime(json['date_to'], '%d.%m.%Y')
        except ValueError:
            try:
                if (json['date_from'] != None and (json['date_to'] != None)):
                    if not isinstance(json['date_from'], str) or not isinstance(json['date_to'], str): return {'message': 'Dates must be in same format d.m.Y or d/m/Y'}, 400
                if json['date_from'] != None:
                    json['date_from'] = dt.strptime(json['date_from'], '%d/%m/%Y')
                if json['date_to'] != None:
                    json['date_to'] = dt.strptime(json['date_to'], '%d/%m/%Y')
            except ValueError:
                return {'message': 'Date must be in format d.m.Y or d/m/Y ex. 18.12.2019'},400
        if (json['date_from'] != None) and (json['date_to'] != None):
            if json['date_from'] > json['date_to']:
                return {'message': 'date from must be lower than date to'}, 400

        return json



#print(Trade_history().validate_parameters({'offset': '2', 'limit': '15', 'exchange_id': '1', 'search': 'B', 'date_from': '5.11.2019', 'date_to': None}))

#Trade_history().validate_parameters({'offset': None, 'limit': None, 'exchange_id': None, 'search': None, 'date_from': None, 'date_to': None})




