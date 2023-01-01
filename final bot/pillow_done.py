from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
import pytz
from datetime import datetime, timedelta, timezone
import requests
import pandas as pd
from newsapi import NewsApiClient
import urllib
import configer
import os
url_im = "https://img5.goodfon.ru/original/1366x768/f/16/abstraktsiia-linii-sirenevyi-rozovyi-tsvet-oblaka-tuchi-otte.jpg"
image_file = urllib.request.urlopen(url_im)
new_im = Image.open(image_file)
new_im.save('fon.png')

heh = Image.open('C:/Users/artem/Downloads/fon.png') #Вставка фона
(width, height) = heh.size
a = (width, height)
heh.save('C:/Users/artem/Downloads/fon.png')

fg = Image.open('C:/Users/artem/Downloads/newfon21.png').resize((1920, 1080), Image.ANTIALIAS) #Вставка шаблона
(width, height) = fg.size
b = (width, height)

if a >= b:
	print("Подходит")
	heh = heh.resize((1920, 1080))
	inp = input('Введите название города: ')
	heh.paste(fg,mask=fg)
	# Вывод погоды
	def meme():
		config_dict = get_default_config()
		config_dict['language'] = 'ru'

		place = inp
		owm = OWM(configer.token_pyow, config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather
		tz = timezone(timedelta(days = 0))
		dtz = datetime.now(tz = tz).strftime("%m/%d/%Y, %H:%M:%S")

		t = w.temperature("celsius")
		t1 = t['temp']
		t2 = t['feels_like']
		t3 = t['temp_max']
		t4 = t['temp_min']

		wi = w.wind()['speed']
		humi = w.humidity
		cl = w.clouds
		st = w.status
		dt = w.detailed_status
		ti = w.reference_time('iso')
		pr = w.pressure['press']
		vd = w.visibility_distance

		a = "В городе " + str(place) + " температура сейчас " + str(t1) + " °C" + "\n\n"
		a += "Ощцщается как" + str(t2) + " °C" + "\n\n"
		a += "Скорость ветра " + str(wi) + " м/с" + "\n\n"
		a += "Давление " + str(pr) + " мм.рт.ст" + "\n\n"
		a += "Влажность " + str(humi) + " %" + "\n\n"
		a += "Описание: " + str(dt) + "\n\n"
		a += "Таймзона: " + str(dtz)

		pogoda = a
		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=28)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((50, 300), pogoda, font=font, fill='#ffffff')
	meme()
	# Вывод даты
	def meme_1():
		tz = pytz.timezone('Europe/Moscow')
		current_date = datetime.now(tz).date().strftime("%d.%m.%Y")
		data = current_date

		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=36)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((50, 50), data, font=font, fill='#ffffff')
	meme_1()
	# Вывод курса
	def meme_2():
	#переменные валют
		dollar = "USD" 
		euro = "EUR"
		rubl = "RUB"
		#токен сайта с которого идёт курс
		access_key = configer.token_money
		#парсинг состояния
		res_d = requests.get("https://openexchangerates.org/api/latest.json?app_id=" + access_key,
		                    params={"base": "USD", "symbols": dollar})
		res_r = requests.get("https://openexchangerates.org/api/latest.json?app_id=" + access_key,
		                    params={"base": "USD", "symbols": rubl})
		res_e = requests.get("https://openexchangerates.org/api/latest.json?app_id=" + access_key,
		                    params={"base": "USD", "symbols": euro})

		if res_d.status_code != 200 or res_r.status_code != 200 or res_e.status_code != 200:
		    raise Exception("ERROR: API request unsuccessful.")
		#счёт валют        
		data_d = res_d.json()
		data_r = res_r.json()
		data_e = res_e.json()

		rate_d = data_d["rates"][dollar]
		rate_r = data_r["rates"][rubl]
		rate_e = data_e["rates"][euro]
		rate = round((rate_r / rate_d), 2)
		rate1 = round((rate_r / rate_e), 2)

		x = (f"{dollar} = {rate} {rubl}")
		y = (f"{euro} = {rate1} {rubl}")
		kurs = x +'\n' + y

		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=28)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((50, 800), kurs, font=font, fill='#ffffff')
	meme_2()
	#Вывод заметки на день
	def meme_3():
		zametka_text = 'Заметка: '
		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=36)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((1200, 50), zametka_text, font=font, fill='#ffffff')
	meme_3()
	def meme_4():
		zam = str(input('Введите заметку на день: '))
		if len(zam) <= 300:
			zametka = zam[0:30] + "\n\n"
			zametka += zam[30:60] + "\n\n"
			zametka += zam[60:90] + "\n\n"
			zametka += zam[90:120] + "\n\n"
			zametka += zam[120:150] + "\n\n"
			zametka += zam[150:180] + "\n\n"
			zametka += zam[180:210] + "\n\n"
			zametka += zam[210:240] + "\n\n"
			zametka += zam[240:270] + "\n\n"
			zametka += zam[270:300] + "\n\n"
		else:
			print('Превысили максимально количество символо!')
			meme_4()
		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=28)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((1200, 125), zametka, font=font, fill='#ffffff')
	meme_4()
	def meme_5():
	    a = ""
	    newsapi = NewsApiClient(api_key= configer.token_newsss)
	    data = newsapi.get_top_headlines(language='ru', country = "ru", page_size = 5)
	    articles = data["articles"]
	    for y in articles:
	        y = f"{y['title']}"
	        a += f"{y}\n"

	        font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=15)
	        draw_text = ImageDraw.Draw(heh)
	        draw_text.text((100, 160), a, font=font, fill='#ffffff')
	meme_5()
	# Сохранение изображения 
	heh.save('C:/Users/artem/Desktop/Work results/newfon.png')
else:  
	print("Не подходит")
	os.remove('C:/Users/artem/Downloads/fon.png')