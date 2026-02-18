#!/bin/bash

STEAMCMD_URL="https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
MMSOURCE_URL="https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-linux.tar.gz"
SOURCEMOD_URL="https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-linux.tar.gz"
DYNAMICCHANNELS_URL="https://github.com/Vauff/DynamicChannels/archive/refs/heads/master.zip"
TICKRATEENABLER_URL="https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-linux-tick100-6e83b42.zip"

clear

if [ "$1" = "install" ]; then
    mkdir -p build
    cd build

    if [ ! -d steamcmd ]; then
        mkdir steamcmd
        cd steamcmd

        echo Downloading SteamCMD...
        curl -O $STEAMCMD_URL
        tar -xf steamcmd_linux.tar.gz
        rm steamcmd_linux.tar.gz

        echo Installing SteamCMD...
        ./steamcmd.sh +login anonymous +logout +quit

        cd ..
    fi

    if [ ! -d game ]; then
        cd steamcmd

        echo Installing Counter Strike: Source Dedicated Server...
        ./steamcmd.sh +force_install_dir ../game +login anonymous +app_update 232330 validate +logout +quit

        cd ..
    fi

    if [ ! -d game/cstrike/addons ]; then
        cd game/cstrike

        echo Downloading MetamodSource...
        curl -L -o mmsource.tar.gz $MMSOURCE_URL
        tar -xf mmsource.tar.gz
        rm mmsource.tar.gz

        echo Downloading SourceMod...
        curl -L -o sourcemod.tar.gz $SOURCEMOD_URL
        tar -xf sourcemod.tar.gz
        rm sourcemod.tar.gz

        echo Downloading DynamicChannels...
        cd addons/sourcemod
        curl -L $DYNAMICCHANNELS_URL -o dynamicchannels.zip
        unzip -o dynamicchannels.zip -d _tmp_dynamicchannels
        cp -r _tmp_dynamicchannels/*/* ./
        rm -rf _tmp_dynamicchannels dynamicchannels.zip
        cd ../..

        echo Downloading TickrateEnabler...
        curl -L -o tickrateenabler.zip $TICKRATEENABLER_URL
        unzip -o tickrateenabler.zip -d _tmp_tickrate
        cp -r _tmp_tickrate/*/* ./
        rm -rf _tmp_tickrate tickrateenabler.zip

        rm -f maps/*

        cd ../..
    fi
elif [ "$1" = "build" ]; then
    cp -r core/* build/game/cstrike/
    cp -r plugins/bhoptimer/* build/game/cstrike/
    cp -r plugins/jumpstats/* build/game/cstrike/
    cp -r plugins/landfix/* build/game/cstrike/
    cp -r plugins/pushfix/* build/game/cstrike/
    cp -r plugins/rngfix/* build/game/cstrike/
    cp -r plugins/showplayerclips/* build/game/cstrike/
    cp -r plugins/showtriggers/* build/game/cstrike/

    cd build/game/cstrike/addons/sourcemod/scripting
    echo | ./compile.sh

    cd ..
    cp -r scripting/compiled/* plugins/
elif [ "$1" = "start_lan" ]; then
    cd build/game

    ./srcds_run -game cstrike +map bhop_ambience +sv_lan 1 -maxplayers 24 -insecure -log -console
else
    echo "No valid command was specified"
fi
