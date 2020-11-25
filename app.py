import telebot
from config import keys, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_command(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате:\n ' \
           '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
           'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    str_list = list(keys.keys())
    str_list.insert(0, 'Доступные валюты:')
    text = '\n'.join(str_list)
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Должно быть ровно 3 параметра')

        base, quote, amount = values

        total_price = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} = {total_price}'
        bot.send_message(message.chat.id, text)


bot.polling()
