import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil
from os import system

TOKEN = 'NzAwNjEyODMwMDQ2NDUzNzkx.Xp8-Gg.5ccgT_tRp5PEwziKws5ciAsLTIs'

bot = commands.Bot(command_prefix = '!')
bot.remove_command('help')
@bot.event
async def on_ready():#------- Вывод "Bot is ready."------------------------------
    print('Bot is ready.')#--------при запуске-----------------------------------
#--------------------------------------------------------------------------------



@bot.event
async def on_member_join(member):#--------------------------------------------------
#--------------------------------Выдача роли новоприбывшим-----(не робит)--------
    print('{member} has joined a server')
    role = discord.utils.get(ctx.guild.roles, name = "{Red}")#------------------- 
    await ctx.add_roles(role)#---------------------------------------------------
#--------------------------------------------------------------------------------

@bot.event
async def on_message(message):#---------------------------------------------------
    channel = message.channel#----------------------------------------------------
    author = message.author#------------------Вывод сообщений канала--------------
    content = message.content#----------------------в терминал--------------------
    print('{}: {}'.format(author, content))#--------------------------------------
    await bot.process_commands(message)#---------------------------------------
#---------------------------------------------------------------------------------


#     if message.content.startswith('!ping'):
#       await channel.send('Pong!')

#     if message.content.startswith('!echo'):
#       msg = message.content.split()
#       output = ''
#       for word in msg[1:]:
#         output += word
#         output += ' '
#       await channel.send(output)
      

# @client.event
# async def on_message_delete(message):
#     author = message.author
#     content = message.content
#     channel = message.channel
#     await channel.send('{}: {}'.format(author,'WoW. Why did you delete that?~')) 

@bot.command()
async def ping(ctx):#-------------------------------------------------------------
    await ctx.send(f'Pong! {round(bot.latency*1000)}ms')
#---------------------------------------------------------------------------------

@bot.command()
async def echo(ctx, *, arg):#-----------------------------------------------------
    await ctx.send(arg)#------------------(Команда: !echo)------------------------
#---------------------------------------------------------------------------------

# @bot.command(pass_context=True)
# async def play(ctx, url):
#     guild = ctx.message.guild
#    voice_channel = ctx.message.author.voice.voice_channel
# voice_client = await bot.join_voice_channel(voice_channel)

# url = 'some_url'
# player = await voice_client.create_ytdl_player(url)

@bot.command(pass_context=True)
async def clear(ctx, amount=100):#------------------------------------------------
    channel = ctx.message.channel#------------------------------------------------
    messages = []#----------------------------------------------------------------
    async for message in channel.history(limit=amount):#-----(Команда: !clear ?)--
              messages.append(message)#---------------------|? - количество(число)
    await channel.delete_messages(messages)#----------------|      сообщений     |
    await ctx.send('Messaged deleted.')#------------------------------------------
#---------------------------------------------------------------------------------

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
            colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='!ping', value='Returns Pong!', inline=False)

    await ctx.send(author, embed=embed)

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


queues = {}

@bot.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)


    await ctx.send("Adding song " + str(q_num) + " to the queue")

    print("Song added to queue\n")


@bot.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        await ctx.send("Next Song")
    else:
        print("No music playing")
        await ctx.send("No music playing failed")

bot.run(TOKEN)
