# Standard library
import os
import re
import sys
import time
import subprocess
import webbrowser

# Third-party libraries
import pyperclip
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

infinite_mode = True # determines if profile will be searched infinitely or not
lobby_program_name = "steam_lobby.exe" # program to run with url
sleep_delay = 3 # seconds between attempts
last_profile = None # stores last visited profile
copy_to_clipboard = False # if a valid lobby url is found copy to clipboard
quiet = False # if retry message should appear or not

def main():
    init() # initializes colors
    while (True):
        is_valid_input = False
        user_input = None
        
        while (not is_valid_input):
            clear_console()
            user_input = get_user_input()
            is_valid_input = (not user_input == None)
        
        join_game_url = scrape_join_url(user_input)
        if (not join_game_url == None):
            join_lobby(join_game_url)

def get_user_input():
    global last_profile, sleep_delay, infinite_mode, copy_to_clipboard, quiet
    print(Fore.CYAN + 'Input a Steam Profile URL or "-help" for more info: ' + Style.RESET_ALL, end='')
    user_input = input().lower().strip()
    
    # URL Creation
    if is_steam_profile_url(user_input):
        return (user_input if user_input.startswith("http") else "https://" + user_input)
    elif (user_input.endswith(" -id")):
        last_profile = "https://www.steamcommunity.com/id/" + user_input[:-4]
        return last_profile
    elif (user_input.endswith(" -64")):
        last_profile = "https://www.steamcommunity.com/profiles/" + user_input[:-4]
        return last_profile
    elif (user_input.startswith("steam://joinlobby")):
        join_lobby(user_input)
        return None
    
    # Commands
    elif (user_input == "-about"):
        print_about()
    elif (user_input == "-privacy"):
        open_privacy()
    elif (user_input == "-return"):
        sys.exit()
    elif (user_input == "-github"):
        open_github()
    elif (user_input == "-help"):
        print_help()
    elif (user_input == "-tutorial"):
        open_tutorial()
    elif (user_input == "-settings"):
        print_settings()
    elif (user_input == "-quiet"):
        quiet = not quiet
        print(Fore.YELLOW + "[→] Toggled Quiet Mode." + Style.RESET_ALL)
    elif (user_input == "-quiet"):
        infinite_mode = not infinite_mode
        print(Fore.YELLOW + "[→] Toggled Search Mode." + Style.RESET_ALL)
    elif (user_input == "-copy"):
        copy_to_clipboard = not copy_to_clipboard
        print(Fore.YELLOW + "[→] Toggled Copying To Clipboard." + Style.RESET_ALL)
    elif (user_input.startswith("-delay ")):
        try:
            sleep_delay = int(user_input.split()[1])
            print(Fore.YELLOW + f"[→] Retry delay set to {sleep_delay} seconds." + Style.RESET_ALL)
        except ValueError:
             print(Fore.RED + "[!] Invalid delay value. Use an integer like -delay 3" + Style.RESET_ALL)
    elif (user_input == "-last"):
        if (not last_profile == None):
            return last_profile
        else:
            print(Fore.RED + "[?] No Last Profile Data Saved!" + Style.RESET_ALL)
    else:
        print_invalid_input_message()
    pause_console()
    return None

def is_steam_profile_url(s):
    pattern = r'^(https?://)?(www\.)?steamcommunity\.com/(id/|profiles/)?[a-zA-Z0-9_-]+/?$'
    return re.match(pattern, s) is not None

def print_about():
    print(Fore.MAGENTA + Style.BRIGHT + "\n[ About GrabSteamURL ]" + Style.RESET_ALL)

    print(Fore.CYAN + "* Version:" + Style.RESET_ALL + " v1.0 (Python build, compiled 6/12/2025)")

    print(Fore.CYAN + "\n* Description:" + Style.RESET_ALL)
    print("  GrabSteamURL is a lightweight web scraper that takes a user-supplied")
    print("  Steam profile and automatically launches the lobby program")
    print("  (steam_lobby.exe) for Dead by Daylight version 4.4.2.")

    print(Fore.CYAN + "\n* Privacy & Safety:" + Style.RESET_ALL)
    print("  This program does NOT access your Steam account.")
    print("  It only reads publicly available info from Steam profiles.")
    print("  (Make sure the host's profile and game info are set to public.)")

    print(Fore.CYAN + "\n* Credits:" + Style.RESET_ALL)
    print("  Created by " + Fore.YELLOW + "@notmerky" + Style.RESET_ALL + " on GitHub\n")

def print_invalid_input_message():
    print(Fore.RED + Style.BRIGHT + "[?] Invalid input!" + Style.RESET_ALL)
    print("Please enter a valid input using one of the formats below:")

    print(Fore.CYAN + "\n== Input Examples ==" + Style.RESET_ALL)
    print(f'{Fore.YELLOW}URL       {Style.RESET_ALL}: https://www.steamcommunity.com/id/eroticgaben')
    print(f'{Fore.YELLOW}Custom ID {Style.RESET_ALL}: eroticgaben -id')
    print(f'{Fore.YELLOW}Steam64   {Style.RESET_ALL}: 76561198085278322 -64\n')

def open_privacy():
    print(Fore.YELLOW + "[>] Opening Steam privacy settings in default browser..." + Style.RESET_ALL)
    webbrowser.open("https://www.steamcommunity.com/id/eroticgaben/edit/settings")

def open_github():
    print(Fore.YELLOW + "[>] Opening GitHub Repository in default browser..." + Style.RESET_ALL)
    webbrowser.open("https://github.com/NotMerky/grabsteamurl")

def open_tutorial():
    print(Fore.YELLOW + "[>] Opening Video Tutorial in default browser..." + Style.RESET_ALL)
    webbrowser.open("https://youtu.be/I_BWOd8Wljo")

def print_help():
    print(Fore.MAGENTA + Style.BRIGHT + "\n[ GrabSteamURL Help ]" + Style.RESET_ALL)

    print(Fore.CYAN + "\n== Commands ==" + Style.RESET_ALL)
    print(f"{Fore.YELLOW}-about     {Style.RESET_ALL}: Show info about GrabSteamURL")
    print(f"{Fore.YELLOW}-help      {Style.RESET_ALL}: Display this help menu")
    print(f"{Fore.YELLOW}-last      {Style.RESET_ALL}: Reuse the last searched profile")
    print(f"{Fore.YELLOW}-id        {Style.RESET_ALL}: Use a Custom ID input format (Switch)")
    print(f"{Fore.YELLOW}-64        {Style.RESET_ALL}: Use Steam-64 ID input format (Switch)")
    print(f"{Fore.YELLOW}-github    {Style.RESET_ALL}: Open the GitHub page")
    print(f"{Fore.YELLOW}-privacy   {Style.RESET_ALL}: Open Steam privacy settings")
    print(f"{Fore.YELLOW}-tutorial  {Style.RESET_ALL}: Opens a video Tutorial")
    print(f"{Fore.YELLOW}-settings  {Style.RESET_ALL}: Displays settings commands")
    print(f"{Fore.YELLOW}-return    {Style.RESET_ALL}: Close the program")

    print(Fore.CYAN + "\n== Input Examples ==" + Style.RESET_ALL)
    print(f'{Fore.GREEN}URL       {Style.RESET_ALL}: https://www.steamcommunity.com/id/eroticgaben')
    print(f'{Fore.GREEN}Custom ID {Style.RESET_ALL}: eroticgaben -id')
    print(f'{Fore.GREEN}Steam64   {Style.RESET_ALL}: 76561198085278322 -64')

    print(Fore.CYAN + "\n== Common Issues ==" + Style.RESET_ALL)
    print(f"{Fore.RED}- Make sure the host has created the lobby. It should say 'Connecting to players' on their screen.")
    print(f"- The host's profile and game details must be set to 'Public' on Steam.")
    print(f"- Ensure the host is Online (not Invisible).")
    print(f"- Double-check the profile URL/ID formatting.")
    print(f"- Verify that steam_lobby.exe exists and is working correctly.\n" + Style.RESET_ALL)

def print_settings():
    print(Fore.MAGENTA + Style.BRIGHT + "\n[ GrabSteamURL Settings ]" + Style.RESET_ALL)

    print(Fore.CYAN + "\n== Commands ==" + Style.RESET_ALL)
    print(f"{Fore.YELLOW}-delay #    {Style.RESET_ALL}: Changes the delay between searching in seconds (default is 3)")
    print(f"{Fore.YELLOW}-toggleinf  {Style.RESET_ALL}: Toggles between infinite search and single search")
    print(f"{Fore.YELLOW}-copy       {Style.RESET_ALL}: Toggles copying join game urls to your clipboard when found")
    print(f"{Fore.YELLOW}-quiet      {Style.RESET_ALL}: Toggles retry message when searching a profile")
    
    print(Fore.CYAN + "\n== Last Saved Profile ==" + Style.RESET_ALL)
    print(f'{Fore.GREEN}URL {Style.RESET_ALL}: {last_profile}')
    
    print(Fore.CYAN + "\n== Notice ==" + Style.RESET_ALL)
    print(f"{Fore.RED}These settings are only saved per session, if the program closes, everything will be reset.\n" + Style.RESET_ALL)

def scrape_join_url(profile_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(Fore.YELLOW + f"[…] Searching {profile_url} for a lobby..." + Style.RESET_ALL)

    try:
        while infinite_mode:
            response = requests.get(profile_url, headers=headers)

            if response.status_code != 200:
                print(Fore.YELLOW + f"[!] Failed to load profile. HTTP {response.status_code}" + Style.RESET_ALL)
                pause_console()
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select('a.btn_green_white_innerfade.btn_small_thin')

            for link in links:
                href = str(link.get('href', ''))
                if href.startswith("steam://joinlobby"):
                    print(Fore.GREEN + "[+] Lobby found!" + Style.RESET_ALL)
                    if copy_to_clipboard:
                        pyperclip.copy(href)
                    return href

            if not infinite_mode:
                print(Fore.RED + "[?] Lobby not found. Use -help for more info." + Style.RESET_ALL)
                pause_console()
                return None
            elif (not quiet):
                print(Fore.CYAN + "[~] Lobby not found, retrying... (Ctrl + C to cancel)" + Style.RESET_ALL)
            time.sleep(sleep_delay)
            
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "[×] Search interrupted by user." + Style.RESET_ALL)
        pause_console()
        return None
    except requests.RequestException as e:
        print(Fore.RED + f"[!] Network error: {e}" + Style.RESET_ALL)
        pause_console()
        return None

def is_profile_public():
    print("WIP")

def join_lobby(join_url):
    if not os.path.exists("steam_lobby.exe"):
        print(Fore.RED + f"[×] steam_lobby.exe not found in the current directory." + Style.RESET_ALL)
        pause_console()
        return

    try:
        print(Fore.GREEN + f"[»] Joining Lobby with Lobby URL..." + Style.RESET_ALL)
        subprocess.run(["powershell", "Start-Process", "steam_lobby.exe", "-Verb", "runAs", "-ArgumentList", f'"{join_url}"'], shell=True)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to launch steam_lobby.exe: {e}" + Style.RESET_ALL)
    finally:
        pause_console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_console():
    os.system('pause' if os.name == 'nt' else '')

if __name__ == "__main__":
    os.system("title GrabSteamURL")
    main()
