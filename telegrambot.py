import random
import datetime
import math
import telebot
from telebot import types
import qrcode
import gtts

print('running')

bot = telebot.TeleBot("5769914217:AAFhU722ZYV7uj0PpSjOcboOQCZvVdLfRAo", parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.reply_to(message, "Hello " + name + ' and Welcome to Sweet Dreams bot')

@bot.message_handler(commands=['help'])
def guess_number(message):
    bot.send_message(message.chat.id, 'Guessing game       : /game')
    bot.send_message(message.chat.id, 'How old are you     : /age')
    bot.send_message(message.chat.id, 'Text2Voice          : /voice')
    bot.send_message(message.chat.id, 'Max Number          : /max')
    bot.send_message(message.chat.id, 'Which number is Max : /argmax')
    bot.send_message(message.chat.id, 'Text2QRcode         : /qrcode')



def verify(message):
    return True

def jalali_to_gregorian(jy, jm, jd):
 jy += 1595
 days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
 if (jm < 7):
    days += (jm - 1) * 31
 else:
    days += ((jm - 7) * 30) + 186
 gy = 400 * (days // 146097)
 days %= 146097
 if (days > 36524):
    days -= 1
    gy += 100 * (days // 36524)
    days %= 36524
    if (days >= 365):
      days += 1
 gy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
    gy += ((days - 1) // 365)
    days = (days - 1) % 365
 gd = days + 1
 if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
    kab = 29
 else:
    kab = 28
 sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
 gm = 0
 while (gm < 13 and gd > sal_a[gm]):
    gd -= sal_a[gm]
    gm += 1
 return [gy, gm, gd]    

usr_num = 0
com_num = random.randint(1,100)

@bot.message_handler(commands=['game'])
def guess_number(message):
    
    game_keyboard = types.ReplyKeyboardMarkup(row_width=5)
    gk1 = types.KeyboardButton('New Game')
    game_keyboard.add(gk1)
    bot.send_message(message.chat.id, '!!Welcome to the Guessing Game!!')
    bot.send_message(message.chat.id, com_num)
    bot.send_message(message.chat.id, 'What is your guess between 1 and 100?! ' )

    @bot.message_handler(func=verify)
    def echo_all(message):
        usr_num = float(message.text)
        if com_num == int(usr_num):
            bot.reply_to(message, 'Congrats!, You Win!!', reply_markup=game_keyboard)
        elif com_num > int(usr_num):
            bot.reply_to(message, 'Up, Up, Up, ⬆️', reply_markup=game_keyboard)
        elif com_num < int(usr_num):
            bot.reply_to(message, 'Down, Down, Down, ⬇️', reply_markup=game_keyboard)    


@bot.message_handler(commands=['age'])
def calc_age(message):
    bot.send_message(message.chat.id, 'Enter your birthday: (Format: 13xx/0x/0x)')
    @bot.message_handler(func=verify)
    def echo_all(message):
        usr_brt = list(message.text.split('/'))
        brt = jalali_to_gregorian(int(usr_brt[0]), int(usr_brt[1]), int(usr_brt[2]))
        dd0 = brt[0]*365 + brt[1]*30 + brt[2]

        now = datetime.datetime.now()
        y = int(now.strftime('%Y'))
        m = int(now.strftime('%m'))
        d = int(now.strftime('%d')) 
        dd1 = y*365 + m*30 + d

        total_days = dd1 - dd0
        years = str(int(total_days/365))
        months = str(int((total_days%365)/30))
        days   = str(int((total_days%365)%30))
        
        bot.reply_to(message, "You are " + years + " Years and " + months  + "  Months and " + days + " Days old")
        #bot.send_message(message.chat.id, years )
        

@bot.message_handler(commands=['max'])
def max_num(message):
    bot.send_message(message.chat.id, 'Enter the list of numbers: (Format: x,y,z,k,t,...)')
    @bot.message_handler(func=verify)
    def echo_all(message):
        usr_num_list = list(message.text.split(','))
        int_num_list = [eval(i) for i in usr_num_list]
        maxn = max(int_num_list)
        bot.reply_to(message, 'Max Number is ' + str(maxn))

@bot.message_handler(commands=['voice'])
def max_num_arg(message):
    bot.send_message(message.chat.id, 'Enter the English text you want to convert to Voice: ')
    @bot.message_handler(func=verify)
    def echo_all(message):
        text_to_voice = message.text
        tts = gtts.gTTS(text_to_voice)
        tts.save('1.mp3')
        audio = open('1.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    
    
    
    
@bot.message_handler(commands=['argmax'])
def max_num_arg(message):
    bot.send_message(message.chat.id, 'Enter the list of numbers: (Format: x,y,z,k,t,...)')
    @bot.message_handler(func=verify)
    def echo_all(message):
        usr_num_list = list(message.text.split(','))
        int_num_list = [eval(i) for i in usr_num_list]
        maxn = max(int_num_list)
        maxarg = int_num_list.index(maxn)
        bot.reply_to(message, 'Max Number is ' + str(maxarg))

@bot.message_handler(commands=['qrcode'])
def qr_code(message):
    bot.send_message(message.chat.id, 'Enter the text you want to make QR-Code out of: ')
    @bot.message_handler(func=verify)
    def echo_all(message):
        text_input = message.text
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        q.add_data(text_input)
        i = q.make_image(fill_color = 'white', back_color = 'black')
        i.save('1.png')
        photo = open('1.png', 'rb')
        bot.send_photo(message.chat.id, photo)
        
                
                


	





bot.infinity_polling()