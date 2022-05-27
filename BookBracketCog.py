from discord.ext import commands
import random
import json
import os
import time


def ensure_book_dir_exists():
    book_dir = os.path.join(os.getcwd(), 'book')
    if not os.path.exists(book_dir):
        os.makedirs(book_dir)
    # Create the music_users.json file if it doesn't already exist:
    book_file = os.path.join(book_dir, 'book_suggestions.json')
    settings_file = os.path.join(book_dir, 'settings.json')
    voting_file = os.path.join(book_dir, "voting.json")

    with open(voting_file, 'w+') as voting_out:
        json.dump({}, voting_out)
    if not os.path.exists(book_file):
        with open(book_file, "w+") as initial_write:
            initial_write.write("[]")
    if not os.path.exists(settings_file):
        with open(settings_file, "w+") as initial_settings_write:
            initial_settings = {"bracket_started": "no",
                                "bracket_filename": ""}
            json.dump(initial_settings, initial_settings_write)


def update_bracket_settings(battle_count, is_odd):
    book_dir = os.path.join(os.getcwd(), 'book')
    settings_file = os.path.join(book_dir, 'settings.json')

    with open(settings_file, 'r') as json_in:
        bracket_settings = json.load(json_in)
    with open(settings_file, 'w') as json_in:
        bracket_settings['battle_count'] = f"{battle_count}"
        bracket_settings['is_odd'] = is_odd
        json.dump(bracket_settings, json_in)
    print("Bracket settings updated")


def set_started_book_bracket(time_in):
    book_dir = os.path.join(os.getcwd(), 'book')
    settings_file = os.path.join(book_dir, 'settings.json')

    with open(settings_file, 'r') as json_in:
        bracket_settings = json.load(json_in)
    with open(settings_file, 'w') as json_out:
        bracket_settings['bracket_started'] = "yes"
        bracket_settings['bracket_filename'] = f"{time_in}"
        bracket_settings['current_battle'] = 0
        json.dump(bracket_settings, json_out)


def is_bracket_started():
    bracket_settings = get_bracket_settings()
    return bracket_settings['bracket_started']


def current_battle_num():
    bracket_settings = get_bracket_settings()
    return bracket_settings['current_battle']


def get_current_bracketID():
    bracket_settings = get_bracket_settings()
    return bracket_settings['bracket_filename']


def get_current_bracket():
    bracketID = get_current_bracketID()
    book_dir = os.path.join(os.getcwd(), 'book')
    bracket_file = os.path.join(book_dir, f'{bracketID}.json')
    with open(bracket_file, 'r') as json_in:
        bracket_settings = json.load(json_in)
    return bracket_settings


def get_bracket_settings():
    book_dir = os.path.join(os.getcwd(), 'book')
    settings_file = os.path.join(book_dir, 'settings.json')
    with open(settings_file, 'r') as json_in:
        bracket_settings = json.load(json_in)
    return bracket_settings


def ensure_bracket_dir_exists():
    book_dir = os.path.join(os.getcwd(), 'book')
    ensure_book_dir_exists()
    current_time = (str)(time.time())
    time_str = current_time[0:current_time.find('.')]
    new_bracket = os.path.join(book_dir, f'{time_str}.json')
    with open(new_bracket, "w+") as initial_write:
        initial_write.write("[]")
    set_started_book_bracket(time_str)
    return new_bracket


def get_booklist():
    """Gets the list of books that have been suggested

    Returns:
        string: the file path of the book suggestions json
        TODO: what type is the booklist? Fill it out here.
    """
    ensure_book_dir_exists()
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
    ensure_book_dir_exists()
    book_dir = os.path.join(os.getcwd(), 'book')
    # Create the music_users.json file if it doesn't already exist:
    book_file = os.path.join(book_dir, 'book_suggestions.json')

    with open(book_file, 'r') as json_in:
        booklist = json.load(json_in)
    return book_file, booklist


class BookBracket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Vote for current book 1")
    async def vote1(ctx):
        if not is_bracket_started():
            await ctx.send("Bracket not currently running.")
            return
        member_id = f'{ctx.message.author.id}'

    @commands.command(brief="Vote for current book 2")
    async def vote2(ctx):
        if not is_bracket_started():
            await ctx.send("Bracket not currently running.")
            return
        member_id = f'{ctx.message.author.id}'

    @commands.command(brief="Shows current voting options")
    async def vo(ctx):
        # TODO: format this better than just a json dump
        currbattle = get_current_bracket()[
            current_battle_num()]
        await ctx.send(f"Choices are:\n\t1: '{currbattle['b1']}'\n\t2: '{currbattle['b2']}'\nVote for one or the other by typing !vote1 or !vote2")

    @commands.command(brief="Creates a random bracket of books")
    async def createbracket(ctx):
        print(
            f"User {ctx.message.author} is attempting to make a bracket of books")
        bracket_file = ensure_bracket_dir_exists()
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
                battlestr = {"b1": battle[0],
                             "b2": battle[1], "winner": "none"}
                battlejsonlist.append(battlestr)
            json.dump(battlejsonlist, battle_json_out)

        # now we update our settings so we know how many battles we have etc
        update_bracket_settings(battle_count, odd_count)
        print("Bracket successfully created")

    @commands.command(brief="Lists all books in the bracket")
    async def listb(ctx):
        print(f"User {ctx.message.author} is attempting to list books")
        out_str = "Books currently in the list are as follows:\n"
        _, booklist = get_booklist()
        for book in booklist:
            out_str += f"\t{book}\n"
        await ctx.send(out_str)

    @commands.command(brief="Removes a book recommendation from the bracket, ensure you type it in quotations!")
    async def rmb(self, ctx, *args):
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

    @commands.command(brief="Adds a book recommendation to the bracket, ensure you type it in quotations!")
    async def ab(self, ctx, *args):
        if len(args) <= 0:
            await ctx.send("When using '!ab', you must include a book you wish to add!")
            return
        print(
            f"User {ctx.message.author} is attempting to add book '{args[0]}'")

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


def setup(bot):
    bot.add_cog(BookBracket(bot))
