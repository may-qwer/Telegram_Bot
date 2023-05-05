import requests
import datetime
from geopy import Nominatim
from pprint import pprint
from dotenv import load_dotenv
import os


load_dotenv()

def weather_from_Bot(city):
#    city = 'saint-petersburg'
    geolocator = Nominatim(user_agent='user')
    loc = geolocator.geocode(city)
    lat = loc.latitude
    lon = loc.longitude
#    lon = float(30.3141)
#    lat = float(59.9386)
#        print('Проверьте введенный город')
    r = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={os.getenv("OPEN_WEATHER_TOKEN")}&units=metric')
    data = r.json()
#    pprint(data)
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    cur_tamp = data['main']['temp']
    wind_speed = data['wind']['speed']
    weather_description = data['weather'][0]['main']
    if weather_description in code_to_smile:
        wb = code_to_smile[weather_description]
    else:
        wb = 'Посмотри, что за окном происходит!'
    len_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunrise']) - datetime.datetime.fromtimestamp(
        data['sys']['sunset'])
    len_of_the_day = str(len_of_the_day)
    len_of_the_day = len_of_the_day[8:]
    today_data = datetime.datetime.now().strftime(f'%H:%M:%S\n%d/%m/%Y')

    weather_forecast = f'{today_data}\n\nПогода в {city}: {wb}\nТемпература: {cur_tamp} C°\nСкорость ветра: {wind_speed}\nПродолжительность часового дня: {len_of_the_day}\n\nХорошего дня!'
    return weather_forecast

if __name__ == '__main__':
   print(weather_from_Bot('saint-peterburg'))