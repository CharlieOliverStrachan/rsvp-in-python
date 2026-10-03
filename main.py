import sys
from time import sleep

import keyboard


def clear():
    # using ascii escape codes or whatever
    print("\033[2J\033[H", end="")


def get_text():
    try:
        with open("words.txt", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("you need to have a file named words.txt with your text (in this folder)")
        sys.exit()
    return text


def main():
    text = get_text()

    # get the speed
    clear()
    try:
        wpm = float(input("what wpm do you want? "))
    except ValueError:
        wpm = 1

    sleep_time = 60 / wpm

    # iterate over the words
    clear()
    for word in text.split():
        print(word)
        clear()
        while keyboard.is_pressed("g"):
            sleep(0.10)
        sleep(sleep_time)

    print("\ndone")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("bye dude")
