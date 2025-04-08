import discord
from llm_querier import get_sql_query, get_nl_response
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
    question = message.content
    query = get_sql_query(question)
    result = get_query_results(query)
    response = get_nl_response(question, result)
    await message.channel.send(response)

client.run()
