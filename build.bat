@echo off

set STEAMCMD_URL=https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip
set MMSOURCE_URL=https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-windows.zip
set SOURCEMOD_URL=https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-windows.zip
set DYNAMICCHANNELS_URL=https://github.com/Vauff/DynamicChannels/archive/refs/heads/master.zip
set TICKRATEENABLER_URL=https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-win-tick100-6e83b42.zip
set RIPEXT_URL=https://github.com/ErikMinekus/sm-ripext/releases/download/1.3.2/sm-ripext-1.3.2-windows.zip
set BZIP2_URL=https://github.com/epsilonbsp/sm_bzip2/releases/download/v1.0.0/sm_bzip2_v1.0.0.zip

cls

if "%~1" == "install" (
    if not exist build mkdir build
    pushd build

    if not exist steamcmd (
        mkdir steamcmd
        pushd steamcmd

        echo Downloading SteamCMD...
        curl -O %STEAMCMD_URL%
        tar -xf steamcmd.zip
        del steamcmd.zip

        echo Installing SteamCMD...
        .\steamcmd.exe +login anonymous +logout +quit

        popd
    )

    if not exist game (
        pushd steamcmd

        echo Installing Counter Strike: Source Dedicated Server...
        .\steamcmd.exe +force_install_dir ../game +login anonymous +app_update 232330 validate +logout +quit

        popd
    )

    if not exist game\cstrike\addons (
        pushd game\cstrike

        echo Downloading MetamodSource...
        curl -L -o mmsource.zip %MMSOURCE_URL%
        tar -xf mmsource.zip
        del mmsource.zip

        echo Downloading SourceMod...
        curl -L -o sourcemod.zip %SOURCEMOD_URL%
        tar -xf sourcemod.zip
        del sourcemod.zip

        echo Downloading DynamicChannels...
        pushd addons\sourcemod
        curl -L %DYNAMICCHANNELS_URL% -o dynamicchannels.zip
        tar -xf dynamicchannels.zip --strip-components=1
        del dynamicchannels.zip
        popd

        echo Downloading TickrateEnabler...
        curl -L -o tickrateenabler.zip %TICKRATEENABLER_URL%
        tar -xf tickrateenabler.zip --strip-components=1
        del tickrateenabler.zip

        echo Downloading REST in Pawn Extension...
        curl -L -o ripext.zip %RIPEXT_URL%
        tar -xf ripext.zip
        del ripext.zip

        echo Downloading Bzip2 Extension...
        curl -L -o bzip2.zip %BZIP2_URL%
        tar -xf bzip2.zip
        del bzip2.zip

        del /f /q maps\*.*

        popd
    )

    popd
) else if "%~1" == "build" (
    xcopy "core\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\bhoptimer\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\jumpstats\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\landfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\pushfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\rngfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\showplayerclips\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\showtriggers\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\maploader\*" "build\game\cstrike\" /E /H /C /Y

    pushd build\game\cstrike\addons\sourcemod\scripting

    echo. | .\compile.exe
    cd ..
    xcopy "scripting\compiled\*" "plugins\" /E /H /C /Y

    popd
) else if "%~1" == "start_lan" (
    pushd build\game

    .\srcds.exe -game cstrike +map bhop_ambience +sv_lan 1 -maxplayers 24 -insecure -log -console

    popd
) else if "%~1" == "start_gui" (
    pushd build\game

    .\srcds.exe -game cstrike -log

    popd
) else (
    echo No valid command was specified
)
