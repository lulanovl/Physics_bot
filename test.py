

import telebot
from telebot import types
import MySQLdb
from datetime import datetime
import config
import dbworker

user_name = ''
def save(id):
    global user_name
    user_id = id
    cursor = db.cursor()
    # cursor.execute(
    #     "SELECT card_id FROM users where name = '%s'" % name)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    cursor.execute(
        f"UPDATE bike_monitor SET user_id = \"{user_name}\", take = \"{current_time}\", status = '0' where status = '1' and id = \"{id}\" limit 1")
    print("User ", user_id, " was added")
    db.commit()
    

# establish connection to MySQL. You'll have to change this for your database.
db = MySQLdb.connect("localhost", "root", "", "db_bikes") or die(
    "could not connect to database")

bot = telebot.TeleBot('5311742394:AAEb9S8-yduplsdlGZpj38lQjGricpHWcDs')

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "Type your name", parse_mode = "html")
    dbworker.set_state(message.chat.id, config.States.NAME.value)

@bot.message_handler(commands=["text"], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.WELCOME.value)
def welcome(message):
    bot.send_message(message.chat.id, "Type your name", parse_mode = "html")
    dbworker.set_state(message.chat.id, config.States.NAME.value)

@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NAME.value)
def name(message):
    global user_name
    if message.text == '':
        dbworker.set_state(message.chat.id, config.States.START.value)
    else:
        user_name = message.text
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM bike_monitor")
        bike_list = cursor.fetchall()
        print("List of bikes")
        print(bike_list)
        db.commit()
        for bike in bike_list:
            if bike[3] == 0:
                mess = "Bike #" + str(bike[0]) + " taken at: " + str(bike[2])
                bot.send_message(message.chat.id, mess,
                                parse_mode='Markdown')
            else:
                mess = ("Bike #" + str(bike[0]) + " is free")
                bot.send_message(message.chat.id, mess,
                                parse_mode='Markdown')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        print()
        if bike_list[0][3] == 1:
            bike_1 = types.KeyboardButton("1")
            markup.add(bike_1)
        if bike_list[1][3] == 1:  
            bike_2 = types.KeyboardButton("2")
            markup.add(bike_2)
        if bike_list[2][3] == 1:
            bike_3 = types.KeyboardButton("3")
            markup.add(bike_3)
        if bike_list[3][3] == 1:
            bike_4 = types.KeyboardButton("4")
            markup.add(bike_4)
    
        bot.send_message(message.chat.id, 'Choose a bike',
                             reply_markup=markup)
        dbworker.set_state(message.chat.id, config.States.CHOOSE.value)

@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.CHOOSE.value)
def choose(message):
    print(f'type:{message.text}, text: {message.text}')
    if message.text in ['1','2','3','4']:
        save(message.text)
        bot.send_message(message.chat.id, f'bike {message.text} is now reserved')
    else:
        bot.send_message(message.chat.id, 'Please choose a bike')
        dbworker.set_state(message.chat.id, config.States.NAME.value)


bot.polling(none_stop=True, interval=0)
