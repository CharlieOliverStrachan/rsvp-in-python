import json
import sys
from time import sleep

from pynput import keyboard


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
        except (FileNotFoundError, json.JSONDecodeError):
            print("absent or invalid settings file detected! using defaults")
            settings = {
                "pause_key": "g",
                "default_wpm": 250,
                "text_file": "words.txt"
            }

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
            return text

        except FileNotFoundError:
            print(
                f"you need to have a file named {self.settings['text_file']} with your text (in this folder)!"
            )
            choice = input("\nwould you like to create one now? (Y/n): ")

            if choice.strip().lower() == "n":
                sys.exit()
            else:
                self.create_text()

            return self.text

    def save_text(self, text):
        with open(self.settings["text_file"], "w", encoding="utf-8") as file:
            file.write(text)

        self.text = text
        print("\nnew text file now saved :)\n")

    def create_text(self):
        text = input("\nenter your text:\n")
        self.save_text(text)


class KeyboardListener:
    def __init__(self, pause_key):
        self.pause_key = pause_key
        self.paused = False

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        self.listener.start()

    def on_press(self, key):
        if hasattr(key, "char") and key.char == self.pause_key:
            self.paused = True

    def on_release(self, key):
        if hasattr(key, "char") and key.char == self.pause_key:
            self.paused = False


class Reader:
    def __init__(self, text, settings, stats):
        self.text = text
        self.settings = settings
        self.stats = stats

        self.keyboard_listener = KeyboardListener(
            settings["pause_key"]
        )

    def clear(self):
        print("\033[2J\033[H", end="")

    def read(self):
        self.clear()

        while True:
            try:
                wpm = input("what wpm do you want? ")

                if not wpm:
                    wpm = float(self.settings["default_wpm"])
                    break

                wpm = float(wpm)

                if wpm <= 0:
                    raise ValueError

                break

            except ValueError:
                print("\nenter a positive number!\n")
                sleep(1)

        sleep_time = 60.0 / wpm

        try:
            for word in self.text.split():
                while self.keyboard_listener.paused:
                    sleep(0.10)

                self.clear()
                print(word, flush=True)
                self.stats.words_read += 1

                sleep(sleep_time)

        finally:
            self.stats.save_stats()

        print("\ndone. ", end="")


class Menu:
    def __init__(self):
        self.stats = Stats()
        self.settings = Settings()
        self.text = TextReader(self.settings.settings)

        self.reader = Reader(
            self.text.text,
            self.settings.settings,
            self.stats
        )

    def run(self):
        while True:
            self.menu()

    def menu(self):
        menu = (
            "what do you want to do?\n\n"
            "1: read some text\n"
            "2: write some text\n"
            "3: view words read\n"
            "4: quit\n\n"
        )

        # get the proper input
        while True:
            try:
                choice = int(input(menu))

                if not 1 <= choice <= 4:
                    raise ValueError

                break

            except ValueError:
                print("\nenter a proper input from 1-4!\n")
                sleep(1)
                continue

        match choice:
            case 1:
                self.reader.read()

            case 2:
                self.text.create_text()
                self.reader.text = self.text.text

            case 3:
                print(
                    f"\ncurrent total words read is {self.stats.words_read}\n"
                )
                sleep(1)

            case 4:
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
