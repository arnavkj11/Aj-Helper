import os
from dotenv import load_dotenv

class Config:
    """
    A class to manage environment variable loading and validation.
    """
    def __init__(self):
        load_dotenv()
        self.DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
        self.N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')
        self.validate()

    def validate(self):
        """
        Validates that all required environment variables are set.
        """
        if not all([self.DISCORD_BOT_TOKEN, self.N8N_WEBHOOK_URL]):
            raise ValueError(
                'ERROR: Missing required environment variables. '
                'Please check your .env file. '
                'Required: DISCORD_BOT_TOKEN, N8N_WEBHOOK_URL'
            )

# Create a single instance of the Config class to be used throughout the application.
config = Config()
