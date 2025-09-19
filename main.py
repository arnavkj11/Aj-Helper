from config import config
from bot import create_bot
from web_server import keep_alive

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
    #keep_alive()
    main()