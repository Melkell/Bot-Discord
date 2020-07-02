#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.utils import get


# create bot
bot = commands.Bot(command_prefix='!')
warnings = {}

with open('warnings.json', 'r') as infile:
    warnings = json.load(infile)

# detect when the bot is online
@bot.event
async def on_ready():
    print("Bot online")
    await bot.change_presence(status = discord.Status.idle, activity=discord.Game("Mel is doing some dumb shit"))
    
#dectect when someone add an emoji on a message
@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    canal = payload.channel_id
    mess = payload.message_id
    
    python_role = get(bot.get_guild(payload.guild_id).roles, name="python")
    membre = bot.get_guild(payload.guild_id).get_member(payload.user_id)
    

    if canal == 728229687364419675 and mess == 728230383757426759 and emoji == "python":
        print("Grade ajouté")
        await membre.add_roles(python_role)
        await membre.send("Tu obtiens le grade python !")
        
@bot.event
async def on_raw_reaction_remove(payload):
    emoji = payload.emoji.name
    canal = payload.channel_id
    mess = payload.message_id
    
    python_role = get(bot.get_guild(payload.guild_id).roles, name="python")
    membre = bot.get_guild(payload.guild_id).get_member(payload.user_id)
    

    if canal == 728229687364419675 and mess == 728230383757426759 and emoji == "python":
        print("Grade supprimé")
        await membre.remove_roles(python_role)
        await membre.send("Tu perds le grade python !")
        
#create command !rules
@bot.command()
async def regles(ctx):
    await ctx.send("Les règles:")
    
    
# create command !warning
@bot.command()
@commands.has_role("Admin")
async def warning(ctx, membre: discord.Member):
    pseudo = membre.mention
    id = membre.id

    # if the membre doesn't have warnings
    if id not in warnings:
        warnings[id] = 0
        print("Le membre n'a aucun avertissement")

    warnings[id] += 1

    print("ajoute l'avertissement", warnings[id], "/3")

    # check the number f warning
    if warnings[id] == 3:
        
        warnings[id] = 0
        # message
        await membre.send("Vous avez été éjécté du serveur ! trop d'avertissements !")
        # kick member
        await membre.kick()

    # update the json file
    with open('warnings.json', 'w') as outfile:
        json.dump(warnings, outfile)

    await ctx.send(f"Le membre {pseudo} a reçu une alerte ! Attention à bien respecter les regles")

# check error with !warning
@warning.error
async def on_command_error(ctx, error):
    # detect error
    if isinstance(error, commands.MissingRequiredArgument):
        # send message
        await ctx.send("Tu dois faire !warning @pseudo")


    
#create command !bienvenue @pseudo
@bot.command()
async def bienvenue(ctx, new_member: discord.Member):
    #recupere le pseudo
    pseudo = new_member.mention
    
    # Execute !welcome
    await ctx.send(f"Bienvenue à {pseudo} sur le serveur Discord ! N'oublie pas de faire !regles")

#check error
@bienvenue.error
async def on_command_error(ctx, error):
    #detect error
    if isinstance(error, commands.MissingRequiredArgument):
        # send a message
        await ctx.send("Mauvaise manipulation ! Tu dois faire !bienvenue @pseudo")

# give token to the bot
jeton = "NzE4ODA4NzY4NTk4NzY5NzE3.XtuagQ.LDz1AiJ5C38yyPKaRcH6d6XKwhw"


#run bot
bot.run(jeton)
