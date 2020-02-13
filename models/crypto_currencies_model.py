from models.others import Correct_string
from db.db_crypto_currencies import DB_crypto_currencies


class Update_crypto_currency_model:
    def __init__(self,crypto_list):
        self.crypto_list = crypto_list

    def validate_crypto_currency_input(self,json):
        """
        Input can be json with one of keys (name,currency) or both of them.
        If both keys was inputted check if name belongs to currency
        If one of them was inputted make validation of input (only underscore of special characters is allowed)
        and input another missing key to json
        :param json:
        :return: validated json/error message
        """

        if ('name' not in json) and ('currency' not in json):
            return {'message':'json must have name or currency key'},400

        #Validate name and currency if both was inputted
        correct = False
        if ('name' in json) and ('currency' in json):
            #Validate name and currency input
            json['name'] = Correct_string.string_corrections(json['name'])
            if json['name'] == None: return {'message':'Name cannot have any special characters only underscore is allowed'},400
            json['currency'] = json['currency'].strip().upper()
            if len(json['currency']) != 3: return {'message':'currency must be 3 character length'},400

            #Validate input currency and name of cryptocurrency
            for asset in self.crypto_list:
                if (asset['asset_id'].upper() == json['currency']) and (asset['name'].capitalize() == json['name']):
                    correct = True

            if correct == False: return {'message': 'wrong input for name or currency'},400

        #Validate name if only name was inputted
        elif ('name' in json) and ('currency' not in json):
            json['name'] = Correct_string.string_corrections(json['name'])
            if json['name'] == None: return {'message': 'Name cannot have any special characters only underscore is allowed'},400

            for asset in self.crypto_list:
                if asset['name'].capitalize() == json['name']:
                    json['currency'] = asset['asset_id'].upper()
                    correct = True

            if correct == False: return {'message':'wrong input for name'},400

        #Validate currency if only currency was inputted
        elif ('name' not in json) and ('currency' in json):
            json['currency'] = json['currency'].strip().upper()
            if len(json['currency']) != 3: return {'message': 'currency must be 3 character length'},400

            for asset in self.crypto_list:
                if asset['asset_id'].upper() == json['currency']:
                    json['name'] = asset['name'].capitalize()
                    correct = True

            if correct == False: return {'message':'wrong input for currency'},400

        # if 'favourite' not in json:
        #     json['favourite'] = False

        if correct == True: return json

class Action_crypto_currency_model:
    def __init__(self,crypto_list = None):
        self.crypto_list = crypto_list

    def set_action_cryptocurrency(self,json):
        """
        IF crypto currency not in DB for specific exchange id then create it
        ELIF crypto currency already in DB and json obtain key 'favourite' then update favourite column in DB for specific exchange id
        ELIF crypto currency in DB and json obtain only NAME or CURRENCY or both of them then delete this currency for specific exchange id
        :param json: validated input json
        :return: action (create,update,delete)
        """

        #Return currency and favourite from DB, If crypto currency doesnt exist yet return None
        crypto_exist_check = DB_crypto_currencies().select_check_existed_currency(json['exchange_id'],json['currency'])

        if crypto_exist_check == None:
            return 'create'
        #If crypto currency is already in DB and favourite of input is not same as favourite boolean in DB then update favourite column
        elif ((crypto_exist_check != None) and ('favourite' in json)) and ((json['favourite'] != crypto_exist_check[1])):
            return 'update'
        elif (crypto_exist_check != None) and ('favourite' not in json):
            return 'delete'
        else:
            return None
















