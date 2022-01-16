import telebot
import json
from telebot import types
from collections import ChainMap

### Either create the keys.json or just add the api key below
with open("keys.json", "r", encoding='utf-8') as read_file:
    key = json.load(read_file)
bot = telebot.TeleBot(key['API_KEY'])
#Open database files
with open("info.json", "r", encoding='utf-8') as read_file:
    infos = json.load(read_file)

with open("announcements.json", "r", encoding='utf-8') as read_file:
    announcements = json.load(read_file)

#pre progress data to make it easier to handle
flatten_json = str(list(infos.values()))
flatten_dicts = dict(ChainMap(*list(infos.values())))
#Add items to the main keyboard
main_keyboard = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Ανακοινώσεις')
itembtn2 = types.KeyboardButton('Κανονισμοί')
main_keyboard.add(itembtn1, itembtn2)

#Add items to the rules selection keyboard (the one from the infos file)
rules_keyboard = types.ReplyKeyboardMarkup(selective=False)
rules_keyboard.add('Πίσω στα αρχικά')
for info in list(infos.keys()):
    rules_keyboard.add(types.KeyboardButton(info))

#Greeting message (when the user sends the /start or /help command) (todo add a different function for /help with some kinda useful info)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Γειά! Είμαι ένα botaki που στέλνει ενημερώσεις ή κάτι τέτοιο.\nΤι ενημερώσεις θα ήθελες?", reply_markup=main_keyboard)

#This handles every other message
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    #Send the first 5 announcements in the chat
    if message.text == 'Ανακοινώσεις':
        for announcement in list(announcements.values())[:5]:
            bot.send_message(message.chat.id,announcement)
        bot.send_message(message.chat.id, "Πως αλλιώς μπορώ να βοηθήσω;", reply_markup=main_keyboard)
    elif message.text == 'Κανονισμοί':
        #Show the available rules categories
        bot.send_message(message.chat.id, "Διάλεξε μία απο τις παρακάτω κατηγορίες κανονισμών", reply_markup=rules_keyboard)
    #If a message contains an available rule category show the keyboard that includes the available questions in said category
    elif message.text in list(infos.keys()):
        questions_keyboard = types.ReplyKeyboardMarkup(selective=False)
        questions_keyboard.add('Πίσω στα αρχικά')
        for question in infos[message.text]:
            questions_keyboard.add(question)
        bot.send_message(message.chat.id, 'Διάλεξε μία απο τις παρακάτω ερωτήσεις', reply_markup=questions_keyboard)
    elif message.text in flatten_json:
        bot.send_message(message.chat.id, flatten_dicts[message.text], reply_markup=rules_keyboard )
    else:
        bot.send_message(message.chat.id, "Γειά! Είμαι ένα botaki που στέλνει ενημερώσεις ή κάτι τέτοιο.\n\nΤι ενημερώσεις θα ήθελες?", reply_markup=main_keyboard)
bot.infinity_polling()