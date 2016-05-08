import requests
import mytoken

# https://openexchangerates.org/api/convert/19999.95/GBP/EUR?app_id=YOUR_APP_APP_ID


class CcyVars:

    base_url = 'https://openexchangerates.org/api/latest.json'
    amount = 1
    ccy_token = mytoken.getToken('ccy')
    full_url = base_url + '?app_id=' + ccy_token

    def getFull_url(self):
        return self.full_url


def getExchangeRate(base_ccy, to_ccy):
    c = CcyVars
    r = requests.get(c.full_url).json()

    print(r.get('rates'))

    if base_ccy == 'USD':
        rate = r.get('rates').get(to_ccy)
        print(rate)

    elif to_ccy == 'USD':
        rate = 1/r.get('rates').get(base_ccy)

    else:
        # XXX/YYY = 1/(USD/XXX) x (USD/YYY)
        rate1 = 1/r.get('rates').get(base_ccy)
        rate2 = r.get('rates').get(to_ccy)
        rate = rate1 * rate2
    print(rate)

    if rate is None:
            print(to_ccy + ' not found...')


def convertAmount(base_ccy, to_ccy, amount=1):

    newAmount = getExchangeRate(base_ccy, to_ccy) * amount
    return newAmount

def getHelp():
    strHelp = 'Currency from, currency to, amount'
    return strHelp


if __name__ == '__main__':
    getExchangeRate('EUR', 'GBP')
