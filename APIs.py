import requests
import random as rn

# the first 3 APIs don't require tokens. the last one requires free registration to get the token

def get_quote():
    content = requests.get('https://type.fit/api/quotes').json()
    quote_dict = rn.choice(content)
    return quote_dict['text'], quote_dict['author']


def get_dog():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_advice():
    contents = requests.get('https://api.adviceslip.com/advice').json()
    string = contents['slip']['advice']
    return string


def get_weather(when):
    """
    this api is fairly easy.
    just register and get a token from openweathermap.org
    the token id is in the url.
    I think there are limited number of calls you can make per day
    """
    content = requests.get('http://api.openweathermap.org/data/2.5/forecast?'
                           'id=7871496&APPID=b5b0b2d3308fdac038056078fb3ae027').json()
    data = content['list']
    to_return = list()
    for item in data:
        if when in item['dt_txt']:
            to_return.append(f'the weather in krems on {item["dt_txt"]} is:'
                             f'\ntemperature: {round(float(item["main"]["temp"])-273.15,1)}\n'
                             f'real feel: {round(float(item["main"]["feels_like"])-273.15,1)}\n'
                             f'condition: {item["weather"][0]["description"]}')
    if len(to_return) > 2:
        return to_return[0], to_return[len(to_return)//2], to_return[-1]
    elif len(to_return) >= 1:
        return to_return[0]
    else:
        return 'No more updates for today. Check for tomorrow'
