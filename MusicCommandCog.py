import json
import os
from discord.ext import commands
import logging
from pydl.musicman import download_playlist_links as dl_playlist
import pydl.musicman as mm


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


class MusicFunctionality(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Downloads all the songs in your playlists")
    async def dl(ctx):
        await ctx.send("Downloading your playlists now. Please be patient!")
        member_id = f'{ctx.message.author.id}'
        logging.info(f"{member_id} began downloading music")
        music_directory = os.path.join(os.getcwd(), 'music', '')
        music_json_path = os.path.join(music_directory, 'music_users.json')
        user_music_directory = os.path.join(music_directory, member_id)
        # download_playlist_links
        with open(music_json_path, 'r') as json_in:
            users = json.load(json_in)
        links = users[member_id]
        for iterator in range(len(links)):
            logging.info(
                f"Downloading playlist index {iterator} link '{links[iterator]}'")

            updated_playlist_link = mm.download_playlist_atomic(
                user_music_directory, links[iterator])
            if (updated_playlist_link == ""):
                # If returns "", then there isn't any new songs.
                await ctx.send(f"Playlist {iterator+1} had no new songs")
                continue
            links[iterator] = updated_playlist_link
            #updated_playlist_links = dl_playlist(user_music_directory, links)
            users[member_id] = links
            # We want to dump this out every time to make sure that we download each playlist individually and update it.
            # This saves us from needing a massive first time download for all playlists.
            with open(music_json_path, 'w') as json_out:
                json.dump(users, json_out)
            await ctx.send(f"Playlist {iterator+1} had new songs, all downloaded and updated.")
        await ctx.send("All playlists updated and downloaded, if necessary.")

    @commands.command(brief="Adds a download link to a user's list")
    async def al(ctx, *args):
        if len(args) <= 0:
            await ctx.send("When using '!al', you must include at least one link to a playlist!")
            return

        music_directory = os.path.join(os.getcwd(), 'music')

        member_id = f'{ctx.message.author.id}'
        logging.info(f"{member_id} is adding playlist(s)")

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
            logging.info(f"{member_id} added playlist link '{link}'")

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


def setup(bot):
    bot.add_cog(MusicFunctionality(bot))
