import requests
from models.others import *

class Add_exchange_model():
    def __init__(self,fiat_list = None,crypto_list = None):
        self.currency_list = fiat_list
        self.crypto_list = crypto_list

    def add_crypto_exchange(self,json):
        """
        Validated inputted json
        Conditions:
        - json must include two keys (name,currency)
        - length of currency must be 3 characters
        :param json: json to validate
        :return: Validated json or None
        """

        if len(json.keys()) > 2:
            return {'message': 'Too much keys in json. Allowed keys = (name,currency)'}
        if len(json.keys()) < 2:
            return {'message': 'Small amount of keys in json. Allowed keys = (name,currency)'}
        #Validate keys of posted JSON
        if ('name' in json) and ('currency' in json):
            if not (isinstance(json['name'],str) and (isinstance(json['currency'],str))):
                return {'message': 'name and currency must be string'}
            #Check if inputted name is correct and delete whitespaces + capitalize text
            correcting_name = Correct_string.string_corrections(json['name'])
            if correcting_name == None:
                return {'message':'Cannot use special characters for name, only underscore is allowed. Minimum length of name = 1'}
            #Set corrected and validated name to json
            json['name'] = correcting_name
            # Change currency to upper case
            json['currency'] = json['currency'].upper()

            if json['currency'] in self.currency_list:
                #Return validated JSON
                return json

            elif len(json['currency']) != 3:
                return {'message': 'Currency can be only 3 length character'}
            elif json['currency'] not in self.currency_list:
                return {'message': "Currency - '" + json['currency'] + "' doesnt exist"}

        elif 'name' not in json:
            return {'message': 'Key name is missing'}
        elif 'currency' not in json:
            return {'message': 'Key currency is missing'}

    def deposit_exchange(self,json):
        """
        Validate json input for deposit
        :param json:
        :return: error message or Success
        """
        if ('currency' in json) and ('amount' in json):
            if not (isinstance(json['currency'],str)):
                return {'message':'Currency must be string'}
            json['currency'] = json['currency'].upper()

            try:
                json['amount'] = float(json['amount'])
            except ValueError:
                return {'message':'Amount must be float'}

            if len(json['currency']) != 3:
                return {'message':'Currency can be only 3 length character'}
            if json['currency'] not in self.currency_list:
                return {'message':'Currency doesnt exists'}
            #Return validated json
            return json
        else:
            return {'message':'Keys can be only currency and amount'}

    def deposit_convert_currency(self,deposit_currency,exchange_currency,amount):
        """
        Before deposit amount to exchange_id convert this amount to specific currency for exchange_id
        :param deposit_currency:
        :param exchange_currency:
        :param amount: amount in deposited currency
        :return: converted amount to exchange id currency
        """
        #If currencies are same return amount
        if deposit_currency == exchange_currency:
            return amount
        rate = Get_currency_api.get_fiat_rate(deposit_currency,exchange_currency)
        converted_amount = float(amount) * float(rate)
        return float(converted_amount)



