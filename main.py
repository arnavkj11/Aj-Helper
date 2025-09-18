import os
import discord
from discord import app_commands
import requests
from dotenv import load_dotenv

# --- Environment Variable Loading & Validation ---
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')
DISCORD_GUILD_ID = discord.Object(id=os.getenv('DISCORD_GUILD_ID'))

if not all([DISCORD_BOT_TOKEN, N8N_WEBHOOK_URL]):
    print('ERROR: Missing required environment variables. Please check your .env file.')
    print('Required: DISCORD_BOT_TOKEN, N8N_WEBHOOK_URL')
    exit()

# The GUILD object is where we'll sync the commands.
# MY_GUILD = discord.Object(id=DISCORD_GUILD_ID) # We no longer need this for global commands


# --- Bot Setup ---
# Intents are still needed for the bot to function.
intents = discord.Intents.all()
client = discord.Client(intents=intents)
# A CommandTree is used to manage and register slash commands.
tree = app_commands.CommandTree(client)


# --- Bot Events ---
@client.event
async def on_ready():
    """
    Event handler for when the bot has connected to Discord and is ready.
    This is where we sync the command tree with Discord's servers.
    """
    # Sync the command tree globally.
    # This can take up to an hour to propagate to all servers.
    await tree.sync()
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('Global commands synced. Bot is online!')
    print('------')

# We are removing the on_message event handler as it's no longer needed for slash commands.
# This makes the bot more efficient as it no longer needs to read every message.


# --- Application Command Definition ---
@tree.command(name="chat", description="Send a prompt to the AI assistant.")
# Add the parameters your command will take. 'prompt' will be a required text field.
@app_commands.describe(prompt="The prompt for the AI agent.")
async def chat_command(interaction: discord.Interaction, prompt: str):
    """
    Handler for the /chat slash command.
    """
    # 1. Defer the response. This tells Discord "I'm working on it!"
    # and gives us more than 3 seconds to respond, which is crucial for API calls.
    await interaction.response.defer()

    try:
        print(f"Received prompt from {interaction.user.name}: \"{prompt}\"")

        # 2. Prepare the payload for the n8n webhook.
        payload = {
            'prompt': prompt,
            'author_id': interaction.user.id,
            'author_name': interaction.user.name
        }

        # 3. Send the data to n8n via an HTTP POST request.
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=300)
        response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)

        # 4. Extract the agent's output from the n8n response.
        response_data = response.json()
        agent_output = response_data.get('response', 'The workflow ran but returned no response.')

        # 5. Send the final reply using a followup webhook.
        # This is used because we deferred the initial response.
        if len(agent_output) > 2000:
            # Handle messages that exceed Discord's character limit
            chunks = [agent_output[i:i + 2000] for i in range(0, len(agent_output), 2000)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await interaction.followup.send(chunk)
                else:
                    await interaction.channel.send(chunk) # Send subsequent chunks as new messages
        else:
            await interaction.followup.send(agent_output)

    except requests.exceptions.RequestException as e:
        print(f'Error connecting to n8n webhook: {e}')
        await interaction.followup.send('Sorry, I couldn\'t connect to the AI workflow. Please try again later.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        await interaction.followup.send('An unexpected error occurred. Please check the bot logs for more details.')

# --- Run the Bot ---
client.run(DISCORD_BOT_TOKEN)