import telebot
from core.config import config


class TGBOT:
    
    config = config.getTelegramConfig()

    bot = telebot.TeleBot(token=config.get('token'))

    @staticmethod
    def Send_Message(message, chat_id=config.get('chat_id')):
        TGBOT.bot.send_message(chat_id, message)