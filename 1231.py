import telebot
import time
from telebot import types
from datetime import datetime

bot = telebot.TeleBot('6651595825:AAEVJU49UaQdiEm8EWGTc37Tl0PouCo0PQg')
i = 1
day = 0
day_name = ['Понедельник','Вторник','Среду','Четверг','Пятницу','Субботу']
day_sub = ['\n\n17:20 - Самбо 7+\n18:30 - JIULAB 3-5\n18:40 - JIULAB\n20:00 - БЖЖ Gi\n20:20 - Бокс 18+',
           '\n\n16:20 - Кик 7-9\n17:40 - Кик 9-14\n19:00 - Бокс 18+\n19:00 - Кроссфит\n20:00 - БЖЖ No-Gi\n20:30 - Тайский бокс 18+',
           '\n\n17:20 - Самбо 7+\n18:30 - JIULAB 3-5\n18:40 - JIULAB\n20:00 - БЖЖ Gi\n20:20 - Бокс 18+',
           '\n\n16:20 - Кик 7-9\n17:40 - Кик 9-14\n19:00 - Бокс 18+\n19:00 - Кроссфит\n20:00 - БЖЖ No-Gi\n20:30 - Тайский бокс 18+',
           '\n\n17:20 - Самбо 7+\n18:30 - JIULAB 3-5\n18:40 - JIULAB\n20:00 - БЖЖ Gi\n20:20 - Бокс 18+',
           '\n\n9:00 - Кроссфит\n10:00 - Кик 7-9\n10:45 - БЖЖ NO-Gi\n11:20 - Кик 9-14\n12:40 - Тайский Бокс 18+']
# bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Тут будет полезная информация о детали и её фотки 😊', reply_markup=to_start)

markup = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('📚 Расписание тренировок', callback_data='tables')
btn2 = types.InlineKeyboardButton('📝 Подробней о секциях', callback_data='info_sec')
btn3 = types.InlineKeyboardButton('📞 О нас', callback_data='info')
markup.row(btn1)
markup.row(btn2, btn3)

back_mark = types.InlineKeyboardMarkup()
back_btn = types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_start')
back_mark.add(back_btn)

start_btn = types.InlineKeyboardButton('🏠 Главная', callback_data='back_to_start')
to_start = types.InlineKeyboardMarkup()
to_start.add(start_btn)

info_mark = types.InlineKeyboardMarkup()
map_btn = types.InlineKeyboardButton('Открыть Я.Карты', url="https://yandex.ru/maps/-/CDrLfE9T")
site_btn = types.InlineKeyboardButton('Перейти на сайт', url="https://jiulab.ru/")
info_mark.row(map_btn, site_btn)
info_mark.row(start_btn)

sec_mark=types.InlineKeyboardMarkup()
sambo_info=types.InlineKeyboardButton('Самбо', callback_data='more_info_sec')
JIULAB_info=types.InlineKeyboardButton('JIULAB', callback_data='more_info_sec')
sec_mark.row(sambo_info,JIULAB_info)
BJJ_info=types.InlineKeyboardButton('Джиу-Джитсу', callback_data='more_info_sec')
boks_info=types.InlineKeyboardButton('Бокс', callback_data='more_info_sec')
sec_mark.row(BJJ_info,boks_info)
kik_boks_info=types.InlineKeyboardButton('Кик-бокс',callback_data='more_info_sec')
tay_boks_info=types.InlineKeyboardButton('Тайский бокс', callback_data='more_info_sec')
sec_mark.row(kik_boks_info,tay_boks_info)
cros_info=types.InlineKeyboardButton('Кроссфит', callback_data='more_info_sec')
sec_mark.row(cros_info)
sec_mark.row(start_btn)

tab_mark=types.InlineKeyboardMarkup()
next=types.InlineKeyboardButton('Следующий день', callback_data='next')
back=types.InlineKeyboardButton('Предыдущий день', callback_data='back')
tab_mark.row(back, next)
tab_mark.row(start_btn)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_photo(message.chat.id, photo=open('avatar.jpg', 'rb'), caption="Приветствую! Я бот-помощник JIULAB.")
    bot.send_message(message.chat.id, text='Напишите /help, если хотите узнать обомне подробней.',reply_markup=markup )
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, 'Тут я рассказываю о себе больше информации')

@bot.message_handler()
def handle_message(message):
    pass

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global day
    if call.data == 'tables':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Расписание на {day_name[day]}{day_sub[day]}',reply_markup=tab_mark)
    if call.data == 'next':
        if day<5:
            day+=1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Расписание на {day_name[day]}{day_sub[day]}', reply_markup=tab_mark)
        elif day==5:
            day=0
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Расписание на {day_name[day]}{day_sub[day]}', reply_markup=tab_mark)
    if call.data == 'back':
        if day>0:
            day-=1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,  text=f'Расписание на {day_name[day]}{day_sub[day]}', reply_markup=tab_mark)
        elif day==0:
            day=5
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Расписание на {day_name[day]}{day_sub[day]}', reply_markup=tab_mark)
    if call.data == 'info':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='JIULAB - клуб единоборств и воспитания духа'
                                                                                                     '\n\nПриезжайте в клуб единоборств JIULAB Удобное местонахождение в центре города.\nАдрес: г.Мытищи, ул. Станционная, д.7, ТЦ Артимолл, -1 этаж.'
                                                                                                     '\n\nТелефон: 8(499)213-05-14', reply_markup=info_mark)
    if call.data == 'info_sec':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text='У нас проходят тренировки по следующим направлениям:'
                                                                                                    '\n\nСамбо'
                                                                                                    '\nJIULAB'
                                                                                                    '\nДжиу-Джитсу'
                                                                                                    '\nБокс'
                                                                                                    '\nКик-бокс'
                                                                                                    '\nТайский бокс'
                                                                                                    '\nКроссфит',reply_markup=sec_mark)
    if call.data == 'more_info_sec':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Тут будет подробная информация о секции',reply_markup=to_start)
    if call.data == 'back_to_start':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Приветствую! Я бот-помощник JIULAB.😊\n\nНапишите /help, если хотите узнать обомне подробней.', reply_markup=markup)

bot.infinity_polling()