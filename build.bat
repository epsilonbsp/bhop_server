@echo off

cls

if "%~1" == "install" (
    if not exist build mkdir build
    cd build

    if not exist steamcmd (
        mkdir steamcmd
        cd steamcmd

        curl -O https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip
        tar -xf steamcmd.zip
        del steamcmd.zip

        .\steamcmd.exe +login anonymous +logout +quit

        cd ..
    )

    if not exist game (
        cd steamcmd

        .\steamcmd.exe +force_install_dir ../game +login anonymous +app_update 232330 validate +logout +quit

        cd ..
    )

    if not exist game\cstrike\addons (
        cd game\cstrike

        curl -L -o mmsource.zip https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-windows.zip
        tar -xf mmsource.zip
        del mmsource.zip

        curl -L -o sourcemod.zip https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-windows.zip
        tar -xf sourcemod.zip
        del sourcemod.zip

        cd addons\sourcemod
        curl -L https://github.com/Vauff/DynamicChannels/archive/refs/heads/master.zip -o dynamicchannels.zip
        tar -xf dynamicchannels.zip --strip-components=1
        del dynamicchannels.zip
        cd ../..

        curl -L -o tickrateenabler.zip https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-win-tick100-6e83b42.zip
        tar -xf tickrateenabler.zip --strip-components=1
        del tickrateenabler.zip

        cd ../..
    )
)

if "%~1" == "build" (
    xcopy "core\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\bhoptimer\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\jumpstats\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\landfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\pushfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\rngfix\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\showplayerclips\*" "build\game\cstrike\" /E /H /C /Y
    xcopy "plugins\showtriggers\*" "build\game\cstrike\" /E /H /C /Y

    cd build\game\cstrike\addons\sourcemod\scripting
    .\compile.exe

    cd ..
    xcopy "scripting\compiled\*" "plugins\" /E /H /C /Y
)

if "%~1" == "start" (
    cd build\game

    .\srcds.exe -game cstrike -insecure +sv_cheats 1 +sv_airaccelerate 1000 +sv_enablebunnyhopping 1 -tickrate 100 +sv_maxcmdrate 100 +sv_maxupdaterate 100 +mp_autokick 0 +mp_freezetime 0 +bot_quota_mode normal +sv_hudhint_sound 0 +mp_ignore_round_win_conditions 1 +mp_autoteambalance 0 +mp_limitteams 0 +bot_join_after_player 0 +bot_dont_shoot 1 +bot_chatter off +mp_roundtime 0 +mp_autoteambalance 0 +sv_accelerate 5
)
