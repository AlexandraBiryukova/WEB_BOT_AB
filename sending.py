import os,sys
import time
import telebot
import pickle
from time import sleep
from const import TOKEN
days=['MON','TUE','WED','THU','FRI','SAT','SUN']
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
				cur_d=days.index(day)
				hour=int(loc[0])+6
				minute=int(loc[1])+10
				if minute>59:
					hour+=1
					minute-=60
				if hour>=24:
					if(cur_d+1>6):
						cur_d-=6
					day=days[cur_d+1]
					hour=hour-24
				if len(str(hour))==1:
					hour='0'+str(hour)
				if len(str(minute))==1:
					minute='0'+str(minute)
				loc=str(hour)+':'+str(minute)
				if(loc in s[i] and day in s[i]):
					bot.send_message(name,"Excuse me, but I have to remind you that\nafter 10 minutes you have the next event:\n"+s[i])
	time.sleep(60)
	
			

	