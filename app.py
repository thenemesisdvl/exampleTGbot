from json import loads
from deep_translator import GoogleTranslator
import telebot, requests

def returnBotToken() -> str:
    return loads(open('token.json', mode="r", encoding="utf-8").read())['token']

bot = telebot.TeleBot(token=returnBotToken())

@bot.message_handler(commands=['start'])
def welcomeMessage(message):
    userName = message.from_user.first_name
    bot.reply_to(message, f"Merhaba {userName} TurkHackTeam Örnek Telegram Botuna Hoşgeldiniz 👋")

@bot.message_handler(commands=["commands"])
def allCommands(message):
    text = f'''
/start : Botu Çalıştırır.
/commands: Bot üzerinde yer alan komutları gösterir.
/numberInfo : Sayılar hakkında rastgele bilgiler verir.

    '''
    bot.reply_to(message, text)

@bot.message_handler(commands=["numberInfo"])
def numberInfo(message):
    __requests = requests.get(url="http://numbersapi.com/random/trivia").text
    __translate = GoogleTranslator(source="auto", target="tr").translate(text=__requests)
    bot.reply_to(message, __translate)


@bot.message_handler(func=lambda message: 'http' in message.text)
def deleteLinks(message):
    username = message.from_user.first_name
    bot.delete_message(message.chat.id, message.message_id)

    bot.send_message(message.chat.id, f"{username} Link paylaşmak yasaktır.")


bot.polling()