import telebot
import time
from telebot import types
from datetime import datetime
from deta import Deta

#12

bot = telebot.TeleBot('6651595825:AAEVJU49UaQdiEm8EWGTc37Tl0PouCo0PQg')
deta = Deta("c0n8ymyprw2_CwMUwv7o9KNkeKG3tdFX4VNF7Zi3km1B")
Users = deta.Base("Users")
Curs = deta.Base("Curs")
Orders = deta.Base("Orders")
# bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Тут будет полезная информация о детали и её фотки 😊', reply_markup=to_start)

markup = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('🛍️ Оформить заказ', callback_data='order')
btn6 = types.InlineKeyboardButton('📦 Мои заказы',callback_data='my_orders')
btn2 = types.InlineKeyboardButton('📜 Отзывы', url='https://t.me/logisticsart/166')
btn3 = types.InlineKeyboardButton('💹 Курс юаня', callback_data='curs')
btn4 = types.InlineKeyboardButton('💴 Расчитать стоимость', callback_data='calculate')
btn5 = types.InlineKeyboardButton('❓ F.A.Q',callback_data='FAQ')
markup.row(btn1,btn6)
markup.row(btn3, btn4)
markup.row(btn2)
markup.row(btn5)

order_markup = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Оставить заявку', callback_data='do_order')
btn2 = types.InlineKeyboardButton('Перейти в чат с менеджером', url='https://t.me/dariiiiiiiiiiiiiiiiiiiiiiiiiiiii')
order_markup.add(btn1,btn2)

adm_markup = types.InlineKeyboardMarkup()
adm = types.InlineKeyboardButton('Админ',url='https://t.me/mangovirus')
adm_markup.add(adm)

@bot.message_handler(commands=['start'])
def welcome(message):
    global message_for_change
    for i in range(0,len(Users.fetch().items)):
        if int(Users.fetch().items[i]['key']) == int(message.chat.id):
            print('Зареган')
            break
        elif i==len(Users.fetch().items)-1:
            print('Регестрирую')
            Users.put({'key':f'{message.chat.id}','name':f'{message.from_user.username}','role':'user','change_id':'','price_wait':0,'orders':[],'fio':'','phone':'','city':'','addres':''})
    bot.send_photo(message.chat.id, photo=open('menu.jpg', 'rb'), caption="Добро пожаловать 👋  "
                                                                            "\n\nЯ тот самый бот, который поможет тебе заказать вещи с китайского маркетплейса Poizon👟"
                                                                            "\n\n🤖 Смотри что я умею 🤖",reply_markup=markup)
    message_for_change=bot.send_message(message.chat.id, text='Напишите /help, если хотите узнать обомне подробней.')
    Users.update({"change_id": message_for_change.message_id}, f"{message.chat.id}")

@bot.message_handler(commands=['help'])
def help(message):
    me=Users.get(f'{message.chat.id}')
    bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text='Тут я рассказываю о себе больше информации')

@bot.message_handler(commands=['cp'])
def change_price(message):
    me=Users.get(f'{message.chat.id}')
    if me['role']=='admin':
        Curs.update({'price': float(message.text[4:])}, 'eb1xt00b78st')
        curs = Curs.get('eb1xt00b78st')
        t = curs['price']
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'],
                          text=f'Курс был изменен на {t}')
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'],
                              text=f'Простите но курс может менять только админ')

@bot.message_handler(commands=['adm'])
def adm_panel(message):
    me = Users.get(f'{message.chat.id}')
    if me['role']=='admin':
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'],
                              text='Админ панель'
                                   '\n/cp {число(13,2)} - для изменения курса'
                                   '\n/user {id пользователя или username} - информация о пользователе(Не работает)')
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'],
                              text='У вас нет админ прав')

@bot.message_handler(commands=['user'])
def adm_panel(message):
    me=Users.get(f'{message.chat.id}')
    if me['role']=='admin':
        info_user=Users.get(f'{int(message.text[5:])}')
        g=info_user['name']
        text=(f'username: {g}')
        g=info_user['orders']
        text+=f'\norders: {g}'
        g=info_user['role']
        text+=f'\nrole: {g}'
        g=info_user['addres']
        text+=f'\nАдрес СДЭКа: {g}'
        g=info_user['city']
        text+=f'\nГород: {g}'
        g=info_user['fio']
        text+=f'\nФИО: {g}'
        g=info_user['phone']
        text+=f'\nНомер телефона: {g}'
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text=f'{text}')
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text='У вас нет админ прав')

@bot.message_handler(content_types=['photo'])
def photo(message):
    me = Users.get(f'{message.from_user.id}')
    if me['price_wait']==9:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_photo(843132138, downloaded_file)
        p=len(Orders.fetch().items)+1
        Orders.put({'key':f'{p}','user_id':f'{message.from_user.id}','user_name':f'{message.from_user.username}','status':'Заявка в обработке'})
        f=me['orders']
        f.append(p)
        Users.update({'orders':f,'price_wait':0},f'{message.from_user.id}')
        bot.send_message(843132138,f'Был создан новый заказ {p}')
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text='Ваш заказ был принят, ожидайте пока вам напишет менеджер')

@bot.message_handler()
def handle_message(message):
    print(message)
    global i,curs
    me = Users.get(f'{message.from_user.id}')
    if me['price_wait']==1:
        curs = Curs.get('eb1xt00b78st')
        t = curs['price']
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text=f'{int(message.text)*t+2000}₽ + 800руб/кг  (доставка)')
    elif me['price_wait']==2:
        Users.update({'fio':f'{message.text}','price_wait':3},f'{message.from_user.id}')
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text='Отправьте ваш номер телефона')
    elif me['price_wait']==3:
        Users.update({'phone':f'{message.text}','price_wait':4},f'{message.from_user.id}')
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text='Отправьте ваш город')
    elif me['price_wait']==4:
        Users.update({'city':f'{message.text}','price_wait':5},f'{message.from_user.id}')
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text='Отправьте адрес удобного вам СДЭКа')
    elif me['price_wait']==5:
        Users.update({'addres':f'{message.text}','price_wait':9},f'{message.from_user.id}')
        bot.edit_message_text(chat_id=message.chat.id, message_id=me['change_id'], text='Отправьте скриншот товара который вас интересует')
def gen_orders_text(me):
    global orders_markup
    text='Ваши заказы:'
    o=me['orders']
    for i in range(0,len(o)):
        n=Orders.get(f'{o[i]}')['status']
        text+=f'\nЗаказ под номером {o[i]}: {n}'
    return text

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    me = Users.get(f'{call.from_user.id}')
    if call.data == 'do_order':
        if me['fio']=='' or me['city']=='' or me['addres']=='' or me['phone']=='':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'], text=f'Заполните немного информации о себе'
                                                                                                 f'\nПодождите...')
            time.sleep(3)
            Users.update({"price_wait":2},f'{call.from_user.id}')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'], text='Отправьте ваше ФИО')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'], text='Отправьте фото интересующего вас товара')
            Users.update({'price_wait':9},f'{call.from_user.id}')
    if call.data == 'my_orders':
        if len(me['orders'])==0:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'], text='🤖 Простите но я не обнаружил у вас заказов, если это ошибка пожалуйста обратитесь к администратору.',reply_markup=adm_markup)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'], text=f'{gen_orders_text(me)}')
        Users.update({"price_wait": 0}, f"{call.from_user.id}")

    if call.data == 'order':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'], text=f'Супер👍 Для оформление заказа, нужно связаться с менеджером или оставить заявку.'
                                                                                                           f'\n\nTG: @dariiiiiiiiiiiiiiiiiiiiiiiiiiiii'
                                                                                                           f'\nWA: +79099101919', reply_markup=order_markup)
        Users.update({"price_wait": 0}, f"{call.from_user.id}")

    if call.data == 'curs':
        curs = Curs.get('eb1xt00b78st')
        t = curs['price']
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'],text=f'1 CNY = {t} RUB'
                                                                                '\n\nКурс обновляется каждый день в 12:00 по МСК')
        Users.update({"price_wait": 0}, f"{call.from_user.id}")

    if call.data == 'calculate':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'], text='💹 Введите цену в Юанях:'
                                                                                             '\n(Можете писать сюда несколько сообщений)')
        Users.update({"price_wait": 1}, f"{call.from_user.id}")

    if call.data == 'FAQ':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=me['change_id'], text='📌 Ответы на основные вопросы  📌'
                                                                                            '\n\n🔘 Оригинал?'
                                                                                            '\n\nАбсолютно все товары с площадки Poizon оригинал '
                                                                                            '\nПлощадка гарантирует оригинальность всех вещей, заказанных через площадку , для этого на каждую позицию крепятся индивидуальные клипсы и кладутся сертификаты подлинности, подтверждающие 100 гарантию пройденной проверки'
                                                                                            '\nВ своей лаборатории проверки на подлинность внедрено 9 уровней проверки, контроля и досмотра. Весь процесс проверки и идентификации обеспечивает полную подлинность продукта. За один день платформа подтверждает более 5.000 оригинальных единиц товара.'
                                                                                            '\nПосле получения своего заказы вы также получаете сертификат на бесплатную проверку на аутентичность, который осуществляет любимый многим пользователями сервис Legit Check👟'
                                                                                            '\n\n🔘 Что будет, если моя посылка будет утеряна?'
                                                                                            '\n\nВаш товар полностью застрахован на полную стоимость от пропажи, в случае утери 100% компенсация 💸'
                                                                                            '\n\n🔘 Доставка по всей России'
                                                                                            '\n\nЕсть два вида доставки:'
                                                                                            '\n✈️ Экспресс - от 2 до 3 дней - 2700 руб/кг'
                                                                                            '\n🌐 Обычная - от 13 до 18 дней - 800 руб/кг'
                                                                                            '\nПосле приезда вашего товара в МСК, оформляется СДЭК.'
                                                                                            '\n\n🔘 Если заказать несколько вещей, нужно будет за каждую заплатить доставку и комиссию?'
                                                                                            '\n\nДа, так как пойзон не является магазином. На данной площадке не существует «корзины». Каждая позиция приезжает от разных продавцов и отдельно проходит легитчек👟'
                                                                                            '\n\n🔘 Как быть с пошлиной?'
                                                                                            '\n\nМы растаможиваем груз самостоятельно, Вам не нужно беспокоиться о лимитах.')
        Users.update({"price_wait": 0}, f"{call.from_user.id}")

print('Бот запущен')
bot.infinity_polling()