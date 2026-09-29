import sys
from time import sleep


def clear():
    # using ascii escape codes or whatever
    print("\033[2J\033[H", end="")


def get_text():
    try:
        with open("words.txt") as file:
            text = file.read()
    except FileNotFoundError:
        print("you need to have a file named words.txt with your words in this folder")
        sys.exit()
    return text


def main():
    clear()
    sleep_amount = float(
        input("how many seconds inbetween words do you want (you can go into decimals)")
    )
    text = get_text()
    for word in text.split():
        print(word)
        clear()
        sleep(sleep_amount)
    print("\nDone")


if __name__ == "__main__":
    main()
