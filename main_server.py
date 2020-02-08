from flask import Flask,request,jsonify
from flask_restful import Resource, Api
from db import db_setting
from db.db_exchanges import DB_exchanges
from db.db_crypto_currencies import DB_crypto_currencies
from models.exchange_model import Add_exchange_model
from models.crypto_currencies_model import Update_crypto_currency_model,Action_crypto_currency_model
from models.others import *
from models.trade_model import Trade_validate_model,Convert_currency_trade


app = Flask(__name__)
#disable strict slahes
app.url_map.strict_slashes = False
api = Api(app)
#Get currencies list for fiat and crypto
fiat_list,crypto_list = Get_currency_api.get_all_assets()


class Add_crypto_exchange(Resource):
    def post(self):
        json = request.json
        if json == None: return {'message': 'json input not founded'},400
        #Model validate condition for json
        result = Add_exchange_model(fiat_list,crypto_list).add_crypto_exchange(json)
        if ('name' in result) and ('currency' in result):
            #Insert validated json to DB
            created_object = DB_exchanges().insert_exchange(json)
            return created_object
        else:
            #Return error message
            return result

class Deposit_exchange(Resource):
    def post(self,exchange_id):
        json = request.json
        if json == None: return {'message':'json input not founded'}

        json['exchange_id'] = exchange_id
        #Model validate condition for json
        result = Add_exchange_model(fiat_list,crypto_list).deposit_exchange(json)
        #insert to DB
        if ('currency' in result) and ('amount' in result):
            deposit_object = DB_exchanges().insert_deposit_exchange(json)
            return deposit_object
        else:
            return result

class Update_crypto_currency(Resource):
    def put(self,exchange_id):
        json = request.json
        json['exchange_id'] = exchange_id
        validated_json = Update_crypto_currency_model(crypto_list).validate_crypto_currency_input(json)
        #If error return error message
        if 'message' in validated_json: return validated_json

        action_check = Action_crypto_currency_model().set_action_cryptocurrency(validated_json)
        if action_check == 'create':
            #IF favourite was not inputted set to default False
            if 'favourite' not in json: json['favourite'] = False

            message = DB_crypto_currencies().insert_crypto_currency(json)
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
        json = request.json
        if json == None: return {'message': 'json input not founded'}

        json['exchange_id'] = exchange_id
        currency_types,validated_json = Trade_validate_model(fiat_list,crypto_list).trade_validate_json(json)
        #IF returned error message then return json with error message. Else return validated json
        if 'message' in validated_json: return validated_json
        #Exchange amount from currency_in to currency_out
        exchanged_amount = Convert_currency_trade.convert_currency(json['currency_in'],json['currency_out'],json['amount'])
        #If currencies was not found in API return error message
        if 'message' in exchanged_amount: return exchanged_amount





api.add_resource(Add_crypto_exchange,'/exchanges')
api.add_resource(Deposit_exchange,'/exchanges/<int:exchange_id>/')
api.add_resource(Update_crypto_currency,'/exchanges/<int:exchange_id>/currencie/')
api.add_resource(Create_trade,'/exchanges/<int:exchange_id>/trades/')



if __name__ == '__main__':
    app.run(debug=True)