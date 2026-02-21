#!/bin/bash

STEAMCMD_URL="https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
MMSOURCE_URL="https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-linux.tar.gz"
SOURCEMOD_URL="https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-linux.tar.gz"
DYNAMICCHANNELS_URL="https://github.com/Vauff/DynamicChannels/archive/refs/heads/master.zip"
TICKRATEENABLER_URL="https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-linux-tick100-6e83b42.zip"
RIPEXT_URL="https://github.com/ErikMinekus/sm-ripext/releases/download/1.3.2/sm-ripext-1.3.2-linux.zip"
BZIP2_URL="https://github.com/epsilonbsp/sm_bzip2/releases/download/v1.0.0/sm_bzip2_v1.0.0.zip"

clear

if [ "$1" = "install" ]; then
    mkdir -p build
    pushd build

    if [ ! -d steamcmd ]; then
        mkdir steamcmd
        pushd steamcmd

        echo Downloading SteamCMD...
        curl -O $STEAMCMD_URL
        tar -xf steamcmd_linux.tar.gz
        rm steamcmd_linux.tar.gz

        echo Installing SteamCMD...
        ./steamcmd.sh +login anonymous +logout +quit

        popd
    fi

    if [ ! -d game ]; then
        pushd steamcmd

        echo Installing Counter Strike: Source Dedicated Server...
        ./steamcmd.sh +force_install_dir ../game +login anonymous +app_update 232330 validate +logout +quit

        popd ..
    fi

    if [ ! -d game/cstrike/addons ]; then
        pushd game/cstrike

        echo Downloading MetamodSource...
        curl -L -o mmsource.tar.gz $MMSOURCE_URL
        tar -xf mmsource.tar.gz
        rm mmsource.tar.gz

        echo Downloading SourceMod...
        curl -L -o sourcemod.tar.gz $SOURCEMOD_URL
        tar -xf sourcemod.tar.gz
        rm sourcemod.tar.gz

        echo Downloading DynamicChannels...
        pushd addons/sourcemod
        curl -L $DYNAMICCHANNELS_URL -o dynamicchannels.zip
        unzip -o dynamicchannels.zip -d _tmp_dynamicchannels
        cp -r _tmp_dynamicchannels/*/* ./
        rm -rf _tmp_dynamicchannels dynamicchannels.zip
        popd

        echo Downloading TickrateEnabler...
        curl -L -o tickrateenabler.zip $TICKRATEENABLER_URL
        unzip -o tickrateenabler.zip -d _tmp_tickrate
        cp -r _tmp_tickrate/*/* ./
        rm -rf _tmp_tickrate tickrateenabler.zip

        echo Downloading REST in Pawn Extension...
        curl -L -o ripext.zip $RIPEXT_URL
        unzip -o ripext.zip
        rm ripext.zip

        echo Downloading Bzip2 Extension...
        curl -L -o bzip2.zip $BZIP2_URL
        unzip -o bzip2.zip
        rm bzip2.zip

        rm -f maps/*

        popd
    fi

    popd
elif [ "$1" = "build" ]; then
    cp -r core/* build/game/cstrike/
    cp -r plugins/bhoptimer/* build/game/cstrike/
    cp -r plugins/jumpstats/* build/game/cstrike/
    cp -r plugins/landfix/* build/game/cstrike/
    cp -r plugins/pushfix/* build/game/cstrike/
    cp -r plugins/rngfix/* build/game/cstrike/
    cp -r plugins/showplayerclips/* build/game/cstrike/
    cp -r plugins/showtriggers/* build/game/cstrike/
    cp -r plugins/maploader/* build/game/cstrike/

    pushd build/game/cstrike/addons/sourcemod/scripting

    echo | ./compile.sh
    cd ..
    cp -r scripting/compiled/* plugins/

    popd
elif [ "$1" = "start_lan" ]; then
    pushd build/game

    ./srcds_run -game cstrike +map bhop_ambience +sv_lan 1 -maxplayers 24 -insecure -log -console

    popd
else
    echo "No valid command was specified"
fi
