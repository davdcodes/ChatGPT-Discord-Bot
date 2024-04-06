import discord
import time
import openai

# sets basic permissions of the Discord Bot
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
client = discord.Client(intents=intents)

# input your openai key that you will have after setting up an account and creating your key. it will only be usable if there is money in your openai wallet
openai.api_key = '[OPEN AI KEY]'

# information that will preset the bot with the personality of the desired character
replies = []
character_name = '[CHARACTER NAME]'
personality = "Respond to all messages as " + character_name + ". [CHARACTER DESCRIPTION]"
replies.append({"role": "system", "content": personality})
context = "[CONTEXT ABOUT USER]" 
replies.append({"role": "system", "content": context})

# sends a confirmation message to the console after the bot has logged in
@client.event
async def on_ready():
    print(f'{client.user} is now online.')


# whenever a message is sent, the bot confirms that the message is not its own message to avoid spam, then uploads the message to ChatGPT and returns the response if it was mentioned
@client.event
async def on_message(message):  
  if message.author == client.user:
    return
  else:
    if character_name.lower() in str(message.content).lower() or client.user.mentioned_in(message):
      message_content = message.content
      message_author_name = message.author.name
    
      replies.append({"role": "system", "content": f"{message_author_name}: {message_content}"})
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=replies)
      bot_response = response["choices"][0]["message"]["content"]
      replies.append({"role": "system", "content": bot_response})
      await message.reply(bot_response)

# claim a discord token after setting up your bot with a free account from the discord developer portal
client.run("[DISCORD TOKEN]")