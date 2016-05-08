import requests
from decimal import Decimal
import mytoken

def convertTemp(fahrenheit):

    # (F-32) x 5/9
    C = Decimal((fahrenheit - 32) * (5/9))
    C = round(C, 2)
    C = str(C)
    return C


def getData(lat=51.1324, long=0.2637):
    # TODO put some sort of long lat lookup? yet another API???
    url = 'https://api.forecast.io/forecast/'
    apikey = mytoken.getToken('weather')
    lat = 51.1324
    long = 0.2637

    fullurl = url + apikey + '/' + str(lat) + ',' + str(long)

    print(fullurl)
    r = requests.get(fullurl)

    # print(r.content)
    # print(r.json())
    temp = r.json()['currently']['temperature']
    apptemp = r.json()['currently']['apparentTemperature']
    summary = r.json()['currently']['summary']
    wind = r.json()['currently']['windSpeed']

    temp = convertTemp(temp)
    apptemp = convertTemp(apptemp)

    t_output = 'Temperature: ' + temp + 'C. Feels like: ' + apptemp
    wind = 'Wind: ' + str(wind) + 'mph'

    # print(summary, t_output, wind, sep='\n')
    output = summary + '\n' + t_output + '\n' + wind
    return output


def getHelp():
    strhelp = 'Returns weather right now.\nDefaults to Tunbridge wells, but takes long/lat arguments.'
    return strhelp
