// SPDX-License-Identifier: GPL-3.0-only
// Copyright (C) 2026 EpsilonBSP

#pragma semicolon 1
#pragma newdecls required

#include <sourcemod>
#include <sdktools>
#include <clientprefs>

#define PLUGIN_VERSION "1.0.0"

// Modes
#define FEET_MODE_OFF          0  // disabled (default)
#define FEET_MODE_STAND_CROUCH 1  // visible when standing or crouching (on ground)
#define FEET_MODE_STAND        2  // visible when standing only
#define FEET_MODE_CROUCH       3  // visible when crouching only
#define FEET_MODE_ALWAYS       4  // always visible (including in air)

#define FEET_BEAM_LIFE     0.12  // slightly longer than timer interval
#define FEET_BEAM_WIDTH    1.5
#define FEET_TIMER_INTERVAL 0.1
#define FEET_RECT_SIZE     16.0  // half-width of the rectangle (matches player hull)
#define FEET_Z_OFFSET       2.0  // lift above ground slightly to avoid z-fighting

static const char g_cModeNames[][] = {
    "Disabled",
    "Enabled (standing/crouching)",
    "Enabled (standing only)",
    "Enabled (crouching only)",
    "Always enabled"
};

int    g_iFeetMode[MAXPLAYERS + 1];
int    g_iBeamSprite;
Handle g_hFeetCookie;

public Plugin myinfo = {
    name        = "Feet",
    author      = "EpsilonBSP",
    description = "Renders a wireframe rectangle at player feet",
    version     = PLUGIN_VERSION,
    url         = "https://github.com/epsilonbsp/sm_feet"
};

public void OnPluginStart() {
    g_hFeetCookie = RegClientCookie("feet_mode", "Feet wireframe mode", CookieAccess_Protected);

    RegConsoleCmd("sm_feet", cmd_Feet, "Cycle feet wireframe display mode.");

    CreateTimer(FEET_TIMER_INTERVAL, Timer_DrawFeet, _, TIMER_REPEAT | TIMER_FLAG_NO_MAPCHANGE);

    for (int i = 1; i <= MaxClients; i++) {
        if (IsClientInGame(i) && AreClientCookiesCached(i)) {
            OnClientCookiesCached(i);
        }
    }
}

public void OnMapStart() {
    g_iBeamSprite = PrecacheModel("sprites/laser.vmt", true);
}

public void OnClientCookiesCached(int client) {
    char sValue[8];
    GetClientCookie(client, g_hFeetCookie, sValue, sizeof(sValue));

    if (sValue[0] == '\0') {
        g_iFeetMode[client] = FEET_MODE_OFF;
    } else {
        int mode = StringToInt(sValue);
        g_iFeetMode[client] = (mode >= FEET_MODE_OFF && mode <= FEET_MODE_ALWAYS) ? mode : FEET_MODE_OFF;
    }
}

public void OnClientDisconnect(int client) {
    g_iFeetMode[client] = FEET_MODE_OFF;
}

public Action cmd_Feet(int client, int args) {
    if (client == 0) {
        return Plugin_Handled;
    }

    g_iFeetMode[client] = (g_iFeetMode[client] + 1) % (FEET_MODE_ALWAYS + 1);

    char sValue[8];
    IntToString(g_iFeetMode[client], sValue, sizeof(sValue));
    SetClientCookie(client, g_hFeetCookie, sValue);

    PrintToChat(client, "[SM] Feet: \x10%s", g_cModeNames[g_iFeetMode[client]]);

    return Plugin_Handled;
}

public Action Timer_DrawFeet(Handle timer) {
    for (int i = 1; i <= MaxClients; i++) {
        if (!IsClientInGame(i) || !IsPlayerAlive(i) || IsFakeClient(i)) {
            continue;
        }

        if (g_iFeetMode[i] == FEET_MODE_OFF) {
            continue;
        }

        bool onGround  = GetEntPropEnt(i, Prop_Send, "m_hGroundEntity") != -1;
        bool crouching = view_as<bool>(GetEntityFlags(i) & FL_DUCKING);

        bool shouldDraw = false;

        switch (g_iFeetMode[i]) {
            case FEET_MODE_STAND_CROUCH: shouldDraw = onGround;
            case FEET_MODE_STAND:        shouldDraw = onGround && !crouching;
            case FEET_MODE_CROUCH:       shouldDraw = onGround && crouching;
            case FEET_MODE_ALWAYS:       shouldDraw = true;
        }

        if (shouldDraw) {
            DrawFeetRect(i);
        }
    }

    return Plugin_Continue;
}

void DrawFeetRect(int client) {
    float origin[3];
    GetClientAbsOrigin(client, origin);

    float z = origin[2] + FEET_Z_OFFSET;
    float s = FEET_RECT_SIZE - FEET_BEAM_WIDTH / 2.0;

    float corners[4][3];
    corners[0][0] = origin[0] - s; corners[0][1] = origin[1] - s; corners[0][2] = z;
    corners[1][0] = origin[0] + s; corners[1][1] = origin[1] - s; corners[1][2] = z;
    corners[2][0] = origin[0] + s; corners[2][1] = origin[1] + s; corners[2][2] = z;
    corners[3][0] = origin[0] - s; corners[3][1] = origin[1] + s; corners[3][2] = z;

    int color[4] = {255, 255, 255, 220};

    for (int edge = 0; edge < 4; edge++) {
        int next = (edge + 1) % 4;
        TE_SetupBeamPoints(corners[edge], corners[next], g_iBeamSprite, 0, 0, 0,
            FEET_BEAM_LIFE, FEET_BEAM_WIDTH, FEET_BEAM_WIDTH, 0, 0.0, color, 0);
        TE_SendToClient(client);
    }
}
