import telebot
import json
from telebot import types

with open("keys.json", "r", encoding='utf-8') as read_file:
    key = json.load(read_file)

bot = telebot.TeleBot(key['API_KEY'])

with open("info.json", "r", encoding='utf-8') as read_file:
    infos = json.load(read_file)

with open("announcements.json", "r", encoding='utf-8') as read_file:
    announcements = json.load(read_file)
    
main_keyboard = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Ανακοινώσεις')
itembtn2 = types.KeyboardButton('Κανονισμοί')
main_keyboard.add(itembtn1, itembtn2)
rules_keyboard = types.ReplyKeyboardMarkup(selective=False)
rules_keyboard.add('Πίσω στα αρχικά')
for info in list(infos.keys()):
    rules_keyboard.add(types.KeyboardButton(info))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Γειά! Είμαι ένα botaki που στέλνει ενημερώσεις ή κάτι τέτοιο.\nΤι ενημερώσεις θα ήθελες?", reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Ανακοινώσεις':
        for announcement in list(announcements.values())[:5]:
            bot.send_message(message.chat.id,announcement)
        bot.send_message(message.chat.id, "Πως αλλιώς μπορώ να βοηθήσω;", reply_markup=main_keyboard)
    elif message.text == 'Κανονισμοί':
        bot.send_message(message.chat.id, "Διάλεξε μία απο τις παρακάτω κατηγορίες κανονισμών", reply_markup=rules_keyboard)
    elif message.text in infos:
        bot.send_message(message.chat.id, infos[message.text], reply_markup=rules_keyboard )
    else:
        bot.send_message(message.chat.id, "Γειά! Είμαι ένα botaki που στέλνει ενημερώσεις ή κάτι τέτοιο.\n\nΤι ενημερώσεις θα ήθελες?", reply_markup=main_keyboard)


bot.infinity_polling()