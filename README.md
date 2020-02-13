# Crypto currency exchange API

## Requirments:
1. pip install -r dependencies.txt

## Info:
**Get list of crypto and fiat currencies** - from online API is commented.
Fiat and crypto currencies list getting from module data.py

**exchange rates** getting from online API

## Functions:
### 1. ADD crypto exchange - 
#### Body must contain:

**name** - Unique name, without any special characters only 'underscore' is allowed.Numbers are allowed. ex. First_exchange1

**currency** - Currency in which total amount for exchange will be displayed. Must be 3 letter shortcut of fiat currency ex. 'USD'

ex. ```json "name":First_exchange","currency":"EUR" ```

#### Details:

**Method** = POST

**URL** = /exchanges

**Response** = new created object or error message ex. ```json {"name":First_exchange","currency":"EUR"}```


### 2. Deposit exchange -
#### Body must contain:

**amount -** Float number

**currency -** 3 letter shortcuts of fiat currency. If deposit currency != exchange_id currency convert deposit currency to exchange currency and insert to exchange. ex. 'EUR'     

ex. ```json {"amount":50,"currency":"USD"} ```

#### Details:

**Method** = POST

**URL** = /exchanges/{int:exchange_id}/

**Response** = 'Success' or error message


## 3. Update cryptocurrencies within exchange
#### Body must contain:
**name** or **currency:**

**name** = Crypto name ex. 'Bitcoin'

**currency** = Crypto currency 3 letter shortcut ex. 'BTC'

ex. ```json {"name":"Bitcoin","currency":"BTC"} ```

#### Body can contain:
**favourite** = Boolean True/False. Default = False

ex. ```json {"name":"Bitcoin","currency":"BTC","Favourite":true} ```

#### Actions:
**Inputted name/currency or both of them** - 

**CREATE** If name/currency doesnt exist for exchange_id then create this crypto currency

ex. ```json {"name":"Bitcoin"} ```

**DELETE** If name/currency exist for exchange_id then delete this crypto currency

ex. ```json {"currency":"BTC"} ```

**Inputted name/currency or both of them and favourite** -


**CREATE** If name/currency doesnt exist for exchange_id then create it with custom favourite.

```json {"name":"Bitcoin","Favourite":true} ```

**UPDATE** If name/currency exist for exchange_id then update favourite parameter in DB

```json {"name":"Bitcoin","Favourite":false} ```

#### Details:

**Method** = PUT

**URL** = /exchanges/{int:exchange_id}/currencie

**Response** = All crypto currencies for specific exchange_id or error message

ex. ```json [
  {
    "amount": 0.13147733829748992,
    "curr": "BTC",
    "exchange_id": 77,
    "favourite": false,
    "id": 20,
    "name": "Bitcoin"
  },
  {
    "amount": 0.48218492007340913,
    "curr": "BTC",
    "exchange_id": 79,
    "favourite": false,
    "id": 21,
    "name": "Bitcoin"
  }]```

## 4. Create trade
#### Body must contain:

**amount** - Float number

**currency_in** - 3 letter shortcut fiat/crypto currency

**currency_out** - 3 letter shortcut fiat/crypto currency 

ex. ```json {
	"currency_in":"usd",
	"currency_out":"btc",
	"amount":5000
}```

#### Info:
Cannot convert from fiat to fiat or crypto to crypto. Only fiat to crypto or crypto to fiat is allowed

Check if trade amount <= balance amount

Convert trade fiat to exchange fiat currency

Add/Substract from crypto and exchange based on operation

#### Details:

**Method** = POST

**URL** = /exchanges/{int:exchange_id}/trades

**Response** = traded amount, actual exchange currency amount,exchange currency or error message

ex. ```json {
    "actual_amount": 0.9818410621979138,
    "currency": "BTC",
    "exchanged_amount": 0.491053058849187
}```

## 5. History of trades
#### Parameters:
**offset** - start from

**limit** - max to show

**exchange_id** - unique index

**search** - searching contain text in trade table and column 'name'. ex. ('Bitcoin','B','coin')

**date_from** - trade_date >= date_from

**date_to**  - trade_date <= date_to

#### Details:

**Method** = GET

**URL** = ```URL /history?offset={offset}&limit={limit}&exchange_id={exchange_id}&search={search}&date_from={date_from}&date_to={date_to}```

ex. ```URL http://127.0.0.1:5000/exchanges/history?exchange_id=1&limit=5&offset=2&search=Bi&date_from=5.11.2019&date_to=15.2.2020```

**Response** = list of json records with applied parameters filter

ex. ```json  [
  {
    "amount": 5000.0,
    "curr_in": "USD",
    "curr_out": "BTC",
    "exchange_id": 81,
    "id": 26,
    "name": "Bitcoin",
    "trade_date": "Thu, 13 Feb 2020 18:42:09 GMT"
  },
  {
    "amount": 5.0,
    "curr_in": "USD",
    "curr_out": "BTC",
    "exchange_id": 81,
    "id": 27,
    "name": "Bitcoin",
    "trade_date": "Thu, 13 Feb 2020 18:42:21 GMT"
  },
  {
    "amount": 1.0,
    "curr_in": "USD",
    "curr_out": "BTC",
    "exchange_id": 81,
    "id": 28,
    "name": "Bitcoin",
    "trade_date": "Thu, 13 Feb 2020 18:42:28 GMT"
  }]```



