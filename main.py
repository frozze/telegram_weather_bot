import telebot
from pyowm import OWM
from pyowm.utils import config as cfg


config = cfg.get_default_config()
config['language'] = 'ru'

bot = telebot.TeleBot('1675368527:AAFblNKuIB0adAfA-RFBoBV6ru2DcgeNYUk')
owm = OWM('2046aa37386aac82ebdceec83f42931f', config)


keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Москва', 'Санкт-Петербург')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, введи название города или нажми кнопку /start', reply_markup=keyboard2)

@bot.message_handler(content_types=['text'])
def temperature(message):
    try:
        mgr = owm.weather_manager()
        weather = mgr.weather_at_place(message.text).weather
        now = weather.temperature('celsius')['temp']
        now1 = weather.wind()['speed']
        now2 = int(weather.pressure['press']//1.33)
        now3 = weather.humidity
        now4 = weather.clouds
        text = (
            f"Погода в городе {message.text}:\n"
            f"Температура - <b>{now} {'С'+chr(176)}</b>\n"
            f"Ветер - <b>{now1} м/с</b>\n"
            f"Давление - <b>{now2} мм рт.ст.\n</b>"
            f"Влажность - <b>{now3} %\n</b>"
            f"Облачность - <b>{now4} %</b>"
        )
        bot.send_message(message.chat.id, text, parse_mode = "HTML")
    except:
        bot.send_message(message.chat.id,"Город не найден, попробуйте использовать латиницу")

bot.polling()

