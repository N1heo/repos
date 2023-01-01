import telebot
from telebot import types
import sqlite3
from pyowm import OWM
from pyowm.utils.config import get_default_config

# Импорт общих данных
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('a01bff19c34db14ebf253e1a3514b7c5', config_dict)
mgr = owm.weather_manager()


# Жи есть
bot = telebot.TeleBot(token = '5076830432:AAGWOmMQSFtRj4zTC9uvVBlAXrM9Qve_r14')
print('Я живой')


# База данных
# Информация о пользователях
def users_settings():
    db = sqlite3.connect('users_settings.db')
    cursor = db.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS users(
        userid INTEGER,
        place TEXT,
        reset TEXT NOT NULL DEFAULT "08:00",
        font TEXT NOT NULL DEFAULT "Шрифт 1",
        category TEXT NOT NULL DEFAULT "None"
    )
    """
    cursor.executescript(query)

# Запуск Data Base для информации о пользователях
users_settings()

# Хранение фона для картинки
def backgrounds():
    db = sqlite3.connect('users_settings.db')
    cursor = db.cursor()
    cursor.row_factory = sqlite3.Row
    
    query1 = """
    CREATE TABLE IF NOT EXISTS backgrounds(
    userid INTEGER,
    background BLOB
    )
    """

    cursor.executescript(query1)

# Запуск Data Base для фона пользователя
backgrounds()


# Оновная Клавиатура
item0 = types.KeyboardButton('🔙 Вернуться на главную страницу')
item1 = types.KeyboardButton('🔙 Вернуться назад в настройки')
item2 = types.KeyboardButton('▶ Запуск')
item3 = types.KeyboardButton('⚙ Настройки')
item4 = types.KeyboardButton('📄 Добавить заметку')

markup = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item2, item3, item4)



# Клавиатура настроек
item5 = types.KeyboardButton('🗺 Указать город')
item6 = types.KeyboardButton('⌚️ Указать время обновлений')
item7 = types.KeyboardButton('💬 Изменить шрифт')
item8 = types.KeyboardButton('🖼 Изменить фон')

markup_settings = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item5, item6, item7, item8, item0)



# Клавиатура городов
city1 = types.KeyboardButton('Москва')
city2 = types.KeyboardButton('Санкт-Петербург')
city3 = types.KeyboardButton('Новосибирск')
city4 = types.KeyboardButton('Екатерингбург')
city5 = types.KeyboardButton('Казань')
city6 = types.KeyboardButton('Нижний Новгород')
city7 = types.KeyboardButton('Челябинск')
city8 = types.KeyboardButton('Омск')
city9 = types.KeyboardButton('Самара')
city10 = types.KeyboardButton('Красноярск')
city11 = types.KeyboardButton('Пермь')
city12 = types.KeyboardButton('Воронеж')

markup_cities = types.ReplyKeyboardMarkup(resize_keyboard = True).add(city1, city2, city3, city4, city5, city6, city7, city8, city9, city10, city11, city12, item1)


# Клавиатура указания времени отправки сообщения
time1 = types.KeyboardButton('1:00')
time2 = types.KeyboardButton('2:00')
time3 = types.KeyboardButton('3:00')
time4 = types.KeyboardButton('4:00')
time5 = types.KeyboardButton('5:00')
time6 = types.KeyboardButton('6:00')
time7 = types.KeyboardButton('7:00')
time8 = types.KeyboardButton('8:00')
time9 = types.KeyboardButton('9:00')
time10 = types.KeyboardButton('10:00')
time11 = types.KeyboardButton('11:00')
time12 = types.KeyboardButton('12:00')



markup_time = types.ReplyKeyboardMarkup(resize_keyboard = True).add(time1, time2, time3, time4, time5, time6, time7, time8, time9, time10, time11, time12, item1)



# Клавиатура выбора шрифтов
font1 = types.KeyboardButton('Шрифт 1')
font2 = types.KeyboardButton('Шрифт 2')
font3 = types.KeyboardButton('Шрифт 3')
font4 = types.KeyboardButton('Шрифт 4')
font5 = types.KeyboardButton('Шрифт 5')
font6 = types.KeyboardButton('Шрифт 6')
font7 = types.KeyboardButton('Шрифт 7')
font8 = types.KeyboardButton('Шрифт 8')
font9 = types.KeyboardButton('Шрифт 9')
font10 = types.KeyboardButton('Шрифт 10')
font11 = types.KeyboardButton('Шрифт 11')
font12 = types.KeyboardButton('Шрифт 12')

correct_font = ['Шрифт 1', 'Шрифт 2', 'Шрифт 3', 'Шрифт 4', 'Шрифт 5', 'Шрифт 6', 'Шрифт 7', 'Шрифт 8', 'Шрифт 9', 'Шрифт 10', 'Шрифт 11', 'Шрифт 12']

markup_fonts= types.ReplyKeyboardMarkup(resize_keyboard = True).add(font1, font2, font3, font4, font5, font6, font7, font8, font9, font10, font11, font12, item1)



# Клавиатура выбора фона
markup_backgrounds = types.ReplyKeyboardMarkup(resize_keyboard = True).add(item1)


# Приветствие бота
@bot.message_handler(commands = ['start'])
def welcome(message):
    global userid
    userid = message.from_user.id
    db = sqlite3.connect('users_settings.db')
    cursor = db.cursor()
    cursor.execute("SELECT userid FROM users WHERE userid = ?", [userid])
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users(userid) VALUES(?)", [userid])
        db.commit()
    cursor.execute("SELECT userid FROM backgrounds WHERE userid = ?", [userid])
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO backgrounds(userid) VALUES(?)", [userid])
        db.commit()
    bot.send_message(message.chat.id, 'Добро пожаловать, <b>{name}</b>!\nЯ - <b>{bot}</b>, позволяющий быстро получать полезную информацию для пользователя по его личным нуждам в одном месте'
        .format(name = message.from_user.first_name, bot = bot.get_me().first_name), parse_mode = 'html', reply_markup = markup)


# Насткройки бота
@bot.message_handler(content_types=['text'])
def settings(message):
    if message.text == "⚙ Настройки":
        msg = bot.send_message(message.chat.id, 'Укажите параметр, в который хотите внести изменения:', reply_markup = markup_settings)
        bot.register_next_step_handler(msg, way)
    elif message.text == "▶ Запуск":
        Bot()
    elif message.text == "🔙 Вернуться назад в настройки":
        msg_settings = bot.send_message(message.chat.id, 'Вы вернулись в настройки ', reply_markup = markup_settings)
        bot.register_next_step_handler(msg_settings, way)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю 🥺')



# Настройки путей бота
@bot.message_handler(content_types=['text'])
def way(message):
    if message.text == "🗺 Указать город":
        msg_cities = bot.send_message(message.chat.id, 'Введите название города: ', reply_markup = markup_cities)
        bot.register_next_step_handler(msg_cities, city_save)
    elif message.text == "⌚️ Указать время обновлений":
        msg_time = bot.send_message(message.chat.id, 'Введите желаемое время для обновлений: ', reply_markup = markup_time)
        bot.register_next_step_handler(msg_time, time_save)
    elif message.text == "💬 Изменить шрифт":
        msg_font = bot.send_message(message.chat.id, 'Выберете желаемый шрифт: ', reply_markup = markup_fonts)
        bot.register_next_step_handler(msg_font, font_save)
    elif message.text == "🖼 Изменить фон":
        msg_background = bot.send_message(message.chat.id, 'Отправьте желаемый фон: ', reply_markup = markup_backgrounds)
        bot.register_next_step_handler(msg_background, background_save)
    elif message.text == "🔙 Вернуться на главную страницу":
        bot.send_message(message.chat.id, 'Вы вернулись на глывную страницу ', reply_markup = markup)
    elif message.text == "🔙 Вернуться назад в настройки":
        msg_settings = bot.send_message(message.chat.id, 'Вы вернулись в настройки ', reply_markup = markup_settings)
        bot.register_next_step_handler(msg_settings, way)
    else:
        msg_error = bot.send_message(message.chat.id, 'Я тебя не понимаю 🥺', reply_markup = markup_settings)
        bot.register_next_step_handler(msg_error, way)


# Сохранение переменной города
def city_save(message):
    try:
        if message.text == '🔙 Вернуться назад в настройки':
            msg_settings = bot.send_message(message.chat.id, 'Вы вернулись в настройки ', reply_markup = markup_settings)
            bot.register_next_step_handler(msg_settings, way)
        else:
            place = message.text
            observation = mgr.weather_at_place(place)
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            cursor.execute("SELECT userid FROM users WHERE userid = ?", [userid])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users(place) VALUES(?)", [place])
                db.commit()
            else:
                cursor.execute("UPDATE users SET place = ? WHERE userid = ?", [place, userid])
                db.commit()
            msg_update = bot.send_message(message.chat.id, 'Город успешно сохранён, вы вернулись в настройки ', reply_markup = markup_settings)
            bot.register_next_step_handler(msg_update, way)
    except:
        city_error = bot.send_message(message.chat.id, 'Я не знаю такого города! ', reply_markup = markup_cities)
        bot.register_next_step_handler(city_error, city_save)

# Сохранение переменной обновления
def time_save(message):
    try:
        if message.text == '🔙 Вернуться назад в настройки':
            msg_settings = bot.send_message(message.chat.id, 'Вы вернулись в настройки ', reply_markup = markup_settings)
            bot.register_next_step_handler(msg_settings, way)
        else:
            reset = message.text
            db = sqlite3.connect('users_settings.db')
            cursor = db.cursor()
            cursor.execute("SELECT userid FROM users WHERE userid = ?", [userid])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users(reset) VALUES(?)", [reset])
                db.commit()
            else:
                cursor.execute("UPDATE users SET reset = ? WHERE userid = ?", [reset, userid])
                db.commit()
            msg_update = bot.send_message(message.chat.id, 'Время успешно сохранено, вы вернулись в настройки ', reply_markup = markup_settings)
            bot.register_next_step_handler(msg_update, way)
    except:
        time_error = bot.send_message(message.chat.id, 'Ошибка формата времени!' + '\n' + 'Введите время ещё раз:', reply_markup = markup_time)
        bot.register_next_step_handler(time_error, time_save)    

# Сохранение переменной шрифта
def font_save(message):   
    if message.text == '🔙 Вернуться назад в настройки':
        msg_settings = bot.send_message(message.chat.id, 'Вы вернулись в настройки ', reply_markup = markup_settings)
        bot.register_next_step_handler(msg_settings, way)
    elif message.text in correct_font:
        font = message.text
        db = sqlite3.connect('users_settings.db')
        cursor = db.cursor()
        cursor.execute("SELECT userid FROM users WHERE userid = ?", [userid])
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users(font) VALUES(?)", [font])
            db.commit()
        else:
            cursor.execute("UPDATE users SET font = ? WHERE userid = ?", [font, userid])
            db.commit()
        msg_update = bot.send_message(message.chat.id, 'Шрифт успешно сохранён, вы вернулись в настройки ', reply_markup = markup_settings)
        bot.register_next_step_handler(msg_update, way)
    else:
        font_error = bot.send_message(message.chat.id, 'Не удалось установить шрифт' + '\n' + 'Укажите шрифт ещё раз:', reply_markup = markup_fonts)
        bot.register_next_step_handler(font_error, font_save)


# Сохранение фона
@bot.message_handler(content_types=['text', 'photo', 'document'])
def background_save(message):
    if message.text == '🔙 Вернуться назад в настройки':
        msg_settings = bot.send_message(message.chat.id, 'Вы вернулись в настройки ', reply_markup = markup_settings)
        bot.register_next_step_handler(msg_settings, way)
    else:
        background = message.photo
        with open(io.BytesIO(background), "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        # with open("fon.png", "rb") as file:
            # cursor.execute("SELECT userid FROM backgrounds WHERE userid = ?", [userid])
            # if cursor.fetchone() is None:
               # cursor.execute("INSERT INTO backgrounds VALUES(?)", [file.read()])
               # db.commit()
            # else:
               # cursor.execute("UPDATE backgrounds SET background = ? WHERE userid = ?", [file.read(), userid])
               # db.commit()
        msg_update = bot.send_photo(message.chat.id, "{photo}".format(photo = bot.get_file(message.photo[0].file_id)), reply_markup = markup_settings)
        bot.register_next_step_handler(msg_update, way)

# Функционал бота
class Bot():
    pass




bot.polling(none_stop=True, interval=0)
