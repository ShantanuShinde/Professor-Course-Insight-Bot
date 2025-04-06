import discord
from llm_querier import get_sql_query
from sql_manager import get_query_results

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

    query = get_sql_query(message.content)
    print(query)
    result = get_query_results(query)
    await message.channel.send(result)

client.run('')
