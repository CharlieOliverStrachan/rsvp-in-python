import json
import sys
from time import sleep

import keyboard


def get_stats():
    try:
        with open("stats.dat", "r") as file:
            stats = file.read()
            return int(stats) if stats else 0
    except FileNotFoundError:
        return 0


def save_stats(words):
    with open("stats.dat", "w") as file:
        file.write(str(words))


def get_settings():
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        print("no ssettings file detected! using defaults")
        settings = {"pause_key": "g", "default_wpm": 250, "text_file": "words.txt"}

        with open("settings.json", "w") as file:
            json.dump(settings, file)
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
    words_read = get_stats()
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
    try:
        for word in text.split():
            print(word)
            words_read += 1
            clear()
            while keyboard.is_pressed(settings["pause_key"]):
                sleep(0.10)
            sleep(sleep_time)
    finally:
        save_stats(words_read)
    print("\ndone. ", end="")
    print(f"(current total words read is {words_read})")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("bye dude")
