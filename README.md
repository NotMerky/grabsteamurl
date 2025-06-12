# GrabSteamURL
A lightweight web scraper that takes a userr-supplied Steam Profile and searches for a Join Game URL on said profile, then launches an application for matchmaking with DBD 4.4.2.

Originally a Java project, this version is fully rebuilt in Python for better readability, features, and footprint size.

## Features
- Command-line interface for inputting commands or profiles to search
- Automatic concatenation of valid Steam Profiles
- Fully offline - no use of Steam's API or login data
- Colored output for readability

## How It Works
1. You input a Steam profile (or Custom ID / Steam64).
2. GrabSteamURL searches the page for a `steam://joinlobby/...` link.
3. When found, it launches `steam_lobby.exe` with that URL.
4. If not found, it keeps searching every few seconds until interrupted.

## Usage
**Run via Terminal or a Batch Script**
Most users will be launching GrabSteamURL in their `4.4.2 Launcher`, but it can be used as a standalone program.

## Important Notice
- Since this does not access any Steam login data, this program can only view online public accounts.
- The matchmaking program `steam_lobby.exe` must be in the same directory as this program (i.e., the `Win64` folder of `4.4.2`).

## Getting Started
1. Download the latest release (EXE version) or build your own executable.
2. Place it in the same folder as `steam_lobby.exe` (the `Win64` Binaries folder.
3. Launch using the launcher or run directly (if your launcher is out of date you can download the updated one here).

## Author
Created by [@notmerky](https://github.com/notmerky)
