import os
import json
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
