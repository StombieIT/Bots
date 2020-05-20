import telebot
import pyowm
import qrcode
from random import choice, randint
owm = pyowm.OWM(API_key='d081b7559097378ebce3dc627c021ee6', language = 'ru')
bot = telebot.TeleBot("993359169:AAHWFCDsZ3vn-F6EE2tiK8gk_b4vZTdxgcU")
keyboardmain = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardmain.row("/подбрось", "/пароль", "/раскладка", "/ссылка", "/погода", "/QR")
keyboardtranslitlanguage = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardtranslitlanguage.row("Русский", "English")
@bot.message_handler(commands=["начать", "помощь", "start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Cписок команд:\nПодбросить монетку - /flip, /подбрось\nСгенерировать пароль - /password, /пароль\nПоменять раскладку - /layout, /раскладка\nПолучить ссылку на скачивание видеоролика YouTube - /link, /ссылка\nПосмотреть погоду - /weather, /погода\nСгенерировать QR код - /QR", reply_markup=keyboardmain)
#Монетка
@bot.message_handler(commands=["flip", "подбрось"])
def flip_coin(message):
    flip = choice([True, False])
    if flip == True:
        bot.reply_to(message, "Выпал орёл.")
    elif flip == False:
        bot.reply_to(message, "Выпала решка.")
#Генератор паролей
@bot.message_handler(commands=["password", "пароль"])
def password_count(message):
    bot.reply_to(message, "Укажите кол-во символов в пароле.")
    bot.register_next_step_handler(message, generate_password)
def generate_password(message):
    letterg = "eyuioaEYUIOA"
    letters = "qwrtpsdfghjklzxcvbnmQWRTPSDFGHJKLZXCVBNM"
    sym = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    num = "0123456789"
    password = ""
    try:
        int(message.text)
    except ValueError:
        bot.reply_to(message, "Обнаружены посторонние символы 🙈.")
    else:
        if int(message.text) <= 4096 and int(message.text) > 0:
            for i in range(int(message.text)):
                if (i % 5 == 0) and (i != 0):
                    password += sym[randint(0, len(sym) - 1)]
                elif i % 2 == 0:
                    password += letters[randint(0, len(letters) - 1)]
                elif i % 3 == 0:
                    password += num[randint(0, len(num) - 1)]
                else:
                    password += letterg[randint(0, len(letterg) - 1)]
            bot.send_message(message.chat.id, "Готово:")
            bot.send_message(message.chat.id, password)
        else:
            bot.reply_to(message, "Некорректно указано кол-во символов 🙈.")
#Транслит
@bot.message_handler(commands=["layout", "раскладка"])
def choose_language(message):
	bot.reply_to(message, "Укажите некорректную раскладку.", reply_markup=keyboardtranslitlanguage)
	bot.register_next_step_handler(message, incorrect_text)
def incorrect_text(message):
    global language
    language = message.text
    language = language.lower()
    if language.startswith("ру") == True:
        bot.send_message(message.chat.id, "Введите текст.")
        bot.register_next_step_handler(message, retranslit)
    elif language.startswith("en") == True:
        bot.send_message(message.chat.id, "Введите текст.")
        bot.register_next_step_handler(message, retranslit)
    else:
        bot.reply_to(message, "Некорректно указана раскладка.")
def retranslit(message):
    resmessage = ""
    ru = "ё1234567890-=йцукенгшщзхъфывапролджэ\\ячсмитьбю.Ё!\"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ, \n"
    en = "`1234567890-=qwertyuiop[]asdfghjkl;'\\zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>? \n"
    for i in message.text:
        if language.startswith("ру") == True:
            try:
                resmessage += en[ru.index(i)]
            except ValueError:
                resmessage += i
        else:
            try:
                resmessage += ru[en.index(i)]
            except ValueError:
                resmessage += i
    bot.send_message(message.chat.id, "Готово:\n")
    bot.send_message(message.chat.id, resmessage)
#Перевод ссылок для скачивания
@bot.message_handler(commands=["ссылка", "link"])
def link_read(message):
    bot.reply_to(message, "Укажите ссылку на видеоролик.")
    bot.register_next_step_handler(message, link_generator)
def link_generator(message):
    if message.text.startswith("https://www.") == True:
        link = copy_to_len(message.text, ".")
        if link.startswith("youtube.com") == True:
            bot.send_message(message.chat.id, "Готово:")
            bot.send_message(message.chat.id, generate_link(link, "https://www."))
        else:
            bot.reply_to(message, "Некорректно указан домен 🙈.")
    elif message.text.startswith("www.") == True:
        link = copy_to_len(message.text, ".")
        if link.startswith("youtube.com") == True:
            bot.send_message(message.chat.id, "Готово:")
            bot.send_message(message.chat.id, generate_link(link, "www."))
        else:
            bot.reply_to(message, "Некорректно указан домен 🙈.")
    elif message.text.startswith("https://") == True:
        link = copy_to_len(message.text, "/", 2)
        if link.startswith("youtube.com") == True:
            bot.send_message(message.chat.id, "Готово:")
            bot.send_message(message.chat.id, generate_link(link, "https://"))
        else:
            bot.reply_to(message, "Некорректно указан домен 🙈.")
    else:
        bot.reply_to(message, "Некорректно указана ссылка 🙈.")
def copy_to_len(string, sym, pos = 1):
    num = 0
    resstr = ""
    for i in string:
        if num == pos:
            resstr += i
        else:
            if i == sym:
                num += 1
    return resstr
def generate_link(domain, proto):
    domain = proto + "ss" + domain
    return domain
#Погода
@bot.message_handler(commands=['weather', 'погода'])
def weather_answer(message):
    bot.reply_to(message, 'Укажите населённый пункт.')
    bot.register_next_step_handler(message, weather_choose_city)
def weather_choose_city(message):
    city = message.text
    try:
        observation = owm.weather_at_place(city)
    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.reply_to(message, 'Не могу найти указанный населённый пункт 🙈.')
    else:
        weather = observation.get_weather()
        status = weather.get_status()
        temperature = weather.get_temperature('celsius')['temp']
        wind = weather.get_wind('meters_sec')['speed']
        humidity = weather.get_humidity()
        if status == 'Clouds':
            status = 'облачно'
        elif status == 'Clear':
            status = 'ясно'
        elif status == 'Rain':
            status = 'идёт дождь'
        elif status == 'Snow':
            status = 'идёт снег'
        bot.send_message(message.chat.id, 'Погода в ' + city + ':\nСейчас ' + status + '.\nТемпература составляет ' + str(temperature) + ' °C.\nСкорость ветра составляет ' + str(wind) + ' м/с.\nВлажность воздуха составляет ' + str(humidity) + ' %.')      
#QR код
@bot.message_handler(commands=['QR'])
def qr_answer(message):
    bot.reply_to(message, 'Укажите текст, содержащий не более 256 символов.')
    bot.register_next_step_handler(message, qr_generate)
def qr_generate(message):
    if len(message.text) <= 256:
        image = qrcode.make(message.text)
        image.save('qrcode.png')
        byte = open('qrcode.png', 'rb')
        bot.send_message(message.chat.id, 'Готово:')
        bot.send_photo(message.chat.id, byte)
        byte.close()
    else:
        bot.reply_to(message, 'Превышено максимальное допустимое количество символов 🙈.')
#Авто-ответ
@bot.message_handler(content_types=["text"])
def answer(message):
    bot.send_message(message.chat.id, "Не понял 😕.\nНапишите \"/помощь\", чтобы посмотреть список команд.")
bot.polling()
