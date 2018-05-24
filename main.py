from const import TOKEN
from messages import START,NEW,SHOW,DELETE,TIME,EVENT,SAVE,NONE,DELETE2,TIME_ER
import telebot
from telebot import types
import requests
import os
import os.path
bot = telebot.TeleBot(TOKEN)
markup= types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
first=types.KeyboardButton('New event')
second=types.KeyboardButton('Show events')
third=types.KeyboardButton('Delete event')
markup.row(first)
markup.row(second)
markup.row(third)

@bot.message_handler(commands=['start','help'])
def starting(message):
	file=open("users/%s.txt"%message.chat.id,"a")
	print(message.chat.first_name)
	bot.send_message(message.chat.id,START%(message.chat.first_name), reply_markup=markup)
	file.close()

@bot.message_handler(func=lambda message: message.text == "Cancel")
def cancel(message):
	bot.send_message(message.chat.id,"Choose command:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "New event")
def add_day(message):
	week= types.InlineKeyboardMarkup()
	days=['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']
	week.add(*[types.InlineKeyboardButton(text=name,callback_data=name)for name in days])
	bot.send_message(message.chat.id,NEW, reply_markup=week)

@bot.message_handler(func=lambda message: message.text == "Show events")
def show_event(message):
	bot.send_message(message.chat.id,SHOW)
	if os.path.exists("users/%s.txt"%message.chat.id):
		file=open("users/%s.txt"%message.chat.id,"r")
		s=file.read()
		if s.isspace()==False:
			bot.send_message(message.chat.id, s)
		else:bot.send_message(message.chat.id, NONE)
		file.close()
	else :bot.send_message(message.chat.id, NONE)

@bot.callback_query_handler(func=lambda c:True)
def save_day(c):
	file=open("users/%s.txt"%c.message.chat.id,"a")
	file.write(c.data+" ")
	file.close()
	bot.edit_message_text(
        chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text=c.data+TIME,
		parse_mode='Markdown')
	
@bot.message_handler(func=lambda message: message.text == "Delete event")
def delete_event(message):
	dele= types.ReplyKeyboardMarkup()
	file=open("users/%s.txt"%message.chat.id,"r")
	s1=file.read()
	s2=s1.split('\n')
	file.close()
	for i in range(0,len(s2)):
		if(s2[i]!=''):
			name=i+1
			dele.row(types.InlineKeyboardButton('DEL::'+s2[i]))
	dele.row(types.InlineKeyboardButton('Cancel'))

	bot.send_message(message.chat.id,s1+DELETE, reply_markup=dele)

@bot.message_handler(func=lambda message: 'DEL::' in message.text  )
def ddd(message):
	file=open("users/%s.txt"%message.chat.id,"r")
	s3=file.read()
	os.remove("users/%s.txt"%message.chat.id)
	file=open("users/%s.txt"%message.chat.id,"a")
	s3=s3.replace(message.text.split('::')[1],'')
	file.write(s3)
	file.close()
	file = open("users/%s.txt"%message.chat.id,"r")
	s=file.read()
	file.close()
	s=s.split('\n')
	res=[]
	for i in range(len(s)):
		if(s[i]!=''):
			res.append(s[i])
	res='\n'.join(res)+'\n'
	file = open("users/%s.txt"%message.chat.id,"w")
	file.write(res)
	file.close()
	bot.send_message(message.chat.id,DELETE2,reply_markup=markup)
	
@bot.message_handler(func=lambda message: 'T:' in message.text )
def adding_time(message):
	message.text=message.text.replace('T:','')
	if len(message.text.split(':')[0])==2 and len(message.text.split(':')[1])==2:
		if int(message.text.split(':')[0])>=0 and int(message.text.split(':')[0])<24:
			if int(message.text.split(':')[1])>=0 and int(message.text.split(':')[1])<59:
				file=open("users/%s.txt"%message.chat.id,"a")
				file.write(message.text+" ")
				file.close()
				bot.send_message(message.chat.id,EVENT)
	else: bot.send_message(message.chat.id,TIME_ER)

@bot.message_handler(func=lambda message: 'EVENT-' in message.text and message.text[len(message.text)-1]=='.' and len(message.text)>7)
def adding_action(message):
	file=open("users/%s.txt"%message.chat.id,"a")
	file.write(message.text.split('-')[1]+'\n')
	file.close()
	bot.send_message(message.chat.id,SAVE,reply_markup=markup)

@bot.message_handler(content_types='text')
def handle_text_doc(message):
	bot.send_message(message.chat.id,"Oooops,something wrong, I can not understand you.",reply_markup=markup)
	
		
	
if __name__ =='__main__':
	print('Starting your bot')
	bot.polling()

	