from telebot import TeleBot
from sqlite3 import connect
#Tokens and other settings
bot = TeleBot("")
def check(id):
	db = connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
		id1 INT NOT NULL PRIMARY KEY,
		id2 INT
	)""")
	db.commit()
	try:
		sql.execute(f"SELECT * FROM users WHERE id1 = {id} OR id2 = {id}")
		sql.fetchall()[0][0]
	except IndexError:
		return None
	else:
		sql.execute(f"SELECT * FROM users WHERE id1 = {id} OR id2 = {id}")
		result = sql.fetchall()
		sql.execute(f"SELECT * FROM users WHERE id1 = {id} OR id2 = {id}")
		if result[0][0] == id and result[0][1] is not None:
			return result[0][1]
		elif result[0][1] == id and result[0][0] is not None:
			return result[0][0]
		else:
			return False
def log(id, message):
	db = connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
		id1 INT NOT NULL PRIMARY KEY,
		id2 INT
	)""")
	db.commit()
	try:
		sql.execute("SELECT * FROM users WHERE id2 IS NULL")
		sql.fetchall()[0]
	except IndexError:
		sql.execute(f"INSERT INTO users (id1) VALUES ({id})")
		db.commit()
		bot.reply_to(message, "I start searching for interlocutor for you.\nIt can takes some time.")
	else:
		sql.execute("SELECT * FROM users WHERE id2 IS NULL")
		result = sql.fetchall()
		if result[0][0] != id:
			bot.reply_to(message, "I start searching for interlocutor for you.\nIt can takes some time.")
			sql.execute(f"UPDATE users SET id2 = {id} WHERE id2 IS NULL")
			db.commit()
			sql.execute(f"SELECT * FROM users WHERE id2 IS {id}")
			result = sql.fetchall()
			bot.send_message(result[0][0], "I have found interlocutor for you.\nYou can start talking.")
			bot.send_message(result[0][1], "I have found interlocutor for you.\nYou can start talking.")
		else:
			bot.reply_to(message, "I have already started searching for interlocutor for you.")
@bot.message_handler(commands=["start"])
def welcome(message):
	bot.reply_to(message, 'Hey, I am anonymous chat bot that can help you find a buddy.\nSend me "/search" to search the conversation and "/stop" to stop it.')
@bot.message_handler(commands=["search"])
def search(message):
	log(message.chat.id, message)
@bot.message_handler(commands=["stop"])
def stop(message):
	id = check(message.chat.id)
	db = connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
		id1 INT NOT NULL PRIMARY KEY,
		id2 INT
	)""")
	db.commit()
	if id is None:
		bot.reply_to(message, "Well, you are not in conversation.")
	elif id is False:
		bot.reply_to(message, "You have stopped searching for interlocutor.")
		sql.execute(f"DELETE FROM users WHERE id1 = {message.chat.id} OR id2 = {message.chat.id}")
		db.commit()
	else:
		bot.send_message(id, "Your interlocutor has stopped the conversation.")
		bot.reply_to(message, "You have stopped the conversation.")
		sql.execute(f"DELETE FROM users WHERE id1 = {message.chat.id} OR id2 = {message.chat.id}")
		db.commit()
@bot.message_handler(content_types=["text"])
def readdress(message):
	id = check(message.chat.id)
	if id is None:
		bot.reply_to(message, 'Well, I think I misunderstand you.')
	else:
		bot.send_message(id, message.text)
bot.polling()
