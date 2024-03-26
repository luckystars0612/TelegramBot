import configparser

class Config:
    
    def __init__(self):
        self.bot_token = None
        self.chat_id = None
        self.sec_token = None
        self.read_config()
        
    def read_config(self):
    
        # Create a configparser object
        config = configparser.ConfigParser()
        
        # Read the configuration file
        config.read('configuration/bot.config')
        
        # Access values from 'bot_section'
        self.bot_token = config.get('bot', 'bot_token')
        self.chat_id = config.get('bot', 'chat_id')
        
        # Access values from 'qradar_section'
        self.sec_token = config.get('qradar', 'SEC_TOKEN')
        


