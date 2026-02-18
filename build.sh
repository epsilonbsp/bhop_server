#!/bin/bash

clear

if [ "$1" = "install" ]; then
    mkdir -p build
    cd build

    if [ ! -d steamcmd ]; then
        mkdir steamcmd
        cd steamcmd

        curl -O https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
        tar -xf steamcmd_linux.tar.gz
        rm steamcmd_linux.tar.gz

        ./steamcmd.sh +login anonymous +logout +quit

        cd ..
    fi

    if [ ! -d game ]; then
        cd steamcmd

        ./steamcmd.sh +force_install_dir ../game +login anonymous +app_update 232330 validate +logout +quit

        cd ..
    fi

    if [ ! -d game/cstrike/addons ]; then
        cd game/cstrike

        curl -L -o mmsource.tar.gz https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-linux.tar.gz
        tar -xf mmsource.tar.gz
        rm mmsource.tar.gz

        curl -L -o sourcemod.tar.gz https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-linux.tar.gz
        tar -xf sourcemod.tar.gz
        rm sourcemod.tar.gz

        cd addons/sourcemod
        curl -L https://github.com/Vauff/DynamicChannels/archive/refs/heads/master.zip -o dynamicchannels.zip
        tar -xf dynamicchannels.zip --strip-components=1
        rm dynamicchannels.zip
        cd ../..

        curl -L -o tickrateenabler.zip https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-linux-tick100-6e83b42.zip
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
