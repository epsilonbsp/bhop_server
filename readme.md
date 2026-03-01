# Bhop Server
My simple bhop server setup.

This setup allows to just download or clone repo, run few commands and have local server working right away.

## Requirements
### Windows
* Download and install [Python](https://www.python.org/downloads/)

### Linux
* Install dependencies

      sudo apt install python3 python-is-python3

## Usage
* Download or clone repo
* Open terminal in `bhop_server` directory and run these commands

      # Install SteamCMD, server, core, extensions, plugins
      python build.py install_all

      # Build plugins (if you make changes to plugins)
      python build.py compile_resources

      # Start server
      python build.py start_lan

## Script Documentation
Main ideas of `build.py` script
* Programmatically assemble a bhop server with collection of extensions and plugins
* Make it relatively easy to start simple LAN server for yourself

### Commands
#### `python build.py install_steamcmd`
* Downloads and installs SteamCMD

#### `python build.py install_server`
* Installs `Counter Strike: Source Dedicated Server` app using SteamCMD

#### `python build.py download_resources`
* Downloads core, extension and plugins specified in `RESOURCES` constant
* Unpacks all of that into `build/resources`

#### `python build.py compile_resources`
* Goes through all resources that are specified in `RESOURCES` constant
* If resource has values in `plugin_paths`, it will attempt to compile them and put into `build/compiled`
* After compilation clears `build/server/cstrike/addons/sourcemod/plugins` directory
* Finally transfers all compiled plugins into `build/server/cstrike/addons/sourcemod/plugins` directory

#### `python build.py merge_resources`
* Merges all resources into `build/server/cstrike` directory

#### `python build.py merge_overrides`
* Merges contents of `core` directory into `build/server/cstrike` directory

#### `python build.py install_all`
* Single command to do everything specified above

#### `python build.py start_lan`
* Starts LAN server in console mode

## References
### SteamCMD
    Website: https://developer.valvesoftware.com/wiki/SteamCMD
    Windows: https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip
    Linux:   https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz

### Core
* SourceMod

      Source:  https://github.com/alliedmodders/sourcemod
      Website: https://www.sourcemod.net/downloads.php?branch=stable
      Windows: https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-windows.zip
      Linux:   https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-linux.tar.gz

* Metamod:Source

      Source:  https://github.com/alliedmodders/metamod-source
      Website: https://www.metamodsource.net/downloads.php?branch=stable
      Windows: https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-windows.zip
      Linux:   https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-linux.tar.gz

* TickrateEnabler

      Source:  https://github.com/idk1703/TickrateEnabler
      Windows: https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-win-tick100-6e83b42.zip
      Linux:   https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-linux-tick100-6e83b42.zip

### Extensions
* Bzip2 Extension

      Source: https://github.com/epsilonbsp/sm_bzip2
      Both:   https://github.com/epsilonbsp/sm_bzip2/releases/download/v1.0.0/sm_bzip2_v1.0.0.zip

* Event Queue Fix Fix

      Source:  https://github.com/srcwr/eventqueuefixfix
      Windows: https://github.com/srcwr/eventqueuefixfix/releases/download/v1.0.1/eventqueuefixfix-v1.0.1-def5b0e-windows-x32.zip

* REST in Pawn Extension

      Source:  https://github.com/ErikMinekus/sm-ripext
      Windows: https://github.com/ErikMinekus/sm-ripext/releases/download/1.3.2/sm-ripext-1.3.2-windows.zip
      Linux:   https://github.com/ErikMinekus/sm-ripext/releases/download/1.3.2/sm-ripext-1.3.2-linux.zip

### Plugins
* DynamicChannels

      Source: https://github.com/Vauff/DynamicChannels

* Bhop Timer

      Source:  https://github.com/shavitush/bhoptimer
      Release: https://github.com/shavitush/bhoptimer/releases/download/v4.0.1/bhoptimer-v4.0.1.zip

* Jump Stats

      Source: https://github.com/KawaiiClan/bhop-get-stats

* Land Fix

      Source:  https://github.com/Haze1337/Landfix
      Release: https://github.com/Haze1337/Landfix/archive/refs/tags/1.3.zip

* Map Loader

      Source: https://github.com/epsilonbsp/sm_maploader

* PushFix Definitive Edition

      Source:  https://github.com/rumourA/PushFixDE
      Release: https://github.com/rumourA/PushFixDE/archive/refs/tags/1.0.zip

* RNG Fix

      Source:  https://github.com/jason-e/rngfix
      Release: https://github.com/jason-e/rngfix/archive/refs/tags/v1.1.3.zip

* Show Player Clips

      Source:  https://github.com/GAMMACASE/ShowPlayerClips
      Release: https://github.com/GAMMACASE/ShowPlayerClips/archive/refs/tags/1.1.3.zip

* Show Triggers

      Source: https://github.com/ecsr/showtriggers
