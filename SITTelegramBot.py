#Модули
import telebot
import pyowm
import sqlite3
from qrcode import make
from cv2 import imread
from os import remove
from pyzbar.pyzbar import decode
from random import choice, randint
from datetime import datetime as dt
#Функции
def log(id, command, datetime):
	db = sqlite3.connect('logs.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
		id INT,
		command TEXT,
		datetime TEXT
	)""")
	db.commit()
	sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (id, command, datetime))
	db.commit()
#Токены и прочие настройки
owm = pyowm.OWM(API_key='', language = 'ru')
bot = telebot.TeleBot("")
#Клавиатуры
keyboardmain = telebot.types.ReplyKeyboardMarkup(True)
keyboardmain.row("/подбрось", "/пароль", "/раскладка", "/ссылка", "/погода", "/QR")
keyboardtranslitlanguage = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardtranslitlanguage.row("Русский", "English")
keyboardqr = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardqr.row("Сгенерировать", "Считать")
#Сообщения
@bot.message_handler(commands=["начать", "помощь", "start", "help"])
def send_welcome(message):
    log(message.chat.id, message.text, dt.today())
    bot.reply_to(message, "Cписок команд:\nПодбросить монетку - /flip, /подбрось\nСгенерировать пароль - /password, /пароль\nПоменять раскладку - /layout, /раскладка\nПолучить ссылку на скачивание видеоролика YouTube - /link, /ссылка\nПосмотреть погоду - /weather, /погода\nСгенерировать, считать QR код - /QR", reply_markup=keyboardmain)
#Монетка
@bot.message_handler(commands=["flip", "подбрось"])
def flip_coin(message):
	log(message.chat.id, message.text, dt.today())
	flip = choice([True, False])
	if flip == True:
		bot.reply_to(message, "Выпал орёл.")
	elif flip == False:
		bot.reply_to(message, "Выпала решка.")
#Генератор паролей
@bot.message_handler(commands=["password", "пароль"])
def password_count(message):
	log(message.chat.id, message.text, dt.today())
	bot.reply_to(message, "Укажите необходимое количество символов, не превышающее 32.")
	bot.register_next_step_handler(message, generate_password)
def generate_password(message):
	if str(type(message.text)) == "<class 'str'>":
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
			if int(message.text) > 0:
				if int(message.text) <= 32:
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
					bot.reply_to(message, 'Превышено максимальное допустимое количество символов 🙈.')
			else:
				bot.reply_to(message, "Некорректно указано количество символов 🙈.")
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
#Раскладка
@bot.message_handler(commands=["layout", "раскладка"])
def choose_language(message):
	log(message.chat.id, message.text, dt.today())
	bot.reply_to(message, "Укажите некорректную раскладку.", reply_markup=keyboardtranslitlanguage)
	bot.register_next_step_handler(message, incorrect_text)
def incorrect_text(message):
	if str(type(message.text)) == "<class 'str'>":
		global language
		language = message.text
		if language == 'Русский':
			bot.send_message(message.chat.id, "Введите текст.")
			bot.register_next_step_handler(message, retranslit)
		elif language == 'English':
			bot.send_message(message.chat.id, "Введите текст.")
			bot.register_next_step_handler(message, retranslit)
		else:
			bot.reply_to(message, "Некорректно указана раскладка.")
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
def retranslit(message):
	if str(type(message.text)) == "<class 'str'>":
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
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
#Перевод ссылок для скачивания
@bot.message_handler(commands=["ссылка", "link"])
def link_read(message):
	log(message.chat.id, message.text, dt.today())
	bot.reply_to(message, "Укажите ссылку на видеоролик.")
	bot.register_next_step_handler(message, link_generator)
def link_generator(message):
	if str(type(message.text)) == "<class 'str'>":
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
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
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
	log(message.chat.id, message.text, dt.today())
	bot.reply_to(message, 'Укажите населённый пункт.')
	bot.register_next_step_handler(message, weather_choose_city)
def weather_choose_city(message):
	if str(type(message.text)) == "<class 'str'>":
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
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
#QR код
@bot.message_handler(commands=['QR'])
def qr_answer(message):
	log(message.chat.id, message.text, dt.today())
	bot.reply_to(message, 'Укажите действие.', reply_markup=keyboardqr)
	bot.register_next_step_handler(message, qr_choice)
def qr_choice(message):
	if str(type(message.text)) == "<class 'str'>":
		if message.text == 'Сгенерировать':
			bot.send_message(message.chat.id, 'Укажите текст, содержащий не более 256 символов.')
			bot.register_next_step_handler(message, qr_generate)
		elif message.text == 'Считать':
			bot.send_message(message.chat.id, 'Прикрепите изображение с QR кодом.')
			bot.register_next_step_handler(message, qr_read)
		else:
			bot.reply_to(message, 'Некорректно указано действие 🙈.')
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
def qr_generate(message):
	if str(type(message.text)) == "<class 'str'>":
		if len(message.text) <= 256:
			image = make(message.text)
			image.save('qrcode.png')
			byte = open('qrcode.png', 'rb')
			bot.send_message(message.chat.id, 'Готово:')
			bot.send_photo(message.chat.id, byte)
			byte.close()
			remove('qrcode.png')
		else:
			bot.reply_to(message, 'Превышено максимальное допустимое количество символов 🙈.')
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
def qr_read(message):
	if str(type(message.photo)) == "<class 'list'>":
		info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
		byte = bot.download_file(info.file_path)
		with open('qrread.png', 'wb') as image:
			image.write(byte)
		image = imread('qrread.png')
		barcodes = decode(image)
		for barcode in barcodes:
			barcodeData = barcode.data.decode('utf-8')
		try:
			type(barcodeData)
		except UnboundLocalError:
			bot.reply_to(message, 'Не удалось распознать QR код 🙈.')
		else:
			bot.send_message(message.chat.id, 'Готово:')
			bot.send_message(message.chat.id, barcodeData)
		remove('qrread.png')
	else:
		bot.reply_to(message, 'Обнаружен некорректный формат сообщения 🙈.')
#Авто-ответ
@bot.message_handler(content_types=["text"])
def answer(message):
	bot.send_message(message.chat.id, "Не понял 😕.\nНапишите \"/помощь\", чтобы посмотреть список команд.")
bot.polling()
