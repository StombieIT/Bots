import smtplib as root
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
def send_mail():
	login = input('Type your mail: ')
	"""
	if login.endswith('@yandex.ru') == True:
		url = 'smtp.yandex.ru'
	elif login.endswith('@mail.ru') == True:
		url = 'smtp.mail.ru'
	elif login.endswith('@inbox.ru') == True:
		url = 'smtp.inbox.ru'
	elif login.endswith('@gmail.com') == True:
		url = 'smtp.gmail.com'
	"""
	url = input('Type URL: ')
	password = input('Type password of your mail: ')
	toaddr = input('Type mail of victime: ')
	topic = input('Type topic: ')
	body = input('Type message: ')
	msg = MIMEMultipart()
	msg['Subject'] = topic
	msg['From'] = login
	msg.attach(MIMEText(body, 'plain'))
	server = root.SMTP_SSL(url, 465)
	server.login(login, password)
	for i in range(int(input('How many times: '))):
		server.sendmail(login, toaddr, msg.as_string())
		print('Sending ' + str(i + 1) + ' message to '  + toaddr)
		sleep(10)
	server.quit()
	print('Done')
if __name__ == '__main__':
	send_mail()
