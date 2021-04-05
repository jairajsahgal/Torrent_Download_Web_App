import requests
import subprocess
# import sys
import time
import os
import sys
from pywebio.input import *
from pywebio.output import *
from pathlib import Path
Path("./download").mkdir(parents=True, exist_ok=True)


def sfw(results):
    Nsfw_Input = results[1]
    results=results[0]
    temp_results = []
    if Nsfw_Input==True:
        for result in results:
            temp_results.append(result)
    else:
        for result in results:
            if result["nsfw"] == True:
                continue
            if result["nsfw"] == False:
                temp_results.append(result)
    return temp_results


def display(results):
    put_table([
        [i+1, results[i]["name"], results[i]["size"], results[i]["seeder"], results[i]["leecher"], results[i]["site"]] for i in range(len(results))
    ],header=["Index","Name","Size","Seeder(s)","Leecher(s)","Site"])


def user_input():
    


    info = input_group("Movie Parameters",
    [
        input('Search Term',type=TEXT,name="name",required=True),
        radio("Include NSFW",options=[{'label':'Yes','value':True},{'label':'No','value':False}],name="nsfw",required=True)
    ])
    url = "https://api.sumanjay.cf/torrent/?query={name}".format(name=info["name"])
    results = requests.get(url).json()
    put_text("Thank you for the input")
    return [results,info["nsfw"]]


def choose(results):
    index = int(input("Enter index to choose torrent  -> "))

    magnet_link = []
    for i in results:
        magnet_link.append(i["magnet"])
    return [index-1, magnet_link[index-1]]


# def movie_or_not(index, results):
#     if "movie" in results[index]["type"].lower():
#         return True
#     else:
#         return False


# def stream(magnet_link):
#     cmd = []
#     cmd.append("webtorrent")
#     cmd.append(magnet_link)
#     cmd.append("--vlc")
#     subprocess.call(cmd)


def open_magnet_link(magnet_link):
    """    cmd = []
        cmd.append("webtorrent")
        cmd.append(magnet_link)
        cmd.append("-o")
        cmd.append("./download")
        subprocess.call(cmd)"""
    """Open magnet according to os."""
    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet_link],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif sys.platform.startswith('win32'):
        os.startfile(magnet_link)
    elif sys.platform.startswith('cygwin'):
        os.startfile(magnet_link)
    elif sys.platform.startswith('darwin'):
        subprocess.Popen(['open', magnet_link],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.Popen(['xdg-open', magnet_link],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    # takes user input and returns list of dictioary of every magnet link with details
    results = user_input()
    results = sfw(results)  # clears up nsfw tags
    display(results)
    var = choose(results)
    """temp = movie_or_not(var[0], results)
    if temp == True:
        t = input("It's a movie. Do you want to stream it? Y or N ->",type=TEXT,required=True)
        if t == "Y":
            stream(var[1])
        elif t == "N":
            download(var[1])
    else:
        download(var[1])"""

    open_magnet_link(var[1])


main()
