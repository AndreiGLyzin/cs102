import telebot


access_token = '1019738386:AAG5G6de4PTjFkyrOGRw9eLLW0XhCVBy6GY'
telebot.apihelper.proxy = {'https': 'https://78.41.53.39:8080'}

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)


# Бот будет отвечать только на текстовые сообщения
@bot.message_handler(content_types=['text'])
def echo(message: str) -> None:
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)