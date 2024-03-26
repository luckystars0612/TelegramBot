from model_bots import TelegramBot
from configuration.config import Config

if __name__ == '__main__':
    
    config = Config()
    # Create an instance of the TelegramBot class
    bot = TelegramBot.TelegramBot(token=config.bot_token, chat_id=config.chat_id)
    # Run the bot
    bot.run()