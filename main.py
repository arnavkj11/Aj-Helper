from config import config
from bot import create_bot

def main():
    """
    Main function to run the bot.
    """
    try:
        bot = create_bot()
        bot.run(config.DISCORD_BOT_TOKEN)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()