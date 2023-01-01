from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pandas as pd
from newsapi import NewsApiClient
from googletrans import Translator
import randfacts
import pytz
import time
import urllib
import sqlite3
import pathlib
import configer
import requests
import base64
import json
from io import BytesIO
from random import randint
import wikipedia, re

# ---------- База данных ----------
# --- Информация о пользователе ---
def users_settings():
    db = sqlite3.connect('users_settings.db')
    cursor = db.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS users(
        userid INTEGER,
        place TEXT,
        font TEXT NOT NULL DEFAULT "Шрифт 1",
        link TEXT NOT NULL DEFAULT "https://i.ibb.co/B4SZ8Kp/fon.png",
        fg TEXT NOT NULL DEFAULT "",
        zametka TEXT NOT NULL DEFAULT "Заметка на день не установлена",
        category TEXT NOT NULL DEFAULT "None",
        fact TEXT NOT NULL DEFAULT "Нет"
    )
    """
    cursor.executescript(query)
users_settings()

# ----- Глобальные переменные -----
bot = Bot(token=configer.token_tg)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('a01bff19c34db14ebf253e1a3514b7c5', config_dict)
mgr = owm.weather_manager()
wikipedia.set_lang("ru")

# ------ Хранение состояний ------
class register(StatesGroup):
    test1 = State()
    test2 = State()
    test3 = State()
    test4 = State()
    test5 = State()
    test6 = State()
    test7 = State()
    test8 = State()
    test9 = State()
# ----- Встроенные клавиатуры ------
# ------- Оновная Клавиатура -------
item0 = types.KeyboardButton('🔙 Вернуться на главную страницу')
item1 = types.KeyboardButton('🔙 Вернуться назад в настройки')
item2 = types.KeyboardButton('▶ Сгенерировать')
item3 = types.KeyboardButton('⚙ Настройки')
item4 = types.KeyboardButton('📄 Добавить заметку')
item9 = types.KeyboardButton('🎲 Дополнительный функционал')

markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True).add(item2, item3, item4, item9)

markup_cansel = types.ReplyKeyboardMarkup(resize_keyboard=True).add(item0)

# ------ Клавиатура настроек ------
item5 = types.KeyboardButton('🗺 Указать город')
item7 = types.KeyboardButton('💬 Изменить шрифт')
item8 = types.KeyboardButton('🖼 Изменить фон')
item10 = types.KeyboardButton('📰 Категория новостей')
item11 = types.KeyboardButton('➕ Добавить факт дня')
item12 = types.KeyboardButton('➖ Удалить факт дня')

markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True).add(item5, item7, item8, item10, item11, item0)

# ------ Клавиатура городов ------
city1 = types.KeyboardButton('Москва')
city2 = types.KeyboardButton('Санкт-Петербург')
city3 = types.KeyboardButton('Новосибирск')
city4 = types.KeyboardButton('Екатеринбург')
city5 = types.KeyboardButton('Казань')
city6 = types.KeyboardButton('Нижний Новгород')
city7 = types.KeyboardButton('Челябинск')
city8 = types.KeyboardButton('Омск')
city9 = types.KeyboardButton('Самара')
city10 = types.KeyboardButton('Красноярск')
city11 = types.KeyboardButton('Пермь')
city12 = types.KeyboardButton('Воронеж')

markup_cities = types.ReplyKeyboardMarkup(resize_keyboard=True).add(city1, city2, city3, city4, city5, city6, city7,city8, city9, city10, city11, city12, item1)

# ------ Клавиатура доп функций ------
dlc1 = types.KeyboardButton('🎰 Рандомное число')
dlc2 = types.KeyboardButton('📀 Игра в "Монетку"')
dlc3 = types.KeyboardButton('📖 Википедия')

markup_dlc = types.ReplyKeyboardMarkup(resize_keyboard=True).add(dlc1, dlc2, dlc3, item0)

# ------ Клавиатура шрифтов ------
font1 = types.KeyboardButton('Шрифт 1')
font2 = types.KeyboardButton('Шрифт 2')
font3 = types.KeyboardButton('Шрифт 3')
font4 = types.KeyboardButton('Шрифт 4')
font5 = types.KeyboardButton('Шрифт 5')
font6 = types.KeyboardButton('Шрифт 6')
font7 = types.KeyboardButton('Шрифт 7')
font8 = types.KeyboardButton('Шрифт 8')
font9 = types.KeyboardButton('Шрифт 9')

correct_font = ['Шрифт 1', 'Шрифт 2', 'Шрифт 3', 'Шрифт 4', 'Шрифт 5', 'Шрифт 6', 'Шрифт 7', 'Шрифт 8', 'Шрифт 9', 'Шрифт 10', 'Шрифт 11', 'Шрифт 12']

Comic_CAT = '../TelegramBot/other/Comic_CAT.otf'

output_font = {'Шрифт 1': Comic_CAT}

def output_font1():
    global font_12
    db = sqlite3.connect('users_settings.db')
    cursor = db.cursor()
    get_font = cursor.execute("SELECT font FROM users WHERE userid = ?", [userid]).fetchone()[0] # тут сейчас 'Шрифт 1'
    font_12 = output_font.get(get_font)

    # Comic_Cat = '../TelegramBot/other/Comic_CAT.otf'

markup_fonts = types.ReplyKeyboardMarkup(resize_keyboard=True).add(font1, font2, font3, font4, font5, font6, font7, font8, font9, item1)

# ------- Клавиатура фонов -------
markup_backgrounds = types.ReplyKeyboardMarkup(resize_keyboard=True).add(item1)

# ------ Клваиатура новостей ------
news1 = types.KeyboardButton('Бизнес')
news2 = types.KeyboardButton('Развлечения')
news3 = types.KeyboardButton('Здоровье')
news4 = types.KeyboardButton('Наука')
news5 = types.KeyboardButton('Спорт')
news6 = types.KeyboardButton('Технологии')
news7 = types.KeyboardButton('Вывод любых новостей')

correct_news = ['Бизнес', 'Развлечения', 'Здоровье', 'Наука', 'Спорт', 'Технологии']

markup_news = types.ReplyKeyboardMarkup(resize_keyboard=True).add(news1, news2, news3, news4, news5, news6, news7)

# -------- Приветствие бота --------
@dp.message_handler(commands=['start'])
async def welcome(message):
    global userid
    userid = message.from_user.id
    db = sqlite3.connect('users_settings.db')
    cursor = db.cursor()
    cursor.execute("SELECT userid FROM users WHERE userid = ?", [userid])
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users(userid) VALUES(?)", [userid])
        db.commit()
    await message.answer('Привет, я .daily Telebot!', reply_markup=markup_start)

# -------- Насткройки бота --------
@dp.message_handler(text=['▶ Сгенерировать', '⚙ Настройки', '🔙 Вернуться назад в настройки', '🔙 Вернуться на главную страницу',
                    '➕ Добавить факт дня', '➖ Удалить факт дня'], content_types=['photo', 'text'])
async def settings(message: types.Message):
    global markup_settings
    db = sqlite3.connect('users_settings.db')
    cursor = db.cursor()
    proverka = cursor.execute("SELECT fact FROM users WHERE userid = ?", [userid]).fetchone()[0]
    if proverka == 'Да':
        markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True).add(item5, item7, item8, item10, item12, item0)
    else:
        markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True).add(item5, item7, item8, item10, item11, item0)
    if message.text == '⚙ Настройки':
        await message.answer("Укажите параметр, в который хотите внести изменения:", reply_markup=markup_settings)
    elif message.text == "🔙 Вернуться назад в настройки":
        await message.answer('Вы вернулись в настройки ', reply_markup=markup_settings)
    elif message.text == "🔙 Вернуться на главную страницу":
        await message.answer('Вы вернулись на главную страницу', reply_markup=markup_start)
    elif message.text == "▶ Сгенерировать":
        output_font1()
        start()
        await bot.send_photo(message.chat.id, photo = photo)
        db = sqlite3.connect('users_settings.db')
        cursor = db.cursor()
        cursor.execute("UPDATE users SET zametka = ? WHERE userid = ?", ['Заметка на день не установлена', userid])
        db.commit()
    elif message.text == "📰 Категория новостей":
        await message.answer('Укажите категорию получаемых новостей', reply_markup=markup_settings)
    elif message.text == "➕ Добавить факт дня":
        markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True).add(item5, item7, item8, item10, item12, item0)
        await message.answer('Факт дня добавлен на картинку', reply_markup=markup_settings)
        db = sqlite3.connect('users_settings.db')
        cursor = db.cursor()
        cursor.execute("UPDATE users SET fact = ? WHERE userid = ?", ['Да', userid])
        db.commit()
    elif message.text == "➖ Удалить факт дня":
        markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True).add(item5, item7, item8, item10, item11, item0)
        await message.answer('Факт дня удалён с картинки', reply_markup=markup_settings)
        db = sqlite3.connect('users_settings.db')
        cursor = db.cursor()
        cursor.execute("UPDATE users SET fact = ? WHERE userid = ?", ['Нет', userid])
        db.commit()


# -------Сохранение заметки -------
@dp.message_handler(text=['📄 Добавить заметку'])
async def zametka_register(message: types.Message):
    await message.answer('Введите заметку на сутки:', reply_markup=markup_cansel)
    await register.test4.set()

@dp.message_handler(state=register.test4)
async def zametka(message: types.Message, state: FSMContext):
    if message.text == '🔙 Вернуться на главную страницу':
        await settings(message)
        await state.finish()
    else:
        answer4 = message.text
        await state.update_data(test4=answer4)
        data_zametka = await state.get_data()
        zametka = data_zametka.get('test4')
        if len(zametka) <= 300:
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            cursor.execute(
                "SELECT userid FROM users WHERE userid = ?", [userid])
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO users(zametka) VALUES(?)", [zametka])
                db.commit()
            else:
                cursor.execute("UPDATE users SET zametka = ? WHERE userid = ?", [zametka, userid])
                db.commit()
            await message.answer('Заметка успешно сохранена, вы вернулись на главную страницу', reply_markup=markup_start)
        else:
            await message.answer('Некоректный ввод', reply_markup=markup_start)
        await state.finish()

# ------- Сохранение города -------
@dp.message_handler(text=['🗺 Указать город'])
async def place_register(message: types.Message):
    await message.answer('Укажите название города', reply_markup=markup_cities)
    await register.test1.set()

@dp.message_handler(state=register.test1)
async def place(message: types.Message, state: FSMContext):
    try:
        if message.text == '🔙 Вернуться назад в настройки':
            await settings(message)
            await state.finish()
        else:
            answer1 = message.text
            await state.update_data(test1=answer1)
            data_place = await state.get_data()
            place = data_place.get('test1')
            observation = mgr.weather_at_place(place)
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            cursor.execute(
                "SELECT userid FROM users WHERE userid = ?", [userid])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users(place) VALUES(?)", [place])
                db.commit()
            else:
                cursor.execute(
                    "UPDATE users SET place = ? WHERE userid = ?", [place, userid])
                db.commit()
            await message.answer('Город успешно сохранён, вы вернулись в настройки ', reply_markup=markup_settings)
            await state.finish()
    except:
        await message.answer('Я не знаю такого города :(', reply_markup = markup_settings)
        await state.finish()

# ------- Сохранение шрифта -------
@dp.message_handler(text=['💬 Изменить шрифт'])
async def font_register(message: types.Message):
    await message.answer('Выберете шрифт', reply_markup=markup_fonts)
    await register.test3.set()

@dp.message_handler(state=register.test3)
async def font(message: types.Message, state: FSMContext):
    if message.text == '🔙 Вернуться назад в настройки':
        await settings(message)
        await state.finish()
    else:
        answer3 = message.text
        if answer3 in correct_font:
            await state.update_data(test3=answer3)
            data_font = await state.get_data()
            font = data_font.get('test3')
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            cursor.execute("SELECT userid FROM users WHERE userid = ?", [userid])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users(font) VALUES(?)", [font])
                db.commit()
            else:
                cursor.execute("UPDATE users SET font = ? WHERE userid = ?", [font, userid])
                db.commit()
            await message.answer('Шрифт успешно сохранён, вы вернулись в настройки ', reply_markup=markup_settings)
            await state.finish()
        else:
            await message.answer('Я не знаю такого шрифта :(', reply_markup=markup_settings)
            await state.finish()

# -------- Сохранение фона --------
@dp.message_handler(text=['🖼 Изменить фон'])
async def link_register(message: types.Message):
    await message.answer('Загрузите фон:', reply_markup=markup_backgrounds)
    await register.test5.set()

@dp.message_handler(content_types=['photo', 'text'], state=register.test5)
async def link_save(message: types.Message, state: FSMContext):
    if message.text == '🔙 Вернуться назад в настройки':
        await settings(message)
        await state.finish()
    else:
        await state.finish()
        api_key = '4574c73620e082ee4c01b3ad34914cdd'
        file = await bot.get_file(message.photo[-1].file_id)
        await message.answer('Подождите, идёт обработка фона...', reply_markup=markup_backgrounds)
        time.sleep(2)
        file_url = f'https://api.telegram.org/file/bot5076830432:AAGWOmMQSFtRj4zTC9uvVBlAXrM9Qve_r14/{file.file_path}'
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": api_key,
            "image": file_url,
        }
        res = requests.post(url, payload)
        res = res.json()
        size_width = res['data']['width']
        size_height = res['data']['height']
        if int(size_width) >= 1280 and int(size_height) >= 720:
            link = (res['data']['url'])
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            cursor.execute("SELECT userid FROM users WHERE userid = ?", [userid])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users(link) VALUES(?)", [link])
                db.commit()
            else:
                cursor.execute("UPDATE users SET link = ? WHERE userid = ?", [link, userid])
                db.commit()
            await message.answer('Фон успешно сохранён, вы вернулись в настройки ',
                                 reply_markup=markup_settings)
        else:
            await message.answer('Неподходящий размер фона, попробуйте другое изображение', reply_markup=markup_settings)

# -------- Сохранение категории --------
@dp.message_handler(text=['📰 Категория новостей'])
async def category_register(message: types.Message):
    await message.answer('Укажите категорию получаемых новостей', reply_markup=markup_news)
    await register.test6.set()

@dp.message_handler(content_types=['text'], state=register.test6)
async def category_save(message: types.Message, state: FSMContext):
    if message.text == '🔙 Вернуться назад в настройки':
        await settings(message)
        await state.finish()
    elif message.text =='Вывод любых новостей':
        await state.finish()
        db = sqlite3.connect('users_settings.db')
        cursor = db.cursor()
        cursor.execute("UPDATE users SET category = ? WHERE userid = ?", ['None', userid])
        await message.answer('Вывод любых новостей сохранён, вы вернулись в настройки', reply_markup=markup_settings)
        db.commit()
    else:
        answer6 = message.text
        if answer6 in correct_news:
            await state.update_data(test6=answer6)
            data_category = await state.get_data()
            category = data_category.get('test6')
            if category == 'Бизнес':
                category = 'business'
            if category == 'Развлечения':
                category = 'entertainment'
            if category == 'Здоровье':
                category = 'health'
            if category == 'Наука':
                category = 'science'
            if category == 'Спорт':
                category = 'sports'
            if category == 'Технологии':
                category = 'technology'
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            cursor.execute("SELECT userid FROM users WHERE userid = ?", [userid])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users(category) VALUES(?)", [category])
                db.commit()
            else:
                cursor.execute("UPDATE users SET category = ? WHERE userid = ?", [category, userid])
                db.commit()
            await message.answer('Категория успешно сохранена, вы вернулись в настройки', reply_markup=markup_settings)
            await state.finish()
        else:
            await message.answer('Категория не найдена, вы вернулись в настройки', reply_markup=markup_settings)
            await state.finish()

# ---- Дополнительный функционал ----
@dp.message_handler(text=['🎲 Дополнительный функционал'])
async def additional_func(message):
    await message.answer('Выберете чем хотите воспользоваться', reply_markup=markup_dlc)

@dp.message_handler(text=['🎰 Рандомное число', '📀 Игра в "Монетку"', '📖 Википедия'])
async def additional_func_choose(message):
    if message.text == '🎰 Рандомное число':
        await message.answer('Введите минимальное значение')
        await register.test7.set()
    if message.text == '📀 Игра в "Монетку"':
        await message.answer('Монетка взлетает ввысь...')
        time.sleep(2)
        d = randint(1, 2)
        if d < 2:
            await bot.send_message(message.chat.id, "Выпал Орёл")
        else:
            await bot.send_message(message.chat.id, "Выпала Решка")
    if message.text == '📖 Википедия':
        await message.answer('Отправьте мне любое слово, и я найду его значение на Wikipedia')
        await register.test9.set()
        def getwiki(s):
            try:
                ny = wikipedia.page(s)
                # Получаем первую тысячу символов
                wikitext=ny.content[:1000]
                # Разделяем по точкам
                wikimas=wikitext.split('.')
                # Отбрасываем всЕ после последней точки
                wikimas = wikimas[:-1]
                # Создаем пустую переменную для текста
                wikitext2 = ''
                # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
                for x in wikimas:
                    if not('==' in x):
                            # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                        if(len((x.strip()))>3):
                           wikitext2=wikitext2+x+'.'
                    else:
                        break
                # Теперь при помощи регулярных выражений убираем разметку
                wikitext2=re.sub('\([^()]*\)', '', wikitext2)
                wikitext2=re.sub('\([^()]*\)', '', wikitext2)
                wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
                # Возвращаем текстовую строку
                return wikitext2
            # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
            except Exception as e:
                return 'В энциклопедии нет информации об этом'
        # Получение сообщений от юзера
        @dp.message_handler(content_types=["text"], state=register.test9)
        async def handle_text(message: types.Message, state: FSMContext):
            await state.finish()
            await bot.send_message(message.chat.id, getwiki(message.text))

@dp.message_handler(content_types=['text'], state=register.test7)
async def random_org_a(message: types.Message, state: FSMContext):
    answer7 = message.text
    await state.update_data(test7=answer7)
    await register.next()
    await message.answer('Введите максимальное значение')

@dp.message_handler(content_types=['text'], state=register.test8)
async def random_org_b(message: types.Message, state: FSMContext):
    answer8 = message.text
    await state.update_data(test8=answer8)
    data_a_b = await state.get_data()
    a = int(data_a_b.get('test7'))
    b = int(data_a_b.get('test8'))
    c = randint(a, b)
    await state.finish()
    await bot.send_message(message.chat.id, f"Ваше число:  {c}")

# ---------- Мозг бота ----------
def start():
    global bg
    db = sqlite3.connect('users_settings.db')
    cursor = db.cursor()
    url_im = cursor.execute("SELECT link FROM users WHERE userid = ?", [userid]).fetchone()[0]  # Тут лежит ссылка на фон
    resp = requests.get(url_im, stream=True).raw
    bg = Image.open(resp)  # Вставка фона

    fg = Image.open('../TelegramBot/other/fgg.png').resize((1280, 800), Image.ANTIALIAS)  # Вставка шаблона

    bg = bg.resize((1280, 800))
    # Вывод погоды

    def main():
        global photo
        def weather_1():
            config_dict = get_default_config()
            config_dict['language'] = 'ru'

            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            place = cursor.execute("SELECT place FROM users WHERE userid = ?", [userid]).fetchone()[0]
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
            font = ImageFont.truetype(font_12, size=28)
            draw_text = ImageDraw.Draw(bg)
            draw_text.text((50, 300), pogoda, font=font, fill='#ffffff')

        # Вывод даты
        def date_1():
            tz = timezone(timedelta(days=0))
            current_date = datetime.now(tz=tz).strftime("%d/%m/%Y")
            data = current_date
            font = ImageFont.truetype(font_12, size=36) # '../TelegramBot/other/Comic_CAT.otf'
            draw_text = ImageDraw.Draw(bg)
            draw_text.text((50, 50), data, font=font, fill='#ffffff')
        # Вывод курса

        def exchange_rate_1():
            # переменные валют
            dollar = "USD"
            euro = "EUR"
            rubl = "RUB"
            # токен сайта с которого идёт курс
            access_key = configer.token_money
            # парсинг состояния
            res_d = requests.get("https://openexchangerates.org/api/latest.json?app_id=" + access_key,
                                 params={"base": "USD", "symbols": dollar})
            res_r = requests.get("https://openexchangerates.org/api/latest.json?app_id=" + access_key,
                                 params={"base": "USD", "symbols": rubl})
            res_e = requests.get("https://openexchangerates.org/api/latest.json?app_id=" + access_key,
                                 params={"base": "USD", "symbols": euro})

            if res_d.status_code != 200 or res_r.status_code != 200 or res_e.status_code != 200:
                raise Exception("ERROR: API request unsuccessful.")
            # счёт валют
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
            kurs = x + '\n' + y

            font = ImageFont.truetype(font_12, size=28)
            draw_text = ImageDraw.Draw(bg)
            draw_text.text((50, 800), kurs, font=font, fill='#ffffff')
        # Вывод заметки на день

        def note_1():
            zametka_text = 'Заметка: '
            font = ImageFont.truetype(font_12, size=36)
            draw_text = ImageDraw.Draw(bg)
            draw_text.text((1200, 50), zametka_text, font=font, fill='#ffffff')

        def note_2():
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            zam = cursor.execute("SELECT zametka FROM users WHERE userid = ?", [userid]).fetchone()[0]
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

            font = ImageFont.truetype(font_12, size=28)
            draw_text = ImageDraw.Draw(bg)
            draw_text.text((1000, 125), zametka, font=font, fill='#ffffff')

        def news_1():
            a = ""
            newsapi = NewsApiClient(api_key=configer.token_newsss)
            category_2 = cursor.execute("SELECT category FROM users WHERE userid = ?", [userid]).fetchone()[0]
            if category_2 == 'None':
                data = newsapi.get_top_headlines(language='ru', country="ru", page_size=5)
                articles = data["articles"]
                for y in articles:
                    y = f"{y['title']}"
                    a += f"{y}\n"

                    font = ImageFont.truetype(font_12, size=15)
                    draw_text = ImageDraw.Draw(bg)
                    draw_text.text((100, 160), a, font=font, fill='#ffffff')
            elif category_2 != 'None':
                data = newsapi.get_top_headlines(language='ru', country="ru", page_size=5, category = category_2)
                articles = data["articles"]
                for y in articles:
                    y = f"{y['title']}"
                    a += f"{y}\n"

                    font = ImageFont.truetype(font_12, size=15)
                    draw_text = ImageDraw.Draw(bg)
                    draw_text.text((100, 160), a, font=font, fill='#ffffff')

        def fact_day_1():
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            fact = cursor.execute("SELECT fact FROM users WHERE userid = ?", [userid]).fetchone()[0]
            if fact == 'Да':
                translator = Translator()
                x = randfacts.get_fact()
                a = translator.translate(x, dest='ru')
                b = a.text
                font = ImageFont.truetype(font_12, size=15)
                draw_text = ImageDraw.Draw(bg)
                draw_text.text((50, 700), b, font=font, fill='#ffffff')
            elif fact == 'Нет':
                return
        weather_1()
        date_1()
        exchange_rate_1()
        note_1()
        note_2()
        news_1()
        fact_day_1()
        photo = BytesIO()
        photo.result = bg.paste(fg, mask=fg)
        bg.save(photo, 'PNG')
        photo.seek(0)
    main()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) # on_startup=on_startup skip_updates=True
