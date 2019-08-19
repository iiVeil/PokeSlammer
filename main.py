import discord
from discord.ext import commands, tasks
import requests
import aiofiles
import datetime
import asyncio
import os
import aiohttp
import base64
import random
import time
import string
import aioconsole
import re
import sys

args = {}
args['pythonFile'] =  sys.argv[0]

for arg in sys.argv[1:]:
  variable = re.search('\-\-(.*)\=',arg)
  variable = variable.group(1)
  value = re.search('\=(.*)',arg)
  value = value.group(1)
  args[variable] = value


start_time = time.time()
bot_prefix = args['bot_prefix'] # Bot prefix has been moved to the .bat files
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command('help')
user_token = args['user_token'] # User token has been moved to the .bat files

client.spammer = False
client.active_guild = None
client.active_channel = None
client.spamming_ = False
client.n_pokemon = 0
client.balance = 0
client.caching = False
client.blacklist = []
client.whitelist = []
client.whitelistactive = False
client.blacklistactive = False
client.remote_console_ = False

'''CONFIG START'''
client.poke_prefix = 'p!' # The prefix of your pokecord bot
#client.allowed_users = [user.id, 300307874725494784]
client.allowed_users = [] # Any user-id you would like to be able to use the bot commands
client.autocatcher = True # Determines whether the Autocatcher will start on or off, Can be toggled with a command. [True | False]
client.identifier = False # Determines whether the Identifier will start on or off, Can be toggled with a command. [True | False]
'''CONFIG END'''

# BOT COMMAND LIST -> https://github.com/iiVeil/PokeSlammer/blob/master/COMMAND_LIST.txt

@client.event
async def on_message(message):
    await client.wait_until_ready()
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    hour = hour
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    try:
        if message.guild != client.active_guild:
            if message.author.id in client.allowed_users:
                await client.process_commands(message)
            return
        if client.remote_console_:
            print(f'{time} [REMOTE CONSOLE][CONTENT] -> {message.content}')
            try:
                print(f'{time} [REMOTE CONSOLE][TITLE] -> {message.embeds[0].title}\n')
            except Exception:
                pass
            try:
                print(f'{time} [REMOTE CONSOLE][DESCRIPTION] -> {message.embeds[0].description}\n')
            except Exception:
                pass
            try:
                print(f'{time} [REMOTE CONSOLE][FOOTER] -> {message.embeds[0].footer.text}\n')
            except Exception:
                pass
            client.remote_console_ = False
        '''
        Caching
        '''
        try:
            if client.caching == True:
                if message.author.id == 365975655608745985:
                    if message.embeds[0].title == 'Your pokémon:':
                        client.n_pokemon = message.embeds[0].footer.text.split(' ')
                        client.n_pokemon = int(client.n_pokemon[3])
                        await message.channel.send(f'**Cached `{client.n_pokemon}` into `client.n_pokemon`**')
                        print(f'{time} [CACHED] -> {client.n_pokemon} pokemon')
                    elif message.embeds[0].description.find('You currently have') != -1:
                        list = message.embeds[0].description.split(' ')
                        balance = list[3]
                        list = balance.split(',')
                        balance = ''
                        for element in list:
                            balance += element
                        client.balance = int(balance)
                        await message.channel.send(f'**Cached `{client.balance}` into `client.balance`**')
                        print(f'{time} [CACHED] -> {client.balance} balance\n')
                        client.caching=False
        except Exception:
            client.caching=False
        '''
        Events
        '''
        if message.author.id == 365975655608745985:
            if message.content.find(f'Congratulations <@{client.user.id}>') != -1:
                list = message.content.split('!')
                message = f'[CATCH] ->{list[1]}'
                try:
                    if list[2] == ' Added to Pokédex.':
                        message += ' | NEW'
                except IndexError:
                    message += ' '
                print(f'{time} ' + message + '\n')
        try:
            if message.embeds[0].description.find('is now level ') != -1:
                print(f'{time} [LEVEL] -> {message.embeds[0].description}\n')
        except Exception:
            pass
        '''PokeIdentifier'''
        if client.identifier == True:
            try:
                if message.author.id == 365975655608745985:
                    try:
                        url = message.embeds[0].image.url
                    except Exception:
                        pass
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    f = await aiofiles.open(f'./temp/temp.png', 'wb')
                                    await f.write(await resp.read())
                                    await f.close()
                                    f = await aiofiles.open(f'./temp/temp.png', 'rb')
                                    string = str(base64.b64encode(await f.read()))
                                    await f.close()
                                    os.remove(f'./temp/temp.png')
                                    for poket in os.listdir('./pokemon'):
                                        f = await aiofiles.open(f'./pokemon/{poket}', 'r')
                                        if await f.read() == string[2:-1]:
                                            await message.channel.send(f'Indentified: {poket[:-4]}')
                                            print(f'{time} [IDENTIFIER] -> {poket[:-4]}\n')
                                        await f.close()
                    except Exception:
                        pass
            except Exception:
                        pass
        '''
        AutoCatcher
        '''
        if client.autocatcher == True:
            try:
                if message.author.id == 365975655608745985:
                    try:
                        url = message.embeds[0].image.url
                    except Exception:
                        pass
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    if client.spammer:
                                        client.spammer = not client.spammer
                                        client.spamming_ = not client.spamming_
                                    f = await aiofiles.open(f'./temp/temp.png', 'wb')
                                    await f.write(await resp.read())
                                    await f.close()
                                    f = await aiofiles.open(f'./temp/temp.png', 'rb')
                                    string = str(base64.b64encode(await f.read()))
                                    await f.close()
                                    os.remove(f'./temp/temp.png')
                                    for poket in os.listdir('./pokemon'):
                                        f = await aiofiles.open(f'./pokemon/{poket}', 'r')
                                        if await f.read() == string[2:-1]:
                                            if client.whitelistactive:
                                                if str.lower(poket[:-4]) not in client.whitelist:
                                                    continue
                                            if client.blacklistactive:
                                                if str.lower(poket[:-4]) in client.blacklist:
                                                    continue
                                            if poket[:-4] == 'Nidoran_f' or poket[:-4] == 'Nidoran_m':
                                                await message.channel.send(f'{client.poke_prefix}catch nidoran')
                                            else:
                                                await message.channel.send(f'{client.poke_prefix}catch {poket[:-4]}')
                                        await f.close()
                                    if client.spamming_:
                                        client.spammer = not client.spammer
                                        client.spamming_ = not client.spamming_
                    except Exception:
                        pass
            except Exception:
                pass

    except Exception as e:
        print(f'[ERROR] -> {e}\n')
    try:
        if message.author.id in client.allowed_users:
            await client.process_commands(message)
    except Exception as e:
        pass

@client.event
async def on_ready():
    spam_.start()
    console_commands_.start()
    print(f"--[HOOKED]--\nDeveloped by iiVeil#0001\nUser Token: {user_token}\nClient: {client.user}\nAvailable console commands: See COMMANDS_LIST.txt\nAnything typed in that isnt a command will be echoed to the bot!\n")

@tasks.loop(seconds=1.25)
async def spam_():
    if client.spammer == True:
        letters = string.ascii_lowercase + string.ascii_uppercase
        stri = ''.join(random.choice(letters) for i in range(random.randint(1,10)))
        await client.active_channel.send(stri)

@tasks.loop(seconds=0.1)
async def console_commands_():
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    timef = f'{hour}:{minute}:{second}'
    commands = ['autocatcher', 'ac', 'print_var_states', 'pvs', 'identifier', 'spammer', 'i', 's', 'uptime', 'whitelistoff', 'wlo', 'blacklistoff', 'blo', 'blacklistadd ', 'bla ', 'whitelistadd ', 'wla ', 'blacklistrem ', 'blr ', 'whitelistrem ', 'wlr ']
    input = await aioconsole.ainput('')
    if str.lower(input) in commands or str.lower(input)[:4] in commands or str.lower(input)[:13] in commands:
        if str.lower(input) == 'ac' or str.lower(input) == 'autocatcher':
            client.autocatcher = not client.autocatcher
            print(f'{timef} [AUTOCATCHER] -> TOGGLED {client.autocatcher}\n')
        elif str.lower(input) == 'pvs' or str.lower(input) == 'print_var_states':
            print(f'{timef} [PVS] -> Autocatcher: ' + str(client.autocatcher))
            print(f'{timef} [PVS] -> Spammer: ' + str(client.spammer))
            print(f'{timef} [PVS] -> Identifier: ' + str(client.identifier))
            print(f'{timef} [PVS] -> Pokemon blacklist: ' + str(client.blacklist))
            print(f'{timef} [PVS] -> Pokemon whitelist: ' + str(client.whitelist))
            print(f'{timef} [PVS] -> Whitelist: ' + str(client.whitelistactive))
            print(f'{timef} [PVS] -> Blacklist: ' + str(client.blacklistactive))
            print(f'{timef} [PVS] -> Poke Prefix: ' + str(client.poke_prefix))
            print(f'{timef} [PVS] -> Cached Pokemon: ' + str(client.n_pokemon))
            print(f'{timef} [PVS] -> Cached Balance: ' + str(client.balance))
            print(f'{timef} [PVS] -> Active Guild: ' + str(client.active_guild))
            print(f'{timef} [PVS] -> Active Channel: ' + str(client.active_channel) + '\n')
        elif str.lower(input) == 'i' or str.lower(input) == 'identifier':
            client.identifier = not client.identifier
            print(f'{timef} [IDENTIFIER] -> TOGGLED {client.identifier}\n')
        elif str.lower(input) == 'spammer' or str.lower(input) == 's':
            if client.active_guild != None and client.active_channel != None:
                client.spammer = not client.spammer
                print(f'{timef} [SPAMMER] -> TOGGLED {client.spammer}\n')
            else:
                print(f'{timef} [CONSOLE] -> Active guild has not been set this session run `[]set` in a channel.\n')
        elif str.lower(input) == 'uptime':
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = str(datetime.timedelta(seconds=difference))
            print(f'{timef} [UPTIME] -> {text}\n')
        elif str.lower(input)[:4] == 'wla ' or str.lower(input)[:13] == 'whitelistadd ':
            if str.lower(input)[:4] == 'wla ':
                args = str.lower(input)[4:] 
            else:
                args = str.lower(input)[13:]
            if args == None:
                return
            list = args.split(',')
            text = ''
            for element in list:
                if str.lower(element.strip(' ')) in client.whitelist:
                    continue
                text += element.strip(' ') + ', '
                client.whitelist.append(str.lower(element.strip(' ')))
            client.whitelistactive = True
            client.blacklistactive = False
            print(f'{timef} [WHITELIST][ADD] -> {text[:-2]}\n')
        elif str.lower(input)[:4] == 'bla ' or str.lower(input)[:13] == 'blacklistadd ':
            if str.lower(input)[:4] == 'bla ':
                args = str.lower(input)[4:] 
            else:
                args = str.lower(input)[13:]
            if args == None:
                return
            list = args.split(',')
            text = ''
            for element in list:
                if str.lower(element.strip(' ')) in client.blacklist:
                    continue
                text += element.strip(' ') + ', '
                client.blacklist.append(str.lower(element.strip(' ')))
            client.whitelistactive = False
            client.blacklistactive = True
            print(f'{timef} [BLACKLIST][ADD] -> {text[:-2]}\n')
        elif str.lower(input)[:4] == 'blr ' or str.lower(input)[:13] == 'blacklistrem ':
            if str.lower(input)[:4] == 'blr ':
                args = str.lower(input)[4:] 
            else:
                args = str.lower(input)[13:]
            if args == None:
                return
            list = args.split(',')
            text = ''
            for element in list:
                if str.lower(element.strip(' ')) not in client.blacklist:
                    continue
                text += element.strip(' ') + ', '
                client.blacklist.remove(str.lower(element.strip(' ')))
            client.whitelistactive = False
            client.blacklistactive = True
            print(f'{timef} [BLACKLIST][REMOVE] -> {text[:-2]}\n')
        elif str.lower(input)[:4] == 'wlr ' or str.lower(input)[:13] == 'whitelistrem ':
            if str.lower(input)[:4] == 'wlr ':
                args = str.lower(input)[4:] 
            else:
                args = str.lower(input)[13:]
            if args == None:
                return
            list = args.split(',')
            text = ''
            for element in list:
                if str.lower(element.strip(' ')) not in client.whitelist:
                    continue
                text += element.strip(' ') + ', '
                client.whitelist.remove(str.lower(element.strip(' ')))
            client.whitelistactive = True
            client.blacklistactive = False
            print(f'{timef} [WHITELIST][REMOVE] -> {text[:-2]}\n')
        elif str.lower(input) == 'wlo' or str.lower(input) == 'whitelistoff':
            client.whitelistactive = False
            print(f'{timef} [WHITELIST] -> OFF\n')
        elif str.lower(input) == 'blo' or str.lower(input) == 'blacklistoff':
            client.blacklistactive = False
            print(f'{timef} [BLACKLIST] -> OFF\n')
    else:
        if client.active_guild != None and client.active_channel != None:
            await client.active_channel.send(f'{input}')
            print(f'{timef} [REMOTE CONSOLE][TRIGGER] -> Sent `{input}` to #{str(client.active_channel)}')
            client.remote_console_ = True
        else:
            print(f'{timef} [CONSOLE] -> Active guild has not been set this session run `[]set` in a channel.\n')

@client.command(name='autocatcher', aliases=['ac'])
async def autocatcher_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    client.autocatcher = not client.autocatcher
    embed= await embed_gen(f'{ctx.message.author.name}',f'Set Autocatcher to `{client.autocatcher}`','green')
    await ctx.send(embed=embed)
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    print(f'{time} [AUTOCATCHER] -> TOGGLED {client.autocatcher}\n')

@client.command(name='identifier', aliases=['i'])
async def identifier_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    client.identifier = not client.identifier
    embed= await embed_gen(f'{ctx.message.author.name}',f'Set Pokemon Identifier to `{client.identifier}`','green')
    await ctx.send(embed=embed)
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    print(f'{time} [IDENTIFIER] -> TOGGLED {client.identifier}\n')

@client.command(name='run')
async def run_command_(ctx, *, params):
    if ctx.message.guild != client.active_guild:
        return
    await ctx.send(params)
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    print(f'{time} [MANUAL COMMAND] -> {params}\n')

@client.command(name='start_spam', aliases=['ss'])
async def start_spam_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    client.spammer = not client.spammer
    client.active_channel = ctx.channel
    embed= await embed_gen(f'{ctx.message.author.name}',f'Set Spammer to `{client.spammer}`','green')
    await ctx.send(embed=embed)
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    print(f'{time} [SPAMMER] -> TOGGLED {client.spammer}\n')

@client.command(name='print_var_states', aliases=['pvs'])
async def print_var_states_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    print(f'{time} [PVS] -> Autocatcher: ' + str(client.autocatcher))
    print(f'{time} [PVS] -> Spammer: ' + str(client.spammer))
    print(f'{time} [PVS] -> Identifier: ' + str(client.identifier))
    print(f'{time} [PVS] -> Poke Prefix: ' + str(client.poke_prefix))
    print(f'{time} [PVS] -> Cached Pokemon: ' + str(client.n_pokemon))
    print(f'{time} [PVS] -> Cached Balance: ' + str(client.balance))
    print(f'{time} [PVS] -> Active Guild: ' + str(client.active_guild))
    print(f'{time} [PVS] -> Active Channel: ' + str(client.active_channel) + '\n')

@client.command(name='bulktrade')
async def bulktrade_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    if client.n_pokemon == 0:
        embed= await embed_gen(f'{ctx.message.author.name}',f'My pokemon have not been cached this session use `[]cache`','red')
        await ctx.send(embed=embed)
        return
    if client.n_pokemon < 25:
        embed= await embed_gen(f'{ctx.message.author.name}',f'You cant bulk trade with less than 25 pokemon.','red')
        await ctx.send(embed=embed)
        return
    user = ctx.author
    await ctx.send(f'{client.poke_prefix}trade {user.mention}')
    def check(m):
        return m.author == user and m.channel == ctx.channel and m.content == f'{client.poke_prefix}accept'
    try:
        await client.wait_for('message', check=check, timeout=15)
        await asyncio.sleep(1)
        test = 0 
        test2 = 0
        sample = 1
        sample2 = 26
        while sample2-1 <= 225:
            message = f'{client.poke_prefix}p add '
            for i in range(sample, sample2):
                message += f'{i} '
                test += 1
            if client.n_pokemon < 25:
                break
            client.n_pokemon -= 25
            sample += 25
            sample2 += 25
            await asyncio.sleep(2)
            await ctx.send(message)
        await asyncio.sleep(2)
        # Make sure the client has atleast 1 pokemon remaining after the trade
        if client.n_pokemon == 0:
            await ctx.send(f'{client.poke_prefix}p remove {random.randint(1,test)}')
            print('[BULKTRADE] -> Removed 1 random pokemon to make sure i have at least 1 pokemon remaining after the trade\n')
        await asyncio.sleep(2)
        await ctx.send(f'{client.poke_prefix}c add {client.balance}')
        test2 = client.balance
        await asyncio.sleep(3.8)
        await ctx.send(f'{client.poke_prefix}confirm')
        client.balance = 0
        today = datetime.datetime.today()
        hour = today.hour
        second = today.second
        minute = today.minute
        if len(str(hour)) == 1:
            hour = f'0{hour}'
        if len(str(minute)) == 1:
            minute = f'0{minute}'
        if len(str(second)) == 1:
            second = f'0{second}'
        time = f'{hour}:{minute}:{second}'
        print(f'{time} [BULK-TRADE] -> -{test} pokemon | -{test2} currency\n')
    except asyncio.TimeoutError:
        return
    
@client.command(name='uptime')
async def uptime_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed= await embed_gen(f'{ctx.message.author.name}',f'Current uptime: {text}','green')
    await ctx.send(embed=embed)
    return
    
@client.command(name='cache')
async def cache_pokemon_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    client.caching = True
    await ctx.send('.pokemon')
    await asyncio.sleep(1.75)
    await ctx.send('.balance')

@client.command(name='set')
async def set_both_(ctx):
    client.active_channel = ctx.channel
    client.active_guild = ctx.guild
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    print(f'{time} [CONSOLE] -> Guild & Channel set!\n')

@client.command(name='blacklistadd', aliases=['bla'])
async def append_blacklist_(ctx, *, pokemon=None):
    if ctx.message.guild != client.active_guild:
        return
    if pokemon == None:
        embed= await embed_gen(f'{ctx.message.author.name}',f'No pokemon specified to blacklist. `{bot_prefix}blacklistadd pokemon, by, comma`','red')
        await ctx.send(embed=embed)
        return
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    list = pokemon.split(',')
    text = ''
    for element in list:
        if str.lower(element.strip(' ')) in client.blacklist:
            continue
        text += element.strip(' ') + ', '
        client.blacklist.append(str.lower(element.strip(' ')))
    embed= await embed_gen(f'{ctx.message.author.name}',f'Blacklisted pokemon: `{text[:-2]}`','green')
    client.whitelistactive = False
    client.blacklistactive = True
    print(f'{time} [BLACKLIST][ADD] -> {text[:-2]}\n')
    await ctx.send(embed=embed)

@client.command(name='blacklistrem', aliases=['blr'])
async def remove_blacklist_(ctx, *, pokemon=None):
    if ctx.message.guild != client.active_guild:
        return
    if pokemon == None:
        embed= await embed_gen(f'{ctx.message.author.name}',f'No pokemon specified to unblacklist. `{bot_prefix}blacklistrem pokemon, by, comma`','red')
        await ctx.send(embed=embed)
        return
    unbl = ''
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    list = pokemon.split(',')
    for element in list:
        if str.lower(element.strip(' ')) not in client.blacklist:
            continue
        unbl += f"{element.strip(' ')}, "
        client.blacklist.remove(str.lower(element.strip(' ')))
    embed= await embed_gen(f'{ctx.message.author.name}',f'Un-blacklisted pokemon: `{unbl[:-2]}`','green')
    print(f'{time} [BLACKLIST][REM] -> {unbl[:-2]}\n')
    client.whitelistactive = False
    client.blacklistactive = True
    await ctx.send(embed=embed)

@client.command(name='whitelistadd', aliases=['wla'])
async def append_whitelist_(ctx, *, pokemon=None):
    if ctx.message.guild != client.active_guild:
        return
    if pokemon == None:
        embed= await embed_gen(f'{ctx.message.author.name}',f'No pokemon specified to whitelist. `{bot_prefix}whitelistadd pokemon, by, comma`','red')
        await ctx.send(embed=embed)
        return
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    list = pokemon.split(',')
    text = ''
    for element in list:
        if str.lower(element.strip(' ')) in client.whitelist:
            continue
        text += element.strip(' ') + ', '
        client.whitelist.append(str.lower(element.strip(' ')))
    embed= await embed_gen(f'{ctx.message.author.name}',f'Whitelisted pokemon: `{text[:-2]}`','green')
    client.whitelistactive = True
    client.blacklistactive = False
    print(f'{time} [WHITELIST][ADD] -> {text[:-2]}\n')
    await ctx.send(embed=embed)

@client.command(name='whitelistrem', aliases=['wlr'])
async def remove_whitelist_(ctx, *, pokemon=None):
    if ctx.message.guild != client.active_guild:
        return
    if pokemon == None:
        embed= await embed_gen(f'{ctx.message.author.name}',f'No pokemon specified to unwhitelist. `{bot_prefix}whitelistrem pokemon, by, comma`','red')
        await ctx.send(embed=embed)
        return
    unbl = ''
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    list = pokemon.split(',')
    for element in list:
        if str.lower(element.strip(' ')) not in client.whitelist:
            continue
        unbl += f"{element.strip(' ')}, "
        client.whitelist.remove(str.lower(element.strip(' ')))
    embed= await embed_gen(f'{ctx.message.author.name}',f'Un-whitelisted pokemon: `{unbl[:-2]}`','green')
    print(f'{time} [WHITELIST][REM] -> {unbl[:-2]}\n')
    client.whitelistactive = True
    client.blacklistactive = False
    await ctx.send(embed=embed)

@client.command(name='whitelistoff', aliases=['wlo'])
async def whitelist_off_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    client.whitelistactive = False
    print(f'{time} [WHITELIST] -> OFF\n')

@client.command(name='blacklistoff', aliases=['blo'])
async def blacklist_off_(ctx):
    if ctx.message.guild != client.active_guild:
        return
    today = datetime.datetime.today()
    hour = today.hour
    second = today.second
    minute = today.minute
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    time = f'{hour}:{minute}:{second}'
    client.whitelistactive = False
    print(f'{time} [BLACKLIST] -> OFF\n')
    
async def embed_gen(title, description, colorr):
    colours = { 
                "red" : 0xEE192D,
                "blue" : 0x197ee3,
                "green" : 0x15fb00,
                "purple" : 0x6e00fb,
                "magenta" : 0xf90871,
                "gold" : 0xffba08,
                "orange" : 0xfb8b00,
                } 
    today = datetime.datetime.today()
    color = colours[colorr]
    embed=discord.Embed(color=color, title=title ,description=description)
    hour = today.hour
    minute = today.minute
    second = today.second
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    embed.set_footer(text=f"COMMAND EXECUTED | {today.month}/{today.day}/{today.year} - {hour}:{minute}:{second}")
    return embed

client.run(user_token, bot=False)
