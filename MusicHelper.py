import requests
import json
import itertools
import time
import random
from termcolor import colored


def main():
    """
    void -> int
    The main body of program
    """
    logo()
    mod = all_prints()

    while 1:
        if mod == "1":
            get_chart()
        elif mod == "2":
            song_info()
        elif mod == "3":
            analitic()
        else:
            print("\nGoodbye!")
            break
        print("\n", "*" * 80, "\n")

        mod = input("\nPlease, enter a number (1-3 or 0)\n")

    return 0


def logo():
    """
    void -> int
    This function print logo of program
    """
    logo = "**   ** ***** *     *  ****    ***** *     *\n\
 *   *  *     *     *  *   *   *     *     *\n\
  * *   *****  *   *   *    *  *****  *   * \n\
   *    *       * *    *   *   *       * *\n\
  ***   *****    *     ****    *****    *\n"

    iterat = itertools.cycle(logo)

    for x in range(len(logo)):
        time.sleep(0.008)  # Пауза
        value = next(iterat)
        if value == "*":
            print(colored("#", 'blue'), end="", flush=True)
        elif value == "\n":
            print()
        else:
            print(" ", end="", flush=True)

    print()

    text = " YevDev presents \n\n*************\n*MusicHelper*\n*************"
    iterat = itertools.cycle(text)

    for x in range(len(text)):
        time.sleep(0.012)  # Пауза
        print(next(iterat), end='', flush=True)

    print()

    return 0


def all_prints():
    """
    void -> str
    Main printing menu
    """
    print("This tool is your trusted helper for powdered music.")
    print("Please select an option:")
    print("\n\t1 - see today's chart of top-10 songs (from deezer.com)")
    print("\n\t2 - find an information about any song")
    print("\n\t3 - check charts from 1958 to 2019")
    print("\n\t0 - exit")

    mode = input("\nPlease, enter a number (1-3 or 0)\n")

    flag = False

    if mode != "1" and mode != "2" and mode != "3" and mode != "0":
        flag = True

    while flag:
        mode = input("\nIncorrect input. Please, enter a number (1-3 or 0)\n")
        if mode == "1" or mode == "2" or mode == "3" or mode == "0":
            flag = False

    return mode


def get_chart():
    """
    void -> int
    This funktion prints a top-chart of modern songs
    """

    api_url = "https://api.deezer.com/chart"

    # Get response of our request
    response = requests.get(api_url)

    # transform into dict
    raw_data = response.json()

    result = []

    # Getting only needed information
    data = raw_data["tracks"]
    data = data["data"]

    for i in range(10):
        current_song = data[i]

        # Get artist info
        art = current_song["artist"]

        # Add info
        one_result = [current_song["title"], art["name"]]

        result.append(tuple(one_result))

    # Making a good-looking tabulation
    max_song = 0
    max_artist = 0

    for elem in result:
        if len(elem[1]) > max_song:
            max_song = len(elem[1])
        if len(elem[0]) > max_artist:
            max_artist = len(elem[0])

    print("\n   Artist", " " * (max_song - 6), "Track\n")

    for elem in result:
        # Printing info
        print(elem[1], " " * (max_song - len(elem[1])), elem[0])

    return 0


def song_info():
    """
    void -> int
    This funktion prints an information of current song
    """

    artist = input("\nPlease, enter a name of artist: ")
    song_name = input("Please, enter a name of song: ")

    try:

        raw_api_url = "https://api.deezer.com/search?q="

        api_url = raw_api_url + 'artist:"' + artist +\
            '" track:"' + song_name + '"'

        # Get response of our request
        response = requests.get(api_url)

        # transform into dict
        raw_data = response.json()

        # Getting only needed information
        data = raw_data["data"]

        data = data[0]  # Get the best (first) result

        song_id = data["id"]

        api_url = "https://api.deezer.com/track/" + str(song_id)

        # Get response of our request
        response = requests.get(api_url)

        # transform into dict
        raw_data = response.json()

        # Getting only needed information
        title = raw_data["title"]
        duration = raw_data["duration"]
        song_link = raw_data["link"]
        position_in_album = raw_data["track_position"]
        bpm = raw_data["bpm"]
        album = raw_data["album"]
        album_name = album["title"]
        artist_name = raw_data["artist"]["name"]

        # Printing info
        print ("\n")
        print("Song title: ", title)
        print("Artist name: ", artist_name)
        print("Song duration (in seconds): ", duration)
        print("Song bpm: ", bpm)
        print("Album title: ", album_name)
        print("Song position in album: ", position_in_album)
        print("Song link in deezer.com: ", song_link)

        return 0

    except:
        print("\nSorry, but your input is incorrect")
        return 0


def analitic():
    """
    void -> int
    Function that starts a menu with options of analitic
    """

    print("\nThis instrument will help you chech charts.")
    print("Pleace, choose an option:")
    print("\n\t1 - Enter a date and check the chart")
    print("\n\t2 - find an information about any song in charts")

    mode = input("\nPlease, enter a number (1-2)\n")

    flag = False

    if mode != "1" and mode != "2":
        flag = True

    while flag:
        # Incorrect input
        mode = input("\nIncorrect input. Please, enter a number (1-2)\n")
        if mode == "1" or mode == "2":
            flag = False

    if mode == "1":
        chart_by_date()
    else:
        song_find()


def chart_by_date():
    """
    void -> int
    Function finds chart of entered date
    """
    year = input("\nPlease, enter a year: ")
    month = input("Please, enter a month: ")

    print()

    result = {}
    counter = 1
    day = 1

    it = itertools.cycle(['.'] * 3 + ['\b \b'] * 3)

    print("Searching", end="")

    while result == {}:
        filee = open("Hot Stuff.csv")

        # Searching for this line:
        looking_date = month + "/" + str(day) + "/" + year

        max_song = 0

        for i in range(317797):

            if i % 500001 == 0:
                # Adding cool animation
                print(next(it), end='', flush=True)

            line = filee.readline()
            arr_of_data = line.split(",")

            if looking_date in arr_of_data:
                # Here we add song and artist names to the result

                if len(arr_of_data[3]) > max_song:
                    max_song = len(arr_of_data[3])

                result[int(arr_of_data[2])] = tuple([arr_of_data[4],
                                                    arr_of_data[3]])

        for i in range(1, len(result)):
            try:
                # Printing from first to last position
                print_rez = result[i]

                if counter == 1:
                    print("\n")
                    counter = 0

                print(print_rez[0], " " * (max_song - len(print_rez[0])),
                      print_rez[1])

            except:
                pass

        day += 1

        if day == 32:
            print("\nSorry, no chart for that date...")
            break

        filee.close()

    return 0


def song_find():
    """
    void -> int
    Function finds entered song in charts
    """
    artist = input("\nPlease, enter a name of artist: ")
    song_title = input("\nPlease, enter a song title: ")

    print()

    result = False

    filee = open("Hot Stuff.csv")

    looking_str = song_title.lower() + artist.lower()

    for i in range(317797):
        # Looking for entered song
        line = filee.readline().lower()
        arr_of_data = line.split(",")

        if looking_str in arr_of_data:
            result = True
            print("Chart date is", arr_of_data[1],
                  "song position in chart is", arr_of_data[2])

    if not result:
        print("Sorry, that song is not in charts...")

    filee.close()

    return 0

if __name__ == "__main__":
    try:
        main()
    except:
        print("Something wrong")
        print("Pleace install termcolor")
