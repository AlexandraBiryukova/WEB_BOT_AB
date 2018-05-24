import os,sys
import time
import telebot
import pickle
from time import sleep
from const import TOKEN

while True:
	bot = telebot.TeleBot(TOKEN)
	path="users/"
	file =open("cron.txt","a")
	file.write("I am working"+str(time.asctime( time.localtime(time.time())))+'\n')
	file.close()
	files=os.listdir(path)
	for f in files:
		if('.txt' in str(f)):
			name=path+str(f)
			file=open(name,'r')
			s=file.read()
			file.close()
			name=str(f).split('.')[0]
			s=s.split('\n')
			for i in range(len(s)):
				localtime = time.asctime( time.localtime(time.time()))
				loc=localtime.split(' ')[3].split(':')
				day=localtime.split(' ')[0].upper()
				loc=loc[0]+':'+loc[1]
				if(loc in s[i] and day in s[i]):
					bot.send_message(name,"YOU HAVE AN EVENT:\n"+s[i])
	time.sleep(60)
	
			

	