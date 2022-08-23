from operator import contains
from queue import Empty
import discord
from discord import user
intents = discord.Intents.all()
intents.members = True
intents.presences = True
import random
import asyncio
import datetime
import aiohttp
import json
import re
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.', help_command=None) #defines the bot

guild = 713133764829642794

#getting hidden keys
token = os.environ.get('token')
sra_api_key = os.environ.get('sra_api_key')


#STATUS
@client.event
async def on_ready():
  staffTesting = client.get_channel(812224835605757972)
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Loading..."))
  await asyncio.sleep(3) 
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Loaded!"))
  await asyncio.sleep(1)
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the server"))
  await staffTesting.send("Bot Online.")


#COMMANDS ----------------------------------------------------------------

#TEST COMMANDS
@client.command()
@commands.has_permissions(manage_messages=True) 
async def test(ctx):
    await ctx.send("testing!")

#handles errors
@client.event
async def on_command_error(ctx, error):
    pass

#shows ping
@client.command()
async def ping(ctx):
    await ctx.send(f'My ping is {round(client.latency * 1000)}ms!!!!')

#pogchamp
@client.command()
async def pog(ctx):
    await ctx.send('Champ!!')

#Handles Bot DMs
msg_dump_channel = 850566676583677982
@client.event
async def on_message(message: discord.Message):
    dmChannel = client.get_channel(msg_dump_channel)
    chatbotChannel = client.get_channel(980079542431526932)
    if message.guild is None and not message.author.bot:
        embed=discord.Embed(title="**New Bot DM**", color=0xec5b5b)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="Message from:", value=message.author.mention, inline=False)
        embed.add_field(name="Contents:", value=message.content, inline=False)
        replyMessage=discord.Embed(title="Thank you for your suggestion!", description="Your suggestion will be heavily looked over by staff! \nOnce again we would like to thank you! \n\n(Also, please be sure to remember that the same rules in the server apply here in the DMs!)", color=0x2ecc71)
        await message.channel.send(embed=replyMessage)
        await dmChannel.send(embed=embed)
        

    if message.channel.id == chatbotChannel.id and not message.author.bot:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/chatbot?key={sra_api_key}&message={message.content}") as response:
                botResponse = (await response.json())["response"]
                await chatbotChannel.send(botResponse)
                
                
    await client.process_commands(message)  

#Replies for suggestions
@client.command()
@commands.has_permissions(manage_messages=True) 
async def reply(ctx, user: discord.Member = None, *, message = None):
    if ctx.channel.id == 850566676583677982:
           
        embed=discord.Embed()
        embed.add_field(name="Reply:", value=f"{message}", inline=False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{ctx.author} • Role: {ctx.author.top_role}')

        if user is None:
            await ctx.send("Forgot User! (.reply [user here] [message])")
        if user is not None:
            if message is None:
                await ctx.send("Forgot Message! (.reply [user here] [message])")
        
        if message is not None:
            await user.send(embed=embed)
            embed1=discord.Embed(title=f'✅ Your reply has been sent to {user.display_name}', color=0x2ecc71) 
            await ctx.send(embed=embed1)

#8Ball Command
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                'Dont count on it.',
                'It is certain.',
                'It is decidedly so.']
    embed=discord.Embed(title="The Magic 8 Ball")
    embed.add_field(name="Question", value=question, inline=False)
    embed.add_field(name="Answer", value=random.choice(responses), inline=True)
    await ctx.send(embed=embed)

#Staff Announcement Command
@client.command()
@commands.has_permissions(manage_messages=True) 
async def announce(ctx, channel: discord.TextChannel):

  def msgcheck(msg):
        return msg.author == ctx.author

  embed1=discord.Embed(title='What is the title of your message?', color=0x2f3136) 
  await ctx.send(embed=embed1)
  titlemsg = await client.wait_for("message", check=msgcheck)
  title = (titlemsg.content)

  embed2=discord.Embed(title='What are the contents of your message?', color=0x2f3136)
  await ctx.send(embed=embed2) 
  contentsmsg = await client.wait_for("message", check=msgcheck)
  contents = (contentsmsg.content)

  embed=discord.Embed(title=title, description=contents, color=0x2ecc71)
  if contentsmsg.attachments:
        attachment = contentsmsg.attachments[0] 
        embed.set_image(url=attachment.url)
  embed.set_footer(icon_url = ctx.author.avatar_url,text=f'- {ctx.author.display_name}')
  

  reactMessage=discord.Embed()
  reactMessage.add_field(name="⬆️ Here is what your announcement will look like ⬆️", 
  value="**Customization** \n📡 - Sign the announcement as Fullblast Network \n📸 - Attach an image or gif. **(must be a file upload. not from discords gifs.)** \n🖼️ - Set a thumbnail. **(must be a file upload. not from discords gifs.)** \n\n**Delivery Options** \n📢 - to send announcement **__with an @ to everyone__** \n📨 - to send this announcement **__without an @__**! \n ⏲️ - Schedule this announcement for a later time! \n❌ - to close this announcement out and start over. \n\n**Reset** \n🔁 - Reset all of your **customization options**.", inline=False)
  example = await ctx.send(embed=embed)
  msg = await ctx.send(embed=reactMessage)

  #Customization
  await msg.add_reaction("📡")
  await msg.add_reaction("📸")
  await msg.add_reaction("🖼️")

  #Delivery
  await msg.add_reaction("📢")
  await msg.add_reaction("📨")
  await msg.add_reaction("⏲️")
  await msg.add_reaction("❌")

  #RESET
  await msg.add_reaction("🔁")

  valid_reactions = ['📡','📨', '❌', '📢', '🔁', '📸', '🖼️', '⏲️', '✅']
  

  def check(reaction, user):
    return user == ctx.author and str(reaction.emoji) in valid_reactions
  
  iterate = True
  
  while iterate is True:
    reactionAdd, user1 = await client.wait_for('reaction_add', timeout=300.0, check=check)
    if reactionAdd:
        if str(reactionAdd.emoji) == '📡':
            embed.set_footer(icon_url = client.user.avatar_url,text=f'- Fullblast Network!')
            await example.edit(embed=embed)
            continue
        
        if str(reactionAdd.emoji) == '📸':
            def msgcheck(msg):
                return msg.author == ctx.author
            prompt = await ctx.send("`Send the image or gif you would like to include.`")
            imageMsg = await client.wait_for("message", check=msgcheck)
            if imageMsg.attachments:
                imgAttachment = imageMsg.attachments[0] 
                embed.set_image(url=imgAttachment.url)
            
            await imageMsg.delete()
            await prompt.delete()
            await example.edit(embed=embed)
            continue

        if str(reactionAdd.emoji) == '🖼️':
            def msgcheck(msg):
                return msg.author == ctx.author
            prompt = await ctx.send("`Send the image or gif you would like to set as the thumbnail.`")
            imageMsg = await client.wait_for("message", check=msgcheck)
            if imageMsg.attachments:
                imgAttachment = imageMsg.attachments[0] 
                embed.set_thumbnail(url=imgAttachment.url)
            
            await imageMsg.delete()
            await prompt.delete()
            await example.edit(embed=embed)
            continue

        if str(reactionAdd.emoji) == '🔁':
            embed.set_footer(icon_url = ctx.author.avatar_url,text=f'- {ctx.author.display_name}')
            embed.set_image(url='https://tenor.com/view/shark-gif-23766673.gif')
            embed.set_thumbnail(url='https://tenor.com/view/shark-gif-23766673.gif')
            await example.edit(embed=embed)
            await msg.remove_reaction('📡', ctx.author)
            await msg.remove_reaction('📸', ctx.author)
            await msg.remove_reaction('🖼️', ctx.author)
            await msg.remove_reaction('🔁', ctx.author)
            continue

        if str(reactionAdd.emoji) == '📢':
            await channel.send("||@everyone||")
            await channel.send(embed=embed)
            iterate = False
            return

        if str(reactionAdd.emoji) == '📨':
            await channel.send(embed=embed)
            iterate = False
            return

        if str(reactionAdd.emoji) == '❌':
            reactMessage.remove_field(0)
            reactMessage.add_field(name="❌ Cancelled ❌", 
            value="You have cancelled this announcement. \nRun the command again to start over.", inline=False)
            await msg.edit(embed=reactMessage)
            iterate = False
            return

        if str(reactionAdd.emoji) == '⏲️':
            prompt = await ctx.send("```Send the amount of hours you would like to wait until the message is sent. \n(i.e. if you would like to send your message in 5 hours simply type \"5\"```")
            hours = 1
            hours = await client.wait_for("message", check=msgcheck)
            hoursint = (hours.content)
            await hours.delete()
            await prompt.delete()
            await ctx.send(f'`you entered {hoursint} hour(s)`')
            yesnoEmbed = discord.Embed(title=f'Would you like to **@ everyone**') 
            yesnoMsg = await ctx.send(embed=yesnoEmbed)
            await yesnoMsg.add_reaction("✅")
            await yesnoMsg.add_reaction("❌")
            reactionAdd1, user2 = await client.wait_for('reaction_add', timeout=300.0, check=check)
            if reactionAdd1:
                if str(reactionAdd1.emoji) == '❌':
                    schedulemsg = await ctx.send('**Message has been scheduled!**')
                    await asyncio.sleep(int(hoursint) * 3600)
                    await schedulemsg.delete()
                    await ctx.send('Message Has Been Sent ✅')
                    await channel.send(embed=embed)
                if str(reactionAdd1.emoji) == '✅':
                    schedulemsg = await ctx.send('**Message has been scheduled!**')
                    await asyncio.sleep(int(hoursint) * 3600)
                    await schedulemsg.delete()
                    await ctx.send('Message Has Been Sent ✅')
                    await channel.send("||@everyone||")
                    await channel.send(embed=embed)
                
            iterate = False
            return

@announce.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the channel you want to send to. Usage: .announce (channel)')

#embed edit command
@client.command()
@commands.has_permissions(manage_messages=True) 
async def embededit(ctx, channel: discord.TextChannel, msgID):
    def check(msg):
        return msg.author == ctx.author
    embedmsg = await channel.fetch_message(msgID)
    for emb in embedmsg.embeds:
        title = emb.title
        description = emb.description
        footerText = emb.footer.text
        footerIconURL = emb.footer.icon_url
        image = emb.image.url
        thumbnail = emb.thumbnail.url

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reactions

    prompt=discord.Embed()
    prompt.add_field(name="What part of the embed would you like to edit!", 
    value="🖥️ - Edit the title. \n📝 - Edit the contents. \n📡 - Switch the footer of the embed. (ex: - fullblast network) \n📸 - Switch the image attached. **(must be a file upload. not from discords gifs.)** \n🖼️ - Switch the thumbnail. **(must be a file upload. not from discords gifs.)**", inline=False)

    reactMessage = await ctx.send(embed=prompt)

    await reactMessage.add_reaction("🖥️")
    await reactMessage.add_reaction("📝")
    await reactMessage.add_reaction("📡")
    await reactMessage.add_reaction("📸")
    await reactMessage.add_reaction("🖼️")
    await reactMessage.add_reaction("❌")

    valid_reactions = ['📡','🖥️', '❌', '📝', '📸', '🖼️']

    reactionAdd, user1 = await client.wait_for('reaction_add', timeout=60.0, check=check)
    if reactionAdd:
        if str(reactionAdd.emoji) == '📡':
            if 'Fullblast Network!' in footerText:
                footerIconURL = ctx.author.avatar_url
                footerText = f'- {ctx.author.display_name}'
            else:
                footerIconURL = client.user.avatar_url
                footerText = '- Fullblast Network!'
            embed=discord.Embed(title=title, description=description, color=0x2ecc71)
            embed.set_footer(icon_url = footerIconURL,text= footerText)
            embed.set_image(url=image)
            embed.set_thumbnail(url=thumbnail)
            await embedmsg.edit(embed=embed)
        
        if str(reactionAdd.emoji) == '📸':
            def msgcheck(msg):
                return msg.author == ctx.author
            prompt = await ctx.send("`Send the image or gif you would like to include.`")
            imageMsg = await client.wait_for("message", check=msgcheck)
            if imageMsg.attachments:
                imageNew = imageMsg.attachments[0] 
            
            await imageMsg.delete()
            await prompt.delete()
            embed=discord.Embed(title=title, description=description, color=0x2ecc71)
            embed.set_footer(icon_url = footerIconURL,text= footerText)
            embed.set_image(url=imageNew.url)
            embed.set_thumbnail(url=thumbnail)
            await embedmsg.edit(embed=embed)
            

        if str(reactionAdd.emoji) == '🖼️':
            def msgcheck(msg):
                return msg.author == ctx.author
            prompt = await ctx.send("`Send the image or gif you would like to include.`")
            imageMsg = await client.wait_for("message", check=msgcheck)
            if imageMsg.attachments:
                imageNew = imageMsg.attachments[0] 
            
            await imageMsg.delete()
            await prompt.delete()
            embed=discord.Embed(title=title, description=description, color=0x2ecc71)
            embed.set_footer(icon_url = footerIconURL,text= footerText)
            embed.set_image(url=image)
            embed.set_thumbnail(url=imageNew.url)
            await embedmsg.edit(embed=embed)
            

        if str(reactionAdd.emoji) == '🖥️':
            def msgcheck(msg):
                return msg.author == ctx.author
            preEdit = await ctx.send(f'```Here\'s the current title of the embed:\n\n{title}```')
            prompt = await ctx.send("**Send the new title!**")
            titleNew = await client.wait_for("message", check=msgcheck)
            actualTitleNew = titleNew.content
            
            await titleNew.delete()
            await prompt.delete()
            await preEdit.delete()
            embed=discord.Embed(title=actualTitleNew, description=description, color=0x2ecc71)
            embed.set_footer(icon_url = footerIconURL,text= footerText)
            embed.set_image(url=image)
            embed.set_thumbnail(url=thumbnail)
            await embedmsg.edit(embed=embed)
            

        if str(reactionAdd.emoji) == '📝':
            def msgcheck(msg):
                return msg.author == ctx.author
            preEdit = await ctx.send(f'```Here\'s the current description of the embed:\n\n{description}```')
            prompt = await ctx.send("**Send the new description!**")
            descNew = await client.wait_for("message", check=msgcheck)
            actualDescNew = descNew.content
            
            await descNew.delete()
            await prompt.delete()
            await preEdit.delete()
            embed=discord.Embed(title=title, description=actualDescNew, color=0x2ecc71)
            embed.set_footer(icon_url = footerIconURL,text= footerText)
            embed.set_image(url=image)
            embed.set_thumbnail(url=thumbnail)
            await embedmsg.edit(embed=embed)
            

        if str(reactionAdd.emoji) == '❌':
            prompt.remove_field(0)
            prompt.add_field(name="❌ Cancelled ❌", 
            value="You have cancelled this edit. \nRun the command again to start over.", inline=False)
            await reactMessage.edit(embed=prompt)
            return
            
    await ctx.send("**Successfully edited message!**")

@embededit.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the channel of the embed you want to edit. Usage: .embededit (channel) (msg id)')

#Roll the dice    
@client.command()
async def roll(ctx):
    dice = random.choice([1,2,3,4,5,6])
    embed=discord.Embed(title="Rolling the dice!")
    embed.add_field(name=f"It rolled a:", value=dice, inline=True)
    await ctx.send(embed=embed)

#Flip a coin
@client.command()
async def flip(ctx):
  coin=random.choice(['Heads!','Tails!'])
  embed=discord.Embed(title="Flipping a coin!")
  embed.add_field(name="It landed on: ", value=coin, inline=False)
  await ctx.send(embed=embed)

#Help Command
@client.command()
async def help(ctx):
  embed=discord.Embed(title="Fullblast Help", description="Prefix for this server is `.`", color=0x2f3136)
  embed.add_field(name="Fun:", value="```.flip\n.roll\n.rps\n.horny <user>\n.simp <user>\n.hug <user>\n.catfact\n.dogfact\n.tweet <contents>\n.8ball <question>```", inline=False)
  embed.add_field(name="Search:", value="```.lyrics <title>\n.pokedex <pokemon>```", inline=False)
  embed.add_field(name="Utility:", value="```.customgame```", inline=False)
  embed.set_footer(icon_url = client.user.avatar_url,text="- Fullblast Network")
  await ctx.channel.send(embed=embed)

#RPS
@client.command()  # ROCK PAPER SCISSORS
async def rps(ctx):
    comp = random.randint(1, 3)
    embed = discord.Embed(
        title="**Choose your figure:**", description="\n\n1) Rock :new_moon:\n\n2) Paper :page_facing_up:\n\n3) Scissors :scissors:\n\n(_ex:  rock **or** 1_)", colour=0x2ecc71)
    await ctx.send(embed=embed)
    figures = {1: 'rock', 2: 'paper', 3: 'scissors'}
    msg = await client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)
    if msg.content.lower() == "rock" or str(msg.content).lower() == "1":
        usr = 1
    elif msg.content.lower() == "paper" or str(msg.content).lower() == "2":
        usr = 2
    elif msg.content.lower() == "scissors" or str(msg.content).lower() == "3":
        usr = 3
    else:
        await ctx.send('Wrong response!')
        return
    timer = 0
    while usr == 0:
        await asyncio.sleep(3)
        timer += 3
        if timer > 10:
            await ctx.send('Game Over.')
            return
    await ctx.send('You chose **{}**.\n'.format(figures[usr]))
    await asyncio.sleep(1.5)
    await ctx.send("I chose **{}**!\n".format(figures[comp]))
    await asyncio.sleep(1)
    if comp == usr:
        await ctx.send("It's a **tie!** :necktie: :clown:")
    elif abs(comp - usr) == 1:
        if comp > usr:
            await ctx.send('I won! :partying_face: ')
        else:
            await ctx.send('You win! :flag_white: ')
    elif abs(comp - usr) == 2:
        if comp < usr:
            await ctx.send('I won! :partying_face: ')
        else:
            await ctx.send('You win! :flag_white: ')

#Giveaway
@client.command()
@commands.has_permissions(manage_messages=True)
async def gstart(ctx, hrs : int, *, prize:str):

    await ctx.message.delete()

    embed=discord.Embed(color=0x2f3136)
    embed.add_field(name="Giveaway!", value=f"{ctx.author.mention} is giving away `{prize}`! \nReact with 🎉 to enter!", inline=False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = hrs*3600)
    embed.add_field(name="Ends in:", value= f"{hrs} hour(s) from now!")
    embed.set_footer(text=f"Ends at {end.replace(microsecond=0)} UTC")
    my_msg = await ctx.send(embed=embed)
    await my_msg.add_reaction('🎉')
    await asyncio.sleep(hrs * 3600)
    new_msg = await ctx.channel.fetch_message(my_msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)
    embed1=discord.Embed(title=f'You just won `{prize}`!', color=0x2f3136) 
    await ctx.send(f"🎉 **CONGRATS {winner.mention}** 🎉")
    await ctx.send(embed=embed1)

#Status Command
@client.command()
@commands.has_permissions(manage_guild=True)
async def status(ctx, statusType: str, *, statusText):

    # Setting `Playing ` status
    if statusType.lower() == "playing":
        await client.change_presence(activity=discord.Game(name=statusText))

    # Setting `Streaming ` status
    if statusType.lower() == "streaming":
        await client.change_presence(activity=discord.Streaming(name=statusText, url=""))

    # Setting `Listening ` status
    if statusType.lower() == "listening":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=statusText))

    # Setting `Watching ` status
    if statusType.lower() == "watching":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=statusText))

    await ctx.send("**✅ Status Changed**")

#Invite Tracker
@client.command()
@commands.has_permissions(manage_messages=True) 
async def invites(ctx, user: discord.Member = None):
  if user == None:
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    await ctx.send(f"You've invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
  else:
    totalInvites = 0
    for i in await ctx.guild.invites():
       if i.inviter == user:
         totalInvites += i.uses
    await ctx.send(f"{user.mention} has invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")

#cat facts
@client.command()
async def catfact(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get("https://some-random-api.ml/animal/cat") as response:
      fact = (await response.json())["fact"]
      image = (await response.json())["image"]
      embed = discord.Embed(title=f'Random Cat Fact', description=f'Cat Fact: {fact}', colour=0x2ecc71)
      embed.set_image(url=image)
      embed.set_footer(text="")
      await ctx.send(embed=embed)

#dog facts
@client.command()
async def dogfact(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get("https://some-random-api.ml/animal/dog") as response:
      fact = (await response.json())["fact"]
      image = (await response.json())["image"]
      embed = discord.Embed(title=f'Random Dog Fact', description=f'Dog Fact: {fact}', colour=0x2ecc71)
      embed.set_image(url=image)
      embed.set_footer(text="")
      await ctx.send(embed=embed)

#horny command
@client.command()
async def horny(ctx, user: discord.Member = None):
    if user == None:
        authorAvatar = ctx.author.avatar_url_as(format='png')
        authorMsg = f'https://some-random-api.ml/canvas/horny?avatar={authorAvatar}'
        authorMsgActual = authorMsg[:-10]
        await ctx.send(authorMsgActual)
    
    if user is not None:
        userAvatar = user.avatar_url_as(format='png')
        userMsg = (f'https://some-random-api.ml/canvas/horny?avatar={userAvatar}')
        userMsgActual = userMsg[:-10]
        await ctx.send(userMsgActual)

#simp command
@client.command()
async def simp(ctx, user: discord.Member = None):
    if user == None:
        authorAvatar = ctx.author.avatar_url_as(format='png')
        authorMsg = f'https://some-random-api.ml/canvas/simpcard?avatar={authorAvatar}'
        authorMsgActual = authorMsg[:-10]
        await ctx.send(authorMsgActual)
    
    if user is not None:
        userAvatar = user.avatar_url_as(format='png')
        userMsg = (f'https://some-random-api.ml/canvas/simpcard?avatar={userAvatar}')
        userMsgActual = userMsg[:-10]
        await ctx.send(userMsgActual)

#pokedex
@client.command(aliases=['pd'])
async def pokedex(ctx, search):
  async with aiohttp.ClientSession() as session:
    async with session.get(f"https://some-random-api.ml/pokedex?pokemon={search}") as response: 

      

      name = (await response.json())["name"]
      description = (await response.json())["description"]
      
      type = (await response.json())["type"]
      typeList = json.dumps(type).strip('[]"').replace('", "', ', ')
      
      abilities = (await response.json())["abilities"]
      abilitiesList = json.dumps(abilities).strip('[]"').replace('", "', ', ')
      
      image = (await response.json())["sprites"]["animated"]
      generation = (await response.json())["generation"]
      id = (await response.json())["id"]

      species = (await response.json())["species"]
      speciesList = json.dumps(species).strip('[]"').replace('", "', ', ')
      speciesListNew = speciesList.replace('\\u00e9', 'e')

      height = (await response.json())["height"]
      weight = (await response.json())["weight"]

      
      #hp = (await response.json())["stats"][0]["hp"]
      #attack = (await response.json())["stats"][0]["attack"]
      #defense = (await response.json())["stats"][0]["defense"]
      #sp_atk = (await response.json())["stats"][0]["sp_atk"]
      #speed = (await response.json())["stats"][0]["speed"]
      #total = (await response.json())["stats"][0]["total"]
      #evolutionStage = (await response.json())["family"]["evolutionStage"]

      evolutionLine = (await response.json())["family"]["evolutionLine"]
      evolutionLineList = json.dumps(evolutionLine).strip('[]"').replace('", "', ', ')
      #evolutionLineListNew = evolutionLineList.replace('\u00e9', 'e')

      #await ctx.send(f"{name} | {description} | {typeList} | {abilitiesList} | {generation} | {id} | {speciesListNew} | {height} | {weight} | {evolutionStage} | {evolutionLineList}")

      embed = discord.Embed(title=f'Pokedex Entry: {name.upper()} \nID: {id}', description=f'Description: From generation {generation}. {description}', colour=0xe4000f)
      embed.add_field(name="Type", value=typeList, inline=True)
      embed.add_field(name="Species", value=speciesListNew, inline=True)
      embed.add_field(name="Abilities", value=abilitiesList, inline=True)
      embed.add_field(name="Height", value=height, inline=True)
      embed.add_field(name="Weight", value=weight, inline=True)
      #embed.add_field(name="Stats", value=f"HP: {hp} | Attack: {attack} | Defense: {defense} \nSpecial Attack: {sp_atk} | Speed: {speed} | Total: {total}", inline=False)
      embed.add_field(name="Evolution Line", value=evolutionLineList, inline=False)
      embed.set_thumbnail(url=image)
      await ctx.send(embed=embed)
      
      error = (await response.json())["error"]
      errorCode = json.loads(error)
      if "error" in errorCode:
          pass
      else:
          await ctx.send(error)
      
@pokedex.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the pokemon you want to look up. Usage: .pokedex (pokemon)')

#hug command
@client.command()
async def hug(ctx, user: discord.Member):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://some-random-api.ml/animu/hug") as response:
            link = (await response.json())["link"]
            embed = discord.Embed(title=f'{ctx.author.display_name} hugged {user.display_name}', colour=0x2ecc71)
            embed.set_image(url=link)
            await ctx.send(embed=embed)

@hug.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the person you want to hug. Usage: .hug <user>')

#tweet command
@client.command()
async def tweet(ctx, *, tweetString):

    await ctx.message.delete()

    oldUser = str(ctx.author)
    newUser = oldUser.replace("#", "")
    actualNewUser = newUser.replace(" ", "")

    tweetStringNew = str(tweetString.replace(' ', '%20'))

    #authorPFP = ctx.author.avatar_url
    #authorPfpActual = authorPFP[:-10]
    #await ctx.send(authorPfpActual)

    #await ctx.send(f"https://some-random-api.ml/canvas/tweet?avatar={ctx.author.avatar_url}&comment={tweetString}&displayname={ctx.author.dispaly_name}&username={ctx.author}")
    userAvatar = ctx.author.avatar_url_as(format='png')
    msgOld = (f"https://some-random-api.ml/canvas/tweet?comment={tweetStringNew}&displayname={ctx.author.display_name}&username={actualNewUser}&avatar={userAvatar}")
    msgNew = msgOld[:-10]
    await ctx.send(msgNew)

@tweet.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include the tweet contents. Usage: .tweet <contents>')

#lyrics command
@client.command()
async def lyrics(ctx, *, search):
  async with aiohttp.ClientSession() as session:
    async with session.get(f"https://some-random-api.ml/lyrics?title={search}") as response: 

      songTitle = (await response.json())["title"]
      author = (await response.json())["author"]
      
      lyrics = (await response.json())["lyrics"]
      
      #await ctx.send(songTitle)
      #await ctx.send(author)
      #await ctx.send(lyrics)

      thumbnail = (await response.json())["thumbnail"]["genius"]
      link = (await response.json())['links']["genius"]
      
      embed = discord.Embed(title=f'{songTitle}', url=link, description=f'Author: {author}\n\n**Lyrics:**\n{lyrics}', colour=0x2ecc71)
      embed.set_thumbnail(url=thumbnail)
      await ctx.send(embed=embed)

@lyrics.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include the song title. Usage: .lyrics <title>')

#polls
@client.command(aliases=['p'])
@commands.has_permissions(manage_messages=True)
async def poll(ctx, question, *options: str):

        await ctx.message.delete()

        if len(options) == 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0].lower() == 'yes' and options[1].lower() == 'no':
            reactions = ['✅', '❌']
        if len(options) == 0:
            reactions = ['✅', '❌']
            yesnoEmbed = discord.Embed(title=f'📥 {question}') 
            yesnoMsg = await ctx.send(embed=yesnoEmbed)
            await yesnoMsg.add_reaction("✅")
            await yesnoMsg.add_reaction("❌")
            return

        else:
            reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=f'📥 {question}', description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)

        poll_message = await ctx.channel.fetch_message(id)
        embed = poll_message.embeds[0]
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        print(f'unformatted{unformatted_options}')
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [client.user.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(reactor.id)
        output = f"Results of the poll for '{embed.title}':\n" + '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await ctx.send(output)

#CustomGame Command
@client.command()
async def customgame(ctx, *, players: int = 10):
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reactions
    valid_reactions = ['✅']
    embed=discord.Embed(title=f'{ctx.author.display_name} is starting a Custom Game!', description=f'This custom game will randomly split the participants into two teams. Be sure to have an even amount of players. \nReact to the message to be entered in. \n**The entry will close when {ctx.author.display_name} hits the ✅.** \n\n**Good Luck and Have Fun!**', color=0xec5b5b)
    embed.set_footer(text=f'Custom game entry is still open. Join Now!')
    entryMsg = await ctx.send(embed=embed)
    await entryMsg.add_reaction('🖐️')
    await entryMsg.add_reaction('✅')
    reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=check)
    if reaction:

        if str(reaction.emoji) == '✅':
            embed.set_footer(text=f'Custom game entry is closed!')
            await entryMsg.edit(embed=embed)
            message = await ctx.fetch_message(entryMsg.id)
            users = await message.reactions[0].users().flatten()
            
            users.pop(0)

            random.shuffle(users)
            team1 = []
            team2 = []
            i = 0
            for member in users:
                if (i % 2) == 0:
                    team1.append(member.name)
                else:
                    team2.append(member.name)
                
                i += 1

            team1String = '\n'.join(team1)
            team2String = '\n'.join(team2)


            embed2=discord.Embed(title=f'Custom game of {(len(team1))+(len(team2))} players!', color=0xec5b5b)
            embed2.add_field(name="Team 1", value=team1String)
            embed2.add_field(name="Team 2", value=team2String)
            embed2.set_footer(text=f'GLHF!')
            await ctx.send(embed=embed2)

#Warn Command
@client.command()
@commands.has_permissions(manage_messages=True) 
async def warn(ctx, user: discord.Member, *, message):
    
    embed=discord.Embed(title="⚠️ You have been warned ⚠️")
    embed.add_field(name="Reason:", value=message, inline=True)
    embed.set_footer(text='- If you would like to dispute this, please open a ticket.')
    await user.send(embed=embed)



@warn.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the user you would like to warn. Usage: .warn <user> <reason>')


#DYNAMIC VC ----------------------------------------------------------

@client.event
async def on_voice_state_update(member, before, after):
    #staffTesting = client.get_channel(812224835605757972)
    
    if after.channel != None:
        #DUO VC
        if after.channel.id == 904799724777926676:
            for guild in client.guilds:
                maincategory = discord.utils.get(
                    guild.categories, id=904800146569699399)
                channel2 = await guild.create_voice_channel(name=f'♦ Duo with {member.display_name}', category=maincategory, user_limit=2)
                await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                await member.move_to(channel2)

                def check(x, y, z):
                    return len(channel2.members) == 0
                await client.wait_for('voice_state_update', check=check)
                await channel2.delete()
        #TRIO VC
        if after.channel.id == 904799755924832318:
            for guild in client.guilds:
                maincategory = discord.utils.get(
                    guild.categories, id=904800146569699399)
                channel2 = await guild.create_voice_channel(name=f'♦ Trio with {member.display_name}', category=maincategory, user_limit=3)
                await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                await member.move_to(channel2)

                def check(x, y, z):
                    return len(channel2.members) == 0
                await client.wait_for('voice_state_update', check=check)
                await channel2.delete()
        #QUAD VC
        if after.channel.id == 904799785498849310:
            for guild in client.guilds:
                maincategory = discord.utils.get(
                    guild.categories, id=904800146569699399)
                channel2 = await guild.create_voice_channel(name=f'♦ Quad with {member.display_name}', category=maincategory, user_limit=4)
                await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                await member.move_to(channel2)

                def check(x, y, z):
                    return len(channel2.members) == 0
                await client.wait_for('voice_state_update', check=check)
                await channel2.delete()
        #SQUAD VC
        if after.channel.id == 904799833745924157:
            for guild in client.guilds:
                maincategory = discord.utils.get(
                    guild.categories, id=904800146569699399)
                channel2 = await guild.create_voice_channel(name=f'♦ Squad with {member.display_name}', category=maincategory, user_limit=5)
                await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                await member.move_to(channel2)

                def check(x, y, z):
                    return len(channel2.members) == 0
                await client.wait_for('voice_state_update', check=check)
                await channel2.delete()
        #GAME HUB
        if after.channel.id == 917192168882450512:
            for guild in client.guilds:
                boolean = True
                maincategory = discord.utils.get(
                    guild.categories, id=904800146569699399)
                for activity in member.activities:
                    x = isinstance(activity, discord.Game)
                    y = isinstance(activity, discord.Activity)
                    if x or y: 
                        gameName = activity.name  
                        channel2 = await guild.create_voice_channel(name=f'{gameName} | {member.display_name}', category=maincategory)
                        boolean = False
                if boolean == True:
                    channel2 = await guild.create_voice_channel(name=f'Game Hub | Not playing.', category=maincategory)
                    #await staffTesting.send(f'{after.member.name} joined game hub without playing a game!')
                await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                await member.move_to(channel2)        

                def check(x, y, z):
                    return len(channel2.members) == 0
                await client.wait_for('voice_state_update', check=check)
                await channel2.delete()        



#ACTIVATE AND PING -------------------------------------------------------
client.run(token)