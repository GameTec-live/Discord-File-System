import lib
import discord
from discord.ext import tasks, commands
import DiscordUtils
import os

token = ""
id = 000000000
client = discord.Client()



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

async def create(file):
    guild = client.get_guild(id)
    await guild.create_text_channel(file)

async def upload(file):
    lib.encode(file)
    file = file.split(".")[0].lower()
    await create(file)
    guild = client.get_guild(id)
    channel = discord.utils.get(guild.channels, name=file)
    await channel.send("init")
    if os.path.exists("index.txt"):
        with open("index.txt", "r") as f:
             file_number = int(f.readline())

        for i in range(1, file_number):
            await channel.send(file=discord.File("split_" + str(i)))
        await channel.send(file=discord.File("index.txt"))
        lib.cleanup(file_number)
    else:
        await channel.send("No files to upload")

async def download(file):
    guild = client.get_guild(id)
    channel = discord.utils.get(guild.channels, name=file)
    channel_messages = await client.get_channel(channel.id).history(limit=None).flatten()
    for message in channel_messages:
        if message.attachments:
            await message.attachments[0].save(message.attachments[0].filename)
    lib.decode("index.txt")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!upload'):
        await upload(message.content[8:])
    if message.content.startswith('!download'):
        await download(message.content[10:].split(".")[0].lower())
    if message.content.startswith('!delete'):
        name = message.content[8:].split(".")[0].lower()
        guild = client.get_guild(id)
        channel = discord.utils.get(guild.channels, name=name)
        await channel.delete()
    if message.content.startswith('!help'):
        await message.channel.send("!upload <file>\n!download <file>\n!delete <file>")

if __name__ == "__main__":
    client.run(token)