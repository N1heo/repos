from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sqlite3
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

class Daily_Telebot():
	db = sqlite3.connect('users_settings.db')
	cursor = db.cursor()
	url_im = cursor.execute("SELECT link FROM users WHERE userid = ?", [userid]) # Тут лежит ссылка на фон
	image_file = urllib.request.urlopen(url_im)
	new_im = Image.open(image_file)

	heh = Image.open(new_im) #Вставка фона

	fg = Image.open('C:/Users/artem/Downloads/newfon21.png').resize((1280, 800), Image.ANTIALIAS) #Вставка шаблона

	heh = heh.resize((1280, 800))
	# Вывод погоды
	def meme():
		config_dict = get_default_config()
		config_dict['language'] = 'ru'

		db = sqlite3.connect('users_settings.db')
		cursor = db.cursor()
		place = cursor.execute("SELECT place FROM users WHERE userid = ?", [userid])
		owm = OWM(configer.token_pyow, config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather

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

		pogoda = a
		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=28)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((50, 300), pogoda, font=font, fill='#ffffff')
	# Вывод даты
	def meme_1():
		tz = timezone(timedelta(days = 0))
		current_date = datetime.now(tz = tz).strftime("%m/%d/%Y")
		# current_date = datetime.now(tz).date().strftime("%d.%m.%Y")
		data = current_date

		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=36)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((50, 50), data, font=font, fill='#ffffff')
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
	#Вывод заметки на день
	def meme_3():
		zametka_text = 'Заметка: '
		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=36)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((1200, 50), zametka_text, font=font, fill='#ffffff')
	def meme_4():
		db = sqlite3.connect('users_settings.db')
		cursor = db.cursor()
		zam = cursor.execute("SELECT zametka FROM users WHERE userid = ?", [userid])
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

		font = ImageFont.truetype('C:/Users/artem/Desktop/Sublime/Comic_CAT.otf', size=28)
		draw_text = ImageDraw.Draw(heh)
		draw_text.text((1200, 125), zametka, font=font, fill='#ffffff')
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
	heh.paste(fg,mask=fg)