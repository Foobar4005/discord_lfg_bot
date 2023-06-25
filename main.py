import random
import discord
import pandas as pd
import numpy as np
import sqlite3


from dotenv import load_dotenv
import os

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


#Create sqlite database
con = sqlite3.connect('lfg_bot.db')#Create database and connection
cur = con.cursor()#Allows us to use commands on db
cur.execute('''CREATE TABLE IF NOT EXISTS lfg
            (datetime text, user text, channel text, message text)''')


#For when bot first enters a server
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#For when a message is sent
@client.event
async def on_message(message):
    #Store data in variables
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    time_created = message.created_at
    print(f'{username}: {user_message} ({channel})')

    #Ensures bot doesn't log its own response
    if message.author == client.user:
        return
    
    if '<@&1121830106982264843>' in user_message:#Checks if user entered '@lfg'
        #Store data in a dict
        data = {
            'user': username,#Store who sent message
            'channel': channel,#Store channel message sent in
            'message': user_message.replace('<@&1121830106982264843>', '@lfg'),#Store message; change the ping tag to @lfg
            'time': (pd.to_datetime(time_created)-pd.Timedelta('7H')).strftime('%m-%d-%Y %H:%M:%S')#Store time. Default is 7 hours ahead of US western
            
        }
        
        #Pass dict into database
        cur.execute("INSERT INTO lfg (datetime, user, channel, message) VALUES (?, ?, ?, ?)", (data['time'], data['user'], data['channel'], data['message']))
        con.commit()

        await message.channel.send(f'Ping registered, {username}')
        return
    
    if user_message.lower() == 'hello':
        await message.channel.send(f'Hello {username}')
        return
    


client.run(TOKEN)





