// SPDX-License-Identifier: GPL-3.0-only
// Copyright (C) 2026 EpsilonBSP

#pragma semicolon 1
#pragma newdecls required

#include <sourcemod>
#include <sdktools>
#include <clientprefs>

#define PLUGIN_VERSION         "1.0.0"
#define SOUND_PREFIX           "fun/" // relative to sound/ folder (for PrecacheSound / EmitSound)
#define SOUND_DURATION_PADDING 0.5 // extra seconds after sound ends before unlocking
#define CONFIG_PATH            "configs/fun_sounds.cfg"

enum struct SoundEntry {
    char  sKey[64];
    char  sFile[PLATFORM_MAX_PATH];
    float fDuration;
}

ArrayList g_aSoundList;
bool      g_bSoundPlaying;
Handle    g_hSoundTimer;
bool      g_bEnabled[MAXPLAYERS + 1];
Handle    g_hEnabledCookie;

public Plugin myinfo = {
    name        = "Fun Sounds",
    author      = "EpsilonBSP",
    description = "Play fun sounds to all players from a shared library",
    version     = PLUGIN_VERSION,
    url         = "https://github.com/epsilonbsp/sm_fun"
};

public void OnPluginStart() {
    g_aSoundList = new ArrayList(sizeof(SoundEntry));

    g_hEnabledCookie = RegClientCookie("funsounds_enabled", "Fun Sounds enabled", CookieAccess_Protected);

    RegConsoleCmd("sm_funsounds",       cmd_FunSounds,       "Open the fun sounds menu");
    RegConsoleCmd("sm_funsoundsenable", cmd_FunSoundsEnable, "Toggle fun sounds on/off for yourself");
    RegConsoleCmd("sm_funsoundslist",   cmd_FunSoundsList,   "Browse and play fun sounds");

    AddCommandListener(OnSay, "say");
    AddCommandListener(OnSay, "say_team");

    for (int i = 1; i <= MaxClients; i++) {
        if (IsClientInGame(i) && AreClientCookiesCached(i)) {
            OnClientCookiesCached(i);
        }
    }
}

public void OnMapStart() {
    LoadSoundConfig();
}

public void OnMapEnd() {
    ClearSoundState();
}

void LoadSoundConfig() {
    ClearSoundState();
    g_aSoundList.Clear();

    char sPath[PLATFORM_MAX_PATH];
    BuildPath(Path_SM, sPath, sizeof(sPath), CONFIG_PATH);

    KeyValues kv = new KeyValues("FunSounds");

    if (!kv.ImportFromFile(sPath)) {
        LogError("[FunSounds] Could not load config '%s'", sPath);
        delete kv;

        return;
    }

    if (!kv.GotoFirstSubKey()) {
        delete kv;

        return;
    }

    do {
        SoundEntry entry;
        kv.GetSectionName(entry.sKey, sizeof(entry.sKey));
        kv.GetString("file", entry.sFile, sizeof(entry.sFile));
        entry.fDuration = kv.GetFloat("duration", 1.0);

        char sSoundPath[PLATFORM_MAX_PATH];
        FormatEx(sSoundPath, sizeof(sSoundPath), "%s%s", SOUND_PREFIX, entry.sFile);
        PrecacheSound(sSoundPath, true);

        char sDlPath[PLATFORM_MAX_PATH];
        FormatEx(sDlPath, sizeof(sDlPath), "sound/%s%s", SOUND_PREFIX, entry.sFile);
        AddFileToDownloadsTable(sDlPath);

        g_aSoundList.PushArray(entry, sizeof(entry));
    } while (kv.GotoNextKey());

    delete kv;

    LogMessage("[FunSounds] Loaded %d sound(s) from config.", g_aSoundList.Length);
}

public void OnClientCookiesCached(int client) {
    char sValue[8];
    GetClientCookie(client, g_hEnabledCookie, sValue, sizeof(sValue));
    g_bEnabled[client] = (sValue[0] == '\0' || StringToInt(sValue) != 0);
}

public void OnClientDisconnect(int client) {
    g_bEnabled[client] = true;
}

public Action cmd_FunSounds(int client, int args) {
    if (client == 0) {
        ReplyToCommand(client, "[MapLoader] This command must be used in-game.");

        return Plugin_Handled;
    }

    OpenMainMenu(client);

    return Plugin_Handled;
}

public Action cmd_FunSoundsEnable(int client, int args) {
    if (client == 0) {
        ReplyToCommand(client, "[MapLoader] This command must be used in-game.");

        return Plugin_Handled;
    }

    ToggleEnabled(client);

    return Plugin_Handled;
}

public Action cmd_FunSoundsList(int client, int args) {
    if (client == 0) {
        ReplyToCommand(client, "[MapLoader] This command must be used in-game.");

        return Plugin_Handled;
    }

    OpenSoundListMenu(client);

    return Plugin_Handled;
}

void OpenMainMenu(int client) {
    Menu menu = new Menu(MenuHandler_Main);
    menu.SetTitle("Fun Sounds");

    char sToggle[64];
    FormatEx(sToggle, sizeof(sToggle), "Sounds: [%s]", g_bEnabled[client] ? "Enabled" : "Disabled");
    menu.AddItem("toggle", sToggle);
    menu.AddItem("list", "Sound List");

    menu.Display(client, MENU_TIME_FOREVER);
}

public int MenuHandler_Main(Menu menu, MenuAction action, int param1, int param2) {
    if (action == MenuAction_Select) {
        char sInfo[16];
        menu.GetItem(param2, sInfo, sizeof(sInfo));

        if (StrEqual(sInfo, "toggle")) {
            ToggleEnabled(param1);
            OpenMainMenu(param1);
        } else if (StrEqual(sInfo, "list")) {
            OpenSoundListMenu(param1);
        }
    } else if (action == MenuAction_End) {
        delete menu;
    }

    return 0;
}

void ToggleEnabled(int client) {
    g_bEnabled[client] = !g_bEnabled[client];

    char sValue[8];
    IntToString(g_bEnabled[client] ? 1 : 0, sValue, sizeof(sValue));
    SetClientCookie(client, g_hEnabledCookie, sValue);

    PrintToChat(client, "[SM] Fun Sounds: \x10%s", g_bEnabled[client] ? "Enabled" : "Disabled");
}

void OpenSoundListMenu(int client) {
    if (g_aSoundList.Length == 0) {
        PrintToChat(client, "[SM] No sounds loaded. Check %s.", CONFIG_PATH);

        return;
    }

    Menu menu = new Menu(MenuHandler_SoundList);
    menu.SetTitle("Fun Sounds");

    for (int i = 0; i < g_aSoundList.Length; i++) {
        SoundEntry entry;
        g_aSoundList.GetArray(i, entry, sizeof(entry));

        char sIdx[12];
        IntToString(i, sIdx, sizeof(sIdx));
        menu.AddItem(sIdx, entry.sKey);
    }

    menu.Display(client, MENU_TIME_FOREVER);
}

public int MenuHandler_SoundList(Menu menu, MenuAction action, int param1, int param2) {
    if (action == MenuAction_Select) {
        if (g_bSoundPlaying) {
            PrintToChat(param1, "[SM] A sound is already playing.");
            OpenSoundListMenu(param1);

            return 0;
        }

        char sIdx[12];
        menu.GetItem(param2, sIdx, sizeof(sIdx));
        PlayFunSound(StringToInt(sIdx));
        OpenSoundListMenu(param1);
    } else if (action == MenuAction_End) {
        delete menu;
    }

    return 0;
}

public Action OnSay(int client, const char[] command, int argc) {
    if (client == 0 || g_bSoundPlaying) {
        return Plugin_Continue;
    }

    char sText[64];
    GetCmdArgString(sText, sizeof(sText));
    StripQuotes(sText);

    for (int i = 0; i < g_aSoundList.Length; i++) {
        SoundEntry entry;
        g_aSoundList.GetArray(i, entry, sizeof(entry));

        if (StrEqual(sText, entry.sKey, false)) {
            PlayFunSound(i);

            return Plugin_Continue;
        }
    }

    return Plugin_Continue;
}

void PlayFunSound(int idx) {
    SoundEntry entry;
    g_aSoundList.GetArray(idx, entry, sizeof(entry));

    g_bSoundPlaying = true;

    char sSoundPath[PLATFORM_MAX_PATH];
    FormatEx(sSoundPath, sizeof(sSoundPath), "%s%s", SOUND_PREFIX, entry.sFile);

    for (int i = 1; i <= MaxClients; i++) {
        if (!IsClientInGame(i) || IsFakeClient(i) || !g_bEnabled[i]) {
            continue;
        }

        EmitSoundToClient(i, sSoundPath);
    }

    PrintToChatAll("[SM] Playing: \x10%s", entry.sKey);
    PrintToServer("[FunSounds] %s duration: %.2fs", entry.sKey, entry.fDuration);

    g_hSoundTimer = CreateTimer( entry.fDuration + SOUND_DURATION_PADDING, Timer_SoundEnd, _, TIMER_FLAG_NO_MAPCHANGE);
}

void ClearSoundState() {
    if (g_hSoundTimer != null) {
        delete g_hSoundTimer;

        g_hSoundTimer = null;
    }

    g_bSoundPlaying = false;
}

public Action Timer_SoundEnd(Handle timer) {
    g_hSoundTimer   = null;
    g_bSoundPlaying = false;

    return Plugin_Stop;
}
