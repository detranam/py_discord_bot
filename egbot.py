import random
import json
import time
import logging
from time import sleep
from textrand import RandomText as rt
import bookbracket as bracket

from pydl.musicman import download_playlist_links as dl_playlist
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import os


bot = commands.Bot(command_prefix="!")
logging.basicConfig(filename=f"{int(time.time())}.log",
                    filemode="w", level=logging.DEBUG)


def check_if_youtube_link(check_link):
    """Lightly fuzzes a string to ensure it seems like a youtube link

    Args:
        check_link (string): The string to check
    """
    # Youtube links have a few things you need in it- first of all, it has to have youtube in it.
    # This is mostly to ensure that they aren't just passing in song names or something weird.
    if check_link.find("youtube.com") < 0 or check_link.find("playlist") < 0:
        raise Exception(
            f"String does not look like a YouTube link.... sanitize better? String: '{check_link}'")


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


@bot.command(brief="Vote for current book 1")
async def vote1(ctx):
    if not bracket.is_bracket_started():
        await ctx.send("Bracket not currently running.")
        return
    member_id = f'{ctx.message.author.id}'


@bot.command(brief="Vote for current book 2")
async def vote2(ctx):
    if not bracket.is_bracket_started():
        await ctx.send("Bracket not currently running.")
        return
    member_id = f'{ctx.message.author.id}'


@bot.command(brief="Shows current voting options")
async def vo(ctx):
    # TODO: format this better than just a json dump
    currbattle = bracket.get_current_bracket()[bracket.current_battle_num()]
    await ctx.send(f"Choices are:\n\t1: '{currbattle['b1']}'\n\t2: '{currbattle['b2']}'\nVote for one or the other by typing !vote1 or !vote2")


@bot.command(brief="Creates a random bracket of books")
async def createbracket(ctx):
    print(f"User {ctx.message.author} is attempting to make a bracket of books")
    bracket_file = bracket.ensure_bracket_dir_exists()
    _, booklist = get_booklist()
    # at this point bracket_file exists but is an empty LIST
    # Shuffle keys
    random.shuffle(booklist)
    # Pair off all the books into tuple:(str,str), if odd make last one
    # (str,"NULL"), create a list out of them
    book_count = len(booklist)
    odd_count = book_count % 2 == 1
    battle_count = book_count//2
    battle_list = []
    for i in range(battle_count):
        battle_list.append((booklist[0+(2*i)], booklist[1+(2*i)]))
    if odd_count:
        battle_list.append((booklist[book_count-1], "NULL"))
    with open(bracket_file, "r") as battle_out:
        battlejsonlist = json.load(battle_out)
    # Create individual 'voting' objects and put them into the
    with open(bracket_file, "w") as battle_json_out:
        for battle in battle_list:
            battlestr = {"b1": battle[0], "b2": battle[1], "winner": "none"}
            battlejsonlist.append(battlestr)
        json.dump(battlejsonlist, battle_json_out)

    # now we update our settings so we know how many battles we have etc
    bracket.update_bracket_settings(battle_count, odd_count)
    print("Bracket successfully created")


@bot.command(brief="Lists all books in the bracket")
async def listb(ctx):
    print(f"User {ctx.message.author} is attempting to list books")
    out_str = "Books currently in the list are as follows:\n"
    _, booklist = get_booklist()
    for book in booklist:
        out_str += f"\t{book}\n"
    await ctx.send(out_str)


@bot.command(brief="Removes a book recommendation from the bracket, ensure you type it in quotations!")
async def rmb(ctx, *args):
    if len(args) <= 0:
        await ctx.send("When using '!ab', you must include a book you wish to add!")
        return
    print(
        f"User {ctx.message.author} is attempting to remove book '{args[0]}'")
    book_to_rm = args[0]
    if " " not in book_to_rm:
        await ctx.send("Detected one-word book title. This is probably a mistake! Make sure to use the command like '!ab \"This is my book!\"'")
        return

    book_file, booklist = get_booklist()

    if book_to_rm in booklist:
        booklist.remove(f"{book_to_rm}")
        print(f"User {ctx.message.author} removed book '{args[0]}'")
        with open(book_file, 'w') as json_out:
            json.dump(booklist, json_out)
    else:
        await ctx.send(f"Book with name '{book_to_rm}' not found.")


def get_booklist():
    """Gets the list of books that have been suggested

    Returns:
        string: the file path of the book suggestions json
        TODO: what type is the booklist? Fill it out here.
    """
    bracket.ensure_book_dir_exists()
    book_dir = os.path.join(os.getcwd(), 'book')
    # Create the music_users.json file if it doesn't already exist:
    book_file = os.path.join(book_dir, 'book_suggestions.json')

    with open(book_file, 'r') as json_in:
        booklist = json.load(json_in)
    return book_file, booklist


def get_battlelist():
    """Gets the list of head-to-head voting battles for each book

    Returns:
        string: the file path of the book suggestions json
        TODO: what type is the booklist? Fill it out here.    
    """
    bracket.ensure_book_dir_exists()
    book_dir = os.path.join(os.getcwd(), 'book')
    # Create the music_users.json file if it doesn't already exist:
    book_file = os.path.join(book_dir, 'book_suggestions.json')

    with open(book_file, 'r') as json_in:
        booklist = json.load(json_in)
    return book_file, booklist


@bot.command(brief="Adds a book recommendation to the bracket, ensure you type it in quotations!")
async def ab(ctx, *args):
    if len(args) <= 0:
        await ctx.send("When using '!ab', you must include a book you wish to add!")
        return
    print(f"User {ctx.message.author} is attempting to add book '{args[0]}'")

    book_to_add = args[0]
    if " " not in book_to_add:
        await ctx.send("Detected one-word book title. This is probably a mistake! Make sure to use the command like '!ab \"This is my book!\"'")
        return

    book_file, booklist = get_booklist()

    already_exists = False
    for book_title in booklist:
        if book_title.casefold() == book_to_add.casefold():
            await ctx.send(f"The book '{book_to_add}' is already in the bracket under '{book_title}'! Skipping.")
            already_exists = True
            break
    # If we didn't find the book, add it
    if not already_exists:
        booklist.append(f"{book_to_add}")
        print(f"User {ctx.message.author} added book '{args[0]}'")

        with open(book_file, 'w') as json_out:
            json.dump(booklist, json_out)


@bot.command(brief="Disconnects the bot")
async def dc(ctx):
    voice_channel = ctx.message.author.voice
    vc = await voice_channel.channel.connect()
    await vc.disconnect()


@bot.command(brief="Downloads all the songs in your playlists")
async def dl(ctx):
    await ctx.send("Downloading your playlists now. Please be patient!")
    member_id = f'{ctx.message.author.id}'
    log_user_and_action(member_id, "download music")
    music_directory = os.path.join(os.getcwd(), 'music', '')
    music_json_path = os.path.join(music_directory, 'music_users.json')
    user_music_directory = os.path.join(music_directory, member_id)
    # download_playlist_links
    with open(music_json_path, 'r') as json_in:
        users = json.load(json_in)
    links = users[member_id]
    updated_playlist_links = dl_playlist(user_music_directory, links)
    users[member_id] = updated_playlist_links
    with open(music_json_path, 'w') as json_out:
        json.dump(users, json_out)
    await ctx.send("Your playlists have been downloaded")


@bot.command(brief="Adds a download link to a user's list")
async def al(ctx, *args):
    if len(args) <= 0:
        await ctx.send("When using '!al', you must include at least one link to a playlist!")
        return

    music_directory = os.path.join(os.getcwd(), 'music')

    member_id = f'{ctx.message.author.id}'
    log_user_and_action(member_id, "add playlist(s)")

    # Create folder for this user's music if there isn't already one
    music_folder_path = os.path.join(music_directory, f'{member_id}')
    if not os.path.exists(music_folder_path):
        os.makedirs(music_folder_path)

    # Create the music_users.json file if it doesn't already exist:
    music_json_path = os.path.join(music_directory, 'music_users.json')
    if not os.path.exists(music_json_path):
        with open(music_json_path, "w+") as initial_write:
            initial_write.write("{\"{nobodysID}\": [\"google.com\"]\}")

    # Get the user list from the json file
    with open(music_json_path, 'r') as json_in:
        users = json.load(json_in)

    for arg in args:
        # Check if the arg seems like a youtube link. If it does, keep going, otherwise catch the exception and log it.
        try:
            check_if_youtube_link(arg)
        except:
            await ctx.send(f"Link '{arg}' does not look like a YouTube link. Skipping!")
            continue

        link = arg
        # If the user exists, check if link is already in there, if not, add it
        if member_id in users:
            if link not in users[member_id]:
                users[member_id].append(link)
            else:
                await ctx.send("This playlist is already being tracked")
        else:
            await ctx.send("Welcome! You're a new user. We created a tracking list for you <3")
            users[member_id] = json.loads(
                json.dumps([f'{link}']))
        await ctx.send(f"Added playlist {link}")
        logging.info(f"Added playlist {link}")

    # Update the json file before we conclude
    with open(music_json_path, 'w') as json_out:
        json.dump(users, json_out)


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

# This runs the bot itself
with open('auth.json') as f:
    data = json.load(f)
    bot.run(data['token'])
