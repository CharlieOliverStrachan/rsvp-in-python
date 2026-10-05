import json
import sys
from time import sleep

import keyboard


def get_settings():
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        print("no ssettings file detected! using defaults")
        settings = {"pause_key": "g", "default_wpm": 250, "text_file": "words.txt"}
        return settings


def clear():
    # using ascii escape codes or whatever
    print("\033[2J\033[H", end="")


def get_text(settings):
    try:
        with open(settings["text_file"], encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("you need to have a file named words.txt with your text (in this folder)")
        sys.exit()
    return text


def main():
    settings = get_settings()
    text = get_text(settings)

    # get the speed
    clear()
    try:
        wpm = float(input("what wpm do you want? "))
    except ValueError:
        wpm = settings["default_wpm"]

    sleep_time = 60 / wpm

    # iterate over the words
    clear()
    for word in text.split():
        print(word)
        clear()
        while keyboard.is_pressed(settings["pause_key"]):
            sleep(0.10)
        sleep(sleep_time)

    print("\ndone")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("bye dude")
