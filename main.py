import sys 
sys.dont_write_bytecode = True
import discord
from discord import client
from discord.ext import commands
import asyncio
import logging
from discord import app_commands
from colorama import Fore
import colorama
import assets.promotion.promotion_levels as config2
import assets.config as config
import openai
colorama.init()


openai.api_key = ''



client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)
client = commands.Bot(command_prefix='/', intents=discord.Intents.all(), application_id="1103011106550710322")
# Logging info
logging.basicConfig(filename="assets/logs/log.txt", level=logging.INFO, format="%(asctime)s %(message)s")

@client.event
async def on_ready():
    activity=discord.Activity(type=discord.ActivityType.streaming, name="/help")
    await client.change_presence(status=discord.Status.idle ,activity=activity)
    print("""
SSPS My beloved
    """)
    synced = await client.tree.sync()
    print("Slash CMDs Synced " + str(len(synced)) + " Commands")



# <------Joining Member------->
@client.event
async def on_member_join(member: discord.Member):
    try:
            print("Recognised that a member called " + member.name + " joined the Server")
            channel = client.get_channel(1101884786571739186)
            server = member.guild
            embed = discord.Embed(title=f"**Welcome {member.name}**👋" ,
                                color=discord.Color.blue())
            embed.add_field(name="📚**Rules**",value="Please make sure that you read the rules")
            embed.add_field(name="❓**Support**",value="If you have any questions open a ticket ")
            embed.add_field(name="🍿**Enjoy**",value=f"Have Fun and enjoy chatting and talking on the Server **{server.name}**")
            embed.set_footer(text="⭐  • SSPŠ 0.K | Systems")
            await channel.send(embed=embed)
    except Exception as e:
        print(e) 




# <---------ban command---------->
@client.tree.command(name="ban", description="ban a user")
async def ban_user(interaction: discord.Interaction, user: discord.User, reason: str = None):
    if config.BAN == True:
        if interaction.user.guild_permissions.ban_members:
            await user.ban(reason=reason)
            embed = discord.Embed(title=f"**{user.name} was banned by {interaction.user.name}**",
                                color=discord.Colour.random())
            embed.add_field(name="📆**Date **", value=interaction.created_at.strftime("%Y-%m-%d"))
            embed.add_field(name="🆔**User ID**", value=user.id)
            embed.add_field(name="💬**Reason**", value=reason)
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed)
            logging.info(f"Command = ban ; Author = {interaction.user.name} ; Banned = {str(user.name)}; Reason = {reason}")
        else:
            embed = discord.Embed(title="**You don't have the permission for that Command**", color=discord.Colour.random())
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)





# <------kick command----->
@client.tree.command(name="kick", description="kick a user")
async def kick(interaction: discord.Interaction, user: discord.User, reason: str = None):
    if config.KICK == True:
        channel = interaction.channel
        server = interaction.guild
        if interaction.user.guild_permissions.kick_members:
            await user.kick(reason=reason)
            embed = discord.Embed(title=f"**{user.name} was kicked by {interaction.user.name}**",
                                color=discord.Colour.random())
            embed.add_field(name="📆**Date **", value=interaction.created_at.strftime("%Y-%m-%d"))
            embed.add_field(name="🆔**User ID**", value=user.id)
            embed.add_field(name="💬**Reason**", value=reason)
            embed.set_thumbnail(url=server.icon.url)
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            logging.info(f"Command = kick ; Author = {interaction.user.name} ; kicked = {str(user.name)}; Reason = {reason}")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="**You don't have the permission for that Command**",
                                color=discord.Colour.random())
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)

    



@client.tree.command(name="gen", description="generates an AI message")
async def gen(interaction: discord.Interaction, text: str):
    if config.GENERATOR == True:
        await interaction.response.defer()
        response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"{text}\n",
                    max_tokens=350,
                    temperature=1,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                ).choices[0].text
        print(f'{Fore.BLUE}Author: {interaction.user.name}')
        print(f'{Fore.CYAN}Message: {text}')
        print(f'{Fore.GREEN}Response: {response}{Fore.RESET}')
        embed = discord.Embed(title=f"**AI to {interaction.user.name}**",
                                color=discord.Colour.random())
        embed.add_field(name='**User -->**', value=text)
        embed.add_field(name="🔍**AI -->**", value= response, inline= False)
        embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
        await asyncio.sleep(5)
        await interaction.followup.send(embed=embed)
        logging.info(f"Command = gen ; Author = {interaction.user.name} ; Message = {text}; Response = {response}")
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)



# <------help command---------->
@client.tree.command(name="help", description="help command")
async def help(interaction: discord.Interaction):
    if config.HELP_COMMAND == True:
        embed = discord.Embed(title="**Command-List for SSPŠ BOT**", color=discord.Colour.random())
        embed.add_field(name="🌐**help**", value="list of all commands")
        embed.add_field(name="🎭**avatar**", value="shows a users avatar")
        embed.add_field(name="ℹ️**serverinfo**", value="gives info about the server")
        embed.add_field(name="⚙️**admin**", value="list all admin commands")
        embed.add_field(name="ℹ️**userinfo**", value="gives information about an user")
        embed.add_field(name="🔰**roles**", value="list all server roles")
        embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)

@client.tree.command(name="owner", description = "shows name of an owner")
async def owner(interaction: discord.Interaction):
    embed = discord.Embed(title="**Owner** -->", description= "Majitelé tohoto discord bota jsou prestižní studenti z 0.K", color=discord.Colour.random())
    embed.set_image(url="https://cdn.discordapp.com/emojis/1103000296478748862.webp?size=44&quality=lossless")
    await interaction.response.send_message(embed=embed)


# <---------serverinfo command---------->
@client.tree.command(name="serverinfo", description="shows you basic info about the server")
async def serverinfo(interaction: discord.Interaction):
    if config.SERVER_INFO == True:
        server = interaction.guild
        embed = discord.Embed(title=f"Server Info for {server.name}", color=discord.Colour.random())
        embed.add_field(name="💬**Server Name**", value=server.name)
        embed.add_field(name="🆔**Server ID**", value=server.id)
        embed.add_field(name="📆**Created On**", value=server.created_at.strftime('%Y-%m-%d'))
        embed.add_field(name="👑**Server Owner**", value=server.owner)
        embed.add_field(name="👥**Server Member Count**", value=server.member_count)
        embed.set_thumbnail(url=server.icon.url)
        embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
        await interaction.response.send_message(embed=embed)
    else: 
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)



@client.tree.command(name="admin", description="lists you all admin commands")
async def admin(interaction: discord.Interaction):
    if config.ADMIN == True:
        if interaction.user.guild_permissions.administrator:
            embed = discord.Embed(title="**Admin-Command List**", color=discord.Colour.random())
            embed.add_field(name="🌐**.kick**", value="kicks a user")
            embed.add_field(name="🚫**.ban**", value="bans a user")
            embed.add_field(name="🧼**.clear**", value="clear chat messages")
            embed.add_field(name="🔐**.mute**", value="chat-locks a user")
            embed.add_field(name="🔓**.unmute**", value="unlock a user (from the chat)")
            embed.add_field(name="⚙️**.admin**", value="list all admin commands")
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="**You don't have the permission for that Command**",
                                color=discord.Colour.random())
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)



@client.tree.command(name='rules', description='Here are some general rules you may want to consider for your Discord server')
async def rules(interaction: discord.Interaction):
    if config.RULES == True:
        if interaction.user.guild_permissions.administrator:
            embed = discord.Embed(title="**Rules**", color=discord.Colour.blurple())
            embed.add_field(name="**1**", value="respektujte se")
            embed.add_field(name="**2**", value="nsfw jen ve formě hentai v #⁠hentai-only jinak ban", inline=False)
            embed.add_field(name="**3**", value="Udrzujte demokracii", inline= False)  
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="**You don't have the permission for that Command**",
                                    color=discord.Colour.random())
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)



@client.tree.command(name="znackaslusnost", description="Naučí debily slušnému chování")
async def slusnost(interaction: discord.Interaction):
        embed = discord.Embed(title=f"**Značka slušnost**",
                              color=discord.Colour.random())
        embed.add_field(name = 'Ahoj, vidím že jsi nevychovaný spratek. Bude ti tímto udělena hodnost čůráka, jelikož i já robot vím, jak slušně pozdravit a poděkovat.', value='Nashledanou')
        embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
        await interaction.response.send_message(embed=embed)



# <----------basic clear command---------->
@client.tree.command(name="clear", description="clears chat messages")
async def clear(interaction: discord.Interaction, amount: int = 0):
    if config.CLEAR == True:
        channel = interaction.channel
        if interaction.user.guild_permissions.manage_messages:
            try:
                await interaction.response.defer()
                await channel.purge(limit=amount + 1)
                embed = discord.Embed(title=f"{interaction.user.name} cleared {amount} Messages",
                                    color=discord.Colour.random())
                embed.add_field(name="🆔 **User ID**", value=interaction.user.id)
                embed.add_field(name="📆**Cleared Messages At**", value=interaction.created_at.strftime("%Y-%m-%d %H:%M:%S"))
                embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                await asyncio.sleep(2)
                await interaction.followup.send(embed=embed)
                logging.info(f"Command = clear ; Author = {interaction.user.name} ; Cleared = {amount}")
            except ValueError:
                embed = discord.Embed(title="**Please enter a valid number of messages to delete.**",
                                    color=discord.Colour.random())
                embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="**You don't have the permission for that Command**",
                                color=discord.Colour.random())
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else: 
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)



# <-------unmute-command---------->
@client.tree.command(name="unmute", description="unmutes a user from the chat")
async def unmute_user(interaction: discord.Interaction, user: discord.User, reason: str = None):
    if config.MUTE == True:
        channel = interaction.channel
        if interaction.user.guild_permissions.manage_messages:
            await channel.set_permissions(user, send_messages=True)
            embed = discord.Embed(
                title=f"**{user.name} has been unmuted by {interaction.user.name}**",
                color=discord.Colour.random())
            embed.add_field(name="🆔**User ID**", value=user.id)
            embed.add_field(name="💬**Reason**", value=reason)
            embed.add_field(name="📆**Unmuted on**", value=interaction.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            embed.set_footer(text="⭐  • SSPŠ 0.K | Systems")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)

# <-------mute-command------->
@client.tree.command(name="mute", description="mutes a user from the chat")
async def mute_user(interaction: discord.Interaction, user: discord.User, reason: str = None, time: int = 0):
    if config.MUTE == True:
        channel = interaction.channel
        if interaction.user.guild_permissions.manage_messages:
            await channel.set_permissions(user, send_messages=False)
            embed = discord.Embed(
                title=f"**{user.name} has been muted by {interaction.user.name}**",
                color=discord.Colour.red())
            embed.add_field(name="🆔**User ID**", value=user.id)
            embed.add_field(name="💬**Reason**", value=reason)
            embed.add_field(name="📆**Muted on**", value=interaction.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            embed.add_field(name="🕒**Muted for**", value=f"{time} seconds")
            embed.set_footer(text="⭐  • SSPŠ 0.K | Systems")
            await interaction.response.defer()
            await interaction.followup.send(embed=embed)
            await asyncio.sleep(time)
            await channel.set_permissions(user, send_messages=True)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)

#<------info command------>

@client.tree.command(name='broadcast', description='Broadcasts message to announcement room')
async def broadcast(interaction: discord.Interaction, message: str):
    if config.BROADCAST == True:
        if interaction.user.guild_permissions.administrator:
            channel = client.get_channel(1101885160531705938)
            embed = discord.Embed(title='** :gem: Announcement :gem: ** ', color=discord.Color.blurple())
            embed.add_field(name=message, value=f'Za prestižní třídu: {interaction.user.name}')
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await channel.send(embed=embed)
            embed2 = discord.Embed(title='**Sended** ', color=discord.Color.blurple())
            await interaction.response.send_message(embed=embed2)
        else:
            embed = discord.Embed(title="**You don't have the permission for that Command**",
                                color=discord.Colour.random())
            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else: 
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)


# for getting userinfo

@client.tree.command(name="userinfo", description="gives information about a user")
async def userinfo(interaction: discord.Interaction, user: discord.User):
    if config.USER_INFO == True:
        rolelist = []
        for role in user.roles:
            if role.name != "@everyone":
                rolelist.append(role.mention)
        b = ",".join(rolelist)

        embed = discord.Embed(title=f"**User Info about {user}**",
                            color=discord.Colour.purple())
        embed.add_field(name="🆔**User ID**", value=user.id)
        embed.add_field(name="📆**Created at**",value=user.created_at.strftime("%Y-%m-%d"))
        embed.add_field(name="🕗**Joined at**", value=user.joined_at.strftime("%Y-%m-%d"))
        embed.add_field(name=f"🔰**Role:** ({len(rolelist)})",value="".join([b]))
        embed.add_field(name=f"🎖**Top-Role**",value=user.top_role.mention)
        embed.add_field(name=f"🏆**Booster**",value=f'{"Yes" if user.premium_since else "No"}')
        embed.add_field(name="🤖**Bot**",value=f"{'Yes' if user.bot else 'No'}")
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_footer(text="⭐  • SSPŠ 0.K | Systems")
        await interaction.response.send_message(embed=embed)
    else: 
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)

#<-------Avatar-Command------------>
# shows a discord users avatar  as "big" format in the chat
@client.tree.command(name="avatar", description="prints the users avatar")
async def avatar(interaction: discord.Interaction, user: discord.User):
    if config.AVATAR == True:
        userAvatarUrl = user.avatar.url
        embed = discord.Embed(title=f"**{user}s Avatar:**",color=discord.Colour.yellow()).set_image(url=user.avatar.url)
        embed.set_footer(text="⭐  • SSPŠ 0.K | Systems")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='chad', description='Sends a chad gif')
async def chad(interaction: discord.Interaction, user: discord.User):
    if config.CHAD == True:
        embed = discord.Embed(title=f"**{user.name} is truly a chad**",color=discord.Colour.random())
        embed.set_image(url="https://media.tenor.com/epNMHGvRyHcAAAAd/gigachad-chad.gif")
        embed.set_footer(text="⭐  • SSPŠ 0.K | Systems")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)

@client.tree.command(name='skull', description='Sends a skull gif')
async def skull(interaction: discord.Interaction):
    if config.SKULL == True:
        embed = discord.Embed(title=f"**Skull**",color=discord.Colour.random())
        embed.set_image(url="https://media.tenor.com/g1bZgt4-tL4AAAAC/skull.gif")
        embed.set_footer(text="⭐  • SSPŠ 0.K | Systems")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='Error', description = 'Command is deactivated', color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='promote', description='Gives a Special **Permision**')
async def star(interaction: discord.Interaction, user: discord.Member, reason: str):
    try:
        if config.STAR:
            if interaction.user.guild_permissions.administrator:
                if config2.PROMOTION is None:
                    embed = discord.Embed(title='Error', description='Set promotion level', color=discord.Colour.red())
                    await interaction.response.send_message(embed=embed)
                else:
                    if config2.PROMOTION == 3:                        
                        role_id = 1101872150186569828
                        role = interaction.guild.get_role(role_id)
                        if role in user.roles:
                            embed = discord.Embed(title='Error', description='User is already promoted', color=discord.Colour.red())
                            await interaction.response.send_message(embed=embed)
                        else:    
                            await user.add_roles(role)
                            embed = discord.Embed(title='**Promotion**', color=discord.Colour.random())
                            embed.add_field(name=f'**{interaction.user.name} promoted {user.name} for {reason}**', value='')
                            
                            if user.avatar:
                                embed.set_image(url=user.avatar.url)
                                
                            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                            await interaction.response.send_message(embed=embed)
                    elif config2.PROMOTION == 2:
                        role_id = 1101872150186569828
                        role = interaction.guild.get_role(role_id)
                        if role in user.roles:
                            embed = discord.Embed(title='Error', description='User is already promoted', color=discord.Colour.red())
                            await interaction.response.send_message(embed=embed)
                        else:    
                            await user.add_roles(role)
                            embed = discord.Embed(title='**Promotion**', color=discord.Colour.random())
                            embed.add_field(name=f'**{interaction.user.name} promoted {user.name} for {reason}**', value='')
                            
                            if user.avatar:
                                embed.set_image(url=user.avatar.url)
                                
                            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                            await interaction.response.send_message(embed=embed)
                    elif config2.PROMOTION == 1:
                        role_id = 1101872150186569828
                        role = interaction.guild.get_role(role_id)
                        if role in user.roles:
                            embed = discord.Embed(title='Error', description='User is already promoted', color=discord.Colour.red())
                            await interaction.response.send_message(embed=embed)
                        else:    
                            await user.add_roles(role)
                            embed = discord.Embed(title='**Promotion**', color=discord.Colour.random())
                            embed.add_field(name=f'**{interaction.user.name} promoted {user.name} for {reason}**', value='')
                            
                            if user.avatar:
                                embed.set_image(url=user.avatar.url)
                                
                            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                            await interaction.response.send_message(embed=embed)
                    else:
                        embed = discord.Embed(title='Error', description='Promotion level not valid', color=discord.Colour.red())
                        await interaction.response.send_message(embed=embed)             
            else:
                embed = discord.Embed(title="**You don't have the permission for that command**", color=discord.Colour.random())
                embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title='Error', description='Command is deactivated', color=discord.Colour.red())
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e) 
    
@client.tree.command(name= 'demote', description='Removes a Special **Permision**')
async def star(interaction: discord.Interaction, user: discord.Member):
    try:
        if config.STAR:
            if interaction.user.guild_permissions.administrator:
                if config2.PROMOTION is None:
                    embed = discord.Embed(title='Error', description='Set promotion level', color=discord.Colour.red())
                    await interaction.response.send_message(embed=embed)
                else: 
                    if config2.PROMOTION == 3:
                        role_id = 1101872150186569828
                        role = interaction.guild.get_role(role_id)
                        if role in user.roles:
                            await user.remove_roles(role)
                            embed = discord.Embed(title='**Demotion**', color=discord.Colour.random())
                            embed.add_field(name=f'**{interaction.user.name} demoted {user.name}**', value='')
                            await interaction.response.send_message(embed=embed)
                        else:    
                            embed = discord.Embed(title='Error', description='User is already demoted', color=discord.Colour.red())
                            await interaction.response.send_message(embed=embed)
                            if user.avatar:
                                embed.set_image(url=user.avatar.url)
                                
                            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                            await interaction.response.send_message(embed=embed)
                    elif config2.PROMOTION == 2:
                        role_id = 1101872150186569828
                        role = interaction.guild.get_role(role_id)
                        if role in user.roles:
                            await user.remove_roles(role)
                            embed = discord.Embed(title='**Demotion**', color=discord.Colour.random())
                            embed.add_field(name=f'**{interaction.user.name} demoted {user.name}**', value='')
                            await interaction.response.send_message(embed=embed)
                        else:    
                            embed = discord.Embed(title='Error', description='User is already demoted', color=discord.Colour.red())
                            await interaction.response.send_message(embed=embed)
                            if user.avatar:
                                embed.set_image(url=user.avatar.url)
                                
                            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                            await interaction.response.send_message(embed=embed)
                    elif config2.PROMOTION == 1:
                        role_id = 1101872150186569828
                        role = interaction.guild.get_role(role_id)
                        if role in user.roles:
                            await user.remove_roles(role)
                            embed = discord.Embed(title='**Demotion**', color=discord.Colour.random())
                            embed.add_field(name=f'**{interaction.user.name} demoted {user.name}**', value='')
                            await interaction.response.send_message(embed=embed)
                        else:    
                            embed = discord.Embed(title='Error', description='User is already demoted', color=discord.Colour.red())
                            await interaction.response.send_message(embed=embed)
                            if user.avatar:
                                embed.set_image(url=user.avatar.url)
                                
                            embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                            await interaction.response.send_message(embed=embed)
                    else:
                        embed = discord.Embed(title='Error', description='Promotion level not valid', color=discord.Colour.red())
                        await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title="**You don't have the permission for that command**", color=discord.Colour.random())
                embed.set_footer(text="⭐  SSPŠ 0.K | Prestiž")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title='Error', description='Command is deactivated', color=discord.Colour.red())
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e) 

client.run(config.TOKEN)