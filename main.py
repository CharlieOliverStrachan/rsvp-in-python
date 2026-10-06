import json
import sys
from time import sleep

import keyboard


class Stats:
    def __init__(self):
        self.words_read = self.get_stats()

    def get_stats(self):
        try:
            with open("stats.dat", "r") as file:
                stats = file.read()
                return int(stats) if stats else 0
        except FileNotFoundError:
            return 0

    def save_stats(self):
        with open("stats.dat", "w") as file:
            file.write(str(self.words_read))


class Settings:
    def __init__(self):
        self.settings = self.get_settings()

    def get_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                return settings
        except FileNotFoundError:
            print("no settings file detected! using defaults")
            settings = {"pause_key": "g", "default_wpm": 250, "text_file": "words.txt"}

            with open("settings.json", "w") as file:
                json.dump(settings, file)

            return settings


class TextReader:
    def __init__(self, settings):
        self.settings = settings
        self.text = self.get_text()

    def get_text(self):
        try:
            with open(self.settings["text_file"], encoding="utf-8") as file:
                text = file.read()
        except FileNotFoundError:
            print(
                "you need to have a file named words.txt with your text (in this folder)"
            )
            sys.exit()

        return text


class Reader:
    def __init__(self, text, settings, stats):
        self.text = text
        self.settings = settings
        self.stats = stats

    def clear(self):
        # using ascii escape codes or whatever
        print("\033[2J\033[H", end="")

    def read(self):
        # get the speed
        self.clear()

        try:
            wpm = float(input("what wpm do you want? "))
        except ValueError:
            wpm = self.settings["default_wpm"]

        sleep_time = 60 / wpm

        # iterate over the words
        self.clear()

        try:
            for word in self.text.split():
                print(word)
                self.stats.words_read += 1
                self.clear()

                while keyboard.is_pressed(self.settings["pause_key"]):
                    sleep(0.10)

                sleep(sleep_time)

        finally:
            self.stats.save_stats()

        print("\ndone. ", end="")


class Menu:
    def __init__(self):
        self.stats = Stats()
        self.settings = Settings()
        self.text = TextReader(self.settings.settings)

        self.reader = Reader(self.text.text, self.settings.settings, self.stats)

    def run(self):
        while True:
            self.menu()

    def menu(self):
        menu = "what do you want to do?\n\n1: read some text\n2: view words read\n3: quit\n\n"

        # get the proper input
        while True:
            try:
                choice = int(input(menu))
                if not 1 <= choice <= 3:
                    raise ValueError
                break
            except ValueError:
                print("\nenter a proper input from 1-3!\n")
                sleep(1)
                continue
        match choice:
            case 1:
                self.reader.read()
            case 2:
                print(f"current total words read is {self.stats.words_read}")
            case 3:
                raise KeyboardInterrupt


def main():
    print("--rsvp python--")
    menu = Menu()
    menu.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("bye dude")
