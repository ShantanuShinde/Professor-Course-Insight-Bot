import discord
from llm_querier import stream_graph_updates

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    reply = stream_graph_updates(message.content)
    await message.channel.send(reply)

client.run('')
