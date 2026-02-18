@echo off

set STEAMCMD_URL=https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip
set MMSOURCE_URL=https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-windows.zip
set SOURCEMOD_URL=https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-windows.zip
set DYNAMICCHANNELS_URL=https://github.com/Vauff/DynamicChannels/archive/refs/heads/master.zip
set TICKRATEENABLER_URL=https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-win-tick100-6e83b42.zip

cls

if "%~1" == "install" (
    if not exist build mkdir build
    cd build

    if not exist steamcmd (
        mkdir steamcmd
        cd steamcmd

        echo Downloading SteamCMD...
        curl -O %STEAMCMD_URL%
        tar -xf steamcmd.zip
        del steamcmd.zip

        echo Installing SteamCMD...
        .\steamcmd.exe +login anonymous +logout +quit

        cd ..
    )

    if not exist game (
        cd steamcmd

        echo Installing Counter Strike: Source Dedicated Server...
        .\steamcmd.exe +force_install_dir ../game +login anonymous +app_update 232330 validate +logout +quit

        cd ..
    )

    if not exist game\cstrike\addons (
        cd game\cstrike

        echo Downloading MetamodSource...
        curl -L -o mmsource.zip %MMSOURCE_URL%
        tar -xf mmsource.zip
        del mmsource.zip

        echo Downloading SourceMod...
        curl -L -o sourcemod.zip %SOURCEMOD_URL%
        tar -xf sourcemod.zip
        del sourcemod.zip

        echo Downloading DynamicChannels...
        cd addons\sourcemod
        curl -L %DYNAMICCHANNELS_URL% -o dynamicchannels.zip
        tar -xf dynamicchannels.zip --strip-components=1
        del dynamicchannels.zip
        cd ../..

        echo Downloading TickrateEnabler...
        curl -L -o tickrateenabler.zip %TICKRATEENABLER_URL%
        tar -xf tickrateenabler.zip --strip-components=1
        del tickrateenabler.zip

        del /f /q maps\*.*

        cd ../..
    )
) else if "%~1" == "build" (
    xcopy "core\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\bhoptimer\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\jumpstats\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\landfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\pushfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\rngfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\showplayerclips\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\showtriggers\*" "build\game\cstrike\" /E /H /C /Y

    cd build\game\cstrike\addons\sourcemod\scripting
    echo. | .\compile.exe

    cd ..
    xcopy "scripting\compiled\*" "plugins\" /E /H /C /Y
) else if "%~1" == "start_lan" (
    cd build\game

    .\srcds.exe -game cstrike +map bhop_ambience +sv_lan 1 -maxplayers 24 -insecure -log -console
) else if "%~1" == "start_gui" (
    cd build\game

    .\srcds.exe -game cstrike -log
) else (
    echo No valid command was specified
)
