from extensions import GetPrice, CovertionException
import telebot
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу введите команду боту в следующем формате:\n<имя валюты>' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты>\n Узнать список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for _ in keys.keys():
        text += f'\n{_}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise CovertionException('Неверное количество параметров')

        quote, base, amount = values
        total_base = round(GetPrice.get_price(quote, base, amount), 2)
    except CovertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()
