import discord
from discord import app_commands
from config import config
from n8n_client import n8n_client
import base64
import io

class AIBot(discord.Client):
    """
    The main bot class, encapsulating all Discord-related functionality.
    """
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        """
        This is called when the bot is setting up.
        We use it to sync our commands.
        """
        await self.tree.sync()

    async def on_ready(self):
        """
        Event handler for when the bot is ready.
        """
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('Global commands synced. Bot is online!')
        print('------')

def create_bot() -> AIBot:
    """
    Factory function to create and configure the bot.
    """
    intents = discord.Intents.default()
    bot = AIBot(intents=intents)

    @bot.tree.command(name="chat", description="Send a prompt to the AI assistant.")
    @app_commands.describe(prompt="The prompt for the AI agent.")
    async def chat_command(interaction: discord.Interaction, prompt: str):
        """
        Handler for the /chat slash command.
        """
        await interaction.response.defer()

        try:
            print(f"Received prompt from {interaction.user.name}: \"{prompt}\"")
            
            response_data = n8n_client.send_prompt(
                prompt=prompt,
                author_id=interaction.user.id,
                author_name=interaction.user.name,
                channel_id=interaction.channel.id,
                command="/chat"
            )
            
            agent_output = response_data.get('response', 'The workflow ran but returned no response.')

            if len(agent_output) > 2000:
                chunks = [agent_output[i:i + 2000] for i in range(0, len(agent_output), 2000)]
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await interaction.followup.send(chunk)
                    else:
                        await interaction.channel.send(chunk)
            else:
                await interaction.followup.send(agent_output)

        except Exception as e:
            print(f'An unexpected error occurred in chat_command: {e}')
            await interaction.followup.send('An unexpected error occurred. Please check the bot logs for more details.')

    @bot.tree.command(name="image", description="Send a prompt to generate an image.")
    @app_commands.describe(prompt="The prompt for the image generation.")
    async def image_command(interaction: discord.Interaction, prompt: str):
        """
        Handler for the /image slash command.
        """
        await interaction.response.defer()

        try:
            print(f"Received image prompt from {interaction.user.name}: \"{prompt}\"")
            
            response_data = n8n_client.send_prompt_image(
                prompt=prompt,
                author_id=interaction.user.id,
                author_name=interaction.user.name,
                channel_id=interaction.channel.id,
                command="/image"
            )

            image_bytes = response_data
            image_file = io.BytesIO(image_bytes)
            discord_file = discord.File(fp=image_file, filename="generated_image.png")
            await interaction.followup.send(f"Here is your generated image for the prompt: \"{prompt}\"", file=discord_file)

        except Exception as e:
            print(f'An unexpected error occurred in image_command: {e}')
            await interaction.followup.send('An unexpected error occurred. Please check the bot logs for more details.')

    @bot.tree.command(name="stock", description="Get stock information.")
    @app_commands.describe(prompt="The stock symbol and the name of exchange.")
    async def stock_command(interaction: discord.Interaction, prompt: str):
        """
        Handler for the /stock slash command.
        """
        await interaction.response.defer()

        try:
            print(f"Received stock prompt from {interaction.user.name}: \"{prompt}\"")
            
            response_data = n8n_client.send_prompt_stock(
                prompt=prompt,
                #exchange=exchange,
                author_id=interaction.user.id,
                author_name=interaction.user.name,
                channel_id=interaction.channel.id,
                command="/stock"
            )
            
            agent_output = response_data.get('response', 'The workflow ran but returned no response.')

            if len(agent_output) > 2000:
                chunks = [agent_output[i:i + 2000] for i in range(0, len(agent_output), 2000)]
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await interaction.followup.send(chunk)
                    else:
                        await interaction.channel.send(chunk)
            else:
                await interaction.followup.send(agent_output)

        except Exception as e:
            print(f'An unexpected error occurred in stock_command: {e}')
            await interaction.followup.send('An unexpected error occurred. Please check the bot logs for more details.')

    @bot.tree.command(name="assistant", description="Send a private prompt to your personal AI assistant.")
    @app_commands.describe(prompt="The prompt for your personal AI assistant.")
    async def assistant_command(interaction: discord.Interaction, prompt: str):
        """
        Handler for the /assistant slash command.
        """
        await interaction.response.defer()

        try:
            if interaction.user.id != config.OWNER_ID:
                await interaction.followup.send("You do not have permission to use this command.")
                return

            print(f"Received personal assistant prompt from {interaction.user.name}: \"{prompt}\"")
            
            response_data = n8n_client.send_prompt(
                prompt=prompt,
                author_id=interaction.user.id,
                author_name=interaction.user.name,
                channel_id=interaction.channel.id,
                command="/assistant"
            )
            
            agent_output = response_data.get('response', 'The workflow ran but returned no response.')

            if len(agent_output) > 2000:
                chunks = [agent_output[i:i + 2000] for i in range(0, len(agent_output), 2000)]
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await interaction.followup.send(chunk)
                    else:
                        await interaction.channel.send(chunk)
            else:
                await interaction.followup.send(agent_output)

        except Exception as e:
            print(f'An unexpected error occurred in assistant_command: {e}')
            await interaction.followup.send('An unexpected error occurred. Please check the bot logs for more details.')

    return bot
