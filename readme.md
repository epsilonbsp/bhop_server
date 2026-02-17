# Bhop Server (WIP)
My simple bhop server setup.

This setup allows to just download or clone repo, run few commands and have local server working right away.

Currently only works for Windows, later will try to update it to work for Linux.
## Setup
* Download or clone repo
* Open terminal in `bhop_server` directory
* First run this command to install server

      .\build.bat install
* Then run this command to build all plugins

      .\build.bat build
* Finally run one of these commands to start server

      # Start LAN server
      .\build.bat start_lan

      # Start server with GUI
      .\build.bat start_gui
* If you don't want to touch terminal, then there is `scripts` folder with separate script for each command. So you can just run them like executables in same order.
## Documentation
### Install command
Install command downloads and installs **SteamCMD** with **Counter Strike Source Dedicated Server**.

Also it downloads base stuff that is required for this bhop server and merges it into `cstrike` game server root directory:
* SourceMod
* MetamodSource
* DynamicChannels
* TickrateEnabler
### Build command
Currently this build system is very simple. It just copies files and runs build command. This may not be ideal, but it works and is enough for now at least.

Build command merges contents of `core` and `plugins` directories into `cstrike` game server root directory.

Then it runs `compile.exe` in `cstrike/addons/sourcemod/scripting` directory which compiles all plugins into `compiled` directory.

Finally it merges contents of `cstrike/addons/sourcemod/scripting/compiled` directory into `cstrike/addons/sourcemod/plugins` directory.

Core directory has `configs` and `scripting` directories which are copied from SourceMod.

Plugins directory has all the plugins.

So if you want to make any changes to `core` or `plugins` then you will have to run `.\build.bat build` command so it merges and compiles stuff into actual server that is located in `build/game`. You can also just compile it once, take the server and use it for your purposes without this setup.

### Start command
Start command starts the actual bhop server
### Helpful
* Server config location: `core/cfg/server.cfg`
* Admin list location: `core/addons/sourcemod/configs/admins_simple.ini`
* Use `sm_zones` command to add zones
## References
### Base
* SteamCMD

      https://developer.valvesoftware.com/wiki/SteamCMD
      https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip
* MetamodSource

      https://www.metamodsource.net/downloads.php?branch=stable
      https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-windows.zip
* SourceMod

      https://www.sourcemod.net/downloads.php?branch=stable
      https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-windows.zip
* DynamicChannels

      https://github.com/Vauff/DynamicChannels
* TickrateEnabler

      https://github.com/idk1703/TickrateEnabler/releases
      https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-win-tick100-6e83b42.zip
### Plugins
* Bhop Timer

      https://github.com/shavitush/bhoptimer/releases
      https://github.com/shavitush/bhoptimer/archive/refs/tags/v4.0.1.zip
* Jump Stats

      https://github.com/KawaiiClan/bhop-get-stats
* Land Fix

      https://github.com/Haze1337/Landfix/releases
      https://github.com/Haze1337/Landfix/archive/refs/tags/1.3.zip
* Push Fix

      https://forums.alliedmods.net/showthread.php?p=2323671
      https://forums.alliedmods.net/attachment.php?attachmentid=146798&d=1437770252
* RNG Fix

      https://github.com/jason-e/rngfix/releases
      https://github.com/jason-e/rngfix/archive/refs/tags/v1.1.3.zip
* Show Player Clips

      https://github.com/GAMMACASE/ShowPlayerClips/releases
      https://github.com/GAMMACASE/ShowPlayerClips/archive/refs/tags/1.1.3.zip
* Show Triggers

      https://github.com/ecsr/showtriggers
