# Crypto currency exchange API

## Requirments:
1. pip install -r dependencies.txt


## Functions:
### 1. ADD crypto exchange - 
####Body must contain:

**name** - Unique name, without any special characters only 'underscore' is allowed.Numbers are allowed. ex. First_exchange1

**currency** - Currency in which total amount for exchange will be displayed. Must be 3 letter shortcut of fiat currency ex. 'USD'

#### Details:

**Method** = POST

**URL** = /exchanges

**Response** = new created object or error message ex. {"name":First_exchange","currency":"EUR"}


### 2. Deposit exchange -
#### Body must contain:

**amount -** Float number

**currency -** 3 letter shortcuts of fiat currency. If deposit currency != exchange_id currency convert deposit currency to exchange currency and insert to exchange. ex. 'EUR'     


#### Details:

**Method** = POST

**URL** = /exchanges/{int:exchange_id}/

**Response** = 'Success' or error message


## 3. Update cryptocurrencies within exchange
#### Body must contain:
**name** or **currency:**

**name** = Crypto name ex. 'Bitcoin'

**currency** = Crypto currency 3 letter shortcut ex. 'BTC'

#### Body can contain:
**favourite** = Boolean True/False. Default = False

#### Actions:
**Inputted name/currency or both of them** - 

**CREATE** If name/currency doesnt exist for exchange_id then create this crypto currency

**DELETE** If name/currency exist for exchange_id then delete this crypto currency

**Inputted name/currency or both of them and favourite** -

**CREATE** If name/currency doesnt exist for exchange_id then create it with custom favourite.

**UPDATE** If name/currency exist for exchange_id then update favourite parameter in DB

#### Details:

**Method** = PUT

**URL** = /exchanges/{int:exchange_id}/currencie

**Response** = All crypto currencies for specific exchange_id or error message

## 4. Create trade
#### Body must contain:

**amount** - Float number

**currency_in** - 3 letter shortcut fiat/crypto currency

**currency_out** - 3 letter shortcut fiat/crypto currency 

#### Info:
Cannot convert from fiat to fiat or crypto to crypto. Only fiat to crypto or crypto to fiat is allowed

Check if trade amount <= balance amount

Convert trade fiat to exchange fiat currency

Add/Substract from crypto and exchange based on operation

#### Details:

**Method** = POST

**URL** = /exchanges/{int:exchange_id}/trades

**Response** = traded amount, actual exchange currency amount,exchange currency or error message

## 5. History of trades
#### Parameters:
**offset**

**limit**

**exchange_id**

**search** - searching contain text in column name. ex. ('Bitcoin','B','coin')

**date_from**

**date_to** 

#### Details:

**Method** = GET

**URL** = /history?offset={offset}&limit={limit}&exchange_id={exchange_id}&search={search}&date_from={date_from}&date_to={date_to}

**Response** = list of json records with applied parameters filter







