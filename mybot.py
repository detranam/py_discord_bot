import json
import time
import logging
from time import sleep

from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import os

#Begin our logging immediately, placed in the logs/ folder
log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(filename=os.path.join(log_dir, f"{int(time.time())}.log"),
                    filemode="w", level=logging.DEBUG)

# Create the bot with cmd prefix '!'
bot = commands.Bot(command_prefix="!")


def ensure_music_folders_exist():
    """Creates the folders on disc that are required for music downloads and storage.
    """
    music_directory = os.path.join(os.getcwd(), 'music')
    # Create the music_users.json file if it doesn't already exist:
    music_json_path = os.path.join(music_directory, 'music_users.json')
    if not os.path.exists(music_json_path):
        with open(music_json_path, "w+") as initial_write:
            initial_write.write("{\"nobodysID\": [\"google.com\"]}")


def ensure_user_exists(member_id):
    """Ensure that a user exists in the music/music_users.json file

    Args:
        member_id (int): the unique integer assigned to each user
    """
    ensure_music_folders_exist()
    music_directory = os.path.join(os.getcwd(), 'music')
    # Create folder for this user's music if there isn't already one
    music_folder_path = os.path.join(music_directory, f'{member_id}')
    if not os.path.exists(music_folder_path):
        os.makedirs(music_folder_path)


def log_user_and_action(member_id, action):
    """Logs the 'user' and action happening to the logging.info log file

    Args:
        member_id (int): The member's ID
        action (string): The action the user is doing, to be logged
    """
    logging.info(f"User {member_id} called {action}")


@bot.command(brief="Disconnects the bot")
async def dc(ctx):
    voice_channel = ctx.message.author.voice
    vc = await voice_channel.channel.connect()
    await vc.disconnect()


@bot.command(brief="Plays a single video, from a youtube URL")
async def play(ctx, *sn):
    await ctx.send("This is a TODO. Suspended because it didn't work. Feels bad.")
    return
    global recent_message
    recent_message = ctx

    songname = ' '.join(sn)
    sn_nospace = songname.replace(" ", "_")

    # Gets voice channel of message author
    voice_channel = ctx.message.author.voice
    if voice_channel != None:
        YDL_OPTIONS = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
                {
                'key': 'FFmpegMetadata'
            }],
            'outtmpl': f'{sn_nospace}.%(ext)s'
        }

        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f == sn_nospace+".mp3":
                # If the song already exists
                pass
            else:
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    ydl.download(['ytsearch:'+songname])  # , download=True)

        vc = await voice_channel.channel.connect()

        # player = vc.create_ffmpeg_player("bingo_bango_bongo.mp3", after=lambda:print('done'))
        # player.start()
        # while not player.is_done():
        #     sleep(1)
        # player.stop()
        # await vc.disconnect()
        print(f"Playing {sn_nospace}.mp3")
        vc.play(FFmpegPCMAudio(
            executable="C:/ffmpeg/bin/ffmpeg.exe", source="warren_zieder_ride_the_lightning.mp3"))  # source=f"{sn_nospace}.mp3"))#source="you_drown_the_whiskey.mp3"))  #
        while vc.is_playing():
            sleep(1.5)  # only check every 1.5 seconds to see if we're playing
        await vc.disconnect()    # if not voice.is_playing():
        return
    #     voice.play(FFmpegPCMAudio("song.mp3"))
    #     voice.is_playing()
    #     await ctx.send(f"Now playing {url}")
    # else:
    #     await ctx.send("Already playing song")
    #     return
    #     # Sleep while audio is playing.
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # # Delete command after the audio is done playing.
    # await ctx.message.delete()
    # voice = get(bot.voice_clients, guild=ctx.guild)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    log_user_and_action("ADMIN", "FIRE UP BOT")

if __name__ == "__main__":
    bot.load_extension('MusicCommandCog')
    bot.load_extension('BookBracketCog')

# This runs the bot itself
with open('auth.json') as f:
    data = json.load(f)
    bot.run(data['token'])
