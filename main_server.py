from flask import Flask,request,jsonify
from flask_restful import Resource, Api
from models.exchange_model import Add_exchange_model
from models.crypto_currencies_model import Update_crypto_currency_model,Action_crypto_currency_model
from models.trade_model import *
from tests import data

app = Flask(__name__)
# disable strict slahes
app.url_map.strict_slashes = False
api = Api(app)


class Add_crypto_exchange(Resource):
    def post(self):
        #If testing set fiat,crypto list from tests.data
        if app.config['TESTING']: fiat_list, crypto_list = [data.fiat_list, data.crypto_list]
        #Get data from online API
        #else: fiat_list, crypto_list = Get_currency_api.get_all_assets()
        #Get data from module
        fiat_list, crypto_list = [data.fiat_list, data.crypto_list]

        json = request.json
        if json == None: return {'message': 'json input not founded'},400
        #Model validate condition for json
        result = Add_exchange_model(fiat_list,crypto_list).add_crypto_exchange(json)
        if ('name' in result) and ('currency' in result):
            #Insert validated json to DB
            created_object = DB_exchanges().insert_exchange(json,app.config['TESTING'])
            return created_object
        else:
            #Return error message
            return result

class Deposit_exchange(Resource):
    def post(self,exchange_id):
        #If testing set testing data for currencies
        if app.config['TESTING']: fiat_list, crypto_list = [data.fiat_list, data.crypto_list]
        #else: fiat_list, crypto_list = Get_currency_api.get_all_assets()
        #Get data from module
        fiat_list, crypto_list = [data.fiat_list, data.crypto_list]

        json = request.json
        if json == None: return {'message':'json input not founded'},400

        json['exchange_id'] = exchange_id
        #Model validate condition for json
        result = Add_exchange_model(fiat_list,crypto_list).deposit_exchange(json)
        #insert to DB
        if ('currency' in result) and ('amount' in result):
            deposit_object = DB_exchanges().insert_deposit_exchange(json,app.config['TESTING'])
            return deposit_object
        else:
            return result

class Update_crypto_currency(Resource):
    def put(self,exchange_id):
        # If testing set fiat,crypto list from tests.data
        if app.config['TESTING']: fiat_list, crypto_list = [data.fiat_list, data.crypto_list]
        #Get data from online API
        #else: fiat_list, crypto_list = Get_currency_api.get_all_assets()
        #Get data from module
        fiat_list, crypto_list = [data.fiat_list, data.crypto_list]

        json = request.json
        json['exchange_id'] = exchange_id
        validated_json = Update_crypto_currency_model(crypto_list).validate_crypto_currency_input(json)
        #If validate_json return tuple of error message and http error then return message error
        if isinstance(validated_json,tuple): return validated_json

        action_check = Action_crypto_currency_model().set_action_cryptocurrency(validated_json)
        if action_check == 'create':
            #IF favourite was not inputted set to default False
            if 'favourite' not in json: json['favourite'] = False

            message = DB_crypto_currencies().insert_crypto_currency(json,app.config['TESTING'])
            # If inputted exchange_id doesnt exist return error message
            if message != None: return message
        elif action_check == 'delete':
            DB_crypto_currencies().delete_crypto_currency(json)
        elif action_check == 'update':
            DB_crypto_currencies().update_crypto_currency(json)

        all_crypto_currencies = DB_crypto_currencies().select_all_crypto_currencies()
        return jsonify(all_crypto_currencies)

class Create_trade(Resource):
    def post(self,exchange_id):
        #Get data from online API
        #fiat_list, crypto_list = Get_currency_api.get_all_assets()
        #Get data from module
        fiat_list, crypto_list = [data.fiat_list, data.crypto_list]

        json = request.json
        if json == None: return {'message': 'json input not founded'},400

        json['exchange_id'] = exchange_id
        #Currency types - dict with keys currency_in,currency_out. Values = Booelan (True = crypto value, False = Fiat value)

        validated_json = Trade_validate_model(fiat_list,crypto_list).trade_validate_json(json)
        #IF validate json return list then json was validated
        if isinstance(validated_json,list):
            currency_types,validated_json = validated_json
        #IF validated_json == tuple, validated was not successfully return error message and http error
        elif isinstance(validated_json,tuple): return validated_json

        #Check if balance_amount >=  exchange_amount
        balance_check = Check_balance.check_balance(exchange_id,json,currency_types)
        #if balance check is not list type [result,balance_amount,balance_currency,converted_amount] return error message, Else balance check was successfully validate
        if not isinstance(balance_check,list):return balance_check
        result,balance_amount,balance_currency,converted_amount = balance_check

        #Exchange amount from currency_in to currency_out
        exchanged_amount = Convert_currency_trade.convert_currency(json['currency_in'],json['currency_out'],json['amount'],exchange_id,currency_types)

        #If currencies was not found in API return error message
        if not isinstance(exchanged_amount,float): return exchanged_amount
        #Update amounts for exchange and crypto currencies after trade
        Trade_update_DB.trade_update(json,currency_types,converted_amount,exchanged_amount)
        #Get crypto name from crypto_currencies
        json['crypto_name'] = DB_crypto_currencies().select_crypto_name(json['exchange_id'],json['currency_in'],json['currency_out'])
        # Insert trade record to DB
        DB_trades().insert_trade_record(json)

        actual_exchange_currency = DB_trades().select_actual_exchange_amount(currency_types['currency_in_crypto'],exchange_id,json['currency_out'])
        actual_exchange_currency['exchanged_amount'] = exchanged_amount

        return actual_exchange_currency

class Trade_history(Resource):
    def get(self):
        # If testing set fiat,crypto list from tests.data
        """
        Get history of trades from DB.
        Arguments: offset,limit,exchange_id,search (crypto name),date_from,date_to
        :return:
        """
        offset = request.args.get('offset', None)
        limit = request.args.get('limit', None)
        exchange_id = request.args.get('exchange_id', None)
        search = request.args.get('search', None)
        date_from = request.args.get('date_from', None)
        date_to = request.args.get('date_to', None)

        param_dict = {'offset':offset,'limit':limit,'exchange_id':exchange_id,'search':search,'date_from':date_from,'date_to':date_to}
        #Validate parameters and get trades history data from DB
        history_data = Trade_history_model.validate_parameters(param_dict)
        #If return tuple with error message and http error
        if isinstance(history_data,tuple):return history_data

        return jsonify(history_data)



api.add_resource(Add_crypto_exchange,'/exchanges')
api.add_resource(Deposit_exchange,'/exchanges/<int:exchange_id>/')
api.add_resource(Update_crypto_currency,'/exchanges/<int:exchange_id>/currencie/')
api.add_resource(Create_trade,'/exchanges/<int:exchange_id>/trades/')
api.add_resource(Trade_history,'/exchanges/history/')


if __name__ == '__main__':
    app.run(debug=True)
