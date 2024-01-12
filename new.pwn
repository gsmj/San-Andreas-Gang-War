public OnGameModeInit()
{


	TD_Capture[1] = TextDrawCreate(5.333312, 275.851837, "Time: 4:02");
	TextDrawLetterSize(TD_Capture[1], 0.323332, 1.346961);
	TextDrawAlignment(TD_Capture[1], 1);
	TextDrawColor(TD_Capture[1], 8388863);
	TextDrawSetShadow(TD_Capture[1], 0);
	TextDrawSetOutline(TD_Capture[1], 1);
	TextDrawBackgroundColor(TD_Capture[1], 128);
	TextDrawFont(TD_Capture[1], 1);
	TextDrawSetProportional(TD_Capture[1], 1);

	TD_Capture[2] = TextDrawCreate(4.666645, 287.637084, "Varios Los Aztecas  ~r~13");
	TextDrawLetterSize(TD_Capture[2], 0.315997, 1.226662);
	TextDrawAlignment(TD_Capture[2], 1);
	TextDrawColor(TD_Capture[2], -1);
	TextDrawSetShadow(TD_Capture[2], 0);
	TextDrawSetOutline(TD_Capture[2], 1);
	TextDrawBackgroundColor(TD_Capture[2], 255);
	TextDrawFont(TD_Capture[2], 1);
	TextDrawSetProportional(TD_Capture[2], 1);

	TD_Capture[3] = TextDrawCreate(5.333312, 298.592864, "Los Santos Vagos  ~r~21");
	TextDrawLetterSize(TD_Capture[3], 0.315997, 1.226662);
	TextDrawAlignment(TD_Capture[3], 1);
	TextDrawColor(TD_Capture[3], -1);
	TextDrawSetShadow(TD_Capture[3], 0);
	TextDrawSetOutline(TD_Capture[3], 1);
	TextDrawBackgroundColor(TD_Capture[3], 255);
	TextDrawFont(TD_Capture[3], 1);
	TextDrawSetProportional(TD_Capture[3], 1);





public OnPlayerConnect(playerid)
{
    ClearVars(playerid);
    SetPlayerColor(playerid, COLOR_ADMMSG);
    currIDspec[playerid] = -1;
    PlayerInfo[playerid][pMaskTime] = -1;
    PlayerInfo[playerid][pJail] = -1;
    PlayerInfo[playerid][pMute] = -1;
    togPM{playerid} = 1;
	PlayerTimerID[playerid] = SetTimerEx("PlayerUpdate", 250, 1, "d", playerid);
	GetPlayerName(playerid, PlayerInfo[playerid][pName], MAX_PLAYER_NAME);
	for(new i = 0; i != sizeof(ZoneInfo); i++) GangZoneShowForPlayer(playerid, ZoneInfo[i][gID], GetGZColor(ZoneInfo[i][gGang]));
	new query[96];
	new tempip[16];
	GetPlayerIp(playerid, tempip, 16);
	mysql_format(mysql_connection, query, sizeof(query), "SELECT `ip`, `daystounban` FROM `ipbans` WHERE `ip`='%s'", tempip);
	mysql_tquery(mysql_connection, query, "CheckForIPBan", "ds", playerid, tempip);

	TD_Speedo[playerid] = CreatePlayerTextDraw(playerid, 440.000000, 400.000000, "0_km/h__~h~Fuel_0__~b~1000~n~~g~~h~Open~w~___max___E_S__M_L_B");
	PlayerTextDrawLetterSize(playerid, TD_Speedo[playerid], 0.400000, 1.700000);
	PlayerTextDrawTextSize(playerid, TD_Speedo[playerid], 625.000000, 500.000000);
	PlayerTextDrawUseBox(playerid, TD_Speedo[playerid], true);
	PlayerTextDrawBoxColor(playerid, TD_Speedo[playerid], 0x00000066);
	PlayerTextDrawColor(playerid, TD_Speedo[playerid], 0x0099FFFF);
	PlayerTextDrawSetShadow(playerid, TD_Speedo[playerid], 2);
	PlayerTextDrawSetOutline(playerid, TD_Speedo[playerid], 1);
	PlayerTextDrawBackgroundColor(playerid, TD_Speedo[playerid], 0x000000FF);
	PlayerTextDrawFont(playerid, TD_Speedo[playerid], 1);
	return 1;
}

public OnPlayerDisconnect(playerid, reason)
{
    if(PlayerInfo[playerid][pRoomCreateID] != -1)
    {
        DeleteRoom(PlayerInfo[playerid][pRoomCreateID]);
        foreach(new i:Player)
        {
            if(PlayerInfo[i][pRoom] == PlayerInfo[playerid][pRoomCreateID])
            {
                PlayerInfo[i][pRoom] = -1;
                SendClientMessage(i, COLOR_YELLOW, "Создатель комнаты вышел с сервера. Комната была удалена");
    			return cmd::newband(i, "");
            }
        }
    }
    if(PlayerInfo[playerid][pAR] == 0) SaveAccount(playerid);
    if(startPVP{playerid} == 1)
    {
    	SendClientMessage(offerID[playerid], COLOR_YELLOW, "Соперник покинул сервер. Дуэль окончена");
     	cmd::newband(offerID[playerid], "");
      	startPVP{playerid} = 0;
       	startPVP{offerID[playerid]} = 0;
       	ClearOffersVars(playerid);
    }
    if(isOffered{playerid} == 1 || isOfferedTo{playerid} == 1) ClearOffersVars(playerid);
    if(PlayerInfo[playerid][pRoom] != -1) RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rOnline]--;
    if(PlayerInfo[playerid][pArena] != 0) onlinearena[PlayerInfo[playerid][pArena]]--;
    DeletePVar(playerid, "RAdm");
    if(idadminspec[playerid] != -1)
    {
        SpawnPlayer(idadminspec[playerid]);
        GameTextForPlayer(playerid, "~y~PLAYER DISCONNECTED", 4, 2000);
        HideMenuForPlayer(spmenu, idadminspec[playerid]);
        idadminspec[playerid] = -1;
    }
    KillTimer(PlayerTimerID[playerid]);
	return 1;
}

public OnPlayerSpawn(playerid)
{
    if(PlayerInfo[playerid][pAR] == 1)
	{
	    SendClientMessage(playerid, COLOR_ORANGE, "Введите /q (/quit) чтобы выйти");
	    SendClientMessage(playerid, COLOR_ORANGE, "Для игры на сервере Вы должны пройти авторизацию");
	    ShowPlayerDialog(playerid, dWarning, DIALOG_STYLE_MSGBOX, "{FF6600}Ошибка", "{ffffff}Для игры на сервере Вы должны пройти авторизацию", "Закрыть", "");
	    return KickEx(playerid);
	}
	if(PlayerInfo[playerid][pAR] == 2)
	{
	    SendClientMessage(playerid, COLOR_ORANGE, "Введите /q (/quit) чтобы выйти");
	    SendClientMessage(playerid, COLOR_ORANGE, "Для игры на сервере Вы должны пройти регистрацию");
	    ShowPlayerDialog(playerid, dWarning, DIALOG_STYLE_MSGBOX, "{FF6600}Ошибка", "{ffffff}Для игры на сервере Вы должны пройти регистрацию", "Закрыть", "");
	    return KickEx(playerid);
	}
	if(PlayerInfo[playerid][pJail] > 0)
	{
	    SetPlayerInterior(playerid, 10);
		SetPlayerVirtualWorld(playerid, 35);
		SetPlayerPos(playerid,223.2032,110.0860,999.0156);
		SetPlayerSkin(playerid, 268);
		SetPlayerColor(playerid, COLOR_ADMMSG);
		return PlayerInfo[playerid][pGang] = 0;
	}
	if(GetPVarInt(playerid, "newband") == 1) cmd::newband(playerid, "");
	if(PlayerInfo[playerid][pRoom] != -1) SetPlayerSpawnRoom(playerid);
	if(PlayerInfo[playerid][pArena] != 0) SetPlayerSpawnArena(playerid);
	if(PlayerInfo[playerid][pGang] != 0) SetPlayerSpawnGhetto(playerid);
	SetPlayerHealth(playerid, 100.0);
	Curr_TD[playerid] = 0;
	if(!PlayerInfo[playerid][pSkin]) return SetPlayerChooseSkin(playerid);
	SetPlayerSkin(playerid, PlayerInfo[playerid][pSkin]);
	if(currIDspec[playerid] != -1)
	{
	    SetPlayerPos(playerid, GetPVarFloat(playerid, "UnSpecPosX"), GetPVarFloat(playerid, "UnSpecPosY"), GetPVarFloat(playerid, "UnSpecPosZ"));
		SetPlayerVirtualWorld(playerid, GetPVarInt(playerid, "UnSpecVirtualWorld"));
		SetPlayerInterior(playerid, GetPVarInt(playerid, "UnSpecInterior"));
		SetPlayerFacingAngle(playerid, GetPVarFloat(playerid, "UnSpecFacingAngle"));
		currIDspec[playerid] = -1;
		DeletePVar(playerid, "UnSpecPosX");
		DeletePVar(playerid, "UnSpecPosY");
		DeletePVar(playerid, "UnSpecPosZ");
		DeletePVar(playerid, "UnSpecVirtualWorld");
		DeletePVar(playerid, "UnSpecInterior");
		DeletePVar(playerid, "UnSpecFacingAngle");
	}
	return 1;
}

public OnPlayerDeath(playerid, killerid, reason)
{
	PlayerInfo[playerid][pHealth] = 0;
    if(killerid != INVALID_PLAYER_ID)
	{
	    if(startPVP{playerid} == 1)
	    {
	    	SendClientMessage(offerID[playerid], COLOR_GREEN, "Соперник был убит. Вы победили");
	    	PlayerPlaySound(offerID[playerid], 1058, 0.0, 0.0, 0.0);
	    	SendClientMessage(playerid, COLOR_YELLOW, "Вы погибли. Дуэль проиграна");
       		cmd::newband(offerID[playerid], "");
	     	SetPVarInt(playerid, "newband", 1);
	      	startPVP{playerid} = 0;
	       	startPVP{offerID[playerid]} = 0;
	       	ClearOffersVars(playerid);
	    }
	    SendDeathMessage(killerid, playerid, reason);
		PlayerInfo[playerid][pDeaths]++;
		PlayerInfo[killerid][pKills]++;
		PlayerInfo[playerid][pMask] = 0;
		PlayerInfo[playerid][pAid] = 0;
	    SetPlayerScore(killerid, PlayerInfo[killerid][pKills]);
	    if(capture == 1)
		{
		    if(PlayerInfo[killerid][pGang] == team_capture[0] && PlayerInfo[playerid][pGang] == team_capture[1])
		    {
				kills_team[0] += 1;
			}
			else if(PlayerInfo[killerid][pGang] == team_capture[1] && PlayerInfo[playerid][pGang] == team_capture[0])
			{
				kills_team[1] += 1;
			}
		}
	}
	PlayerInfo[playerid][pMask] = 0;
	PlayerInfo[playerid][pAid] = 0;
	PlayerInfo[playerid][pMaskTime] = -1;
	return 1;
}

public OnPlayerTakeDamage(playerid, issuerid, Float:amount, weaponid)
{
    /*new Float:HP;
    new Float:x, Float:y, Float:z;
    GetPlayerPos(issuerid, x, y, z);
    GetPlayerHealth(playerid, HP);
    if(weaponid == 27)
    {
        if(IsPlayerInRangeOfPoint(playerid, 26.5 , x, y ,z))
        {
            SetPlayerHealth(playerid, HP-45);
        }
    }*/
    return true;
}

public OnVehicleSpawn(vehicleid)
{
    SetVehicleParamsEx(vehicleid, VehInfo[vehicleid][vEngine], VehInfo[vehicleid][vLight], 0, VehInfo[vehicleid][vLock], 0, 0, 0);
	return 1;
}

public OnVehicleDeath(vehicleid, killerid)
{
    VehInfo[vehicleid][vFuel] = 40;
    VehInfo[vehicleid][vEngine] = 0;
    VehInfo[vehicleid][vLock] = 0;
	VehInfo[vehicleid][vLimiter] = 1;
	VehInfo[vehicleid][vWasLimit] = 1;
	VehInfo[vehicleid][vLight] = 0;
	VehInfo[vehicleid][vBelt][0] = 0;
	VehInfo[vehicleid][vBelt][1] = 0;
	VehInfo[vehicleid][vBelt][2] = 0;
	VehInfo[vehicleid][vBelt][3] = 0;
	VehInfo[vehicleid][vBelt][4] = 0;
	return 1;
}

public OnPlayerText(playerid, text[])
{
	if(PlayerInfo[playerid][pMute] != -1)
	{
	    SendClientMessage(playerid, COLOR_ORANGE, "Вы не можете писать в чат");
	    return false;
	}
	ProxDetector(playerid, 30.0, text);
	SetPlayerChatBubble(playerid, text, 0x00CCFFAA, 15.0, 1200);
	return 0;
}

public OnPlayerCommandText(playerid, cmdtext[])
{
	return 0;
}

public OnPlayerEnterVehicle(playerid, vehicleid, ispassenger)
{
	if(ispassenger)
	{
	    if(VehInfo[vehicleid][vSignal] == 1)
		{
		    SetTimerEx("ClearSignal", 4000, false, "d", vehicleid);
		    SetVehicleParamsEx(vehicleid, VehInfo[vehicleid][vEngine], VehInfo[vehicleid][vLight], 1, VehInfo[vehicleid][vLock], 0, 0, 0);
		}
	}
	return 1;
}


public OnPlayerPickUpPickup(playerid, pickupid)
{
    if(pickupid == grove_io[0])
	{
	    if(PlayerInfo[playerid][pGang] != GANG_GROVE) return SendClientMessage(playerid, COLOR_ORANGE, "У Вас нет доступа"), PlayerPlaySound(playerid, 1145, 0.0, 0.0, 0.0);
		SetPlayerPos(playerid, 2466.9431,-1698.1516,1013.5078);
		SetPlayerFacingAngle(playerid, 90.0);
		SetCameraBehindPlayer(playerid);
		SetPlayerVirtualWorld(playerid, 2);
		return SetPlayerInterior(playerid, 2);
	}
	if(pickupid == grove_io[1])
	{
		SetPlayerPos(playerid, 2512.0674,-1689.0492,13.5518);
		SetCameraBehindPlayer(playerid);
		SetPlayerFacingAngle(playerid, 42.0);
		SetPlayerVirtualWorld(playerid, 0);
		return SetPlayerInterior(playerid, 0);
	}
	if(pickupid == ballas_io[0])
	{
	    if(PlayerInfo[playerid][pGang] != GANG_BALLAS) return SendClientMessage(playerid, COLOR_ORANGE, "У Вас нет доступа"), PlayerPlaySound(playerid, 1145, 0.0, 0.0, 0.0);
	    SetPlayerPos(playerid, -42.6860,1408.4878,1084.4297);
		SetPlayerFacingAngle(playerid, 1.4398);
		SetCameraBehindPlayer(playerid);
		SetPlayerVirtualWorld(playerid, 2);
		return SetPlayerInterior(playerid, 8);
	}
	if(pickupid == ballas_io[1])
	{
		SetPlayerPos(playerid, 2022.9169,-1122.7472,26.2329);
		SetCameraBehindPlayer(playerid);
		SetPlayerInterior(playerid, 0);
		return SetPlayerVirtualWorld(playerid, 0);
	}
	if(pickupid == vagos_io[0])
	{
	    if(PlayerInfo[playerid][pGang] != GANG_VAGOS) return SendClientMessage(playerid, COLOR_ORANGE, "У Вас нет доступа"), PlayerPlaySound(playerid, 1145, 0.0, 0.0, 0.0);
	    SetPlayerPos(playerid, 318.5781,1116.8354,1083.8828);
		SetPlayerFacingAngle(playerid, 359.2);
		SetCameraBehindPlayer(playerid);
		SetPlayerVirtualWorld(playerid, 2);
		return SetPlayerInterior(playerid, 5);
	}
	if(pickupid == vagos_io[1])
	{
		SetPlayerPos(playerid, 2756.3386,-1180.5819,69.3947);
		SetPlayerFacingAngle(playerid, 359.5);
		SetCameraBehindPlayer(playerid);
		SetPlayerVirtualWorld(playerid, 0);
		return SetPlayerInterior(playerid, 0);
	}
	if(pickupid == aztecas_io[0])
	{
	    if(PlayerInfo[playerid][pGang] != GANG_AZTECAS) return SendClientMessage(playerid, COLOR_ORANGE, "У Вас нет доступа"), PlayerPlaySound(playerid, 1145, 0.0, 0.0, 0.0);
	    SetPlayerPos(playerid, 224.1984,1240.0269,1082.1406);
	    SetPlayerFacingAngle(playerid, 88.7);
	    SetCameraBehindPlayer(playerid);
		SetPlayerVirtualWorld(playerid, 2);
		return SetPlayerInterior(playerid, 2);
	}
	if(pickupid == aztecas_io[1])
	{
	    SetPlayerPos(playerid, 2185.8420,-1812.8882,13.5469);
	    SetPlayerFacingAngle(playerid, 359.28);
	    SetCameraBehindPlayer(playerid);
	    SetPlayerVirtualWorld(playerid, 0);
		return SetPlayerInterior(playerid, 0);
	}
	if(pickupid == rifa_io[0])
	{
	    if(PlayerInfo[playerid][pGang] != GANG_RIFA) return SendClientMessage(playerid, COLOR_ORANGE, "У Вас нет доступа"), PlayerPlaySound(playerid, 1145, 0.0, 0.0, 0.0);
	    SetPlayerPos(playerid, -68.8697,1353.4139,1080.2109);
		SetPlayerFacingAngle(playerid, 358.4);
		SetCameraBehindPlayer(playerid);
		SetPlayerVirtualWorld(playerid, 2);
		return SetPlayerInterior(playerid, 6);
	}
	if(pickupid == rifa_io[1])
	{
	    SetPlayerPos(playerid, 2784.6641,-1926.0099,13.5469);
		SetPlayerFacingAngle(playerid, 89.2);
		SetCameraBehindPlayer(playerid);
		SetPlayerVirtualWorld(playerid, 0);
		return SetPlayerInterior(playerid, 0);
	}
	return 1;
}

public OnPlayerSelectedMenuRow(playerid, row)
{
    if(GetPlayerMenu(playerid) == spmenu)
	{
	    switch(row)
	    {
	        case 0:
		 	{
		 		return cmd::spoff(playerid);
		 	}
		 	case 1:
	        {
				new str[76];
				format(str, sizeof(str), "[SP] %s[%d] пнул игрока %s[%d]", PlayerInfo[playerid][pName], playerid, PlayerInfo[currIDspec[playerid]][pName], currIDspec[playerid]);
				SendAdminMessage(COLOR_ADMMSG, str, 1);
				new Float:slapx, Float:slapy, Float:slapz;
				GetPlayerPos(currIDspec[playerid], slapx, slapy, slapz);
				SetPlayerPos(currIDspec[playerid], slapx, slapy, slapz+5.0);
				PlayerPlaySound(currIDspec[playerid], 1130, 0.0, 0.0, 0.0);
				return ShowMenuForPlayer(spmenu, playerid);
		 	}
		 	case 2:
	        {
	            new str[108];
				format(str, sizeof(str), "[SP] %s[%d] кикнул игрока %s[%d] без лишнего шума", PlayerInfo[playerid][pName], playerid, PlayerInfo[currIDspec[playerid]][pName], currIDspec[playerid]);
				SendAdminMessage(COLOR_ADMMSG, str, 1);
				format(str, sizeof(str), "Вы были кикнуты администратором %s[%d] за нарушение правил сервера", PlayerInfo[currIDspec[playerid]][pName], currIDspec[playerid]);
				SendClientMessage(currIDspec[playerid], COLOR_ADMMSG, str);
				return KickEx(currIDspec[playerid]);
		 	}
		 	case 3:
	        {
                new ip[16];
	            GetPlayerIp(currIDspec[playerid], ip, 16);
				new str[78];
				if(PlayerInfo[playerid][pAdmin] <= 2) format(str, sizeof(str), "[SP] %s[%d]  |  PING %d", PlayerInfo[currIDspec[playerid]][pName], currIDspec[playerid], GetPlayerPing(currIDspec[playerid]));
				else format(str, sizeof(str), "[SP] %s[%d]  |  PING %d  |  IP %s", PlayerInfo[currIDspec[playerid]][pName], currIDspec[playerid], GetPlayerPing(currIDspec[playerid]), ip);
				SendClientMessage(playerid, 0x61DF8FAA, str);
				return ShowMenuForPlayer(spmenu, playerid);
		 	}
		 	case 4:
	        {
	            ShowPlayerStats(playerid, currIDspec[playerid]);
	            return ShowMenuForPlayer(spmenu, playerid);
		 	}
		 	case 5:
	        {
				new str[3];
				format(str, sizeof(str), "%d", currIDspec[playerid]);
				return cmd::sp(playerid, str);
		 	}
		 	case 6:
	        {
				return cmd::spoff(playerid);
		 	}
	    }
	}
	return 1;
}

public OnPlayerKeyStateChange(playerid, newkeys, oldkeys)
{
    if((newkeys & KEY_YES) && !(oldkeys & KEY_YES)) return cmd::yes(playerid);
    if((newkeys & KEY_SPRINT) && !(oldkeys & KEY_SPRINT) && GetPVarInt(playerid, "WasAnim") == 1)
	{
	    ClearAnimations(playerid);
	    DeletePVar(playerid, "WasAnim");
		return TextDrawHideForPlayer(playerid, TD_AnimStop);
	}
    if((newkeys & KEY_NO) && !(oldkeys & KEY_NO)) return cmd::no(playerid);
    if((newkeys & KEY_ACTION ) && !(oldkeys & KEY_ACTION ) && IsPlayerInAnyVehicle(playerid)) return cmd::e(playerid);
    if((newkeys & KEY_ANALOG_LEFT ) && !(oldkeys & KEY_ANALOG_LEFT ) && IsPlayerInAnyVehicle(playerid)) return cmd::sl(playerid);
    if((newkeys & KEY_FIRE ) && !(oldkeys &  KEY_FIRE ) && IsPlayerInAnyVehicle(playerid)) return cmd::l(playerid);
    if((newkeys & KEY_ACTION ) && !(oldkeys & KEY_ACTION ) && IsPlayerInAnyVehicle(playerid)) return cmd::e(playerid);
	return 1;
}

public OnPlayerClickTextDraw(playerid, Text:clickedid)
{
	if(_:clickedid == INVALID_TEXT_DRAW)
	{
	    if(Curr_TD[playerid] != 0) return SelectTextDraw(playerid, COLOR_GREY);
	}
    if(clickedid == TD_ChooseGang[0])
    {
        counter_skin[playerid] = 0;
        SetPlayerSkin(playerid, skinsgrove[counter_skin[playerid]]);
        return PlayerInfo[playerid][pGang] = GANG_GROVE;
    }
    if(clickedid == TD_ChooseGang[1])
    {
        counter_skin[playerid] = 0;
        SetPlayerSkin(playerid, skinsballas[counter_skin[playerid]]);
        return PlayerInfo[playerid][pGang] = GANG_BALLAS;
    }
    if(clickedid == TD_ChooseGang[2])
    {
        counter_skin[playerid] = 0;
        SetPlayerSkin(playerid, skinsvagos[counter_skin[playerid]]);
        return PlayerInfo[playerid][pGang] = GANG_VAGOS;
    }
    if(clickedid == TD_ChooseGang[3])
    {
        counter_skin[playerid] = 0;
        SetPlayerSkin(playerid, skinsaztecas[counter_skin[playerid]]);
        return PlayerInfo[playerid][pGang] = GANG_AZTECAS;
    }
    if(clickedid == TD_ChooseGang[4])
    {
        counter_skin[playerid] = 0;
        SetPlayerSkin(playerid, skinsrifa[counter_skin[playerid]]);
        return PlayerInfo[playerid][pGang] = GANG_RIFA;
    }
    if(clickedid == TD_ChooseGang[6])
	{
		switch(PlayerInfo[playerid][pGang])
		{
			case GANG_GROVE: return SetPrevSkin(playerid, GANG_GROVE);
			case GANG_BALLAS: return SetPrevSkin(playerid, GANG_BALLAS);
			case GANG_VAGOS: return SetPrevSkin(playerid, GANG_VAGOS);
			case GANG_AZTECAS: return SetPrevSkin(playerid, GANG_AZTECAS);
			case GANG_RIFA: return SetPrevSkin(playerid, GANG_RIFA);
		}
	}
	if(clickedid == TD_ChooseGang[7])
	{
		switch(PlayerInfo[playerid][pGang])
		{
			case GANG_GROVE: return SetNextSkin(playerid, GANG_GROVE);
			case GANG_BALLAS: return SetNextSkin(playerid, GANG_BALLAS);
			case GANG_VAGOS: return SetNextSkin(playerid, GANG_VAGOS);
			case GANG_AZTECAS: return SetNextSkin(playerid, GANG_AZTECAS);
			case GANG_RIFA: return SetNextSkin(playerid, GANG_RIFA);
		}
	}
	if(clickedid == TD_ChooseGang[8])
	{
		for(new i = 0; i != 10; i++) TextDrawHideForPlayer(playerid, TD_ChooseGang[i]);
		SpawnPlayer(playerid);
		TogglePlayerControllable(playerid, true);
		CancelSelectTextDraw(playerid);
		SetPlayerInterior(playerid, 0);
		SetPlayerVirtualWorld(playerid, 0);
	}
	if(clickedid == TD_Pin[0])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "0");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[1])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "1");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[2])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "2");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[3])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "3");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[4])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "4");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[5])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "5");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[6])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "6");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[7])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "7");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[8])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "8");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
	if(clickedid == TD_Pin[9])
	{
	    PlayerPlaySound(playerid, 4203, 0.0, 0.0, 0.0);
		strcat(tempPIN[playerid], "9");
		if(strlen(tempPIN[playerid]) == 4)
		{
		    if(typePIN{playerid} == 1) return CheckForCorrectPin(playerid, 1);
		    if(typePIN{playerid} == 2) return CheckForCorrectPin(playerid, 2);
		    if(typePIN{playerid} == 3) return CheckForCorrectPin(playerid, 3);
		}
	}
    return 1;
}

public OnPlayerEnterDynamicCP(playerid, checkpointid)
{
	if(checkpointid == warehouse_cp[0]) return ShowPlayerWarehouse(playerid);
	if(checkpointid == warehouse_cp[1]) return ShowPlayerWarehouse(playerid);
	if(checkpointid == warehouse_cp[2]) return ShowPlayerWarehouse(playerid);
	if(checkpointid == warehouse_cp[3]) return ShowPlayerWarehouse(playerid);
	if(checkpointid == warehouse_cp[4]) return ShowPlayerWarehouse(playerid);
	return true;
}

public OnPlayerUpdate(playerid)
{
	PlayerInfo[playerid][pAFK] = 0;
	return 1;
}

public OnDialogResponse(playerid, dialogid, response, listitem, inputtext[])
{
	switch(dialogid)
	{
	    case dAnimPlayer:
	    {
	        if(response) return SelectPlayerAnimation(playerid, listitem);
        	else return true;
		}
	    case dWarning:
	    {
	        if(response) return ShowPlayerRegister(playerid);
	        else return ShowPlayerRegister(playerid);
	    }
     	case dReg:
	    {
	        if(response)
	        {
	            if(!strlen(inputtext)) return ShowPlayerRegister(playerid);
	        	if(strlen(inputtext) > 32 || strlen(inputtext) < 6) return ShowPlayerWarning(playerid);
	        	for (new i, l = strlen(inputtext); i != l; i++ )
				{
					switch(inputtext[i])
                    {
                    	case '\'': return ShowPlayerWarning(playerid);
                    }
				}
                CreateAccount(playerid, inputtext);
	        }
	        else
	        {
	            SendClientMessage(playerid, COLOR_ORANGE, "Введите /q (/quit) чтобы выйти");
				return KickEx(playerid);
	        }
	    }
	    case dAuth:
	    {
	        if(response)
	        {
	            if(!strlen(inputtext)) return ShowPlayerAuth(playerid, -1);
	            if(!strcmp(PlayerInfo[playerid][pPassword], inputtext, false))
	            {
					new query[128];
					mysql_format(mysql_connection, query, sizeof(query), "SELECT `name`, `nameadm`, `date`, `reason`, `daystounban` FROM `bans` WHERE name='%s'", PlayerInfo[playerid][pName]);
					return mysql_tquery(mysql_connection, query, "OnCheckForBan", "d", playerid);
	            }
	            else
				{
					SetPVarInt(playerid,"WrongPassword",GetPVarInt(playerid, "WrongPassword")+1);
					if(GetPVarInt(playerid, "WrongPassword") == 3) SendClientMessage(playerid, COLOR_ORANGE, "При неправильном вводе пароля Вы будете исключены из игры");
					if(GetPVarInt(playerid, "WrongPassword") > 3)
					{
						ShowPlayerDialog(playerid, dWarning, DIALOG_STYLE_MSGBOX, "{FF9933}Лимит попыток авторизации", "{ffffff}Вы ввели неправильный пароль 3 раза подряд. Вы были исключены из игры", "Закрыть", "");
						KickEx(playerid);
						return true;
					}
					ShowPlayerAuth(playerid, 4-GetPVarInt(playerid, "WrongPassword"));
					return PlayerPlaySound(playerid, 1053, 0.0, 0.0, 0.0);
				}
	        }
	        else
	        {
	            SendClientMessage(playerid, COLOR_ORANGE, "Введите /q (/quit) чтобы выйти");
				return KickEx(playerid);
	        }
	    }
	    case dWarehouse:
	    {
	        if(response)
	        {
	            switch(listitem)
	            {
	                case 0:
	                {
	                    if(PlayerInfo[playerid][pAid] >= 1)
						{
						    ShowPlayerWarehouse(playerid);
						    return SendClientMessage(playerid, COLOR_GREY, "У Вас уже есть аптечки");
						}
						if(PlayerInfo[playerid][pVip] == 1) PlayerInfo[playerid][pAid] += 4;
	                    else PlayerInfo[playerid][pAid] += 2;
                        ShowPlayerWarehouse(playerid);
                        SendClientMessage(playerid, COLOR_GREEN, "Вы взяли набор аптечек. Введите {3399FF}/healme{66CC00} для их использования");
                        new str[96];
                        format(str, sizeof(str), "Текущее количество аптечек: {6699FF}%d шт.", PlayerInfo[playerid][pAid]);
                        return SendClientMessage(playerid, COLOR_ROSE, str);
	                }
	                case 1:
	                {
	                    if(PlayerInfo[playerid][pMask] >= 1 || PlayerInfo[playerid][pMaskTime] >= 1)
						{
						    ShowPlayerWarehouse(playerid);
						    return SendClientMessage(playerid, COLOR_GREY, "У Вас уже есть маска");
						}
						if(PlayerInfo[playerid][pVip] == 1) PlayerInfo[playerid][pMask] += 2;
	                    else PlayerInfo[playerid][pMask] += 1;
	                    ShowPlayerWarehouse(playerid);
	                    SendClientMessage(playerid, COLOR_GREEN, "Вы взяли маску");
	                    SendClientMessage(playerid, COLOR_GREEN, "Используйте {FFCD00}/mask{66CC00} для скрытия Вашего расположения на карте (на 10 минут)");
	                    new str[96];
	                    format(str, sizeof(str), "Сейчас у Вас масок: {33CC33}%d шт.", PlayerInfo[playerid][pMask]);
	                    return SendClientMessage(playerid, COLOR_ROSE, str);
	                }
	                case 2: return ShowPlayerWeapons(playerid);
	            }
	        }
	        else return true;
	    }
	    case dWeapons:
	    {
	        if(response)
			{
				switch(listitem)
				{
				    case 0:
				    {
				        GivePlayerWeapon(playerid, 24, 250);
				        GivePlayerWeapon(playerid, 31, 400);
				        SendClientMessage(playerid, COLOR_BLUE, "Вы взяли Desert Eagle и M4");
				        return ShowPlayerWeapons(playerid);
				    }
				    case 1:
				    {
				        GivePlayerWeapon(playerid, 24, 250);
				        GivePlayerWeapon(playerid, 30, 400);
				        SendClientMessage(playerid, COLOR_BLUE, "Вы взяли Desert Eagle и AK-47");
				        return ShowPlayerWeapons(playerid);
				    }
				    case 2:
				    {
				        GivePlayerWeapon(playerid, 24, 250);
				        GivePlayerWeapon(playerid, 25, 400);
				        SendClientMessage(playerid, COLOR_BLUE, "Вы взяли Desert Eagle и ShotGun");
				        return ShowPlayerWeapons(playerid);
				    }
				    case 3:
				    {
				        GivePlayerWeapon(playerid, 24, 250);
				        GivePlayerWeapon(playerid, 34, 400);
				        SendClientMessage(playerid, COLOR_BLUE, "Вы взяли Desert Eagle и Sniper Rifle");
				        return ShowPlayerWeapons(playerid);
				    }
				}
			}
			else return ShowPlayerWarehouse(playerid);
	    }
	    case dMn:
	    {
	        if(response)
	        {
	            switch(listitem)
	            {
	                case 0: return ShowPlayerStats(playerid, playerid);
	                case 1:
					{
						SendClientMessage(playerid, 0xCCCC33AA, "Общие команды:  /mn  /newband  /arena  /pm  /togpm  /tp  /back");
						SendClientMessage(playerid, 0xCCCC33AA, "Общие команды:  /capture  /pvp");
						SendClientMessage(playerid, 0xCCCC33AA, "Комнаты:  /createroom  /rooms  /editroom");
						return cmd::mn(playerid, "");
					}
	                case 2: return ShowPersonalSettings(playerid);
	                case 3: return ShowGuardSettings(playerid);
	                case 4: return ShowPlayerDialog(playerid, dReport, DIALOG_STYLE_INPUT, "{FFCD00}Связь с администрацией", "{ffffff}Введите своё сообщение для администрации сервера\n\
					Оно должно быть кратким и ясным\n\n\
	                {66CC66}Если вы хотите подать жалобу на игрока,\n\
	                обязательно укажите его ID и причину жалобы", "Отправить", "Назад");
	                case 5: return ShowDonateMenu(playerid);


	            }
	        }
	        else return true;
	    }
	    case dPersSettings:
	    {
	        if(response)
	        {
	            switch(listitem)
	            {
					case 0:
					{
					    if(PlayerInfo[playerid][pTypeChat] == 0)
					    {
					        PlayerInfo[playerid][pTypeChat]++;
					        return ShowPersonalSettings(playerid);
					    }
					    if(PlayerInfo[playerid][pTypeChat] == 1)
					    {
					        PlayerInfo[playerid][pTypeChat]++;
					        return ShowPersonalSettings(playerid);
					    }
					    if(PlayerInfo[playerid][pTypeChat] == 2)
					    {
					        PlayerInfo[playerid][pTypeChat] = 0;
					        return ShowPersonalSettings(playerid);
					    }
					}
					case 1:
					{
					    if(PlayerInfo[playerid][pChatGang] == 0)
					    {
					        PlayerInfo[playerid][pChatGang]++;
					        return ShowPersonalSettings(playerid);
					    }
					    if(PlayerInfo[playerid][pChatGang] == 1)
					    {
					        PlayerInfo[playerid][pChatGang]--;
					        return ShowPersonalSettings(playerid);
					    }
					}
					/*case 2:
					{
					    if(PlayerInfo[playerid][pShowNicks] == 0)
					    {
					        PlayerInfo[playerid][pShowNicks]++;
					        foreach(new i:Player) ShowPlayerNameTagForPlayer(playerid, i, true);
					        return ShowPersonalSettings(playerid);
					    }
					    if(PlayerInfo[playerid][pShowNicks] == 1)
					    {
					        PlayerInfo[playerid][pShowNicks]--;
					        foreach(new i:Player) ShowPlayerNameTagForPlayer(playerid, i, false);
					        return ShowPersonalSettings(playerid);
					    }
					}*/
					case 2:
					{
					    if(PlayerInfo[playerid][pGangOnline] == 0)
					    {
					        PlayerInfo[playerid][pGangOnline]++;
					        return ShowPersonalSettings(playerid);
					    }
					    if(PlayerInfo[playerid][pGangOnline] == 1)
					    {
					        PlayerInfo[playerid][pGangOnline]--;
					        return ShowPersonalSettings(playerid);
					    }
					}
					case 3:
					{
					    ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{FFCD00}Сохранено", "{ffffff}Новые настройки будут устанавливаться после каждой авторизации", "Ок", "");
					    new query[128];
					    mysql_format(mysql_connection, query, sizeof(query), "UPDATE `accounts` SET `nicks`=%i,`gchat`=%i,`typechat`=%i, `gangonline`=%i WHERE name='%s'", PlayerInfo[playerid][pShowNicks], PlayerInfo[playerid][pChatGang], PlayerInfo[playerid][pTypeChat], PlayerInfo[playerid][pGangOnline], PlayerInfo[playerid][pName]);
					    mysql_tquery(mysql_connection, query, "", "");
					}
	            }
	        }
	        else return cmd::mn(playerid, "");
	    }
	    case dGuardSettings:
	    {
	        if(response)
			{
			    switch(listitem)
			    {
			        case 0:
			        {
			            new test[386] = "\
						{ffffff}Для продолжения, вам необходимо придумать и набрать 4-х значный код.\n\
						\n\
						Эта система безопасности поможет защитить Ваш аккаунт, если на\n\
						компьютер попадёт вирус-кейлоггер, который перехватывает данные с\n\
						клавиатуры. Кнопки всегда располагаются в случайном порядке, что не даст\n\
						злоумышленникам возможность узнать ваш PIN-код.";
			            if(!strlen(PlayerInfo[playerid][pPin])) return ShowPlayerDialog(playerid, dConfPin, DIALOG_STYLE_MSGBOX, "{FFCD00}Случайный PIN-код", test, "Далее", "Назад");
			            else return ShowPlayerDialog(playerid, dChangeTypeAskPin, DIALOG_STYLE_LIST, "{FFCD00}При авторизации запрашивать PIN-код...", "Не запрашивать\nЕсли подсеть не совпадает с моей\nЕсли IP не совпадает с моим", "Сохранить", "Назад");
			        }
			        case 1: return ShowPlayerDialog(playerid, dConfPass, DIALOG_STYLE_INPUT, "{FFCD00}Изменение пароля", "{ffffff}Введите Ваш текущий пароль в поле ниже:", "Далее", "Назад");
			        case 2:
			        {
			            new test[386] = "\
						{ffffff}Для продолжения, вам необходимо придумать и набрать 4-х значный код.\n\
						\n\
						Эта система безопасности поможет защитить Ваш аккаунт, если на\n\
						компьютер попадёт вирус-кейлоггер, который перехватывает данные с\n\
						клавиатуры. Кнопки всегда располагаются в случайном порядке, что не даст\n\
						злоумышленникам возможность узнать ваш PIN-код.";
		   				if(!strlen(PlayerInfo[playerid][pPin])) return ShowPlayerDialog(playerid, dConfPin, DIALOG_STYLE_MSGBOX, "{FFCD00}Случайный PIN-код", test, "Далее", "Назад");
			            ShowPlayerPin(playerid);
						typePIN{playerid} = 3;
						return SendClientMessage(playerid, COLOR_YELLOW, "Наберите Ваш текущий PIN-код");
			        }
			        case 3:
			        {
						new str[312] = "{ffffff}Тут вы можете увидеть статус всех Ваших настроек безопасности.\n\
						Для их изменения, выберите нужный пункт в меню настроек\n\n";
						if(PlayerInfo[playerid][pAskForPin] == 1) strcat(str, "PIN-код:\t\t\t{CC9900}Не запрашивается");
						if(PlayerInfo[playerid][pAskForPin] == 2) strcat(str, "PIN-код:\t\t\t{3399FF}Запрашивается при несовпадении подсети");
						if(PlayerInfo[playerid][pAskForPin] == 3) strcat(str, "PIN-код:\t\t\t{009900}Запрашивается при несовпадении IP");
						ShowPlayerDialog(playerid, dBackEndStatusSett, DIALOG_STYLE_MSGBOX, "{FFCD00}Статус безопасности", str, "Назад", "");
			        }
			    }
			}
			else return cmd::mn(playerid, "");
	    }
	    case dBackEndStatusSett:
	    {
	        if(response) return ShowGuardSettings(playerid);
	        else return ShowGuardSettings(playerid);
	    }
	    case dConfPass:
	    {
	        if(response)
	        {
	            if(!strcmp(PlayerInfo[playerid][pPassword], inputtext, false)) return ShowPlayerDialog(playerid, dNewPass, DIALOG_STYLE_INPUT, "{FFCD00}Новый пароль", "{ffffff}Введите новый пароль в поле ниже:", "Изменить", "Отмена");
	            else
	            {
	                SendClientMessage(playerid, COLOR_ORANGE, "Вы ввели неверный пароль");
	                return ShowGuardSettings(playerid);
	            }
	        }
	        else return ShowGuardSettings(playerid);
	    }
	    case dNewPass:
	    {
	        if(response)
	        {
	            PlayerInfo[playerid][pPassword][0] = EOS;
	            strins(PlayerInfo[playerid][pPassword], inputtext, 0);
	            new query[128];
	            mysql_format(mysql_connection, query, sizeof(query), "UPDATE `accounts` SET ,`password`='%s' WHERE name='%s'", PlayerInfo[playerid][pPassword], PlayerInfo[playerid][pName]);
	            mysql_tquery(mysql_connection, query, "", "");
				new str[1] = EOS;
				SendClientMessage(playerid, COLOR_WHITE, str);
				format(query, sizeof(query), "Ваш новый пароль: {3399FF}%s", PlayerInfo[playerid][pPassword]);
				SendClientMessage(playerid, COLOR_YELLOW, query);
				SendClientMessage(playerid, COLOR_WHITE, "Рекомендуем сделать скрин{00CC00} (клавиша F8) {ffffff}чтобы не забыть его");
	        }
	        else return ShowGuardSettings(playerid);
	    }
	    case dConfPin:
	    {
	        if(response)
	        {
				ShowPlayerPin(playerid);
				typePIN{playerid} = 1;
				return SendClientMessage(playerid, COLOR_BLUE, "Придумайте свой PIN-код и наберите его");
			}
	        else return ShowGuardSettings(playerid);
	    }
	    case dChangeTypeAskPin:
	    {
	        if(response)
	        {
	            new str[96];
				switch(listitem)
				{
				    case 0:
				    {
						mysql_format(mysql_connection, str, sizeof(str), "UPDATE `accounts` SET `typepin`=1 WHERE name='%s'", PlayerInfo[playerid][pName]);
						mysql_tquery(mysql_connection, str, "", "");
						PlayerInfo[playerid][pAskForPin] = 1;
						SendClientMessage(playerid, COLOR_ORANGE, "Запрос случайного PIN-кода отключён");
						SendClientMessage(playerid, COLOR_WHITE, "Изменения в настройках безопасности {00FFCC}сохранены");
						return ShowGuardSettings(playerid);
				    }
				    case 1:
				    {
						mysql_format(mysql_connection, str, sizeof(str), "UPDATE `accounts` SET `typepin`=2 WHERE name='%s'", PlayerInfo[playerid][pName]);
						mysql_tquery(mysql_connection, str, "", "");
						PlayerInfo[playerid][pAskForPin] = 2;
						SendClientMessage(playerid, COLOR_YELLOW, "Ваш случайный PIN-код будет запрашиваться при несовпадении подсети");
						SendClientMessage(playerid, COLOR_WHITE, "Изменения в настройках безопасности {00FFCC}сохранены");
						return ShowGuardSettings(playerid);
				    }
				    case 2:
				    {
						mysql_format(mysql_connection, str, sizeof(str), "UPDATE `accounts` SET `typepin`=3 WHERE name='%s'", PlayerInfo[playerid][pName]);
						mysql_tquery(mysql_connection, str, "", "");
						PlayerInfo[playerid][pAskForPin] = 3;
						SendClientMessage(playerid, COLOR_GREEN, "Случайный PIN-код будет запрашиваться при несовпадении IP адресов");
						SendClientMessage(playerid, COLOR_WHITE, "Изменения в настройках безопасности {00FFCC}сохранены");
						return ShowGuardSettings(playerid);
				    }
				}
			}
	        else return ShowGuardSettings(playerid);
	    }
	    case dReport:
	    {
	        if(response)
	        {
	            //if(!strval(inputtext)) return ShowPlayerDialog(playerid, dNoActions,
	            new str[144];
				format(str, sizeof(str), "%s[%d] : {FFCD00}%s", PlayerInfo[playerid][pName], playerid, inputtext);
				SendClientMessage(playerid, COLOR_GREEN, str);
				SendClientMessage(playerid, COLOR_WHITE, "Ваше сообщение отправлено");
				SendAdminMessage(COLOR_GREEN, str, 1);
	        }
	        else return cmd::mn(playerid, "");
	    }
	    case dTP:
	    {
	        if(response)
	        {
				SendClientMessage(playerid, 0x66CCFFAA, "Вы были доставлены на место проведения мероприятия");
				SendClientMessage(playerid, 0x66CCFFAA, "Чтобы вернуться обратно, введите {FF9900}/back");
				SetPlayerPos(playerid, settp[0], settp[1], settp[2]);
				SetPlayerVirtualWorld(playerid, tp_info[0]);
				SetPlayerInterior(playerid, tp_info[1]);
				ResetPlayerWeapons(playerid);
				return wasTP{playerid} = 1;
	        }
			else return true;
	    }
	    case dDonateMenu:
	    {
	        if(response) return ShowDonateSubMenu(playerid);
			else return cmd::mn(playerid, "");
	    }
	    case dDonateSubMenu:
	    {
	        if(response)
	        {
	            switch(listitem)
	            {
	                case 0:
					{
					    new str[120];
	                	mysql_format(mysql_connection, str, sizeof(str), "SELECT * FROM lastdonates WHERE name='%s' ORDER BY date LIMIT 0, 20", PlayerInfo[playerid][pName]);
	                	return mysql_tquery(mysql_connection, str, "OnLastDonatesLoaded", "d", playerid);
					}
					case 1: return ShowPlayerDialog(playerid, dConvertKills, DIALOG_STYLE_INPUT, "{ffdd00}Обмен убийств (конвертер)", "\
					{ffffff}Ставка:\t\t\t1 руб. = 2 убийства\n\
					Кол-во рублей:\t0.00\n\
					Будет зачислено:\t0 убийств\n\n\
					Введите количество рублей, которые Вы\n\
					хотите конвертировать в игровые убийства", "Далее", "Назад");
					case 2: return ShowPlayerDialog(playerid, dChangeName, DIALOG_STYLE_INPUT, "{ffdd00}Изменение имени", "{ffffff}Введите новое имя в поле ниже:", "Далее", "Назад");
					case 3: return ShowPlayerDialog(playerid, dVipAccept, DIALOG_STYLE_MSGBOX, "{ffdd00}Покупка VIP", "{ffffff}Вы действительно хотите приобрести VIP статус?\nДанная услуга стоит{66A3FF} 65.00 руб.", "Купить", "Назад");
					case 4: return ShowPlayerDialog(playerid, dAdmAccept, DIALOG_STYLE_MSGBOX, "{ffdd00}Покупка прав администратора", "{ffffff}Вы действительно хотите приобрести права администратора 1 уровня?\nДанная услуга стоит{66A3FF} 100.00 руб.", "Купить", "Назад");
	            }
	        }
	        else return true;
	    }
	    case dVipAccept:
	    {
	        if(response)
	        {
	            if(PlayerInfo[playerid][pDonate] < 65) return SendClientMessage(playerid, COLOR_WHITE, "Для покупки VIP статуса необходимо иметь на счету {669933}65.00 руб.");
	            new str[128];
	            mysql_format(mysql_connection, str, sizeof(str), "UPDATE `acccounts` SET `vip` = 1 WHERE `name` = '%s'", PlayerInfo[playerid][pName]);
	            mysql_tquery(mysql_connection, str, "", "");
	            PlayerInfo[playerid][pVip] = 1;
	            ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{83c21b}VIP статус", "{ffffff}Советуем посмотреть список команд ({ffdd00}/vhelp{ffffff})", "Ок", "");
	            PlayerInfo[playerid][pDonate] -= 65;
	            GameTextForPlayer(playerid, "~b~+ VIP~n~~y~-65 RUB.", 4500, 1);
	            return PlayerPlaySound(playerid, 1149, 0.0, 0.0, 0.0);
	        }
	        else return ShowDonateSubMenu(playerid);
	    }
	    case dAdmAccept:
	    {
	        if(response)
	        {
	            if(PlayerInfo[playerid][pDonate] < 100) return SendClientMessage(playerid, COLOR_WHITE, "Для покупки прав администратора необходимо иметь на счету {669933}100.00 руб.");
	            new str[128];
	            mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `newadm`(`name`, `level`) VALUES ('%s', 1)", PlayerInfo[playerid][pName]);
	            mysql_tquery(mysql_connection, str, "", "");
	            ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{83c21b}Права администратора", "{ffffff}Для получения прав администратора 1 уровня используйте {ffdd00}/adm\n{ffffff}Советуем посмотреть список команд ({ffdd00}/ahelp{ffffff})", "Ок", "");
	            PlayerInfo[playerid][pDonate] -= 100;
	            GameTextForPlayer(playerid, "~b~+ ADMIN~n~~y~-100 RUB.", 4500, 1);
	            return PlayerPlaySound(playerid, 1139, 0.0, 0.0, 0.0);
	        }
	        else return ShowDonateSubMenu(playerid);
	    }
	    case dConvertKills:
	    {
	        if(response)
	        {
	            new val = strval(inputtext);
	            if(!strlen(inputtext))
	            {
	                new converted = GetPVarInt(playerid, "convert");
	                if(converted == 0)
	                {
	                    SendClientMessage(playerid, COLOR_ORANGE, "Вы не указали сумму");
	                    return ShowPlayerDialog(playerid, dConvertKills, DIALOG_STYLE_INPUT, "{ffdd00}Обмен убийств (конвертер)", "\
						{ffffff}Ставка:\t\t\t1 руб. = 2 убийства\n\
						Кол-во рублей:\t0.00\n\
						Будет зачислено:\t0 убийств\n\n\
						{FF9966}Введите количество рублей, которые Вы\n\
						хотите конвертировать в игровые убийства", "Далее", "Назад");
	                }
	                new str[86];
	                format(str, sizeof(str), "Вы сконвертировали {66CC00}%d.00 руб.{ffff00} в {66cc00}%d убийств", converted, converted*2);
	                SendClientMessage(playerid, 0xFFFF00AA, str);
	                format(str, sizeof(str), "~b~+%d KILLS~n~~y~-%d RUB.", converted*2, converted);
	                GameTextForPlayer(playerid, str, 4500, 1);
	                PlayerPlaySound(playerid, 1052, 0.0, 0.0, 0.0);
					PlayerInfo[playerid][pKills] += converted*2;
					PlayerInfo[playerid][pDonate] -= converted;
					SetPlayerScore(playerid, PlayerInfo[playerid][pKills]);
	                return DeletePVar(playerid, "convert");
				}
				else
				{
				    if(val < 1)
					{
					    SendClientMessage(playerid, COLOR_ORANGE, "Введена ошибочная сумма, либо она меньше 1 руб.");
				        ShowPlayerDialog(playerid, dConvertKills, DIALOG_STYLE_INPUT, "{ffdd00}Обмен убийств (конвертер)", "\
						{ffffff}Ставка:\t\t\t1 руб. = 2 убийства\n\
						Кол-во рублей:\t0.00\n\
						Будет зачислено:\t0 убийств\n\n\
						{00E6AC}Введите количество рублей, которые Вы\n\
						хотите конвертировать в игровые убийства", "Далее", "Назад");
						return DeletePVar(playerid, "convert");
					}
				    new str[249];
				    if(val > PlayerInfo[playerid][pDonate])
				    {
						format(str, sizeof(str), "Недостаточно средств. Сейчас на Вашем счету {00E6AC}%d.00 руб.", PlayerInfo[playerid][pDonate]);
						SendClientMessage(playerid, COLOR_ORANGE, str);
				        ShowPlayerDialog(playerid, dConvertKills, DIALOG_STYLE_INPUT, "{ffdd00}Обмен убийств (конвертер)", "\
						{ffffff}Ставка:\t\t\t1 руб. = 2 убийства\n\
						Кол-во рублей:\t0.00\n\
						Будет зачислено:\t0 убийств\n\n\
						{00E6AC}Введите количество рублей, которые Вы\n\
						хотите конвертировать в игровые убийства", "Далее", "Назад");
						return DeletePVar(playerid, "convert");
				    }
				    format(str, sizeof(str), "\
					{ffffff}Ставка:\t\t\t1 руб. = 2 убийства\n\
					Кол-во рублей:\t%d.00\n\
					Будет зачислено:\t%d убийств\n\n\
					Для изменения суммы, укажите новое\n\
					значение и нажмите \"Обновить\"\n\n\
					{66A3FF}Чтобы зачислать выбранную сумму, оставьте\n\
					поле пустым и нажмите \"Обновить\"", val, val*2);
					ShowPlayerDialog(playerid, dConvertKills, DIALOG_STYLE_INPUT, "{ffdd00}Обмен убийств (конвертер)", str, "Обновить", "Назад");
					SetPVarInt(playerid, "convert", val);
				}
	        }
	        else return ShowDonateSubMenu(playerid);
	    }
	    case dChangeName:
	    {
	        if(response)
	        {
	            if(PlayerInfo[playerid][pDonate] < 8) return SendClientMessage(playerid, COLOR_WHITE, "Для изменении имени необходимо иметь на счету {669933}8.00 руб.");
				new str[96];
                mysql_format(mysql_connection, str, sizeof(str), "SELECT `name` FROM `accounts` WHERE `name`='%s'", inputtext);
                mysql_tquery(mysql_connection, str, "CheckName", "ds", playerid, inputtext);
	        }
	        else return ShowDonateSubMenu(playerid);
	    }
	    case dAllDonates:
	    {
	        if(response) return ShowDonateSubMenu(playerid);
	        else return ShowDonateSubMenu(playerid);
	    }
	    case dCapture:
	    {
	        if(response)
	        {
	            if(capture == 1) return SendClientMessage(playerid, COLOR_LGREY, "Уже происходит захват одной из зон. Дождитесь окончания");
	            GetPlayer2DZone(playerid, zone_name, MAX_ZONE_NAME);
				new Float:x = (ZoneInfo[zoneid_capture][gCoords][0]+ZoneInfo[zoneid_capture][gCoords][2])/2.0;
				new Float:y = (ZoneInfo[zoneid_capture][gCoords][1]+ZoneInfo[zoneid_capture][gCoords][3])/2.0;
				new Float:z = 0;
				new str[48];
				GangZoneFlashForAll(zoneid_capture, GetGZColor(PlayerInfo[playerid][pGang]));
				StartCapture(PlayerInfo[playerid][pGang], ZoneInfo[zoneid_capture][gGang]);
				capture = 1;
				format(str, sizeof(str), "%s[%d] инициировал захват", PlayerInfo[playerid][pName], playerid);
				SendClientMessageToAll(COLOR_ORANGE, str);
				foreach(new a: Player)
				{
				    if(PlayerInfo[a][pGang] != team_capture[0] || PlayerInfo[a][pGang] != team_capture[1]) continue;
					switch(PlayerInfo[playerid][pGang])
					{
						case 1: SetPlayerMapIcon(playerid, 31, x, y, z, 62, 0, MAPICON_GLOBAL);
						case 2: SetPlayerMapIcon(playerid, 31, x, y, z, 59, 0, MAPICON_GLOBAL);
						case 3: SetPlayerMapIcon(playerid, 31, x, y, z, 60, 0, MAPICON_GLOBAL);
						case 4: SetPlayerMapIcon(playerid, 31, x, y, z, 58, 0, MAPICON_GLOBAL);
						case 5: SetPlayerMapIcon(playerid, 31, x, y, z, 61, 0, MAPICON_GLOBAL);
					}
				}
	        }
	        else return true;
	    }
	    case dObjectNew:
	    {
	        if(response)
	        {
	            new Float:cX, Float:cY, Float:cZ;
	            GetPlayerPos(playerid, cX, cY, cZ);
             	lastobj = CreateObject(strval(inputtext), cX+1, cY, cZ, 0.0, 0.0, 0.0, 150.0);
	            return EditObject(playerid, lastobj);
	        }
	        else return true;
	    }
	    case dObjectEdit:
	    {
	        if(response)
	        {
	            switch(listitem)
	            {
	                case 0: return EditObject(playerid, currobj);
	                case 1:
	                {
	                    SendClientMessage(playerid, COLOR_GREEN, "Объект был успешно удалён");
	                    DestroyObject(currobj);
	                    CancelEdit(playerid);
	                    return currobj = -1;
	                }
	            }
	        }
	        else return true;
	    }
	    case dStyle:
	    {
	        if(response)
	        {
	            switch(listitem)
	            {
	                case 0: return SetPlayerFightingStyle(playerid, FIGHT_STYLE_NORMAL), SendClientMessage(playerid, 0x847BD8AA, "Стиль боя сменён на обычный");
		            case 1: return SetPlayerFightingStyle(playerid, FIGHT_STYLE_BOXING), SendClientMessage(playerid, 0x847BD8AA, "Стиль боя сменён на боксёрский");
		            case 2: return SetPlayerFightingStyle(playerid, FIGHT_STYLE_KUNGFU), SendClientMessage(playerid, 0x847BD8AA, "Стиль боя сменён на Кунг-Фу");
		            case 3: return SetPlayerFightingStyle(playerid, FIGHT_STYLE_KNEEHEAD), SendClientMessage(playerid, 0x847BD8AA, "Стиль боя сменён на Тэйк-Ван-До");
	            }
	        }
	        else return true;
	    }
	    case dArena:
	    {
	        if(response)
	        {
				PlayerInfo[playerid][pArena] = listitem+1;
				SendClientMessage(playerid, COLOR_YELLOW, "Для выхода из арены используйте {66cc00}/newband");
    			SetPlayerSpawnArena(playerid);
    			onlinearena[PlayerInfo[playerid][pArena]]++;
	        }
	        else return true;
	    }
	    case dRooms:
	    {
	        if(response)
	        {
	            currRoom[playerid] = roomids[listitem];
	            return ShowInfoAboutRoom(playerid, currRoom[playerid]);
	        }
	        else return true;
	    }
	    case dRoomInfo:
	    {
	        if(response)
	        {
	            if(RoomInfo[currRoom[playerid]][rClosed] == 1) return ShowPlayerDialog(playerid, dRoomEnterPass, DIALOG_STYLE_INPUT, "{ffdd00}Ввод пароля", "{ffffff}Данная комната закрыта\nВведите пароль в поле ниже:", "Войти", "Отмена");
	            PlayerInfo[playerid][pRoom] = currRoom[playerid];
				SendClientMessage(playerid, COLOR_YELLOW, "Для выхода из комнаты используйте {66cc00}/newband");
    			SetPlayerSpawnRoom(playerid);
    			return RoomInfo[currRoom[playerid]][rOnline]++;
	        }
	        else return cmd::rooms(playerid);
	    }
	    case dRoomEnterPass:
	    {
	        if(response)
	        {
	            if(strval(inputtext) == RoomInfo[currRoom[playerid]][rPassword])
	            {
	                PlayerInfo[playerid][pRoom] = currRoom[playerid];
					SendClientMessage(playerid, COLOR_YELLOW, "Для выхода из комнаты используйте {66cc00}/newband");
	    			SetPlayerSpawnRoom(playerid);
	    			return RoomInfo[currRoom[playerid]][rOnline]++;
	            }
				else return ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{ff6600}Ошибка", "{ffffff}Пароль был введён неверно.", "Закрыть", "");
	        }
	        else
	        {
	            ShowInfoAboutRoom(playerid, currRoom[playerid]);
	            return currRoom[playerid] = roomids[listitem];
	        }
	    }
	    case dRoomEdit:
	    {
	        if(response)
	        {
	            switch(listitem)
	            {
	                case 0:
	                {
	                    if(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rClosed] == 0) return ShowPlayerDialog(playerid, dRoomPassword, DIALOG_STYLE_INPUT, "{ffdd00}Пароль комнаты", "{ffffff}Введите желаемый пароль (из цифр) в поле ниже:", "Далее", "Отмена");
						if(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rClosed] == 1)
						{
						    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rClosed] = 0;
						    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rPassword] = 0;
						    return cmd::editroom(playerid);
						}
	                }
	                case 1:
	                {
	                    if(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rClosed] == 0) return ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{FF6600}Ошибка", "{ffffff}Для изменения пароля необходимо сделать комнату закрытой", "Ок", "");
	                    return ShowPlayerDialog(playerid, dRoomPassword, DIALOG_STYLE_INPUT, "{ffdd00}Пароль комнаты", "{ffffff}Введите желаемый пароль (из цифр) в поле ниже:", "Далее", "Отмена");
	                }
	                case 2: return ShowPlayerDialog(playerid, dRoomMap, DIALOG_STYLE_LIST, "{ffdd00}Карта комнаты", "{ffffff}1. Заброшеная деревня", "Выбрать", "Назад");
					case 3: return ShowDialogGunsRoom(playerid);
					case 4:
					{
					    if(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rClosed] == 1 && GetPVarInt(playerid, "ChangedPassword") == 1)
					    {
					        DeletePVar(playerid, "ChangedPassword");
             				foreach(new i:Player)
					        {
					            if(PlayerInfo[i][pRoom] == PlayerInfo[playerid][pRoomCreateID])
						        {
									PlayerInfo[i][pRoom] = -1;
									SendClientMessage(i, COLOR_YELLOW, "Создатель комнаты добавил пароль");
									RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rOnline] = 0;
									return cmd::newband(playerid, "");
						        }
					        }
					    }
					    else
					    {
					        foreach(new i:Player)
						    {
						        if(PlayerInfo[i][pRoom] == PlayerInfo[playerid][pRoomCreateID])
						        {
						            SetPlayerSpawnRoom(i);
									SendClientMessage(i, COLOR_YELLOW, "Создатель комнаты применил изменения настроек");
						        }
						    }
					    }
					}
					case 5:
	    			{
				        foreach(new i:Player)
				        {
            				if(PlayerInfo[i][pRoom] == PlayerInfo[playerid][pRoomCreateID])
           					{
				            	PlayerInfo[i][pRoom] = -1;
				            	SendClientMessage(i, COLOR_YELLOW, "Создатель комнаты удалил её. Все игроки были исключены");
								cmd::newband(i, "");
        					}
   						}
				        SendClientMessage(playerid, COLOR_GREEN, "Комната была успешно удалена");
   						DeleteRoom(PlayerInfo[playerid][pRoomCreateID]);
   						PlayerInfo[playerid][pRoomCreateID] = -1;
				        PlayerInfo[playerid][pRoom] = -1;
				        return DeletePVar(playerid, "ChangedPassword");
				    }
	            }
	        }
	        else return true;
	    }
	    case dRoomWeapons:
	    {
	        if(response)
	        {
	            SetPVarInt(playerid, "CurrSlotWeap", listitem);
	            return ShowPlayerDialog(playerid, dRoomListWeap, DIALOG_STYLE_TABLIST_HEADERS, "{ffdd00}Выбор оружия", "Оружие\tКол-во\n1. Нож\t1\n2. Бензопила\t1\n3. Граната\t10\n4. Desert Eagle\t250\n5. ShotGun\t100\n6. M4A1\t500\n7. Sniper Rifle\t100\n8. MiniGun\t2000\n9. Убрать оружие", "Выбрать", "Назад");
	        }
	        else return cmd::editroom(playerid);
	    }
	    case dWeapConf:
	    {
	        if(response)
	        {
	            if(GetPVarInt(playerid, "Knife") >= 1)
	            {
	                new currWeap = GetPVarInt(playerid, "Knife");
	                RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 4;
	                DeletePVar(playerid, "Knife");
           			DeletePVar(playerid, "Chainsaw");
	                return ShowDialogGunsRoom(playerid);
	            }
	            if(GetPVarInt(playerid, "Chainsaw") >= 1)
	            {
	                new currWeap = GetPVarInt(playerid, "Chainsaw");
	                RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 9;
	                DeletePVar(playerid, "Knife");
	            	DeletePVar(playerid, "Chainsaw");
	                return ShowDialogGunsRoom(playerid);
	            }
	        }
	        else
	        {
	            DeletePVar(playerid, "Knife");
	            DeletePVar(playerid, "Chainsaw");
	            return ShowDialogGunsRoom(playerid);
	        }
	    }
	    case dRoomListWeap:
	    {
	        if(response)
	        {
	            new currWeap = GetPVarInt(playerid, "CurrSlotWeap");
	            DeletePVar(playerid, "CurrSlotWeap");
	            switch(listitem)
	            {
	                case 0:
	                {
	                    for(new i = 0; i != 6; i++)
	                    {
	                        if(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][i] == 9)
							{
							    SetPVarInt(playerid, "Knife", currWeap);
								return ShowPlayerDialog(playerid, dWeapConf, DIALOG_STYLE_MSGBOX, "{FF6600}Подтверждение", "{ffffff}Данное оружие заменит бензопилу при выдаче оружия\nВы уверены, что хотите добавить нож?", "Да", "Нет");
							}
	                    }
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 4;
	                    return ShowDialogGunsRoom(playerid);
	                }
	                case 1:
	                {
	                    for(new i = 0; i != 6; i++)
	                    {
	                        if(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][i] == 4)
							{
							    SetPVarInt(playerid, "Chainsaw", currWeap);
								return ShowPlayerDialog(playerid, dWeapConf, DIALOG_STYLE_MSGBOX, "{FF6600}Подтверждение", "{ffffff}Данное оружие заменит нож при выдаче оружия\nВы уверены, что хотите добавить безопилу?", "Да", "Нет");
							}
	                    }
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 9;
	                    return ShowDialogGunsRoom(playerid);
	                }
	                case 2:
	                {
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 16;
	                    return ShowDialogGunsRoom(playerid);
	                }
	                case 3:
	                {
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 24;
	                    return ShowDialogGunsRoom(playerid);
	                }
	                case 4:
	                {
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 25;
	                    return ShowDialogGunsRoom(playerid);
	                }
	                case 5:
	                {
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 31;
	                    return ShowDialogGunsRoom(playerid);
	                }
	                case 6:
	                {
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 34;
	                    return ShowDialogGunsRoom(playerid);
	                }
	                case 7:
	                {
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 38;
	                    return ShowDialogGunsRoom(playerid);
	                }
	                case 8:
	                {
	                    RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][currWeap] = 0;
	                    return ShowDialogGunsRoom(playerid);
	                }
	            }
	        }
	        else return ShowDialogGunsRoom(playerid);
	    }
	    case dRoomMap:
	    {
			if(response)
			{
			    switch(listitem)
			    {
			        case 0: return RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rMap] = 1, cmd::editroom(playerid);
			    }
			}
			else return cmd::editroom(playerid);
	    }
	    case dRoomPassword:
	    {
	        if(response)
	        {
	            RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rPassword] = strval(inputtext);
	            RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rClosed] = 1;
	            SetPVarInt(playerid, "ChangedPassword", 1);
	            return cmd::editroom(playerid);
	        }
	        else return cmd::editroom(playerid);
	    }
	    case dActorNew:
	    {
	        if(response)
	        {
	            new Float:cX, Float:cY, Float:cZ;
	            GetPlayerPos(playerid, cX, cY, cZ);
	            for(new i = 0; i != sizeof(actorids); i++)
	            {
	                if(actorids[i] == -1)
	                {
	                    objectactor = CreateObject(1318, cX, cY+1, cZ, 0.0, 0.0, 0.0, 50.0);
	                    EditObject(playerid, objectactor);
	                    curractori = i;
	                    SetPVarInt(playerid, "SkinActor", strval(inputtext));
	                    typemove = 1;
	                    break;
	                }
	            }
	        }
	        else return true;
	    }
	    case dActorEdit:
	    {
	        if(response)
	        {
	            switch(listitem)
	            {
	                case 0:
	                {
	                    new Float:cX, Float:cY, Float:cZ;
          				GetActorPos(actorids[curractor], cX, cY, cZ);
	                 	objectactor = CreateObject(1318, cX, cY, cZ, 0.0, 0.0, 0.0, 50.0);
		                typemove = 2;
	                 	return EditObject(playerid, objectactor);
	                }
	                case 1: return ShowPlayerDialog(playerid, dActorSkin, DIALOG_STYLE_INPUT, "{ffdd00}Изменение скина", "{ffffff}Введите новый ID скина для актёра:", "Изменить", "Закрыть");
	                case 2: return ShowActorAnimList(playerid);
	                case 3:
	                {
	                   	Delete3DTextLabel(actor3d[curractor]);
	                   	return SendClientMessage(playerid, COLOR_GREEN, "Информация была успешно убрана. Для включения переместите актёра");
	                }
	                case 4:
	                {
	                    DestroyActor(actorids[curractor]);
	                   	actorids[curractor] = -1;
	                   	Delete3DTextLabel(actor3d[curractor]);
	                   	return SendClientMessage(playerid, COLOR_GREEN, "Актёр был успешно удалён");
	                }
	            }
	        }
	        else return true;
	    }
	    case dActorSkin:
	    {
	        if(response)
	        {
	            new str[64];
	            format(str, sizeof(str), "Установлен новый ID скина: %d", strval(inputtext));
	            SendClientMessage(playerid, COLOR_GREEN, str);
				new Float:aX, Float:aY, Float:aZ;
				new Float:fA;
				GetActorFacingAngle(actorids[curractor], fA);
				GetActorPos(actorids[curractor], aX, aY, aZ);
				DestroyActor(actorids[curractor]);
				actorids[curractor] = -1;
				actorids[curractor] = CreateActor(strval(inputtext), aX, aY, aZ, fA);
				return SetTimerEx("PreloadAnimLibActor", 2000, false, "d", actorids[curractor]);
	        }
	        else return true;
	    }
	    case dActorAnim:
	    {
	        if(response) SelectAnimation(actorids[curractor], listitem);
	        else return true;
	    }
	    case dPvp:
	    {
	        if(response)
	        {
         		SetPVarInt(offerID[playerid], "GunPVP", listitem);
         		new str[128];
         		format(str, sizeof(str), "Вы предложили %s дуэль на Desert Eagle", PlayerInfo[offerID[playerid]][pName]);
           		SendClientMessage(playerid, COLOR_BLUE, str);
             	format(str, sizeof(str), "%s предлагает вам дуэль на Desert Eagle", PlayerInfo[playerid][pName]);
             	SendClientMessage(offerID[playerid], COLOR_BLUE, str);
             	isOffered{offerID[playerid]} = 1;
				isOfferedTo{playerid} = 1;
				typeOffer{offerID[playerid]} = 1;
				offerID[offerID[playerid]] = playerid;
     			return SendClientMessage(offerID[playerid], COLOR_WHITE, "Нажмите {00D600}Y{ffffff} для соглашения или {FF6600}N{ffffff} для отказа");
	        }
	        else return true;
	    }
	}
	return 1;
}

public OnPlayerSelectObject(playerid, type, objectid, modelid, Float:fX, Float:fY, Float:fZ)
{
    if(type == SELECT_OBJECT_GLOBAL_OBJECT)
    {
        CancelEdit(playerid);
        currobj = objectid;
        return ShowPlayerDialog(playerid, dObjectEdit, DIALOG_STYLE_LIST, "{CC9900}Редактирование объекта", "1. Изменить расположение\n2. Удалить объект", "Выбрать", "Закрыть");
    }
    return 1;
}

public OnPlayerEditObject(playerid, playerobject, objectid, response, Float:fX, Float:fY, Float:fZ, Float:fRotX, Float:fRotY, Float:fRotZ)
{
	new Float:oldX, Float:oldY, Float:oldZ, Float:oldRotX, Float:oldRotY, Float:oldRotZ;
	GetObjectPos(objectid, oldX, oldY, oldZ);
	GetObjectRot(objectid, oldRotX, oldRotY, oldRotZ);
	if(!playerobject)
	{
	    if(!IsValidObject(objectid)) return 1;
	    SetObjectPos(objectid, fX, fY, fZ);
	    SetObjectRot(objectid, fRotX, fRotY, fRotZ);
	}

	if(response == EDIT_RESPONSE_FINAL)
	{
	    if(objectid == objectactor && typemove == 1)
	    {
	        actorids[curractori] = CreateActor(GetPVarInt(playerid, "SkinActor"), fX, fY, fZ, fRotZ);
	        DestroyObject(objectactor);
	        objectactor = -1;
	        new str[64];
	        format(str, sizeof(str), "Поставил %s\n\n\n{777777}ID: %d", PlayerInfo[playerid][pName], actorids[curractori]);
	        actor3d[curractori] = Create3DTextLabel(str, 0x5881BBAA, fX, fY, fZ, 5.0, GetPlayerVirtualWorld(playerid), 1);
			SendClientMessage(playerid, COLOR_GREEN, "Актёр успешно создан");
			DeletePVar(playerid, "SkinActor");
			return SetTimerEx("PreloadAnimLibActor", 2000, false, "d", actorids[curractor]);
	    }
	    if(objectid == objectactor && typemove == 2)
	    {
	        SetActorPos(actorids[curractor], fX, fY, fZ);
	        SetActorFacingAngle(actorids[curractor], fRotZ);
	        DestroyObject(objectactor);
	        objectactor = -1;
	        new str[64];
	        format(str, sizeof(str), "Поставил %s\n\n\n{777777}ID: %d", PlayerInfo[playerid][pName], actorids[curractori]);
	        Delete3DTextLabel(actor3d[curractor]);
	        actor3d[curractor] = Create3DTextLabel(str, 0x5881BBAA, fX, fY, fZ, 5.0, GetPlayerVirtualWorld(playerid), 1);
	        return SendClientMessage(playerid, COLOR_YELLOW, "Измените внешность актёра для применения угла поворота");
	    }
		SetObjectPos(objectid, fX, fY, fZ);
		SetObjectRot(objectid, fRotX, fRotY, fRotZ);
	}
	if(response == EDIT_RESPONSE_CANCEL)
	{
	    if(objectid == objectactor)
	    {
	        DestroyObject(objectactor);
	        objectactor = -1;
	        return true;
	    }
		if(!playerobject) DestroyObject(objectid);
	}
	return true;
}

public OnPlayerClickPlayer(playerid, clickedplayerid, source)
{
	return 1;
}

public OnPlayerClickMap(playerid, Float:fX, Float:fY, Float:fZ)
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	new vehicleid = GetPlayerVehicleID(playerid);
	if(vehicleid > 0 && (GetPlayerState(playerid) == PLAYER_STATE_DRIVER || GetPlayerState(playerid) == PLAYER_STATE_PASSENGER)) SetVehiclePos(vehicleid, fX, fY, fZ);
	else SetPlayerPos(playerid, fX, fY, fZ);
	return 1;
}

public IsAccountRegister(playerid)
{
	new rows;
	cache_get_row_count(rows);
	SetPVarInt(playerid, "time_to_kick", GetTickCount() + 30000);
	if(!PlayerInfo[playerid][pAR]) SendClientMessage(playerid, COLOR_BLUE, "Добро пожаловать на Advance GangWar");
	if(!rows) return ShowPlayerRegister(playerid);
	else
	{
		cache_get_value_name(0, "password", PlayerInfo[playerid][pPassword], 32);
		cache_get_value_name(0, "pin", PlayerInfo[playerid][pPin], 10);
		cache_get_value_name(0, "lip", PlayerInfo[playerid][pIP], 16);
		cache_get_value_name_int(0, "typepin", PlayerInfo[playerid][pAskForPin]);
		ShowPlayerAuth(playerid, -1);
	}
	return true;
}

public UploadPlayerAccount(playerid)
{
    cache_get_value_name_int(0, "IDacc", PlayerInfo[playerid][pID]);
	cache_get_value_name_int(0, "admin", PlayerInfo[playerid][pAdmin]);
	cache_get_value_name_int(0, "kills", PlayerInfo[playerid][pKills]);
	cache_get_value_name_int(0, "deaths", PlayerInfo[playerid][pDeaths]);
	cache_get_value_name_int(0, "vip", PlayerInfo[playerid][pVip]);
	cache_get_value_name_int(0, "mute", PlayerInfo[playerid][pMute]);
	cache_get_value_name_int(0, "jail", PlayerInfo[playerid][pJail]);
	cache_get_value_name_int(0, "nicks", PlayerInfo[playerid][pShowNicks]);
	cache_get_value_name_int(0, "gangonline", PlayerInfo[playerid][pGangOnline]);
	cache_get_value_name_int(0, "gchat", PlayerInfo[playerid][pChatGang]);
	cache_get_value_name_int(0, "typechat", PlayerInfo[playerid][pTypeChat]);
	cache_get_value_name_int(0, "donate", PlayerInfo[playerid][pDonate]);
	switch(PlayerInfo[playerid][pAdmin])
	{
	    case 1: SendClientMessage(playerid, COLOR_YELLOW, "Вы вошли как администратор первого уровня");
	    case 2: SendClientMessage(playerid, COLOR_YELLOW, "Вы вошли как администратор второго уровня");
	    case 3: SendClientMessage(playerid, COLOR_YELLOW, "Вы вошли как администратор третьего уровня");
	    case 4: SendClientMessage(playerid, COLOR_YELLOW, "Вы вошли как администратор четвёртого уровня");
	    case 5: SendClientMessage(playerid, COLOR_YELLOW, "Вы вошли как главный администратор");
	}
	if(PlayerInfo[playerid][pAdmin] > 0)
	{
	    for(new i = 0; i != 11; i++)
	    {
	        TextDrawShowForPlayer(playerid, TD_ACGm[i]);
	        TextDrawShowForPlayer(playerid, TD_ACSh[i]);
	        admTimer[playerid] = SetTimerEx("ClearAdmVars", 60000, true, "d", playerid);
	    }
	}
	SetPlayerScore(playerid, PlayerInfo[playerid][pKills]);
	return ActionsAfterAllDialogs(playerid);
}

public OnGZLoaded()
{
    new fields;
    cache_get_field_count(fields);
    for(new i = 0; i != sizeof(ZoneInfo); i++)
    {
        cache_get_value_name_float(i, "X", ZoneInfo[i][gCoords][0]);
        cache_get_value_name_float(i, "Y", ZoneInfo[i][gCoords][1]);
        cache_get_value_name_float(i, "XX", ZoneInfo[i][gCoords][2]);
        cache_get_value_name_float(i , "YY", ZoneInfo[i][gCoords][3]);
        cache_get_value_name_int(i, "gangid", ZoneInfo[i][gGang]);
        switch(ZoneInfo[i][gGang])
        {
            case 1: gangzone[0]++;
            case 2: gangzone[1]++;
            case 3: gangzone[2]++;
            case 4: gangzone[3]++;
            case 5: gangzone[4]++;
            case 6: gangzone[5]++;
            case 7: gangzone[6]++;
            case 8: gangzone[7]++;
        }
        ZoneInfo[i][gID] = GangZoneCreate(ZoneInfo[i][gCoords][0], ZoneInfo[i][gCoords][1], ZoneInfo[i][gCoords][2], ZoneInfo[i][gCoords][3]);
    }

    new str[96];
    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n\n\n{009900}Склад\nGrove Street", gangzone[0]);
    warehouses[1] = Create3DTextLabel(str, 0xFFFFFFFF, 2455.5740, -1706.3229, 1014.8078, 5.0, 2, 1);

    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{CC00FF}Склад\nThe Ballas", gangzone[1]);
    warehouses[2] = Create3DTextLabel(str, 0xFFFFFFFF, -42.5511,1412.5063,1085.5297, 5.0, 2, 1);

    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{FFCD00}Склад\nLos Santos Vagos", gangzone[2]);
    warehouses[3] = Create3DTextLabel(str, 0xFFFFFFFF, 333.0990, 1118.9160, 1085.0503, 5.0, 2, 1);

    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{00CCFF}Склад\nVarios Los Aztecas", gangzone[3]);
    warehouses[4] = Create3DTextLabel(str, 0xFFFFFFFF, 223.0501,1249.4037,1083.0406, 5.0, 2, 1);

    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{6666FF}Склад\nThe Rifa", gangzone[4]);
    warehouses[5] = Create3DTextLabel(str, 0xFFFFFFFF, -71.8009,1366.5933,1081.4185, 5.0, 2, 1);
    return print("[MySql] Зоны успешно загружены");
}

public EverySecond()
{
	CaptureTimer();
	return true;
}

public PlayerUpdate(playerid)
{
	if(PlayerTact[playerid] == 4)
	{
	    if(PlayerInfo[playerid][pAdmin] >= 1)
		{
		    if(AdminInfo[playerid][aBan] > 9 || AdminInfo[playerid][aJail] > 9 ||
			AdminInfo[playerid][aRBan] > 9 || AdminInfo[playerid][aKick] > 10 ||
			AdminInfo[playerid][aMsg] > 5 || AdminInfo[playerid][aJail] > 9 || AdminInfo[playerid][aUnBan] > 3 || AdminInfo[playerid][aReturn] == 1)
			{
			    new str[96];
			    returnedAdminLVL = PlayerInfo[playerid][pAdmin];
			    returnedAdmin = playerid;
			    ClearAdmVars(playerid);
				PlayerInfo[playerid][pAdmin] = 0;
		        KillTimer(admTimer[playerid]);
		        format(str, sizeof(str), "[Внимание] Администратор %s[%d] был снят с админки системой безопасности", PlayerInfo[playerid][pName], playerid);
			    SendAdminMessage(COLOR_RED, str, 1);
				mysql_format(mysql_connection, str, sizeof(str), "UPDATE accounts SET admin=0 WHERE name='%s'", PlayerInfo[playerid][pName]);
				mysql_tquery(mysql_connection, str, "", "");
			    SendAdminMessage(COLOR_RED, "[Внимание] Для возврата пропишите /returnadm", 4);
			}
		}
		if(GetPVarInt(playerid, "TimeToDelVeh") > 0) SetPVarInt(playerid, "TimeToDelVeh", GetPVarInt(playerid, "TimeToDelVeh")-1);
		if(GetPVarInt(playerid, "TimeToDelVeh") == 1)
		{
			DestroyVehicle(idplayercar[playerid]);
			idplayercar[playerid] = 0;
			DeletePVar(playerid, "TimeToDelVeh");
			SendClientMessage(playerid, COLOR_YELLOW, "Срок действия вашего транспорта истёк");
		}
		new tick = GetTickCount();
		if(IsPlayerConnected(playerid) && GetPVarInt(playerid, "time_to_kick") != 0 && GetPVarInt(playerid, "time_to_kick") < tick)
		{
			SendClientMessage(playerid, COLOR_ORANGE, "Время на авторизацию ограничено");
			SendClientMessage(playerid, COLOR_ORANGE, "Введите /q (/quit) чтобы выйти");
			ShowPlayerDialog(playerid, -1, 0, " ", " ", " ", " ");
			KickEx(playerid);
		}
		if(PlayerInfo[playerid][pMaskTime] > 0) PlayerInfo[playerid][pMaskTime]--;
		if(PlayerInfo[playerid][pMaskTime] == 0)
		{
			switch(PlayerInfo[playerid][pGang])
			{
				case GANG_GROVE: SetPlayerColor(playerid, COLOR_GROVE);
				case GANG_BALLAS: SetPlayerColor(playerid, COLOR_BALLAS);
				case GANG_VAGOS: SetPlayerColor(playerid, COLOR_VAGOS);
				case GANG_AZTECAS: SetPlayerColor(playerid, COLOR_AZTECAS);
				case GANG_RIFA: SetPlayerColor(playerid, COLOR_RIFA);
			}
			GameTextForPlayer(playerid, "~y~INVISIBLE OFF", 4000, 4);
			PlayerInfo[playerid][pMaskTime] = -1;
			if(IsPlayerAttachedObjectSlotUsed(playerid, 2)) RemovePlayerAttachedObject(playerid, 2);
		}
		if(GetPVarInt(playerid, "ACTimerFLY") > 0)
		{
		    SetPVarInt(playerid, "ACTimerFLY", GetPVarInt(playerid, "ACTimerFLY")-1);
		}
		if(GetPVarInt(playerid, "ACTimerSH") > 0)
		{
		    SetPVarInt(playerid, "ACTimerSH", GetPVarInt(playerid, "ACTimerSH")-1);
		}
		if(PlayerInfo[playerid][pMute] == 0)
		{
			SendClientMessage(playerid, COLOR_GREEN, "Срок действия бана чата закончился");
			PlayerInfo[playerid][pMute] = -1;
		}
		if(PlayerInfo[playerid][pJail] == 0)
		{
			SendClientMessage(playerid, COLOR_YELLOW, "Вы отбыли свой срок и можете идти на свободу");
			PlayerInfo[playerid][pJail] = -1;
			PlayerInfo[playerid][pSkin] = 0;
			SpawnPlayer(playerid);
		}
		if(PlayerInfo[playerid][pMute] != -1 && PlayerInfo[playerid][pAFK] == 0) PlayerInfo[playerid][pMute]--;
		if(PlayerInfo[playerid][pJail] != -1 && PlayerInfo[playerid][pAFK] == 0) PlayerInfo[playerid][pJail]--;
		PlayerInfo[playerid][pAFK]++;
		if(PlayerInfo[playerid][pAFK] > 3)
		{
			new str_local[24];
			format(str_local, sizeof(str_local),"На паузе: %s", ConvertTime(PlayerInfo[playerid][pAFK]));
			SetPlayerChatBubble(playerid, str_local, COLOR_RED, 5.0, 1000);
		}
		if(GetPlayerSpeed(playerid) > 180 && (GetPlayerState(playerid) == PLAYER_STATE_DRIVER || GetPlayerState(playerid) == PLAYER_STATE_PASSENGER))
		{
		    if(GetPVarInt(playerid, "ACTimerSH") == 0)
		    {
		        SetPVarInt(playerid, "ACTimerSH", 10);
		        AddPlayerToCheatPanel(playerid, 0);
		    }
		}
		if(GetPlayerSpeed(playerid) > 50 && GetPlayerState(playerid) == PLAYER_STATE_ONFOOT)
		{
		    if(GetPVarInt(playerid, "ACTimerSH") == 0)
		    {
		        SetPVarInt(playerid, "ACTimerSH", 10);
		        AddPlayerToCheatPanel(playerid, 0);
		    }
		}
	    PlayerTact[playerid] = 0;
	}
	if(IsPlayerInAnyVehicle(playerid))
	{
 		new vId = GetPlayerVehicleID(playerid);
   		#define MAX_SPEEDO 0.55
		#define SLOW_FACTOR 0.8
		if(VehInfo[vId][vLimiter] == 1)
		{
  			new Float:cX, Float:cY, Float:cZ;
			GetVehicleVelocity(vId, cX, cY, cZ);
			if((cX > MAX_SPEEDO || cX < -MAX_SPEEDO) || (cY > MAX_SPEEDO || cY < -MAX_SPEEDO)) SetVehicleVelocity(vId, cX*SLOW_FACTOR, cY*SLOW_FACTOR, cZ);
		}
	}
	if(PlayerTact[playerid] == 2)
	{
	    if(IsPlayerInAnyVehicle(playerid))
		{
		    new str[115];
		    new vId = GetPlayerVehicleID(playerid);
		    new Float:vHealth;
		    GetVehicleHealth(vId, vHealth);
		    new vLimiterText[14];
		    new vLockText[14];
			new vEngineText[10];
			new vLightText[10];
			new vSignalText[14];
			new vFuelText[14];
		    if(VehInfo[vId][vLimiter] == 1) vLimiterText = "~r~~h~~h~max";
		    if(VehInfo[vId][vLimiter] == 0) vLimiterText = "~w~max";
		    if(VehInfo[vId][vLock] == 1) vLockText = "~r~~h~Close";
		    if(VehInfo[vId][vLock] == 0) vLockText = "~g~~h~Open";
		    if(VehInfo[vId][vFuel] < 10) vFuelText = "~r~~h~~h~E";
		    if(VehInfo[vId][vFuel] >= 10) vFuelText = "~w~E";
		    if(VehInfo[vId][vEngine] == 1) vEngineText = "~g~M";
		    if(VehInfo[vId][vEngine] == 0) vEngineText = "~w~M";
		    if(VehInfo[vId][vLight] == 1) vLightText = "~g~L";
		    if(VehInfo[vId][vLight] == 0) vLightText = "~w~L";
		    if(VehInfo[vId][vSignal] == 1) vSignalText = "~p~S";
		    if(VehInfo[vId][vSignal] == 0) vSignalText = "~w~S";
		    format(str, sizeof(str), "%d_km/h__~h~Fuel_%d__~b~%d~n~%s~w~___%s___%s_%s__%s_%s_~w~B", GetPlayerSpeed(playerid), VehInfo[vId][vFuel], floatround(vHealth, floatround_round), vLockText, vLimiterText, vFuelText, vSignalText, vEngineText, vLightText);
		    PlayerTextDrawSetString(playerid, TD_Speedo[playerid], str);
		    //0_km/h__~h~Fuel_0__~b~1000~n~~g~~h~Open~w~___max___E_S__M_L_B
		}
	}
	if(IsPlayerInAnyVehicle(playerid)) PlayerTextDrawShow(playerid, TD_Speedo[playerid]);
	if(!IsPlayerInAnyVehicle(playerid)) PlayerTextDrawHide(playerid, TD_Speedo[playerid]);
	PlayerTact[playerid]++;
	return true;
}

public RemoveObject(playerid, slot)
{
	if(IsPlayerAttachedObjectSlotUsed(playerid, slot)) return RemovePlayerAttachedObject(playerid, slot);
	return true;
}

public OnCheckForBan(playerid)
{
	new rows;
	new query[96];
	cache_get_row_count(rows);
	if(rows)
	{
	    new nameadm[MAX_PLAYER_NAME];
		new date[20];
		new reason[30];
		new unbandays;
		new str[202];
		cache_get_value_name(0, "nameadm", nameadm);
		cache_get_value_name(0, "date", date);
		cache_get_value_name(0, "reason", reason);
		cache_get_value_name_int(0, "daystounban", unbandays);
	    if(unbandays <= 0)
	    {
			mysql_format(mysql_connection, query, sizeof(query), "DELETE FROM `bans` WHERE name='%s'", PlayerInfo[playerid][pName]);
			mysql_tquery(mysql_connection, query, "", "");
			return CheckForPin(playerid);
	    }
	    format(str, sizeof(str), "{FFFFFF}Этот аккаунт заблокирован на {ff4400}%d дней.{FFFFFF}\n\nНик администратора: %s\nПричина блокировки: %s\nДата и время: %s\n\nВведите {ffcd00}/q (/quit){FFFFFF} чтобы выйти.", unbandays, nameadm, reason, date);
     	ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{3399ff}Advance GangWar", str, "Закрыть", "");
	    return KickEx(playerid);
	}
	else return CheckForPin(playerid);
}

public Restart()
{
	foreach(new i:Player) if(PlayerInfo[i][pAR] != 0) SaveAccount(i);
	mysql_tquery(mysql_connection, "UPDATE `bans` SET `daystounban`=`daystounban`-1", "", "");
	return mysql_tquery(mysql_connection, "UPDATE `ipbans` SET `daystounban`=`daystounban`-1", "", "");
}

public OnRipAccountsShow(playerid, rip[])
{
	new rows;
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Аккаунтов с таким регистрационным IP не найдено");
	new name[MAX_PLAYER_NAME];
	new kills;
	new tempstr[64];
	new bigstr[512];
	strcat(bigstr, "Ник\t\tУбийства\n\n{ffffff}");
	for(new i = 0; i < rows; i++)
	{
	    cache_get_value_name(i, "name", name);
	    cache_get_value_name_int(i, "kills", kills);
	    format(tempstr, sizeof(tempstr), "%s\t%d\n", name, kills);
	    strcat(bigstr, tempstr);
	}
	format(tempstr, sizeof(tempstr), "\n{00D600}Всего аккаунтов: %d", rows);
	strcat(bigstr, tempstr);
	format(tempstr, sizeof(tempstr), "IP: %s", rip);
	return ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, tempstr, bigstr, "Закрыть", "");
}

public OnLipAccountsShow(playerid, lip[])
{
	new rows;
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Не найдено аккаунтов на которые заходили с данного IP");
	new name[MAX_PLAYER_NAME];
	new kills;
	new tempstr[64];
	new bigstr[512];
	strcat(bigstr, "Ник\t\tУбийства\n\n{ffffff}");
	for(new i = 0; i < rows; i++)
	{
	    cache_get_value_name(i, "name", name);
	    cache_get_value_name_int(i, "kills", kills);
	    format(tempstr, sizeof(tempstr), "%s\t%d\n", name, kills);
	    strcat(bigstr, tempstr);
	}
	format(tempstr, sizeof(tempstr), "\n{00D600}Всего аккаунтов: %d", rows);
	strcat(bigstr, tempstr);
	format(tempstr, sizeof(tempstr), "IP: %s", lip);
	return ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, tempstr, bigstr, "Закрыть", "");
}

public GetAccInfo(playerid, nick[])
{
	new rows;
	new idacc, kills, deaths;
	new rip[16];
	new lip[16];
	new datereg[24];
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Игрок с таким ником не найден");
	cache_get_value_name_int(0, "IDacc", idacc);
	cache_get_value_name_int(0, "kills", kills);
	cache_get_value_name_int(0, "deaths", deaths);
	cache_get_value_name(0, "rip", rip);
	cache_get_value_name(0, "lip", lip);
	cache_get_value_name(0, "datereg", datereg);
	new str[256];
	format(str, sizeof(str), "\
	Номер аккаунта:\t%d\n\
	Убийства:\t\t%d\n\
	Смерти:\t\t%d\n\
	IP адрес(регис.):\t%s\n\
	IP адрес(послед.):\t%s\n\
	Дата регистрации:\t%s\n", idacc, kills, deaths, rip, lip, datereg);
	ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, nick, str, "Закрыть", "");
	format(str, sizeof(str), "[A][GET] %s[%d] просматривает данные игрока %s", PlayerInfo[playerid][pName], playerid, nick);
	return SendAdminMessage(COLOR_ADMMSG, str, 1);
}

public GetBanInfo(playerid, nick[])
{
    new rows;
	new idacc, daystounban;
	new name[MAX_PLAYER_NAME];
	new nameadm[MAX_PLAYER_NAME];
	new ip[16];
	new date[24];
	new reason[30];
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Данный игрок не получал блокировки");
	cache_get_value_name_int(0, "IDacc", idacc);
	cache_get_value_name_int(0, "daystounban", daystounban);
	cache_get_value_name(0, "name", name);
	cache_get_value_name(0, "nameadm", nameadm);
	cache_get_value_name(0, "ip", ip);
	cache_get_value_name(0, "date", date);
	cache_get_value_name(0, "reason", reason);
	new str[256];
	format(str, sizeof(str), "\
	Номер аккаунта:\t\t%d\n\
	Ник забанненого:\t\t%s\n\
	Ник администратора:\t%s\n\
	Дней до конца бана:\t%d\n\
	Причина:\t\t\t%s\n\
	IP во время бана:\t\t%s\n\
	Дата бана:\t\t\t%s", idacc, name, nameadm, daystounban, reason, ip, date);
	return ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, nick, str, "Закрыть", "");
}

public CheckForIPBan(playerid, ip[])
{
    new rows;
	new query[96];
	cache_get_row_count(rows);
	if(rows)
	{
		new unbandays;
		cache_get_value_name_int(0, "daystounban", unbandays);
 		if(unbandays <= 0)
 		{
			mysql_format(mysql_connection, query, sizeof(query), "DELETE FROM `ipbans` WHERE ip='%s'", ip);
			mysql_tquery(mysql_connection, query, "", "");
 		}
 		else
 		{
 		    SendClientMessage(playerid, COLOR_ORANGE, "Ваш IP адрес заблокирован");
	    	KickEx(playerid);
 		}
	}
}

public IsBannedIP(playerid, ip[])
{
    new rows;
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Данный IP не был заблокирован");
	else
	{
	    new str[128];
	    format(str, sizeof(str), "[A] %s[%d] разбанил IP %s", PlayerInfo[playerid][pName], playerid, ip);
		SendAdminMessage(COLOR_ADMMSG, str, 1);
		mysql_format(mysql_connection, str, sizeof(str), "DELETE FROM `ipbans` WHERE `ip`='%s'", ip);
		return mysql_tquery(mysql_connection, str, "", "");
	}
}

public CheckBan(playerid, bannednick[], time, reason[])
{
    new rows;
	cache_get_row_count(rows);
	if(rows) return SendClientMessage(playerid, 0x999999AA, "Данный игрок уже был заблокирован");
	else
	{
	    new str[128];
	    mysql_format(mysql_connection, str, sizeof(str), "SELECT `IDacc`, `lip` FROM `accounts` WHERE name='%s'", bannednick);
		return mysql_tquery(mysql_connection, str, "OffBan", "dsds", playerid, bannednick, time, reason);
	}
}

public OffBan(playerid, bannednick[], time, reason[])
{
    new rows;
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нету");
	new idacc;
	new ip[16];
	cache_get_value_name(0, "lip", ip);
	cache_get_value_name_int(0, "IDacc", idacc);
	new str[196];
	mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `bans`(`IDacc`, `name`, `nameadm`, `ip`, `date`, `reason`, `daystounban`) VALUES (%d, '%s', '%s', '%s', NOW(), '%s', %d)", idacc, bannednick, PlayerInfo[playerid][pName], ip, reason, time);
	mysql_tquery(mysql_connection, str, "", "");
	format(str, sizeof(str), "Администратор %s забанил игрока %s оффлайн на %d дней. Причина: %s", PlayerInfo[playerid][pName], bannednick, time, reason);
	SendClientMessageToAll(0xFF5030AA, str);
	mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `ipbans`(`ip`, `daystounban`) VALUES ('%s', %d)", ip, time);
	AdminInfo[playerid][aBan]++;
	return mysql_tquery(mysql_connection, str, "", "");
}

public UnBan(playerid, nick[])
{
	new rows;
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Данный игрок не заблокирован");
	new ip[16], idacc;
	cache_get_value_name(0, "ip", ip);
	cache_get_value_name_int(0, "IDacc", idacc);
	new str[128];
	mysql_format(mysql_connection, str, sizeof(str), "DELETE FROM `bans` WHERE name='%s'", nick);
	mysql_tquery(mysql_connection, str, "", "");
	mysql_format(mysql_connection, str, sizeof(str), "DELETE FROM `ipbans` WHERE ip='%s'", ip);
	mysql_tquery(mysql_connection, str, "", "");
	format(str, sizeof(str), "[A] %s[%d] разбанил игрока %s (аккаунт %d, IP %s)", PlayerInfo[playerid][pName], playerid, nick, idacc, ip);
	AdminInfo[playerid][aUnBan]++;
	return SendAdminMessage(COLOR_ADMMSG, str, 1);
}

public ADM(playerid)
{
	new rows;
	cache_get_row_count(rows);
	if(!rows) return true;
	else
	{
	    SendClientMessage(playerid, COLOR_YELLOW, "Ваш уровень администратора был изменён");
	    cache_get_value_name_int(0, "level", PlayerInfo[playerid][pAdmin]);
	    new str[100];
	    for(new i = 0; i != 11; i++)
	    {
	        TextDrawShowForPlayer(playerid, TD_ACGm[i]);
	        TextDrawShowForPlayer(playerid, TD_ACSh[i]);
	    }
	    admTimer[playerid] = SetTimerEx("ClearAdmVars", 60000, true, "d", playerid);
	    mysql_format(mysql_connection, str, sizeof(str), "DELETE FROM `newadm` WHERE name='%s'", PlayerInfo[playerid][pName]);
		mysql_tquery(mysql_connection, str, "", "");
		mysql_format(mysql_connection, str, sizeof(str), "UPDATE `accounts` SET `admin`=%d WHERE `name`='%s'", PlayerInfo[playerid][pAdmin], PlayerInfo[playerid][pName]);
		return mysql_tquery(mysql_connection, str, "", "");
	}
}

public DelAccount(playerid, delname[], att)
{
	new str[100];
	new rows;
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Игрока с таким ником нет");
	new idacc, kills;
	cache_get_value_name_int(0, "IDacc", idacc);
	cache_get_value_name_int(0, "kills", kills);
	if(att == 0)
	{
	    SetPVarInt(playerid, "DelACC", 1);
	    format(str, sizeof(str), "Ник: %s, номер: %d, убийства: %d. Удалять аккаунт?", delname, idacc, kills);
	    SendClientMessage(playerid, COLOR_ORANGE, str);
     	SendClientMessage(playerid, COLOR_YELLOW, "Для ОТМЕНЫ удаления введите /delacc без ника");
	    return SendClientMessage(playerid, COLOR_YELLOW, "Для ПОДТВЕРЖДЕНИЯ повторите /delacc [ник]");
	}
	else
	{
	    format(str, sizeof(str), "Аккаунт №%d удалён", idacc);
	    SendClientMessage(playerid, COLOR_GREEN, str);
	    format(str, sizeof(str), "[Внимание] %s[%d] удалил аккаунт игрока %s", PlayerInfo[playerid][pName], playerid, delname);
	    SendAdminMessage(COLOR_RED, str, 1);
	    mysql_format(mysql_connection, str, sizeof(str), "DELETE FROM `accounts` WHERE name='%s'", delname);
		mysql_tquery(mysql_connection, str, "", "");
		new iddel = GetPlayerID(delname);
		if(iddel != -1)
		{
		    SendClientMessage(iddel, COLOR_RED, "Ваш аккаунт был удалён за нарушение правил сервера");
		    KickEx(iddel);
		}
		DeletePVar(playerid, "DelACC");
	}
	return true;
}

public CheckForAdmin(playerid, adm[])
{
	new rows;
	new str[128];
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Игрок с таким ником не найден");
	if(rows)
	{
	    new admlevel;
	    cache_get_value_name_int(0, "admin", admlevel);
	    if(admlevel > 0)
	    {
	        mysql_format(mysql_connection, str, sizeof(str), "UPDATE `accounts` SET `admin`=0 WHERE `name`='%s'", adm);
	        mysql_tquery(mysql_connection, str, "", "");
	        format(str, sizeof(str), "Администратор %s был снят оффлайн", adm);
			return SendClientMessage(playerid, COLOR_GREEN, str);
	    }
	    else
	    {
	        mysql_format(mysql_connection, str, sizeof(str), "SELECT `name` FROM `newadm` WHERE `name`='%s'", adm);
	        return mysql_tquery(mysql_connection, str, "CheckInNewAdm", "ds", playerid, adm);
	    }
	}
	return true;
}

public CheckInNewAdm(playerid, adm[])
{
	new rows;
	new str[64];
	cache_get_row_count(rows);
	if(!rows) return SendClientMessage(playerid, COLOR_LGREY, "Данный игрок не администратор");
	if(rows)
	{
 		mysql_format(mysql_connection, str, sizeof(str), "DELETE FROM `newadm` WHERE name='%s'", adm);
		mysql_tquery(mysql_connection, str, "", "");
 		format(str, sizeof(str), "Администратор %s был снят оффлайн", adm);
		return SendClientMessage(playerid, COLOR_GREEN, str);
	}
	return true;
}

public ClearAdmVars(playerid)
{
	AdminInfo[playerid][aBan] = 0;
	AdminInfo[playerid][aRBan] = 0;
	AdminInfo[playerid][aJail] = 0;
	AdminInfo[playerid][aKick] = 0;
	AdminInfo[playerid][aMsg] = 0;
	AdminInfo[playerid][aUnBan] = 0;
	AdminInfo[playerid][aReturn] = 0;
	return true;
}

public OnLastDonatesLoaded(playerid)
{
	new rows;
	cache_get_row_count(rows);
	if(!rows) return ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{ffdd00}Последние пополнения", "Вы ещё ни разу не пополняли свой аккаунт.\nСделать это можно на сайте {00CC66}advance-gw.ru {ffffff}в разделе{6699FF} \"Донат\"", "Закрыть", "");
	new bigstr[333];
	new date[25];
	new tempstr[48];
	new sum;
	strcat(bigstr, "Дата и время\t\tСумма\n\n");
	for(new i = 0; i < rows; i++)
	{
	    cache_get_value_name(i, "date", date);
	    cache_get_value_name_int(i, "sum", sum);
	    format(tempstr, sizeof(tempstr), "{ffffff}%s\t\t%d\n", date, sum);
	    strcat(bigstr, tempstr);
	}
	return ShowPlayerDialog(playerid, dAllDonates, DIALOG_STYLE_MSGBOX, "{ffdd00}20 последних операций пополенения", bigstr, "Назад", "");
}

public CheckName(playerid, name[])
{
	new rows;
	cache_get_row_count(rows);
	if(rows)
	{
	    ShowPlayerDialog(playerid, dChangeName, DIALOG_STYLE_INPUT, "{ffdd00}Изменение имени", "{ffffff}Введите новое имя в поле ниже:", "Далее", "Назад");
	    return SendClientMessage(playerid, COLOR_ORANGE, "Данное имя занято");
	}
	else
	{
		new str[128];
		format(str, sizeof(str), "%s сменил имя на %s", PlayerInfo[playerid][pName], name);
		SendClientMessageToAll(0xCCFF00AA, str);
		mysql_format(mysql_connection, str, sizeof(str), "UPDATE accounts SET name='%s' WHERE name='%s'", name, PlayerInfo[playerid][pName]);
		mysql_tquery(mysql_connection, str, "", "");
		mysql_format(mysql_connection, str, sizeof(str), "UPDATE lastdonates SET name='%s' WHERE name='%s'", name, PlayerInfo[playerid][pName]);
		mysql_tquery(mysql_connection, str, "", "");
		mysql_format(mysql_connection, str, sizeof(str), "UPDATE newadm SET name='%s' WHERE name='%s'", name, PlayerInfo[playerid][pName]);
		mysql_tquery(mysql_connection, str, "", "");
		SetPlayerName(playerid, name);
		PlayerInfo[playerid][pName][0] = EOS;
		PlayerInfo[playerid][pDonate] -= 8;
		strins(PlayerInfo[playerid][pName], name, 0);
		ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{ffdd00}Имя успешно изменено", "{ffffff}\
		Не забудьте изменить имя в окне клиента SA-MP\n\
		Рекомендуем прямо сейчас свернуть игру и сделать это\n\n\
		С Вашего игрового счёта было снято 8.00 руб.", "Ок", "");
		GameTextForPlayer(playerid, "~b~NAME CHANGED~n~~y~-8 RUB.", 4500, 1);
		return PlayerPlaySound(playerid, 1056, 0.0, 0.0, 0.0);
	}
}

public DestroyVipVehicle(playerid, vehid)
{
	DestroyVehicle(vehid);
	return SendClientMessage(playerid, COLOR_YELLOW, "Срок действия вашего VIP авто истёк");
}

public PreloadAnimLibActor(actorid)
{
    ApplyActorAnimation(actorid,"DANCING","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"ON_LOOKERS","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"BEACH","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"ped","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"benchpress","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"BOMBER","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"SHOP","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"COP_AMBIENT","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"FOOD","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"SWEET","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"DEALER","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"CRACK","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"LOWRIDER","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"PARK","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"BAR","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"BSKTBALL","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"MISC","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"CAMERA","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"GANGS","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"INT_HOUSE","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"INT_OFFICE","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"INT_SHOP","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"JST_BUISNESS","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"KISSING","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"MEDIC","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"ON_LOOKERS","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"PAULNMAC","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"GHANDS","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"POLICE","null",0.0,0,0,0,0,0);
    ApplyActorAnimation(actorid,"RIOT","null",0.0,0,0,0,0,0);
    return ApplyActorAnimation(actorid,"SWAT","null",0.0,0,0,0,0,0);
}

public ClearSignal(vehicleid)
{
    return SetVehicleParamsEx(vehicleid, VehInfo[vehicleid][vEngine], VehInfo[vehicleid][vLight], 0, VehInfo[vehicleid][vLock], 0, 0, 0);
}

public PlayerKick(playerid) return Kick(playerid);

/*----------------------------[ Stocks ]---------------------------*/

stock ShowPlayerRegister(playerid)
{
    ShowPlayerDialog(playerid, dReg, DIALOG_STYLE_INPUT, "{66CCFF}Регистрация", "{ffffff}Добро пожаловать на сервер Advance GangWar\n\
	Чтобы начать игру вам необходимо пройти регистрацию\n\
	\n\
	Введите пароль для Вашего аккаунта\n\
	Он будет запрашиваться каждый раз, когда вы заходите на сервер\n\
	\n\
	\t{66CC33}Примечания:\n\
	\t- Пароль может состоять из русских и латинских символов\n\
	\t- Пароль чувствителен к регистру\n\
	\t- Длина пароля от 6-ти до 32-ух символов", "Далее", "Выход");
    return PlayerInfo[playerid][pAR] = 2;
}

stock ShowPlayerAuth(playerid, attempts)
{
    new str[196];
	if(attempts == -1) format(str, sizeof(str), "{ffffff}Добро пожаловать на сервер Advance GangWar\nВаш ник зарегистрирован\n\nЛогин: {66CC33}%s\n{ffffff}Введите пароль:", PlayerInfo[playerid][pName]);
	else format(str, sizeof(str), "{ffffff}Добро пожаловать на сервер Advance GangWar\nВаш ник зарегистрирован\n\nЛогин: {66CC33}%s\n{FF3300}Неверный пароль! Осталось попыток: %d", PlayerInfo[playerid][pName], attempts);
	ShowPlayerDialog(playerid, dAuth, DIALOG_STYLE_INPUT, "{66CCFF}Авторизация", str, "Далее", "Выход");
	return PlayerInfo[playerid][pAR] = 1;
}

stock ShowPlayerWarning(playerid)
{
    PlayerPlaySound(playerid, 1053, 0.0, 0.0, 0.0);
    return ShowPlayerDialog(playerid, dWarning, DIALOG_STYLE_MSGBOX, "{FF8000}Ошибка", "\
	{ffffff}Длина пароля должна быть от 6 до 32 символов\n\
	Рекомендуется использовать русские и латинские буквы, а также любые знаки", "Повтор", "");
}

stock ShowPlayerWarehouse(playerid)
{
    return ShowPlayerDialog(playerid, dWarehouse, DIALOG_STYLE_LIST, "{FFCD00}Склад", "1. Аптечка\n2. Маска\n3. Оружие", "Выбрать", "Выход");
}

stock ShowPlayerWeapons(playerid)
{
	return ShowPlayerDialog(playerid, dWeapons, DIALOG_STYLE_LIST, "{FFCD00}Выбор оружия", "1. Deagle + M4\n2. Deagle + AK-47\n3. Deagle + ShotGun\n4. Deagle + Sniper Rifle", "Выбрать", "Назад");
}

stock ShowPersonalSettings(playerid)
{
	new str[512];
	if(PlayerInfo[playerid][pTypeChat] == 0) strcat(str, "Основной чат\t\t{0099FF}Advance{ffffff}\n");
	if(PlayerInfo[playerid][pTypeChat] == 1) strcat(str, "Основной чат\t\t{00CC00}Стандартный{ffffff}\n");
	if(PlayerInfo[playerid][pTypeChat] == 2) strcat(str, "Основной чат\t\t{FF3333}Отключён{ffffff}\n");
	if(PlayerInfo[playerid][pChatGang] == 0) strcat(str, "Чат банды\t\t{FF3333}Отключён{ffffff}\n");
	if(PlayerInfo[playerid][pChatGang] == 1) strcat(str, "Чат банды\t\t{00CC00}Включён{ffffff}\n");
	//if(PlayerInfo[playerid][pShowNicks] == 0) strcat(str, "Ники над игроками\t{FF3333}Отключены{ffffff}\n");
	//if(PlayerInfo[playerid][pShowNicks] == 1) strcat(str, "Ники над игроками\t{00CC00}Включены{ffffff}\n");
	if(PlayerInfo[playerid][pGangOnline] == 0) strcat(str, "Онлайн банд\t\t{FF3333}Отключён{ffffff}\n");
	if(PlayerInfo[playerid][pGangOnline] == 1) strcat(str, "Онлайн банд\t\t{00CC00}Включён{ffffff}\n");
	strcat(str, "{888888}[Сохранить настройки]{ffffff}");
	return ShowPlayerDialog(playerid, dPersSettings, DIALOG_STYLE_LIST, "{FFCD00}Личные настройки", str, "Вкл|Выкл", "Назад");
}

stock ShowGuardSettings(playerid)
{
	return ShowPlayerDialog(playerid, dGuardSettings, DIALOG_STYLE_LIST, "{FFCD00}Настройки безопасности", "\
	1. 'Случайный' PIN-код\n\
	{00CC66}2. Изменить пароль\n\
	{ffffff}3. Изменить 'случайный' PIN-код\n\
	{0099FF}4. Статус безопасности", "Выбрать", "Назад");
}

stock ShowDonateMenu(playerid)
{
	new str[396];
	format(str, sizeof(str), "{ffffff}В этом разделе вы можете использовать дополнительные\n\
	возможности сервера. Чтобы получить к ним доступ,\n\
	необходимо пополнить свой игровой счёт. Описание всех\n\
	дополнительных возможностей, а также о способах\n\
	пополнения счёта вы можете узнать на нашем сайте:\n\
	{00CC66}advance-gw.ru (Раздел \"Донат\")\n\n\
	{6699FF}Информация:{ffffff}\n\
	Номер аккаунта:\t\t\t%d\n\
	Текущее состояние счёта:\t\t%d.00 руб.", PlayerInfo[playerid][pID], PlayerInfo[playerid][pDonate]);
	return ShowPlayerDialog(playerid, dDonateMenu, DIALOG_STYLE_MSGBOX, "{ffdd00}Дополнительные возможности (донат)", str, "Просмотр", "Закрыть");
}

stock ShowDonateSubMenu(playerid)
{
	return ShowPlayerDialog(playerid, dDonateSubMenu, DIALOG_STYLE_LIST, "{ffdd00}Меню дополнительных возможностей", "{99CC33}1. Просмотреть последние пополнения\n\
	{99CC33}2. Конвертировать рубли в игровые убийства{ffffff}\n\
	3. Изменить имя\t\t\t\t\t{6699FF}8 руб.\n\
	4. Приобрести VIP статус\t\t\t\t{6699FF}65 руб.\n\
	5. Приобрести 1 уровень администрирования\t\t{6699FF}100 руб.", "Выбрать", "Закрыть");
}

stock CreateAccount(playerid, password[])
{
	PlayerInfo[playerid][pPin][0] = EOS;
	new query[256];
	GetPlayerIp(playerid, PlayerInfo[playerid][pIP], 16);
	mysql_format(mysql_connection, query, sizeof(query), "INSERT INTO `accounts`(`name`, `password`, `rip`, `datereg`, `nicks`, `gchat` , `typechat`, `pin`) VALUES ('%s', '%s', '%s', NOW(), 1, 1, 0, '%s')", PlayerInfo[playerid][pName], password, PlayerInfo[playerid][pIP], PlayerInfo[playerid][pPin]);
	mysql_tquery(mysql_connection, query, "", "");
	PlayerInfo[playerid][pPassword][0] = EOS;
	strins(PlayerInfo[playerid][pPassword], password, 0);
	new str[1];
	SendClientMessage(playerid, -1, str);
	SendClientMessage(playerid, COLOR_WHITE, "Регистрация завершена!");
	SendClientMessage(playerid, COLOR_GREEN, "Теперь выберите внешность и банду");
	SendClientMessage(playerid, COLOR_GREEN, "Для перехода на DM часть используйте команду {ffdd00}/arena");
	SendClientMessage(playerid, COLOR_LGREY, "Подсказка: Используйте {669900}СТРЕЛКИ{CECECE} и кнопку {00CCCC}SELECT{CECECE} для выбора");
	SendClientMessage(playerid, COLOR_RED, "ВНИМАНИЕ:{ffffff} ЕСЛИ ВЫ НАЙДЁТЕ ОШИБКУ - СООБЩИТЕ О НЕЙ С ПОМОЩЬЮ {ff0000}/bugs");
	PlayerInfo[playerid][pTypeChat] = 0;
	PlayerInfo[playerid][pShowNicks] = 1;
	PlayerInfo[playerid][pChatGang] = 1;
	PlayerInfo[playerid][pGangOnline] = 1;
	return ActionsAfterAllDialogs(playerid);
}

stock CheckForPin(playerid)
{
	new query[96];
    if(strlen(PlayerInfo[playerid][pPin]) > 2)
   	{
  		if(PlayerInfo[playerid][pAskForPin] == 2)
  		{
			new TIP[16], LIP[16];
			GetPlayerIp(playerid, TIP, 16);
			GetIpSubnet(TIP);
			strins(LIP, PlayerInfo[playerid][pIP], 0);
			GetIpSubnet(LIP);
			if(strcmp(TIP, LIP, true))
			{
				ShowPlayerPin(playerid);
				SendClientMessage(playerid, COLOR_WHITE, "Система безопасности запрашивает ввода Вашего PIN-кода");
				return typePIN{playerid} = 2;
			}
		}
		if(PlayerInfo[playerid][pAskForPin] == 3)
		{
			new TIP[16];
			GetPlayerIp(playerid, TIP, 16);
			if(strcmp(TIP, PlayerInfo[playerid][pIP], true))
			{
				ShowPlayerPin(playerid);
				SendClientMessage(playerid, COLOR_WHITE, "Система безопасности запрашивает ввода Вашего PIN-кода");
				return typePIN{playerid} = 2;
			}
		}
	}
	mysql_format(mysql_connection, query, sizeof(query), "SELECT * FROM `accounts` WHERE `name` = '%s'", PlayerInfo[playerid][pName]);
	return mysql_tquery(mysql_connection, query, "UploadPlayerAccount","i", playerid);
}

stock ActionsAfterAllDialogs(playerid)
{
	new str[96];
	PreloadAnimLib(playerid, "SHOP");
	format(str, sizeof(str), "~y~welcome~n~~b~%s", PlayerInfo[playerid][pName]);
	GameTextForPlayer(playerid, str, 6000, 1);
	PlayerInfo[playerid][pAR] = 0;
	DeletePVar(playerid, "time_to_kick");
	tempPIN[playerid][0] = EOS;
	GetPlayerIp(playerid, PlayerInfo[playerid][pIP], 16);
	mysql_format(mysql_connection, str, sizeof(str), "UPDATE `accounts` SET `lip` = '%s' WHERE name='%s'", PlayerInfo[playerid][pIP], PlayerInfo[playerid][pName]);
	mysql_tquery(mysql_connection, str, "", "");
	return SpawnPlayer(playerid);
}

stock SetPlayerChooseSkin(playerid)
{
	counter_skin[playerid] = random(7);
	SetPlayerSkin(playerid, skinsgrove[counter_skin[playerid]]);
	PlayerInfo[playerid][pGang] = GANG_GROVE;
	TogglePlayerControllable(playerid, false);
	SetPlayerPos(playerid, 2454.8958,-1704.5184,1013.5078);
	SetPlayerFacingAngle(playerid, 33.000);
	SetPlayerCameraPos(playerid, 2450.239746, -1697.923217, 1014.750427);
	SetPlayerCameraLookAt(playerid, 2454.8958,-1704.5184,1013.5078);
	SetPlayerVirtualWorld(playerid, 100+playerid);
	SetPlayerInterior(playerid, 2);
	for(new i = 0; i != 10; i++) TextDrawShowForPlayer(playerid, TD_ChooseGang[i]);
	SelectTextDraw(playerid, COLOR_GREY);
	return Curr_TD[playerid] = TD_CHOOSE_GANG;
}

stock SetPrevSkin(playerid, gangid)
{
    counter_skin[playerid]--;
    switch(gangid)
	{
		case GANG_GROVE:
		{
			if(counter_skin[playerid] == -1) counter_skin[playerid] = 6;
			return SetPlayerSkin(playerid, skinsgrove[counter_skin[playerid]]);
		}
		case GANG_BALLAS:
		{
			if(counter_skin[playerid] == -1) counter_skin[playerid] = 3;
			return SetPlayerSkin(playerid, skinsballas[counter_skin[playerid]]);
		}
		case GANG_VAGOS:
		{
			if(counter_skin[playerid] == -1) counter_skin[playerid] = 3;
			return SetPlayerSkin(playerid, skinsvagos[counter_skin[playerid]]);
		}
		case GANG_AZTECAS:
		{
			if(counter_skin[playerid] == -1) counter_skin[playerid] = 4;
			return SetPlayerSkin(playerid, skinsaztecas[counter_skin[playerid]]);
		}
		case GANG_RIFA:
		{
			if(counter_skin[playerid] == -1) counter_skin[playerid] = 4;
			return SetPlayerSkin(playerid, skinsrifa[counter_skin[playerid]]);
		}
	}
	return true;
}

stock SetNextSkin(playerid, gangid)
{
    counter_skin[playerid]++;
    switch(gangid)
	{
		case GANG_GROVE:
		{
			if(counter_skin[playerid] == 7) counter_skin[playerid] = 0;
			return SetPlayerSkin(playerid, skinsgrove[counter_skin[playerid]]);
		}
		case GANG_BALLAS:
		{
			if(counter_skin[playerid] == 4) counter_skin[playerid] = 0;
			return SetPlayerSkin(playerid, skinsballas[counter_skin[playerid]]);
		}
		case GANG_VAGOS:
		{
			if(counter_skin[playerid] == 4) counter_skin[playerid] = 0;
			return SetPlayerSkin(playerid, skinsvagos[counter_skin[playerid]]);
		}
		case GANG_AZTECAS:
		{
			if(counter_skin[playerid] == 5) counter_skin[playerid] = 0;
			return SetPlayerSkin(playerid, skinsaztecas[counter_skin[playerid]]);
		}
		case GANG_RIFA:
		{
			if(counter_skin[playerid] == 5) counter_skin[playerid] = 0;
			return SetPlayerSkin(playerid, skinsrifa[counter_skin[playerid]]);
		}
	}
	return true;
}


stock IsPlayerInGZ(playerid, Float:min_x, Float:min_y, Float:max_x, Float:max_y)
{
    new Float: pos[3];
    GetPlayerPos(playerid, pos[0], pos[1], pos[2]);
    if((pos[0] <= max_x && pos[0] >= min_x) && (pos[1] <= max_y && pos[1] >= min_y)) return true;
    return false;
}

stock ClearOffersVars(playerid)
{
    offerID[offerID[playerid]] = 0;
    isOffered{playerid} = 0;
    isOffered{offerID[playerid]} = 0;
    isOfferedTo{offerID[playerid]} = 0;
    isOfferedTo{playerid} = 0;
    offerID[playerid] = 0;
    return true;
}


stock GetPlayerID(const nick[])
{
	foreach(new i:Player)
	{
	  if(IsPlayerConnected(i))
	  {
	    new name[MAX_PLAYER_NAME];
	    GetPlayerName(i, name, sizeof(name));
	    if(strcmp(nick, name, true)==0)
	    {
	      return i;
	    }
	  }
	}
	return -1;
}

stock GetGZColor(gangid)
{
    new gangid_color;
    switch(gangid)
    {
		case 0: gangid_color = 0xFFFFFFAA;
        case 1: gangid_color = 0x009900AA;
		case 2: gangid_color = 0xCC33FFAA;
        case 3: gangid_color = 0xFFCD00AA;
        case 4: gangid_color = 0x00CCFFAA;
        case 5: gangid_color = 0x6666FFAA;
        case 6: gangid_color = 0x00767688;
        case 7: gangid_color = 0x99336688;
        case 8: gangid_color = 0xBB000088;
    }
    return gangid_color;
}

stock StartCapture(gang_one, gang_two)
{
	new str[96];
	format(str, sizeof(str), "%s начали захват территории банды %s в районе %s", gang_name[gang_one-1], gang_name[gang_two-1], zone_name);
	SendClientMessageToAll(COLOR_ORANGE, str);
	new str_capture[32];
	format(str_capture, sizeof(str_capture), "%s  ~r~%i", gang_name[gang_one-1], kills_team[0]);
	TextDrawSetString(TD_Capture[2], str_capture);
	format(str_capture, sizeof(str_capture), "%s  ~r~%i", gang_name[gang_two-1], kills_team[1]);
	TextDrawSetString(TD_Capture[3], str_capture);
    foreach(new i: Player)
    {
		TextDrawShowForPlayer(i, TD_Capture[0]);
		TextDrawShowForPlayer(i, TD_Capture[1]);
		TextDrawShowForPlayer(i, TD_Capture[2]);
		TextDrawShowForPlayer(i, TD_Capture[3]);
	}
    return true;
}

stock ProxDetector(playerid, Float:range, string[])
{
    new Float:POS[3],Float:radius;
    new str[144];
    GetPlayerPos(playerid, POS[0], POS[1], POS[2]);
    new tempcolor[9];
    switch(PlayerInfo[playerid][pGang])
 	{
  		case 1: tempcolor = "{009900}";
    	case 2: tempcolor = "{CC00FF}";
     	case 3: tempcolor = "{ffcd00}";
      	case 4: tempcolor = "{00CCFF}";
       	case 5: tempcolor = "{6666ff}";
    }
    format(str, sizeof(str), "- %s %s(%s)[%d]", string, tempcolor, PlayerInfo[playerid][pName], playerid);
	SendClientMessage(playerid, 0xCECECEAA, str);
    foreach(new i: Player)
    {
        if(IsPlayerConnected(i) && GetPlayerVirtualWorld(playerid) == GetPlayerVirtualWorld(i) && i != playerid)
        {
            if(PlayerInfo[i][pTypeChat] == 0) format(str, sizeof(str), "- %s %s(%s)[%d]", string, tempcolor, PlayerInfo[playerid][pName], playerid);
            if(PlayerInfo[i][pTypeChat] == 1) format(str, sizeof(str), "%s%s[%d]: {ffffff}%s", tempcolor, PlayerInfo[playerid][pName], playerid, string);
            if(PlayerInfo[i][pTypeChat] == 2) return true;
            radius = GetPlayerDistanceFromPoint(i, POS[0], POS[1], POS[2]);
            if(radius < range/16) return SendClientMessage(i, 0xCECECEAA, str);
            else if(radius < range/8) return SendClientMessage(i, 0x999999AA, str);
            else if(radius < range/4) return SendClientMessage(i, 0x999999AA, str);
            else if(radius < range/2) return SendClientMessage(i, 0x6B6B6BAA, str);
            else if(radius < range) return SendClientMessage(i, 0x6B6B6BAA, str);
        }
    }
    return 1;
}

stock CaptureTimer()
{
	if(capture == 1)
	{
	    capture_time--;
		new str[128];
		format(str, sizeof(str), "Time: %s", ConvertTime(capture_time));
		TextDrawSetString(TD_Capture[1], str);
		format(str, sizeof(str), "%s  ~r~%i", gang_name[team_capture[0]-1], kills_team[0]);
		TextDrawSetString(TD_Capture[2], str);
		format(str, sizeof(str), "%s  ~r~%i", gang_name[team_capture[1]-1], kills_team[1]);
		TextDrawSetString(TD_Capture[3], str);
		if(!capture_time)
	    {
	        foreach(new i: Player)
	        {
	            GangZoneStopFlashForAll(zoneid_capture);
	            RemovePlayerMapIcon(i, 31);
	            if(wasstoppedc == 1)
	            {
	                kills_team[0] = 0;
	                kills_team[1] = 0;
	            }
	            if(kills_team[0] == kills_team[1] || kills_team[0] < kills_team[1])
				{
				    if(wasstoppedc == 0)
				    {
				        format(str, sizeof(str), "Попытка %s захватить территорию у %s провалилась", gang_name[team_capture[0]-1], gang_name[team_capture[1]-1]);
	  					SendClientMessage(i, COLOR_ORANGE, str);
				    }

				}
	            else if(kills_team[0] > kills_team[1])
				{
				    ZoneInfo[zoneid_capture][gGang] = team_capture[0];
	                SaveGZ(zoneid_capture);
				    format(str, sizeof(str), "%s захватили территорию у банды %s в районе %s", gang_name[team_capture[0]-1], gang_name[team_capture[1]-1], zone_name);
			    	SendClientMessage(i, COLOR_ORANGE, str);
	                GangZoneHideForAll(zoneid_capture);
		            GangZoneShowForAll(zoneid_capture, GetGZColor(team_capture[0]));
	                gangzone[0] = 0, gangzone[1] = 0, gangzone[2] = 0, gangzone[3] = 0, gangzone[4] = 0;
					for(new territory = 0; territory < sizeof(ZoneInfo); territory++)
					{
					    switch(ZoneInfo[territory][gGang])
					    {
					        case 1: gangzone[0]++;
				            case 2: gangzone[1]++;
				            case 3: gangzone[2]++;
				            case 4: gangzone[3]++;
				            case 5: gangzone[4]++;
					    }
					}
					format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n\n\n{009900}Склад\nGrove Street", gangzone[0]);
				    Update3DTextLabelText(warehouses[1], 0xFFFFFFFF, str);

				    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{CC00FF}Склад\nThe Ballas", gangzone[1]);
				    Update3DTextLabelText(warehouses[2], 0xFFFFFFFF, str);

				    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{FFCD00}Склад\nLos Santos Vagos", gangzone[2]);
				    Update3DTextLabelText(warehouses[3], 0xFFFFFFFF, str);

				    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{00CCFF}Склад\nVarios Los Aztecas", gangzone[3]);
				    Update3DTextLabelText(warehouses[4], 0xFFFFFFFF, str);

				    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{6666FF}Склад\nThe Rifa", gangzone[4]);
				    Update3DTextLabelText(warehouses[5], 0xFFFFFFFF, str);
				}
	            TextDrawHideForPlayer(i, TD_Capture[0]);
	            TextDrawHideForPlayer(i, TD_Capture[1]);
	            TextDrawHideForPlayer(i, TD_Capture[2]);
	            TextDrawHideForPlayer(i, TD_Capture[3]);
	        }
	        zoneid_capture = 0;
	        capture = 0;
	        capture_time = 0;
		}
	}
}

stock SaveGZ(zoneid)
{
    new str[256];
    mysql_format(mysql_connection, str, sizeof(str), "UPDATE `gangzone` SET `X`='%f', `Y`='%f', `XX`='%f', `YY`='%f', `gangid`='%d' WHERE `id`='%d'", ZoneInfo[zoneid][gCoords][0], ZoneInfo[zoneid][gCoords][1], ZoneInfo[zoneid][gCoords][2], ZoneInfo[zoneid][gCoords][3], ZoneInfo[zoneid][gGang], zoneid);
    return mysql_tquery(mysql_connection, str, "", "");
}

stock VecToPoint(Float:radius, vecid, Float:x, Float:y, Float:z)
{
	new Float:oldposx, Float:oldposy, Float:oldposz;
	new Float:tempposx, Float:tempposy, Float:tempposz;
	GetVehiclePos(vecid, oldposx, oldposy, oldposz);
	tempposx = (oldposx -x);
	tempposy = (oldposy -y);
	tempposz = (oldposz -z);
	if (((tempposx < radius) && (tempposx > -radius)) && ((tempposy < radius) && (tempposy > -radius)) && ((tempposz < radius) && (tempposz > -radius))) return true;
	return 0;
}

stock ConvertTime(seconds)
{
	new tempstr[20];
 	new minutes = floatround(seconds/60);
  	seconds -= minutes*60;
   	format(tempstr, sizeof(tempstr), "%d:%02d", minutes, seconds);
    return tempstr;
}

stock GetPlayerSubnet(playerid, ip[], buffer[], size=sizeof(buffer))
{
    for(new i=0,dots=0; ; ++i)
    {
        switch(ip[i])
        {
            case '\0': break;
            case '.':
            {
                if(++dots == 2)
                {
                    buffer[i] = '\0';
                    break;
                }
			}
        }
	}
}

stock GetIpSubnet(buffer[])
{
    for(new i=0,dots=0; ; ++i)
        switch(buffer[i])
        {
            case '\0':
                break;
            case '.':
                if(++dots == 2)
                {
                    buffer[i] = '\0';
                    break;
                }
        }
}

stock SendAdminMessage(color, msg[], level)
{
	foreach(new i:Player)
	{
	    if(PlayerInfo[i][pAdmin] >= level && PlayerInfo[i][pAR] == 0) SendClientMessage(i, color, msg);
	}
	return true;
}

stock SendVipMessage(color, msg[])
{
	foreach(new i:Player)
	{
	    if(PlayerInfo[i][pVip] == 1 && PlayerInfo[i][pAR] == 0) SendClientMessage(i, color, msg);
	}
	return true;
}

stock GetPlayerSpeed(playerid)
{
	new Float:ST[4];
	if(IsPlayerInAnyVehicle(playerid)) GetVehicleVelocity(GetPlayerVehicleID(playerid), ST[0], ST[1], ST[2]);
	else GetPlayerVelocity(playerid, ST[0], ST[1], ST[2]);
	ST[3] = floatsqroot(floatpower(floatabs(ST[0]), 2.0) + floatpower(floatabs(ST[1]), 2.0) + floatpower(floatabs(ST[2]), 2.0)) * 100.0;
	return floatround(ST[3]);
}

stock SendGangMessage(gangid, color, msg[])
{
	foreach(new i:Player)
	{
	    if(PlayerInfo[i][pGang] == gangid && PlayerInfo[i][pAR] == 0 && PlayerInfo[i][pChatGang] == 1) SendClientMessage(i, color, msg);
	}
	return true;
}

stock PreloadAnimLib(playerid, animlib[])
{
   ApplyAnimation(playerid,animlib,"null",0.0,0,0,0,0,0);
   return 1;
}

stock AC_PlusPlayerHealth(playerid, Float:amount)
{
	new Float:real_hp;
	GetPlayerHealth(playerid, real_hp);
	new Float:new_hp;
 	new_hp = real_hp + amount;
  	if(new_hp > 100.0) new_hp = 100.0;
   	return SetPlayerHealth(playerid, new_hp);
}

stock AddPlayerToCheatPanel(playerid, type)
{
	new str[4];
	if(type == 1)
	{
	    for(new i = 11; i != 0; i--)
		{
		    if(i == 0) break;
			poolCheatsGM[i] = poolCheatsGM[i-1];
			format(str, sizeof(str), "%d", poolCheatsGM[i]);
			if(poolCheatsGM[i] == -1) format(str, sizeof(str), "_");
			TextDrawSetString(TD_ACGm[i], str);
		}
		poolCheatsGM[0] = playerid;
		format(str, sizeof(str), "%d", poolCheatsGM[0]);
		TextDrawSetString(TD_ACGm[0], str);
	}
	else
	{
	    for(new i = 11; i != 0; i--)
		{
		    if(i == 0) break;
			poolCheatsSH[i] = poolCheatsSH[i-1];
			format(str, sizeof(str), "%d", poolCheatsSH[i]);
			if(poolCheatsSH[i] == -1) format(str, sizeof(str), "_");
			TextDrawSetString(TD_ACSh[i], str);
		}
		poolCheatsSH[0] = playerid;
		format(str, sizeof(str), "%d", poolCheatsSH[0]);
		TextDrawSetString(TD_ACSh[0], str);
	}
	return true;
}

stock randomwithex(const max_value, ...)
{
	new result;
	rerandom: result = random(max_value + 1);
	for(new i = numargs() + 1; --i != 0;)
	{
		if(result == getarg(i))
		{
			goto rerandom;
		}
	}
	return result;
}

stock ShowPlayerPin(playerid)
{
	tempPIN[playerid][0] = EOS;
	new Float:poolpositions[10][2];
	new str[2];
	poolpositions[0][0] = 408.666656;
	poolpositions[0][1] = 184.592773;

	poolpositions[1][0] = 408.666656;
	poolpositions[1][1] = 220.022399;

	poolpositions[2][0] = 408.666656;
	poolpositions[2][1] = 256.281707;

	poolpositions[3][0] = 454.666656;
	poolpositions[3][1] = 184.348327;

	poolpositions[4][0] = 454.666656;
	poolpositions[4][1] = 220.192779;

	poolpositions[5][0] = 454.666656;
	poolpositions[5][1] = 256.037231;

	poolpositions[6][0] = 500.666656;
	poolpositions[6][1] = 184.518707;

	poolpositions[7][0] = 500.666656;
	poolpositions[7][1] = 219.948364;

	poolpositions[8][0] = 500.666656;
	poolpositions[8][1] = 256.207672;

	poolpositions[9][0] = 454.666656;
	poolpositions[9][1] = 292.296569;

	new Float:pooltextsizes[10];
	pooltextsizes[0] = 432.800030;
	pooltextsizes[1] = 432.800030;
	pooltextsizes[2] = 432.800030;
	pooltextsizes[3] = 478.799969;
	pooltextsizes[4] = 478.799969;
	pooltextsizes[5] = 478.799969;
	pooltextsizes[6] = 525.133312;
	pooltextsizes[7] = 525.133312;
	pooltextsizes[8] = 525.133312;
	pooltextsizes[9] = 478.799969;

	new wasnumber[10] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
	new tempnum;
	for(new i = 0; i != 10; i++)
	{
		tempnum = randomwithex(9, wasnumber[0], wasnumber[1], wasnumber[2], wasnumber[3], wasnumber[4], wasnumber[5], wasnumber[6], wasnumber[7], wasnumber[8], wasnumber[9]);
		wasnumber[i] = tempnum;
		format(str, sizeof(str), "%d", tempnum);
		TD_Pin[tempnum] = TextDrawCreate(poolpositions[i][0], poolpositions[i][1], str);
		TextDrawTextSize(TD_Pin[tempnum], pooltextsizes[i], 18.5);
		TextDrawLetterSize(TD_Pin[tempnum], 0.940332, 2.802966);
		TextDrawAlignment(TD_Pin[tempnum], 1);
		TextDrawColor(TD_Pin[tempnum], -1);
		TextDrawUseBox(TD_Pin[tempnum], true);
		TextDrawBoxColor(TD_Pin[tempnum], 2021095850);
		TextDrawSetShadow(TD_Pin[tempnum], 0);
		TextDrawSetOutline(TD_Pin[tempnum], 1);
		TextDrawBackgroundColor(TD_Pin[tempnum], 255);
		TextDrawFont(TD_Pin[tempnum], 1);
		TextDrawSetProportional(TD_Pin[tempnum], 1);
		TextDrawSetSelectable(TD_Pin[tempnum], true);
	}
	for(new i = 0; i != 10; i++) TextDrawShowForPlayer(playerid, TD_Pin[i]);
	SelectTextDraw(playerid, COLOR_BLUE);
	return Curr_TD[playerid] = TD_PINCODE;
}

stock CheckForCorrectPin(playerid, type)
{
    if(type == 1)
    {
	    new str[48];
	    format(str, sizeof(str), "PIN-код успешно установлен: {FFFF00}%s", tempPIN[playerid]);
	    SendClientMessage(playerid, COLOR_GREEN, str);
	    SendClientMessage(playerid, COLOR_GREEN, "Запомните или запишите это число");
	    CancelSelectTextDraw(playerid);
		PlayerInfo[playerid][pPin][0] = EOS;
	    strins(PlayerInfo[playerid][pPin], tempPIN[playerid], 0);
	    new query[96];
		mysql_format(mysql_connection, query, sizeof(query), "UPDATE `accounts` SET `pin`='%s', `typepin`=3 WHERE name='%s'", tempPIN[playerid], PlayerInfo[playerid][pName]);
		mysql_tquery(mysql_connection, query, "", "");
		for(new i = 0; i != 10; i++) TextDrawHideForPlayer(playerid, TD_Pin[i]);
		PlayerInfo[playerid][pAskForPin] = 3;
		return Curr_TD[playerid] = 0;
	}
	if(type == 2)
	{
		if(!strcmp(PlayerInfo[playerid][pPin], tempPIN[playerid], false))
		{
			new query[96];
	   		mysql_format(mysql_connection, query, sizeof(query), "SELECT * FROM `accounts` WHERE `name` = '%s'", PlayerInfo[playerid][pName]);
	     	mysql_tquery(mysql_connection, query, "UploadPlayerAccount","i", playerid);
			for(new i = 0; i != 10; i++) TextDrawHideForPlayer(playerid, TD_Pin[i]);
			return Curr_TD[playerid] = 0;
		}
		else
		{
			SendClientMessage(playerid, COLOR_RED, "PIN-код введён неверно. Доступ запрещён");
			SendClientMessage(playerid, COLOR_ORANGE, "Введите /q (/quit) чтобы выйти");
			CancelSelectTextDraw(playerid);
			for(new i = 0; i != 10; i++) TextDrawHideForPlayer(playerid, TD_Pin[i]);
			Curr_TD[playerid] = 0;
			return KickEx(playerid);
		}
	}
	if(type == 3)
	{
		if(!strcmp(PlayerInfo[playerid][pPin], tempPIN[playerid], false))
		{
			typePIN{playerid} = 1;
			for(new i = 0; i != 10; i++) TextDrawHideForPlayer(playerid, TD_Pin[i]);
			SendClientMessage(playerid, COLOR_YELLOW, "Наберите новый PIN-код");
			return ShowPlayerPin(playerid);
		}
		else
		{
			for(new i = 0; i != 10; i++) TextDrawHideForPlayer(playerid, TD_Pin[i]);
			CancelSelectTextDraw(playerid);
			SendClientMessage(playerid, COLOR_ORANGE, "PIN-код введён неверно");
			Curr_TD[playerid] = 0;
			return tempPIN[playerid][0] = EOS;
		}
	}
	return true;
}

stock ShowPlayerStats(playerid, statsid)
{
	new str[256];
	format(str, sizeof(str), "{ffffff}Имя:\t\t{0099FF}%s{ffffff}\n\
	Убийства:\t%d\n\
	Смерти:\t%d", PlayerInfo[statsid][pName], PlayerInfo[statsid][pKills], PlayerInfo[statsid][pDeaths]);
	return ShowPlayerDialog(playerid, dStats, DIALOG_STYLE_MSGBOX, "{CC9900}Статистика игрока", str, "Закрыть", "");
}

stock SetPlayerSpawnGhetto(playerid)
{
    switch(PlayerInfo[playerid][pGang])
	{
	    case GANG_GROVE:
	    {
	        SetPlayerPos(playerid, 2450.3474,-1687.9340,1013.5078);
	        SetPlayerFacingAngle(playerid, 178.6);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 2);
	        SetPlayerVirtualWorld(playerid, 2);
	        SetPlayerColor(playerid, COLOR_GROVE);
	    }
	    case GANG_BALLAS:
	    {
	        SetPlayerPos(playerid, -50.1813,1400.0217,1084.4297);
	        SetPlayerFacingAngle(playerid, 358.7);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 8);
	        SetPlayerVirtualWorld(playerid, 2);
	        SetPlayerColor(playerid, COLOR_BALLAS);
	    }
	    case GANG_VAGOS:
	    {
	        SetPlayerPos(playerid, 330.8807,1128.4902,1083.8828);
	        SetPlayerFacingAngle(playerid, 180.0);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 5);
	        SetPlayerVirtualWorld(playerid, 2);
	        SetPlayerColor(playerid, COLOR_VAGOS);
	    }
	    case GANG_AZTECAS:
	    {
	        SetPlayerPos(playerid, 223.8616,1251.1467,1082.1481);
	        SetPlayerFacingAngle(playerid, 87.3);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 2);
	        SetPlayerVirtualWorld(playerid, 2);
	        SetPlayerColor(playerid, COLOR_AZTECAS);
	    }
	    case GANG_RIFA:
	    {
	        SetPlayerPos(playerid, -59.0675,1364.3116,1080.2109);
	        SetPlayerFacingAngle(playerid, 85.9);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 6);
	        SetPlayerVirtualWorld(playerid, 2);
	        SetPlayerColor(playerid, COLOR_RIFA);
	    }
	    default: SetPlayerColor(playerid, 0xFFFFFFF);
	}
}

stock SetPlayerSpawnRoom(playerid)
{
	switch(RoomInfo[PlayerInfo[playerid][pRoom]][rMap])
	{
	    case 1:
	    {
	        new rand = random(8);
			PlayerInfo[playerid][pGang] = 0;
			PlayerInfo[playerid][pArena] = 0;
	        SetPlayerPos(playerid, posvillage[rand][0], posvillage[rand][1], posvillage[rand][2]);
	        SetPlayerVirtualWorld(playerid, PlayerInfo[playerid][pRoom]+500);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 0);
			for(new i = 0; i != 6; i++)
			{
			    if(RoomInfo[PlayerInfo[playerid][pRoom]][rGun][i] == 4) GivePlayerWeapon(playerid, 4, 1);
			    if(RoomInfo[PlayerInfo[playerid][pRoom]][rGun][i] == 9) GivePlayerWeapon(playerid, 9, 1);
			    if(RoomInfo[PlayerInfo[playerid][pRoom]][rGun][i] == 16) GivePlayerWeapon(playerid, 16, 10);
			    if(RoomInfo[PlayerInfo[playerid][pRoom]][rGun][i] == 24) GivePlayerWeapon(playerid, 24, 250);
			    if(RoomInfo[PlayerInfo[playerid][pRoom]][rGun][i] == 25) GivePlayerWeapon(playerid, 25, 100);
				if(RoomInfo[PlayerInfo[playerid][pRoom]][rGun][i] == 31) GivePlayerWeapon(playerid, 31, 500);
				if(RoomInfo[PlayerInfo[playerid][pRoom]][rGun][i] == 34) GivePlayerWeapon(playerid, 34, 100);
				if(RoomInfo[PlayerInfo[playerid][pRoom]][rGun][i] == 38) GivePlayerWeapon(playerid, 38, 2000);
			}
	        return SetPlayerColor(playerid, COLOR_ADMMSG);
	    }
	}
	return true;
}

stock SetPlayersSpawnPvp(playerid, pvpID)
{
	new rand = random(8);
	PlayerInfo[playerid][pGang] = 0;
	PlayerInfo[playerid][pArena] = 0;
	PlayerInfo[playerid][pRoom] = -1;
	PlayerInfo[pvpID][pGang] = 0;
	PlayerInfo[pvpID][pArena] = 0;
	PlayerInfo[pvpID][pRoom] = -1;
	SetPlayerPos(playerid, posvillage[rand][0], posvillage[rand][1], posvillage[rand][2]);
	SetPlayerVirtualWorld(playerid, playerid+600);
	SetCameraBehindPlayer(playerid);
	SetPlayerInterior(playerid, 0);
	rand = random(8);
	SetPlayerPos(pvpID, posvillage[rand][0], posvillage[rand][1], posvillage[rand][2]);
	SetPlayerVirtualWorld(pvpID, playerid+600);
	SetCameraBehindPlayer(pvpID);
	SetPlayerInterior(pvpID, 0);
	SetPlayerColor(pvpID, COLOR_ADMMSG);

	isOffered{playerid} = 0;
	isOffered{pvpID} = 0;
	isOfferedTo{playerid} = 0;
	isOfferedTo{pvpID} = 0;

	startPVP{playerid} = 1;
	startPVP{pvpID} = 1;

	PlayerPlaySound(playerid, 1056, 0.0, 0.0, 0.0);
	PlayerPlaySound(pvpID, 1056, 0.0, 0.0, 0.0);

	if(GetPVarInt(playerid, "GunPVP") == 0) GivePlayerWeapon(playerid, 24, 500), GivePlayerWeapon(pvpID, 24, 500);

	return SetPlayerColor(playerid, COLOR_ADMMSG);
}

stock SetPlayerSpawnArena(playerid)
{
    switch(PlayerInfo[playerid][pArena])
	{
	    case 1:
	    {
	        new rand = random(8);
			PlayerInfo[playerid][pGang] = 0;
	        SetPlayerPos(playerid, posvillage[rand][0], posvillage[rand][1], posvillage[rand][2]);
	        SetPlayerVirtualWorld(playerid, 1);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 0);
	        GiveWeaponForArena(playerid);
	        return SetPlayerColor(playerid, COLOR_ADMMSG);
	    }
	    case 2:
	    {
	        new rand = random(8);
			PlayerInfo[playerid][pGang] = 0;
	        SetPlayerPos(playerid, posvillage[rand][0], posvillage[rand][1], posvillage[rand][2]);
	        SetPlayerVirtualWorld(playerid, 1);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 0);
	        GiveWeaponForArena(playerid);
	        return SetPlayerColor(playerid, COLOR_ADMMSG);
	    }
	    case 3:
	    {
	        new rand = random(8);
			PlayerInfo[playerid][pGang] = 0;
	        SetPlayerPos(playerid, posvillage[rand][0], posvillage[rand][1], posvillage[rand][2]);
	        SetPlayerVirtualWorld(playerid, 1);
	        SetCameraBehindPlayer(playerid);
	        SetPlayerInterior(playerid, 0);
	        GiveWeaponForArena(playerid);
	        return SetPlayerColor(playerid, COLOR_ADMMSG);
	    }
	}
	return true;
}

stock ShowActorAnimList(playerid)
{
	new anims[2048];
	strcat(anims, "1. Махать рукой\n2. Лечь на землю\n3. Походка пьяного\n4. Кувыркаться\n");
	strcat(anims, "5. Попрощаться\n6. Читать рэп\n7. Укрыться\n8. Подложить бомбу\n");
	strcat(anims, "9. Надеть маску\n10. Вытянуть руку перед собой\n11. Сложить руки вместе\n");
	strcat(anims, "12. Съел что-то не то...\n13. Перекусить\n14. Шлёпнуть кому-то по заднице\n");
	strcat(anims, "15. Предложить наркотики\n16. Эффект электрошокера\n17. Мужское курение\n");
	strcat(anims, "18. Женское курение\n19. Присесть\n20. Восточное единоборство\n21. Выпить напиток\n");
	strcat(anims, "22. Танец на одной ноге\n23. Поза вратаря\n25. Facepalm\n");
	strcat(anims, "26. Элемент восточного танца\n27. Позвать кого-то\n28. Руки вверх!\n");
	strcat(anims, "29. Спать на боку\n30. Спать на спине\n31. Смотреть по сторонам\n");
	strcat(anims, "32. Облокотиться на бок\n33. Толкнуть боком\n34. Раздумье\n");
	strcat(anims, "35. Лечь, оперевшись на ладонь\n36. Сесть на стул\n");
	strcat(anims, "37. Сидеть уставшим за компьютером\n38. Сидеть за столом\n");
	strcat(anims, "39. Сидеть и печатать\n40. Взять что-то и рассмотреть\n");
	strcat(anims, "41. Сесть, закинув ногу на ногу\n42. Отказаться от чего-либо\n");
	strcat(anims, "43. Поцелуй 1\n44. Поцелуй 2\n45. Поцелуй 3\n");
	strcat(anims, "46. Размахивать руками на месте\n47. Искуственное дыхание\n");
	strcat(anims, "48. Пощёчины для лежачего\n49. Подглядывать через что-то\n");
	strcat(anims, "50. Движение тореодора\n51. Сесть на стул (2)\n52. Сесть на стул (3)\n");
	strcat(anims, "53. Смотреть наверх\n54. Указать рукой наверх\n55. Быть в страхе\n");
	strcat(anims, "56. Призывать к чему-либо\n57. Сходить по-маленькому\n58. Гангстерский жест\n");
	strcat(anims, "59. Голосовать на остановке\n60. Удар ногой\n61. Стучаться в дверь\n");
	strcat(anims, "62. Устроить бунт\n63. Пританцовывать\n64. Лечь на землю (2)\n");
	strcat(anims, "64. Плохое самочувствие\n65. Приветствие 1\n66. Приветствие 2\n");
    strcat(anims, "67. Приветствие 3\n68. Приветствие 4");
    ShowPlayerDialog(playerid, dActorAnim, DIALOG_STYLE_LIST, "{ffdd00}Анимации", anims, "Выбрать", "Закрыть");
	return true;
}

stock SelectAnimation(actorid, animation)
{
	switch(animation)
 	{
        case 0: ApplyActorAnimation(actorid, !"ON_LOOKERS", !"wave_loop" ,4.1,1,0,0,0,0);
        case 1: ApplyActorAnimation(actorid, !"BEACH", !"bather" ,4.1,1,0,0,0,0);
        case 2: ApplyActorAnimation(actorid, !"ped", !"WALK_drunk" ,4.1,1,1,1,0,0);
        case 3: ApplyActorAnimation(actorid, !"ped", !"Crouch_Roll_L" , 4.1,1,1,1,0,0);
        case 4: ApplyActorAnimation(actorid, !"ped", !"endchat_03" ,4.1,1,0,0,0,0);
        case 5: ApplyActorAnimation(actorid, !"benchpress", !"gym_bp_celebrate" ,4.1,1,0,0,0,0);
        case 6: ApplyActorAnimation(actorid, !"ped", !"cower" ,4.1,1,0,0,0,0);
        case 7: ApplyActorAnimation(actorid, !"BOMBER", !"BOM_Plant" ,4.1,0,0,0,0,0);
        case 8: ApplyActorAnimation(actorid, !"SHOP", !"ROB_Shifty" ,4.1,0,0,0,0,0);
        case 9: ApplyActorAnimation(actorid, !"SHOP", !"ROB_Loop_Threat" ,4.1,1,0,0,0,0);
        case 10: ApplyActorAnimation(actorid, !"COP_AMBIENT", !"Coplook_loop" ,4.1,1,0,0,0,0);
        case 11: ApplyActorAnimation(actorid, !"FOOD", !"EAT_Vomit_P" ,4.1,0,0,0,0,0);
        case 12: ApplyActorAnimation(actorid, !"FOOD", !"EAT_Burger" ,4.1,0,0,0,0,0);
        case 13: ApplyActorAnimation(actorid, !"SWEET", !"sweet_ass_slap" ,4.1,0,0,0,0,0);
        case 14: ApplyActorAnimation(actorid, !"DEALER", !"DEALER_DEAL" ,4.1,0,0,0,0,0);
        case 15: ApplyActorAnimation(actorid, !"CRACK", !"crckdeth2" ,4.1,1,0,0,0,0);
        case 16: ApplyActorAnimation(actorid, !"LOWRIDER", !"M_smklean_loop" ,4.1,1,0,0,0,0);
        case 17: ApplyActorAnimation(actorid, !"LOWRIDER", !"F_smklean_loop" ,4.1,1,0,0,0,0);
        case 18: ApplyActorAnimation(actorid, !"BEACH", !"ParkSit_M_loop" ,4.1,1,0,0,0,0);
        case 19: ApplyActorAnimation(actorid, !"PARK", !"Tai_Chi_Loop" ,4.1,1,0,0,0,0);
        case 20: ApplyActorAnimation(actorid, !"BAR", !"dnk_stndF_loop" ,4.1,1,0,0,0,0);
        case 21: ApplyActorAnimation(actorid, !"DANCING", !"DAN_Right_A" ,4.1,1,0,0,0,0);
        case 22: ApplyActorAnimation(actorid, !"BSKTBALL", !"BBALL_def_loop" ,4.1,1,0,0,0,0);
        case 23: ApplyActorAnimation(actorid, !"MISC", !"plyr_shkhead" ,4.1,0,0,0,0,0);
        case 24: ApplyActorAnimation(actorid, !"BSKTBALL", !"BBALL_idle" ,4.1,0,0,0,0,0);
        case 25: ApplyActorAnimation(actorid, !"CAMERA", !"camstnd_cmon" ,4.1,1,0,0,0,0);
        case 26: ApplyActorAnimation(actorid, !"SHOP", !"SHP_Rob_HandsUP" ,4.1,1,0,0,0,0);
        case 27: ApplyActorAnimation(actorid, !"CRACK", !"crckidle2" ,4.1,1,0,0,0,0);
        case 28: ApplyActorAnimation(actorid, !"CRACK", !"crckidle4" ,4.1,1,0,0,0,0);
        case 29: ApplyActorAnimation(actorid, !"DEALER", !"DEALER_IDLE" ,4.1,1,0,0,0,0);
        case 30: ApplyActorAnimation(actorid, !"GANGS", !"leanIDLE" ,4.1,1,0,0,0,0);
        case 31: ApplyActorAnimation(actorid, !"GANGS", !"shake_carSH" ,4.1,0,0,0,0,0);
        case 32: ApplyActorAnimation(actorid, !"GANGS", !"smkcig_prtl" ,4.1,0,0,0,0,0);
        case 33: ApplyActorAnimation(actorid, !"BEACH", !"ParkSit_W_loop" ,4.1,1,0,0,0,0);
        case 34: ApplyActorAnimation(actorid, !"INT_HOUSE", !"LOU_Loop" ,4.1,1,0,0,0,0);
        case 35: ApplyActorAnimation(actorid, !"INT_OFFICE", !"OFF_Sit_Bored_Loop" ,4.1,1,0,0,0,0);
        case 36: ApplyActorAnimation(actorid, !"INT_OFFICE", !"OFF_Sit_Idle_Loop" ,4.1,1,0,0,0,0);
        case 37: ApplyActorAnimation(actorid, !"INT_OFFICE", !"OFF_Sit_Type_Loop" ,4.1,1,0,0,0,0);
        case 38: ApplyActorAnimation(actorid, !"INT_SHOP", !"shop_shelf" ,4.1,1,0,0,0,0);
        case 39: ApplyActorAnimation(actorid, !"JST_BUISNESS", !"girl_02" ,4.1,1,0,0,0,0);
        case 40: ApplyActorAnimation(actorid, !"KISSING", !"GF_StreetArgue_02" ,4.1,0,0,0,0,0);
        case 41: ApplyActorAnimation(actorid, !"KISSING", !"Grlfrd_Kiss_01" ,4.1,0,0,0,0,0);
        case 42: ApplyActorAnimation(actorid, !"KISSING", !"Grlfrd_Kiss_02" ,4.1,0,0,0,0,0);
        case 43: ApplyActorAnimation(actorid, !"KISSING", !"Grlfrd_Kiss_03" ,4.1,0,0,0,0,0);
        case 44: ApplyActorAnimation(actorid, !"LOWRIDER", !"RAP_B_Loop" ,4.1,1,0,0,0,0);
        case 45: ApplyActorAnimation(actorid, !"MEDIC", !"CPR" ,4.1,1,0,0,0,0);
        case 46: ApplyActorAnimation(actorid, !"MISC", !"bitchslap" ,4.1,1,0,0,0,0);
        case 47: ApplyActorAnimation(actorid, !"MISC", !"bng_wndw" ,4.1,1,0,0,0,0);
        case 48: ApplyActorAnimation(actorid, !"MISC", !"KAT_Throw_K" ,4.1,0,0,0,0,0);
        case 49: ApplyActorAnimation(actorid, !"MISC", !"SEAT_LR" ,4.1,1,0,0,0,0);
        case 50: ApplyActorAnimation(actorid, !"ped", !"SEAT_idle" ,4.1,1,0,0,0,0);
        case 51: ApplyActorAnimation(actorid, !"ON_LOOKERS", !"lkup_loop" ,4.1,1,0,0,0,0);
        case 52: ApplyActorAnimation(actorid, !"ON_LOOKERS", !"Pointup_loop" ,4.1,1,0,0,0,0);
        case 53: ApplyActorAnimation(actorid, !"ON_LOOKERS", !"panic_loop" ,4.1,1,0,0,0,0);
        case 54: ApplyActorAnimation(actorid, !"ON_LOOKERS", !"shout_02" ,4.1,1,0,0,0,0);
        case 55: ApplyActorAnimation(actorid, !"PAULNMAC", !"Piss_loop" ,4.1,1,0,0,0,0);
        case 56: ApplyActorAnimation(actorid, !"GHANDS", !"gsign1LH" ,4.1,1,0,0,0,0);
        case 57: ApplyActorAnimation(actorid, !"ped", !"IDLE_taxi" ,4.1,1,0,0,0,0);
        case 58: ApplyActorAnimation(actorid, !"POLICE", !"Door_Kick" ,4.1,0,0,0,0,0);
        case 59: ApplyActorAnimation(actorid, !"POLICE", !"CopTraf_Stop" ,4.1,1,0,0,0,0);
        case 60: ApplyActorAnimation(actorid, !"RIOT", !"RIOT_ANGRY_B" ,4.1,1,0,0,0,0);
        case 61: ApplyActorAnimation(actorid, !"LOWRIDER", !"RAP_C_Loop" ,4.1,1,0,0,0,0);
        case 62: ApplyActorAnimation(actorid, !"SWAT", !"gnstwall_injurd" ,4.1,1,0,0,0,0);
        case 63: ApplyActorAnimation(actorid, !"SWEET", !"Sweet_injuredloop" ,4.1,1,0,0,0,0);
        case 64: ApplyActorAnimation(actorid, !"RIOT", !"RIOT_ANGRY" ,4.1,1,0,0,0,0);
        case 65: ApplyActorAnimation(actorid, !"GHANDS", !"gsign2" ,4.1,1,0,0,0,0);
        case 66: ApplyActorAnimation(actorid, !"GHANDS", !"gsign4" ,4.1,1,0,0,0,0);
        case 67: ApplyActorAnimation(actorid, !"GHANDS", !"gsign5" ,4.1,1,0,0,0,0);
	}
}

stock ShowDialogGunsRoom(playerid)
{
    new weaponname[48];
	new str[196];
	strcat(str, "Параметр\tЗначение\n");
	for(new i = 0; i != 6; i++)
	{
 		if(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][i] == 0)
 		{
 			format(weaponname, sizeof(weaponname), "%d слот\tНету\n", i+1);
			strcat(str, weaponname);
 		}
 		if(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][i] != 0)
 		{
 			GetWeaponName(RoomInfo[PlayerInfo[playerid][pRoomCreateID]][rGun][i], weaponname, 48);
			format(weaponname, sizeof(weaponname), "%d слот\t%s\n", i+1, weaponname);
			strcat(str, weaponname);
 		}
	}
	return ShowPlayerDialog(playerid, dRoomWeapons, DIALOG_STYLE_TABLIST_HEADERS, "{ffdd00}Оружие комнаты", str, "Выбрать", "Назад");
}

stock GiveWeaponForArena(playerid)
{
	switch(PlayerInfo[playerid][pArena])
	{
	    case 1: return GivePlayerWeapon(playerid, 24, 500);
	    case 2:
	    {
			GivePlayerWeapon(playerid, 24, 500);
			GivePlayerWeapon(playerid, 25, 500);
			return GivePlayerWeapon(playerid, 31, 500);
	    }
	    case 3: return GivePlayerWeapon(playerid, 24, 500);
	}
	return true;
}

stock ShowInfoAboutRoom(playerid, roomid)
{
	if(RoomInfo[roomid][rID] == -1) return ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{ff6600}Ошибка", "{ffffff}Данная комната не была создана", "Закрыть", "");
    new str[386];
    new status[24];
    new map[48];
    new tempstr[64];
    new weapname[48];
    if(RoomInfo[roomid][rClosed] == 0) status = "{00CC99}Открыто";
    if(RoomInfo[roomid][rClosed] == 1) status = "{FF5C33}Закрыто";
    if(RoomInfo[roomid][rMap] == 1) map = "Заброшеная деревня";
    format(str, sizeof(str), "\
    {ffffff}Создал:{66CCFF} %s\n\
    {ffffff}Статус: %s\n\
    {ffffff}ID в игре:{9999FF} %d\n\
    {ffffff}Карта:{85E085} %s\n", PlayerInfo[RoomInfo[roomid][rCreateID]][pName], status, RoomInfo[roomid][rCreateID], map);
    if(RoomInfo[roomid][rOnline] == 0) strcat(str, "{ffffff}Онлайн:{FFA64D} 0\n");
    if(RoomInfo[roomid][rOnline] != 0)
    {
	    format(tempstr, sizeof(tempstr), "{ffffff}Онлайн: {00CC99}%d\n", RoomInfo[roomid][rOnline]);
	    strcat(str, tempstr);
    }
    for(new i = 0; i != 6; i++)
	{
		if(RoomInfo[roomid][rGun][i] == 0) continue;
		if(RoomInfo[roomid][rGun][i] != 0)
		{
			GetWeaponName(RoomInfo[roomid][rGun][i], weapname, 48);
			format(tempstr, sizeof(tempstr), "{ffffff}%d оружие: {66CCFF}%s\n", i+1, weapname);
			strcat(str, tempstr);
		}
	}
	return ShowPlayerDialog(playerid, dRoomInfo, DIALOG_STYLE_MSGBOX, "{ffdd00}Информация о комнате", str, "Зайти", "Назад");
}

stock SelectPlayerAnimation(const playerid, const animation)
{
	switch(animation)
 	{
        case 0: SetPlayerSpecialAction(playerid, SPECIAL_ACTION_DANCE1);
        case 1: SetPlayerSpecialAction(playerid, SPECIAL_ACTION_DANCE2);
        case 2: SetPlayerSpecialAction(playerid, SPECIAL_ACTION_DANCE3);
        case 3: SetPlayerSpecialAction(playerid, SPECIAL_ACTION_DANCE4);
        case 4: ApplyAnimation(playerid, !"DANCING", !"DAN_Left_A" ,4.1,1,0,0,0,0,0);
        case 5: ApplyAnimation(playerid, !"DANCING", !"dnce_M_a" ,4.1,1,0,0,0,0,0);
        case 6: ApplyAnimation(playerid, !"ON_LOOKERS", !"wave_loop" ,4.1,1,0,0,0,0,0);
        case 7: ApplyAnimation(playerid, !"BEACH", !"bather" ,4.1,1,0,0,0,0,0);
        case 8: ApplyAnimation(playerid, !"ped", !"WALK_drunk" ,4.1,1,1,1,0,0,0);
        case 9: ApplyAnimation(playerid, !"ped", !"Crouch_Roll_L" , 4.1,1,1,1,0,0,0);
        case 10: ApplyAnimation(playerid, !"ped", !"endchat_03" ,4.1,1,0,0,0,0,0);
        case 11: ApplyAnimation(playerid, !"benchpress", !"gym_bp_celebrate" ,4.1,1,0,0,0,0,0);
        case 12: ApplyAnimation(playerid, !"ped", !"cower" ,4.1,1,0,0,0,0,0);
        case 13: ApplyAnimation(playerid, !"BOMBER", !"BOM_Plant" ,4.1,0,0,0,0,0,0);
        case 14: ApplyAnimation(playerid, !"SHOP", !"ROB_Shifty" ,4.1,0,0,0,0,0,0);
        case 15: ApplyAnimation(playerid, !"SHOP", !"ROB_Loop_Threat" ,4.1,1,0,0,0,0,0);
        case 16: ApplyAnimation(playerid, !"COP_AMBIENT", !"Coplook_loop" ,4.1,1,0,0,0,0,0);
        case 17: ApplyAnimation(playerid, !"FOOD", !"EAT_Vomit_P" ,4.1,0,0,0,0,0,0);
        case 18: ApplyAnimation(playerid, !"FOOD", !"EAT_Burger" ,4.1,0,0,0,0,0,0);
        case 19: ApplyAnimation(playerid, !"SWEET", !"sweet_ass_slap" ,4.1,0,0,0,0,0,0);
        case 20: ApplyAnimation(playerid, !"DEALER", !"DEALER_DEAL" ,4.1,0,0,0,0,0,0);
        case 21: ApplyAnimation(playerid, !"CRACK", !"crckdeth2" ,4.1,1,0,0,0,0,0);
        case 22: ApplyAnimation(playerid, !"LOWRIDER", !"M_smklean_loop" ,4.1,1,0,0,0,0,0);
        case 23: ApplyAnimation(playerid, !"LOWRIDER", !"F_smklean_loop" ,4.1,1,0,0,0,0,0);
        case 24: ApplyAnimation(playerid, !"BEACH", !"ParkSit_M_loop" ,4.1,1,0,0,0,0,0);
        case 25: ApplyAnimation(playerid, !"PARK", !"Tai_Chi_Loop" ,4.1,1,0,0,0,0,0);
        case 26: ApplyAnimation(playerid, !"BAR", !"dnk_stndF_loop" ,4.1,1,0,0,0,0,0);
        case 27: ApplyAnimation(playerid, !"DANCING", !"DAN_Right_A" ,4.1,1,0,0,0,0,0);
        case 28: ApplyAnimation(playerid, !"BSKTBALL", !"BBALL_def_loop" ,4.1,1,0,0,0,0,0);
        case 29: ApplyAnimation(playerid, !"MISC", !"plyr_shkhead" ,4.1,0,0,0,0,0,0);
        case 30: ApplyAnimation(playerid, !"BSKTBALL", !"BBALL_idle" ,4.1,0,0,0,0,0,0);
        case 31: ApplyAnimation(playerid, !"CAMERA", !"camstnd_cmon" ,4.1,1,0,0,0,0,0);
        case 32: ApplyAnimation(playerid, !"SHOP", !"SHP_Rob_HandsUP" ,4.1,1,0,0,0,0,0);
        case 33: ApplyAnimation(playerid, !"CRACK", !"crckidle2" ,4.1,1,0,0,0,0,0);
        case 34: ApplyAnimation(playerid, !"CRACK", !"crckidle4" ,4.1,1,0,0,0,0,0);
        case 35: ApplyAnimation(playerid, !"DEALER", !"DEALER_IDLE" ,4.1,1,0,0,0,0,0);
        case 36: ApplyAnimation(playerid, !"GANGS", !"leanIDLE" ,4.1,1,0,0,0,0,0);
        case 37: ApplyAnimation(playerid, !"GANGS", !"shake_carSH" ,4.1,0,0,0,0,0,0);
        case 38: ApplyAnimation(playerid, !"GANGS", !"smkcig_prtl" ,4.1,0,0,0,0,0,0);
        case 39: ApplyAnimation(playerid, !"BEACH", !"ParkSit_W_loop" ,4.1,1,0,0,0,0,0);
        case 40: ApplyAnimation(playerid, !"INT_HOUSE", !"LOU_Loop" ,4.1,1,0,0,0,0,0);
        case 41: ApplyAnimation(playerid, !"INT_OFFICE", !"OFF_Sit_Bored_Loop" ,4.1,1,0,0,0,0,0);
        case 42: ApplyAnimation(playerid, !"INT_OFFICE", !"OFF_Sit_Idle_Loop" ,4.1,1,0,0,0,0,0);
        case 43: ApplyAnimation(playerid, !"INT_OFFICE", !"OFF_Sit_Type_Loop" ,4.1,1,0,0,0,0,0);
        case 44: ApplyAnimation(playerid, !"INT_SHOP", !"shop_shelf" ,4.1,1,0,0,0,0,0);
        case 45: ApplyAnimation(playerid, !"JST_BUISNESS", !"girl_02" ,4.1,1,0,0,0,0,0);
        case 46: ApplyAnimation(playerid, !"KISSING", !"GF_StreetArgue_02" ,4.1,0,0,0,0,0,0);
        case 47: ApplyAnimation(playerid, !"KISSING", !"Grlfrd_Kiss_01" ,4.1,0,0,0,0,0,0);
        case 48: ApplyAnimation(playerid, !"KISSING", !"Grlfrd_Kiss_02" ,4.1,0,0,0,0,0,0);
        case 49: ApplyAnimation(playerid, !"KISSING", !"Grlfrd_Kiss_03" ,4.1,0,0,0,0,0,0);
        case 50: ApplyAnimation(playerid, !"LOWRIDER", !"RAP_B_Loop" ,4.1,1,0,0,0,0,0);
        case 51: ApplyAnimation(playerid, !"MEDIC", !"CPR" ,4.1,1,0,0,0,0,0);
        case 52: ApplyAnimation(playerid, !"MISC", !"bitchslap" ,4.1,1,0,0,0,0,0);
        case 53: ApplyAnimation(playerid, !"MISC", !"bng_wndw" ,4.1,1,0,0,0,0,0);
        case 54: ApplyAnimation(playerid, !"MISC", !"KAT_Throw_K" ,4.1,0,0,0,0,0,0);
        case 55: ApplyAnimation(playerid, !"MISC", !"SEAT_LR" ,4.1,1,0,0,0,0,0);
        case 56: ApplyAnimation(playerid, !"ped", !"SEAT_idle" ,4.1,1,0,0,0,0,0);
        case 57: ApplyAnimation(playerid, !"ON_LOOKERS", !"lkup_loop" ,4.1,1,0,0,0,0,0);
        case 58: ApplyAnimation(playerid, !"ON_LOOKERS", !"Pointup_loop" ,4.1,1,0,0,0,0,0);
        case 59: ApplyAnimation(playerid, !"ON_LOOKERS", !"panic_loop" ,4.1,1,0,0,0,0,0);
        case 60: ApplyAnimation(playerid, !"ON_LOOKERS", !"shout_02" ,4.1,1,0,0,0,0,0);
        case 61: ApplyAnimation(playerid, !"PAULNMAC", !"Piss_loop" ,4.1,1,0,0,0,0,0);
        case 62: ApplyAnimation(playerid, !"GHANDS", !"gsign1LH" ,4.1,1,0,0,0,0,0);
        case 63: ApplyAnimation(playerid, !"ped", !"IDLE_taxi" ,4.1,1,0,0,0,0,0);
        case 64: ApplyAnimation(playerid, !"POLICE", !"Door_Kick" ,4.1,0,0,0,0,0,0);
        case 65: ApplyAnimation(playerid, !"POLICE", !"CopTraf_Stop" ,4.1,1,0,0,0,0,0);
        case 66: ApplyAnimation(playerid, !"RIOT", !"RIOT_ANGRY_B" ,4.1,1,0,0,0,0,0);
        case 67: ApplyAnimation(playerid, !"LOWRIDER", !"RAP_C_Loop" ,4.1,1,0,0,0,0,0);
        case 68: ApplyAnimation(playerid, !"SWAT", !"gnstwall_injurd" ,4.1,1,0,0,0,0,0);
        case 69: ApplyAnimation(playerid, !"SWEET", !"Sweet_injuredloop" ,4.1,1,0,0,0,0,0);
        case 70: ApplyAnimation(playerid, !"RIOT", !"RIOT_ANGRY" ,4.1,1,0,0,0,0,0);
        case 71: ApplyAnimation(playerid, !"GHANDS", !"gsign2" ,4.1,1,0,0,0,0,0);
        case 72: ApplyAnimation(playerid, !"GHANDS", !"gsign4" ,4.1,1,0,0,0,0,0);
        case 73: ApplyAnimation(playerid, !"GHANDS", !"gsign5" ,4.1,1,0,0,0,0,0);
        default: return ShowPlayerDialog(playerid, dNoActions, DIALOG_STYLE_MSGBOX, "{ffdd00}Информация", "{ffffff}Для быстрого запуска нужной анимации можно использовать{66cc33} /anim(list) [номер анимации из списка]", "Закрыть", "");
	}
	if(animation >= 4) TextDrawShowForPlayer(playerid, TD_AnimStop);
	SetPVarInt(playerid, "WasAnim", 1);
	return true;
}

stock PreloadAllAnimLibs(playerid)
{
	PreloadAnimLib(playerid,"BAR");
	PreloadAnimLib(playerid,"BEACH");
	PreloadAnimLib(playerid,"benchpress");
	PreloadAnimLib(playerid,"BSKTBALL");
	PreloadAnimLib(playerid,"CAMERA");
	PreloadAnimLib(playerid,"COP_AMBIENT");
	PreloadAnimLib(playerid,"CRACK");
	PreloadAnimLib(playerid,"DANCING");
	PreloadAnimLib(playerid,"DEALER");
	PreloadAnimLib(playerid,"FOOD");
	PreloadAnimLib(playerid,"GANGS");
	PreloadAnimLib(playerid,"GHANDS");
	PreloadAnimLib(playerid,"INT_HOUSE");
	PreloadAnimLib(playerid,"INT_OFFICE");
	PreloadAnimLib(playerid,"INT_SHOP");
	PreloadAnimLib(playerid,"JST_BUISNESS");
	PreloadAnimLib(playerid,"KISSING");
	PreloadAnimLib(playerid,"LOWRIDER");
	PreloadAnimLib(playerid,"MEDIC");
	PreloadAnimLib(playerid,"MISC");
	PreloadAnimLib(playerid,"ON_LOOKERS");
	PreloadAnimLib(playerid,"PAULNMAC");
	PreloadAnimLib(playerid,"ped");
	PreloadAnimLib(playerid,"POLICE");
	PreloadAnimLib(playerid,"RIOT");
	PreloadAnimLib(playerid,"SHOP");
	PreloadAnimLib(playerid,"SWAT");
	PreloadAnimLib(playerid,"SWEET");
	PreloadAnimLib(playerid,"MEDIC");
	PreloadAnimLib(playerid,"BOMBER");
	PreloadAnimLib(playerid,"PARK");
	PreloadAnimLib(playerid,"PED");
  	return 1;
}

stock DeleteRoom(roomid)
{
    RoomInfo[roomid][rID] = -1;
    RoomInfo[roomid][rPassword] = 0;
    RoomInfo[roomid][rCreateID] = -1;
    RoomInfo[roomid][rMap] = 0;
    RoomInfo[roomid][rOnline] = 0;
    RoomInfo[roomid][rGun][0] = 0;
    RoomInfo[roomid][rGun][1] = 0;
    RoomInfo[roomid][rGun][2] = 0;
    RoomInfo[roomid][rGun][3] = 0;
    RoomInfo[roomid][rGun][4] = 0;
    RoomInfo[roomid][rGun][5] = 0;
    return PlayerInfo[roomid][pRoomCreateID] = -1;
}

CMD:capture(playerid, params[])
{
    if(capture == 1) return SendClientMessage(playerid, COLOR_GREY, "Уже происходит захват одной из зон. Дождитесь окончания захвата");
	for(new i = 0; i != sizeof(ZoneInfo); i++)
	{
		if(IsPlayerInGZ(playerid, ZoneInfo[i][gCoords][0], ZoneInfo[i][gCoords][1], ZoneInfo[i][gCoords][2], ZoneInfo[i][gCoords][3]))
		{
		    if(ZoneInfo[i][gID] >= 104) return SendClientMessage(playerid, COLOR_LGREY, "Вы должны находиться на территории вражеской банды для начала захвата");
			if(PlayerInfo[playerid][pGang] == ZoneInfo[i][gGang]) return SendClientMessage(playerid, COLOR_GREY, "Эта территория принадлежит вашей банде");
			switch(i)
			{
				case 7, 25, 67, 74, 90: return SendClientMessage(playerid, COLOR_GREY, "Вы не можете начать захват территорий респауна банд");
			}
			team_capture[0] = PlayerInfo[playerid][pGang];
			team_capture[1] = ZoneInfo[i][gGang];
			new str[128];
			format(str, sizeof(str), "{ffffff}Эта территория принадлежит банде %s\nВы уверены, что хотите начать её захват?", gang_name[ZoneInfo[i][gGang]-1]);
			capture_time = 420;
			kills_team[0] = 0;
			kills_team[1] = 0;
			zoneid_capture = i;
			ShowPlayerDialog(playerid, dCapture, DIALOG_STYLE_MSGBOX, "{ffcd00}Захват территории", str, "Да", "Нет");
			wasstoppedc = 0;
			return true;
		}
	}
	return true;
}


CMD:vhelp(playerid, params[])
{
	SendClientMessage(playerid, COLOR_YELLOW, "Доступные команды:");
	return SendClientMessage(playerid, 0xCC9900AA, "VIP:  /v  /vec  /style  /admins  /vips");
}

CMD:newadm(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 5) return true;
	new str[100];
	if(sscanf(params, "S()[24]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /newadm [ник игрока]");
	if(!strlen(params[0]))
	{
	    if(GetPVarInt(playerid, "NewADM") == 1)
	    {
	        SendClientMessage(playerid, COLOR_GREEN, "Действие команды было успешно отменено");
	        return DeletePVar(playerid, "NewADM");
	    }
	    else return SendClientMessage(playerid, COLOR_LGREY, "Используй /newadm [ник игрока]");
	}
 	if(GetPVarInt(playerid, "NewADM") == 0)
	{
	    SetPVarInt(playerid, "NewADM", 1);
	    format(str, sizeof(str), "Вы собираетесь назначить игрока %s администратором", params[0]);
	    SendClientMessage(playerid, COLOR_ORANGE, str);
     	SendClientMessage(playerid, COLOR_YELLOW, "Для ОТМЕНЫ действия введите /newadm без ника");
	    return SendClientMessage(playerid, COLOR_YELLOW, "Для ПОДТВЕРЖДЕНИЯ повторите /newadm [ник]");
	}
	mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `newadm`(`name`, `level`) VALUES ('%s', 1)", params[0]);
	mysql_tquery(mysql_connection, str, "", "");
	format(str, sizeof(str), "Игрок %s был успешно назначен администратором", params[0]);
	SendClientMessage(playerid, COLOR_GREEN, str);
	return DeletePVar(playerid, "NewADM");
}

ALT:animlist:anim;
CMD:animlist(playerid, params[])
{
	if(GetPVarInt(playerid, "Anim") == 0)
	{
	    PreloadAllAnimLibs(playerid);
	    SetPVarInt(playerid, "Anim", 1);
	    return SendClientMessage(playerid, COLOR_YELLOW, "Список анимаций загружен. Введите команду ещё раз");
	}
	if(IsPlayerInAnyVehicle(playerid)) return SendClientMessage(playerid, COLOR_LGREY, "Вы не можете использовать это в машине");
	sscanf(params, "I(-1)", params[0]);
	if(params[0] == -1)
	{
	    new anims[2048];
	    strcat(anims, "1. Танец 1\n2. Танец 2\n3. Танец 3\n4. Танец 4\n5. Танец 5\n6. Танец 6\n");
		strcat(anims, "7. Махать рукой\n8. Лечь на землю\n9. Походка пьяного\n10. Кувыркаться\n");
		strcat(anims, "11. Попрощаться\n12. Читать рэп\n13. Укрыться\n14. Подложить бомбу\n");
		strcat(anims, "15. Надеть маску\n16. Вытянуть руку перед собой\n17. Сложить руки вместе\n");
		strcat(anims, "18. Съел что-то не то...\n19. Перекусить\n20. Шлёпнуть кому-то по заднице\n");
		strcat(anims, "21. Предложить наркотики\n22. Эффект электрошокера\n23. Мужское курение\n");
		strcat(anims, "24. Женское курение\n25. Присесть\n26. Восточное единоборство\n27. Выпить напиток\n");
		strcat(anims, "28. Танец на одной ноге\n29. Поза вратаря\n30. Facepalm\n");
		strcat(anims, "31. Элемент восточного танца\n32. Позвать кого-то\n33. Руки вверх!\n");
		strcat(anims, "34. Спать на боку\n35. Спать на спине\n36. Смотреть по сторонам\n");
		strcat(anims, "37. Облокотиться на бок\n38. Толкнуть боком\n39. Раздумье\n");
		strcat(anims, "40. Лечь, оперевшись на ладонь\n41. Сесть на стул\n");
		strcat(anims, "42. Сидеть уставшим за компьютером\n43. Сидеть за столом\n");
		strcat(anims, "44. Сидеть и печатать\n45. Взять что-то и рассмотреть\n");
		strcat(anims, "46. Сесть, закинув ногу на ногу\n47. Отказаться от чего-либо\n");
		strcat(anims, "48. Поцелуй 1\n49. Поцелуй 2\n50. Поцелуй 3\n");
		strcat(anims, "51. Размахивать руками на месте\n52. Искуственное дыхание\n");
		strcat(anims, "53. Пощёчины для лежачего\n54. Подглядывать через что-то\n");
		strcat(anims, "55. Движение тореодора\n56. Сесть на стул (2)\n57. Сесть на стул (3)\n");
		strcat(anims, "58. Смотреть наверх\n59. Указать рукой наверх\n60. Быть в страхе\n");
		strcat(anims, "61. Призывать к чему-либо\n62. Сходить по-маленькому\n63. Гангстерский жест\n");
		strcat(anims, "64. Голосовать на остановке\n65. Удар ногой\n66. Стучаться в дверь\n");
		strcat(anims, "67. Устроить бунт\n68. Пританцовывать\n69. Лечь на землю (2)\n");
		strcat(anims, "70. Плохое самочувствие\n71. Приветствие 1\n72. Приветствие 2\n");
	    strcat(anims, "73. Приветствие 3\n74. Приветствие 4\n{33cc00}Информация");
	    return ShowPlayerDialog(playerid, dAnimPlayer, DIALOG_STYLE_LIST, "{9966FF}Анимации", anims, "Выбрать", "Закрыть");
	}
	return SelectPlayerAnimation(playerid, params[0]-1);
}

CMD:test(playerid)
{
    TextDrawShowForPlayer(playerid, selectskin_td[0]);
    TextDrawShowForPlayer(playerid, selectskin_td[1]);
    TextDrawShowForPlayer(playerid, selectskin_td[2]);
    TextDrawShowForPlayer(playerid, selectskin_td[3]);
    PlayerTextDrawShow(playerid, TD_Speedo[playerid]);
    SelectTextDraw(playerid, 0x0093B4AA);
    return TextDrawShowForPlayer(playerid, selectskin_td[4]);
}

CMD:returnadm(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 0) return true;
	if(returnedAdmin == -1) return SendClientMessage(playerid, COLOR_LGREY, "Администратора не снимало системой безопасности");
	new str[100];
	if(GetPVarInt(playerid, "RAdm") == 0)
	{
	    format(str, sizeof(str), "Вы собираетесь вернуть администратора %s[%d] на %d уровень", PlayerInfo[returnedAdmin][pName], returnedAdmin, returnedAdminLVL);
	    SendClientMessage(playerid, COLOR_ORANGE, str);
	    SetPVarInt(playerid, "RAdm", 1);
	    SendClientMessage(playerid, COLOR_YELLOW, "Для ОТМЕНЫ действия перезайдите на сервер");
	    return SendClientMessage(playerid, COLOR_YELLOW, "Для ПОДТВЕРЖДЕНИЯ повторите /returnadm");
	}
	mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `newadm`(`name`, `level`) VALUES ('%s', %d)", PlayerInfo[returnedAdmin][pName], returnedAdminLVL);
	mysql_tquery(mysql_connection, str, "", "");
	format(str, sizeof(str), "[Внимание] %s[%d] был возвращён на пост администратора", PlayerInfo[returnedAdmin][pName], returnedAdmin);
	SendAdminMessage(COLOR_RED, str, 1);
	DeletePVar(playerid, "RAdm");
	returnedAdmin = -1;
	format(str, sizeof(str), "Игрок %s был возвращён на пост администратора %d уровня", PlayerInfo[returnedAdmin][pName], returnedAdmin);
	SendClientMessage(playerid, COLOR_GREEN, str);
	return AdminInfo[playerid][aReturn]++;
}

CMD:delacc(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 5) return true;
	new str[100];
	if(sscanf(params, "S()[24]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /delacc [ник игрока]");
	if(!strlen(params[0]))
	{
		if(GetPVarInt(playerid, "DelACC") == 1)
		{
		    DeletePVar(playerid, "DelACC");
		    return SendClientMessage(playerid, COLOR_GREEN, "Действие команды было успешно отменено");
		}
		else return SendClientMessage(playerid, COLOR_LGREY, "Используй /delacc [ник игрока]");
	}
	mysql_format(mysql_connection, str, sizeof(str), "SELECT `IDacc`, `kills` FROM `accounts` WHERE `name`='%s'", params[0]);
	return mysql_tquery(mysql_connection, str, "DelAccount", "dsd", playerid, params[0], GetPVarInt(playerid, "DelACC"));
}

CMD:deladmin(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 5) return true;
	new str[100];
	if(sscanf(params, "s[24]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /deladmin [ник админа]");
	mysql_format(mysql_connection, str, sizeof(str), "SELECT `name`, `admin` FROM `accounts` WHERE `name`='%s'", params[0]);
	return mysql_tquery(mysql_connection, str, "CheckForAdmin", "ds", playerid, params[0]);
}

CMD:admdown(playerid, params[])
{
    if(PlayerInfo[playerid][pAdmin] < 5) return true;
	if(sscanf(params, "dd", params[0], params[1])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /admdown [id админа] [уровень]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(params[1] < 0) return SendClientMessage(playerid, COLOR_LGREY, "Уровень администратора не может быть меньше 0");
	if(params[1] >= PlayerInfo[params[0]][pAdmin]) return SendClientMessage(playerid, COLOR_LGREY, "Администратора нельзя повысить данной командой");
	new str[100];
	format(str, sizeof(str), "Вы изменили уровень администратора %s до %d", PlayerInfo[params[0]][pName], params[1]);
	SendClientMessage(playerid, COLOR_YELLOW, str);
	PlayerInfo[params[0]][pAdmin] = params[1];
	format(str, sizeof(str), "Ваш уровень администратирования был измененён до %d", params[1]);
	return SendClientMessage(params[0], COLOR_YELLOW, str);
}

CMD:adm(playerid, params[])
{
	new str[100];
	mysql_format(mysql_connection, str, sizeof(str), "SELECT `name`, `level` FROM `newadm` WHERE `name`='%s'", PlayerInfo[playerid][pName]);
	return mysql_tquery(mysql_connection, str, "ADM", "d", playerid);
}

CMD:vec(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 4 && PlayerInfo[playerid][pVip] == 0) return SendClientMessage(playerid, COLOR_LGREY, "Данная функция доступная только VIP игрокам");
	if(sscanf(params, "iii", params[0], params[1], params[2])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /vec [id транспорта] [1 цвет] [2 цвет]");
	if(params[0] < 400 || params[0] > 611) return SendClientMessage(playerid, COLOR_LGREY, "ID транспорта от 410 до 611");
	if(PlayerInfo[playerid][pVip] == 1 && PlayerInfo[playerid][pAdmin] == 0)
	{
	    if(idplayercar[playerid] != 0) return SendClientMessage(playerid, COLOR_LGREY, "Вы уже создали транспорт, для удаления используйте {FF9933}/delvec");
		if(params[0] == 406 || params[0] == 417 || params[0] == 425 ||
		params[0] == 430 || params[0] == 432 || params[0] == 435 ||
		params[0] == 411 || params[0] == 444 || params[0] == 446 ||
		params[0] == 447 || params[0] == 449 || params[0] == 450 ||
		params[0] == 452 || params[0] == 453 || params[0] == 454 ||
		params[0] == 460 || params[0] == 464 || params[0] == 465 ||
		params[0] == 469 || params[0] == 472 || params[0] == 473 ||
		params[0] == 476 || params[0] == 484 || params[0] == 487 ||
		params[0] == 488 || params[0] == 493 || params[0] == 497 ||
		params[0] == 501 || params[0] == 406 || params[0] == 511 ||
		params[0] == 512 || params[0] == 513 || params[0] == 519 ||
		params[0] == 520 || params[0] == 406 || params[0] == 537 ||
		params[0] == 538 || params[0] == 548 || params[0] == 553 ||
		params[0] == 556 || params[0] == 557 || params[0] == 563 ||
		params[0] == 564 || params[0] == 569 || params[0] == 570 ||
		params[0] == 577 || params[0] == 584 || params[0] == 590 ||
		params[0] == 591 || params[0] == 592 || params[0] == 595 ||
		params[0] == 606 || params[0] == 607 || params[0] == 608 ||
		params[0] == 610 || params[0] == 611) return SendClientMessage(playerid, COLOR_ORANGE, "Данный транспорт запрещено создавать");
		new Float:carx, Float:cary, Float:carz;
		GetPlayerPos(playerid, carx, cary, carz);
		SendClientMessage(playerid, COLOR_GREEN, "Транспорт успешно создан");
		SendClientMessage(playerid, COLOR_YELLOW, "Транспорт будет доступен в течение 30 минут, для удаления досрочно используйте {66cc00}/delvec");
		SetPVarInt(playerid, "TimeToDelVeh", 1800);
		idplayercar[playerid] = CreateVehicle(params[0], carx, cary-5, carz, 0.0, params[1], params[2], 10000, 0);
		return true;
	}
	new Float:carx, Float:cary, Float:carz;
	GetPlayerPos(playerid, carx, cary, carz);
	admcars++;
	idadmcar[admcars] = CreateVehicle(params[0], carx, cary-5, carz, 0.0, params[1], params[2], 10000, 0);
	return true;
}

CMD:delvec(playerid)
{
	if(PlayerInfo[playerid][pVip] == 0) return SendClientMessage(playerid, COLOR_LGREY, "Данная функция доступная только VIP игрокам");
	if(idplayercar[playerid] == 0) return SendClientMessage(playerid, COLOR_LGREY, "Вы не создавали транспорт");
	SendClientMessage(playerid, COLOR_GREEN, "Транспорт был успешно удалён. Для создания нового используйте {ffdd00}/vec");
	DestroyVehicle(idplayercar[playerid]);
	idplayercar[playerid] = 0;
	return DeletePVar(playerid, "TimeToDelVeh");
}

CMD:hp(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 4) return true;
	if(sscanf(params, "id", params[0], params[1])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /hp [id игрока] [уровень hp]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(params[1] < 10 || params[1] > 100) return SendClientMessage(playerid, 0x999999AA, "Уровень HP от 10 до 100");
	new str[88];
	format(str, sizeof(str), "Администратор %s изменил Вам здоровье", PlayerInfo[playerid][pName]);
	SendClientMessage(params[0], COLOR_WHITE, str);
	format(str, sizeof(str), "Здоровье игрока %s[%i] изменено на %i", PlayerInfo[params[0]][pName], params[0], params[1]);
	SendClientMessage(playerid, COLOR_WHITE, str);
	return SetPlayerHealth(params[0], params[1]);
}

CMD:skin(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 4) return true;
	if(sscanf(params, "id", params[0], params[1])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /skin [id игрока] [id внешности]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(params[1] < 1 || params[1] > 310) return SendClientMessage(playerid, 0x999999AA, "ID скина от 1 до 310");
	if(params[1] == 74) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла ошибка при выдаче скина");
	new str[88];
	format(str, sizeof(str), "Администратор %s выдал Вам временный скин", PlayerInfo[playerid][pName]);
	SendClientMessage(params[0], COLOR_WHITE, str);
	format(str, sizeof(str), "Вы выдали временный скин(%d) игроку %s", params[1], PlayerInfo[params[0]][pName]);
	SendClientMessage(playerid, COLOR_WHITE, str);
	return SetPlayerSkin(params[0], params[1]);
}

CMD:givegun(playerid, params[])
{
    if(PlayerInfo[playerid][pAdmin] < 5) return true;
    if(sscanf(params, "idd", params[0], params[1], params[2])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /givegun [радиус] [id оружия] [кол-во патрон]");
    if(params[0] < 5 || params[0] > 100) return SendClientMessage(playerid, 0x999999AA, "Радиус от 5 до 100");
    if(params[1] < 0 || params[1] > 46) return SendClientMessage(playerid, COLOR_ORANGE, "Неверный ID оружия. ID оружия может быть от 1 до 46");
	if(params[1] >= 35 && params[1] <= 38) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла ошибка при выдаче оружия");
    new Float:curr_x, Float:curr_y, Float:curr_z;
    GetPlayerPos(playerid, curr_x, curr_y, curr_z);
    new gun[16];
    GetWeaponName(params[1], gun, 16);
    new str[128];
	foreach(new i:Player)
	{
	    if(IsPlayerInRangeOfPoint(i, params[0], curr_x, curr_y, curr_z))
	    {
	        GivePlayerWeapon(i, params[1], params[2]);
			format(str, sizeof(str), "Администратор %s выдал Вам %s на %d патрон", PlayerInfo[playerid][pName], gun, params[2]);
			SendClientMessage(i, 0xCC9900AA, str);
	    }
	}
	format(str, sizeof(str), "Всем игрокам в указаном радиусе был выдан %s на %d патрон", gun, params[2]);
	return SendClientMessage(playerid, COLOR_GREEN, str);
}

CMD:tempzone(playerid, params[])
{
    if(PlayerInfo[playerid][pAdmin] < 5) return true;
    if(sscanf(params, "i", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /tempzone [id банды]");
    if(params[0] < 1 || params[0] > 8) return SendClientMessage(playerid, 0x999999AA, "ID банды от 1 до 8");
    for(new i = 0; i != sizeof(ZoneInfo); i++)
	{
		if(IsPlayerInGZ(playerid, ZoneInfo[i][gCoords][0], ZoneInfo[i][gCoords][1], ZoneInfo[i][gCoords][2], ZoneInfo[i][gCoords][3]))
		{
		    //if(i == zoneid_capture) return SendClientMessage(playerid, COLOR_ORANGE, "Эту зону нельзя перекрасить в данный момент");
		    ZoneInfo[i][gGang] = params[0];
   			SaveGZ(i);
			GangZoneHideForAll(i);
   			GangZoneShowForAll(i, GetGZColor(params[0]));
      		gangzone[0] = 0, gangzone[1] = 0, gangzone[2] = 0, gangzone[3] = 0, gangzone[4] = 0;
			for(new territory = 0; territory < sizeof(ZoneInfo); territory++)
			{
			   switch(ZoneInfo[territory][gGang])
			   {
				   	case 1: gangzone[0]++;
       				case 2: gangzone[1]++;
		            case 3: gangzone[2]++;
		            case 4: gangzone[3]++;
		            case 5: gangzone[4]++;
		            case 6: gangzone[5]++;
		            case 7: gangzone[6]++;
		            case 8: gangzone[7]++;
			   }
			}
			new str[128];
			format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n\n\n{009900}Склад\nGrove Street", gangzone[0]);
		    Update3DTextLabelText(warehouses[1], 0xFFFFFFFF, str);

		    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{CC00FF}Склад\nThe Ballas", gangzone[1]);
		    Update3DTextLabelText(warehouses[2], 0xFFFFFFFF, str);

		    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{FFCD00}Склад\nLos Santos Vagos", gangzone[2]);
		    Update3DTextLabelText(warehouses[3], 0xFFFFFFFF, str);

		    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{00CCFF}Склад\nVarios Los Aztecas", gangzone[3]);
		    Update3DTextLabelText(warehouses[4], 0xFFFFFFFF, str);

		    format(str, sizeof(str), "Количество\nтерриторий:{99FF99} %d\n\n\n\n\n\n\n\n{6666FF}Склад\nThe Rifa", gangzone[4]);
		    Update3DTextLabelText(warehouses[5], 0xFFFFFFFF, str);
			format(str, sizeof(str), "[A] %s[%d] перекрасил территорию (ID: %d)", PlayerInfo[playerid][pName], playerid, i);
			SendAdminMessage(COLOR_ADMMSG, str, 1);
			format(str, sizeof(str), "Территория №%d была успешно перекрашена", i);
			SendClientMessage(playerid, COLOR_GREEN, str);
			break;
		}
	}
	return true;
}

CMD:hpall(playerid, params[0])
{
    if(PlayerInfo[playerid][pAdmin] < 3) return true;
    if(sscanf(params, "i", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /hpall [радиус]");
    if(params[0] < 5 || params[0] > 100) return SendClientMessage(playerid, 0x999999AA, "Радиус от 5 до 100 метров");
    new Float:curr_x, Float:curr_y, Float:curr_z;
    GetPlayerPos(playerid, curr_x, curr_y, curr_z);
	foreach(new i:Player)
	{
	    if(IsPlayerInRangeOfPoint(i, params[0], curr_x, curr_y, curr_z))
	    {
	        SetPlayerHealth(i, 100.0);
	        SendClientMessage(i, COLOR_WHITE, "Администратор восстановил Вам здоровье");
	    }
	}
	return SendClientMessage(playerid, COLOR_GREEN, "Всем игрокам в указаном радиусе было восстановлено здоровье");
}

CMD:gethere(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 4) return true;
	if(sscanf(params, "i", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /gethere [id игрока]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	new Float:tempx, Float:tempy, Float:tempz;
	GetPlayerPos(playerid, tempx, tempy, tempz);
	new vw = GetPlayerVirtualWorld(playerid);
	new inter = GetPlayerInterior(playerid);
	SetPlayerPos(params[0], tempx+1, tempy, tempz);
	SetPlayerVirtualWorld(params[0], vw);
	SetPlayerInterior(params[0], inter);
	new str[88];
	format(str, sizeof(str), "[A] %s[%d] телепортировал к себе игрока %s[%d]", PlayerInfo[playerid][pName], playerid, PlayerInfo[params[0]][pName], params[0]);
	SendAdminMessage(COLOR_ADMMSG, str, 1);
	format(str, sizeof(str), "Администратор %s[%d] телепортировал Вас к себе", PlayerInfo[playerid][pName], playerid);
	return SendClientMessage(params[0], COLOR_WHITE, str);
}

CMD:setvw(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params,"ii", params[0], params[1])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /setvw [id игрока] [id вирт. мира]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(params[1] < 0) return SendClientMessage(playerid, COLOR_ORANGE, "При установке виртуального мира произошла ошибка");
	new str[96];
	format(str, sizeof(str), "Администратор %s[%d] установил Вам виртуальный мир №%d", PlayerInfo[playerid][pName], playerid, params[1]);
	SendClientMessage(params[0], COLOR_WHITE, str);
	format(str, sizeof(str), "Вы установили игроку %s[%d] виртуальный мир №%d", PlayerInfo[params[0]][pName], params[0], params[1]);
	SendClientMessage(playerid, COLOR_WHITE, str);
	return SetPlayerVirtualWorld(params[0], params[1]);
}

CMD:setint(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params,"ii", params[0], params[1])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /setint [id игрока] [id интерьера]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(params[1] < 0) return SendClientMessage(playerid, COLOR_ORANGE, "При установке интерьера произошла ошибка");
	new str[96];
	format(str, sizeof(str), "Администратор %s[%d] установил Вам ID интерьера №%d", PlayerInfo[playerid][pName], playerid, params[1]);
	SendClientMessage(params[0], COLOR_WHITE, str);
	format(str, sizeof(str), "Вы установили игроку %s[%d] ID интерьера №%d", PlayerInfo[params[0]][pName], params[0], params[1]);
	SendClientMessage(playerid, COLOR_WHITE, str);
	return SetPlayerInterior(params[0], params[1]);
}

CMD:vw(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params,"i", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /vw [id вирт. мира]");
	if(params[0] < 0) return SendClientMessage(playerid, COLOR_ORANGE, "При установке виртуального мира произошла ошибка");
	new str[52];
	format(str, sizeof(str), "Вы установили виртуальный мир №%d", params[0]);
	SendClientMessage(playerid, COLOR_WHITE, str);
	return SetPlayerVirtualWorld(playerid, params[0]);
}

CMD:get(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params, "s[24]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /get [ник игрока]");
	new str[128];
	mysql_format(mysql_connection, str, sizeof(str), "SELECT * FROM `accounts` WHERE name='%s'", params[0]);
	return mysql_tquery(mysql_connection, str, "GetAccInfo", "is", playerid, params[0]);
}

CMD:stats(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] == 0) return true;
	if(sscanf(params, "i", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /stats [id игрока]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	return ShowPlayerStats(playerid, params[0]);
}

CMD:ip(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params,"s[16]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /ip [ip адрес]");
	new query[128];
	mysql_format(mysql_connection, query, sizeof(query), "SELECT `name`, `kills` FROM `accounts` WHERE `rip` = '%s'", params[0]);
	return mysql_tquery(mysql_connection, query, "OnRipAccountsShow", "is", playerid, params[0]);
}

CMD:lip(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params,"s[16]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /lip [ip адрес]");
	new query[128];
	mysql_format(mysql_connection, query, sizeof(query), "SELECT `name`, `kills` FROM `accounts` WHERE `lip` = '%s'", params[0]);
	return mysql_tquery(mysql_connection, query, "OnLipAccountsShow", "is", playerid, params[0]);
}

CMD:ban(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params, "iiS()[30]", params[0], params[1], params[2]))
	{
	    if(GetPVarInt(playerid, "BanADM") == 1)
		{
		    DeletePVar(playerid, "BanADM");
		    return SendClientMessage(playerid, COLOR_GREEN, "Вы отменили действие команды");
		}
		else return SendClientMessage(playerid, COLOR_LGREY, "Используй /ban [id игрока] [кол-во дней] [причина]");
	}
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(params[1] < 3 || params[1] > 30) return SendClientMessage(playerid, 0x999999AA, "Кол-во дней от 3 до 30");
	if(PlayerInfo[params[0]][pAdmin] >= 1 && GetPVarInt(playerid, "BanADM") == 0)
	{
	    SetPVarInt(playerid, "BanADM", 1);
     	return SendClientMessage(playerid, COLOR_ORANGE, "Вы собираетесь забанить администратора сервера. Чтобы Далее введите команду ещё раз");
	}
	new str[250];
	if(!strlen(params[2])) format(str, sizeof(str), "Администратор %s забанил игрока %s на %i дней.", PlayerInfo[playerid][pName], PlayerInfo[params[0]][pName], params[1]);
	else format(str, sizeof(str), "Администратор %s забанил игрока %s на %i дней. Причина: %s", PlayerInfo[playerid][pName], PlayerInfo[params[0]][pName], params[1], params[2]);
	SendClientMessageToAll(0xFF5030AA, str);
	mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `bans`(`IDacc`, `name`, `nameadm`, `ip`, `date`, `reason`, `daystounban`) VALUES (%d, '%s', '%s', '%s', NOW(), '%s', %d)", PlayerInfo[params[0]][pID], PlayerInfo[params[0]][pName], PlayerInfo[playerid][pName], PlayerInfo[params[0]][pIP], params[2], params[1]);
	mysql_tquery(mysql_connection, str, "", "");
	new Year, Month, Day;
	getdate(Year, Month, Day);
	new monthname[9];
	if(PlayerInfo[params[0]][pAdmin] != 0)
	{
		PlayerInfo[params[0]][pAdmin] = 0;
		format(str, sizeof(str), "UPDATE `accounts` SET `admin` = '0' WHERE `name` = '%s' LIMIT 1", PlayerInfo[params[0]][pName]);
		mysql_tquery(mysql_connection, str, "", "");
	}
	switch(Month)
	{
	    case 1: monthname = "января";
	    case 2: monthname = "февраля";
	    case 3: monthname = "марта";
	    case 4: monthname = "апреля";
	    case 5: monthname = "мая";
	    case 6: monthname = "июня";
	    case 7: monthname = "июля";
	    case 8: monthname = "августа";
	    case 9: monthname = "сентября";
	    case 10: monthname = "октября";
	    case 11: monthname = "ноября";
	    case 12: monthname = "декабря";
	}
	if(!strlen(params[2]))format(str, sizeof(str), "{FFFFFF}Дата: %02d %s %d г.\nВаш ник: %s\nНик администратора: %s.\nКоличество дней: %d\nПричина: отсутствует\n\n{B2FF66}Если вы не согласны с наказанием, сделайте скриншот (F8)\nи оставьте жалобу на форуме forum.advance-gw.ru", Day, monthname, Year, PlayerInfo[params[0]][pName], PlayerInfo[playerid][pName], params[1]);
	else format(str, sizeof(str), "{FFFFFF}Дата: %02d %s %d г.\nВаш ник: %s\nНик администратора: %s.\nКоличество дней: %d\nПричина: %s\n\n{B2FF66}Если вы не согласны с наказанием, сделайте скриншот (F8)\nи оставьте жалобу на форуме forum.advance-gw.ru", Day, monthname, Year, PlayerInfo[params[0]][pName], PlayerInfo[playerid][pName], params[1], params[2]);
    ShowPlayerDialog(params[0], dNoActions, DIALOG_STYLE_MSGBOX, "{FF5555}Бан аккаунта", str, "Закрыть", "");
    DeletePVar(playerid, "BanADM");
	mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `ipbans`(`ip`, `daystounban`) VALUES ('%s', %d)", PlayerInfo[params[0]][pIP], params[1]);
	mysql_tquery(mysql_connection, str, "", "");
	AdminInfo[playerid][aBan]++;
	return KickEx(params[0]);
}

CMD:offban(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 4) return true;
	new nick[MAX_PLAYER_NAME];
	if(sscanf(params, "s[24]is[30]", nick, params[1], params[2])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /offban [ник игрока] [кол-во дней] [причина]");
	foreach(new i: Player)
	{
		if(!strcmp(PlayerInfo[i][pName], nick, true, 24)) return SendClientMessage(playerid, COLOR_LGREY, "Игрок не должен быть подключён");
	}
	if(params[1] < 3 || params[1] > 30) return SendClientMessage(playerid, COLOR_LGREY, "Срок бана от 3 до 30 дней");
    new str[160];
    mysql_format(mysql_connection, str, sizeof(str), "SELECT `name` FROM `bans` WHERE name='%s'", nick);
	return mysql_tquery(mysql_connection, str, "CheckBan", "dsds", playerid, nick, params[1], params[2]);
}

CMD:unban(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 4) return true;
	if(sscanf(params, "s[24]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /unban [ник игрока]");
    new str[160];
    mysql_format(mysql_connection, str, sizeof(str), "SELECT `IDacc`, `name`, `ip` FROM `bans` WHERE name='%s'", params[0]);
	return mysql_tquery(mysql_connection, str, "UnBan", "ds", playerid, params[0]);
}

CMD:rban(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 4) return true;
	if(sscanf(params, "i", params[0]))
	{
	    if(GetPVarInt(playerid, "RBanADM") == 1)
		{
		    DeletePVar(playerid, "RBanADM");
		    return SendClientMessage(playerid, COLOR_GREEN, "Вы отменили действие команды");
		}
		else return SendClientMessage(playerid, COLOR_LGREY, "Используй /rban [id игрока]");
	}
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(PlayerInfo[params[0]][pAdmin] >= 1 && GetPVarInt(playerid, "RBanADM") == 0)
	{
	    SetPVarInt(playerid, "RBanADM", 1);
	    return SendClientMessage(playerid, COLOR_ORANGE, "Вы собираетесь забанить IP администратора сервера НАВСЕГДА. Чтобы Далее введите команду ещё раз");
	}
	new str[158];
	format(str, sizeof(str), "[Внимание] %s[%d] внёс в черный список IP игрока %s[%d] [IP: %s]", PlayerInfo[playerid][pName], playerid, PlayerInfo[params[0]][pName], params[0], PlayerInfo[params[0]][pIP]);
	SendAdminMessage(COLOR_RED, str, 1);
    DeletePVar(playerid, "RBanADM");
	mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `ipbans`(`ip`, `daystounban`) VALUES ('%s', 99999)", PlayerInfo[params[0]][pIP]);
	mysql_tquery(mysql_connection, str, "", "");
	AdminInfo[playerid][aRBan]++;
	return KickEx(params[0]);
}

CMD:unrban(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 4) return true;
	if(sscanf(params, "s[16]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /unrban [ip адрес]");
	new str[158];
	mysql_format(mysql_connection, str, sizeof(str), "SELECT `ip` FROM `ipbans` WHERE ip='%s'", params[0]);
	return mysql_tquery(mysql_connection, str, "IsBannedIP", "ds", playerid, params[0]);
}


CMD:respv(playerid, params[0])
{
    if(PlayerInfo[playerid][pAdmin] < 3) return true;
    if(sscanf(params, "i", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /respv [радиус]");
    if(params[0] < 3 || params[0] > 80) return SendClientMessage(playerid, 0x999999AA, "Радиус от 3 до 80");
    new Float:curr_x, Float:curr_y, Float:curr_z;
    GetPlayerPos(playerid, curr_x, curr_y, curr_z);
	for(new i = 0; i < MAX_VEHICLES; i++)
	{
	    if(VecToPoint(params[0], i, curr_x, curr_y, curr_z))
		{
		    if(idadmcar[admcars] == i)
			{
			    DestroyVehicle(i);
				admcars--;
			}
		    SetVehicleToRespawn(i);
		}
	}
	return SendClientMessage(playerid, COLOR_GREEN, "Машины в указаном радиусе были респавнены");
}

CMD:baninfo(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params,"s[24]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /baninfo [ник игрока]");
	new query[128];
	mysql_format(mysql_connection, query, sizeof(query), "SELECT `IDacc`, `name`, `nameadm`, `ip`, `date`, `reason`, `daystounban` FROM `bans` WHERE `name`='%s'", params[0]);
	return mysql_tquery(mysql_connection, query, "GetBanInfo", "ds", playerid, params[0]);
}

CMD:goto(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params, "i", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /goto [id игрока]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	new Float:tpx, Float:tpy, Float:tpz;
	GetPlayerPos(params[0], tpx, tpy, tpz);
	GameTextForPlayer(playerid, "TELEPORT", 1000, 4);
	SetPlayerPos(playerid, tpx, tpy+1, tpz);
	SetPlayerInterior(playerid, GetPlayerInterior(params[0]));
	return SetPlayerVirtualWorld(playerid, GetPlayerVirtualWorld(params[0]));
}

CMD:skick(playerid, params[])
{
	if(PlayerInfo[playerid][pAdmin] < 3) return true;
	if(sscanf(params, "i", params[0]))
	{
	    if(GetPVarInt(playerid, "SkickADM") == 1)
		{
		    DeletePVar(playerid, "SkickADM");
		    return SendClientMessage(playerid, COLOR_GREEN, "Вы отменили действие команды");
		}
		else return SendClientMessage(playerid, COLOR_LGREY, "Используй /skick [id игрока]");
	}
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(PlayerInfo[params[0]][pAdmin] >= 1 && GetPVarInt(playerid, "SkickADM") == 0)
	{
	    SetPVarInt(playerid, "SkickADM", 1);
	    return SendClientMessage(playerid, COLOR_ORANGE, "Вы собираетесь тихо кикнуть администратора сервера. Чтобы Далее введите команду ещё раз");
	}
	new str[108];
	format(str, sizeof(str), "[A] %s[%d] кикнул игрока %s[%d] без лишнего шума", PlayerInfo[playerid][pName], playerid, PlayerInfo[params[0]][pName], params[0]);
	SendAdminMessage(COLOR_ADMMSG, str, 1);
	format(str, sizeof(str), "Вы были кикнуты администратором %s[%d] за нарушение правил сервера", PlayerInfo[playerid][pName], playerid);
	SendClientMessage(params[0], COLOR_ADMMSG, str);
	DeletePVar(playerid, "SkickADM");
	return KickEx(params[0]);
}

CMD:a(playerid, params[])
{
    if(PlayerInfo[playerid][pAdmin] == 0) return true;
	if(sscanf(params, "s[116]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /a [сообщение]");
	new str[144];
	format(str, sizeof(str), "[A] %s[%d]: %s", PlayerInfo[playerid][pName], playerid, params[0]);
	return SendAdminMessage(0x99CC00AA, str, 1);
}

CMD:e(playerid)
{
	if(!IsPlayerInAnyVehicle(playerid)) return SendClientMessage(playerid, COLOR_LGREY, "Вы не за рулём");
	new vId = GetPlayerVehicleID(playerid);
	if(VehInfo[vId][vEngine] == 0)
	{
	    VehInfo[vId][vEngine] = 1;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	if(VehInfo[vId][vEngine] == 1)
	{
	    VehInfo[vId][vEngine] = 0;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	return true;
}

CMD:lock(playerid)
{
	if(!IsPlayerInAnyVehicle(playerid)) return SendClientMessage(playerid, COLOR_LGREY, "Вы не за рулём");
	new vId = GetPlayerVehicleID(playerid);
	new Float:cX, Float:cY, Float:cZ;
	GetVehiclePos(vId, cX, cY, cZ);
	if(VehInfo[vId][vLock] == 0)
	{
	    PlayerPlaySound(playerid, 25800, cX, cY, cZ);
	    VehInfo[vId][vLock] = 1;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	if(VehInfo[vId][vLock] == 1)
	{
	    PlayerPlaySound(playerid, 25800, cX, cY, cZ);
	    VehInfo[vId][vLock] = 0;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	return true;
}

CMD:l(playerid)
{
	if(!IsPlayerInAnyVehicle(playerid)) return SendClientMessage(playerid, COLOR_LGREY, "Вы не за рулём");
	new vId = GetPlayerVehicleID(playerid);
	if(VehInfo[vId][vLight] == 0)
	{
	    PlayerPlaySound(playerid, 4604, 0.0, 0.0, 0.0);
	    VehInfo[vId][vLight] = 1;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	if(VehInfo[vId][vLight] == 1)
	{
	    PlayerPlaySound(playerid, 4604, 0.0, 0.0, 0.0);
	    VehInfo[vId][vLight] = 0;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	return true;
}

CMD:alarm(playerid)
{
	if(!IsPlayerInAnyVehicle(playerid)) return SendClientMessage(playerid, COLOR_LGREY, "Вы не за рулём");
	new vId = GetPlayerVehicleID(playerid);
	if(VehInfo[vId][vSignal] == 0)
	{
	    PlayerPlaySound(playerid, 21000, 0.0, 0.0, 0.0);
	    VehInfo[vId][vSignal] = 1;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	if(VehInfo[vId][vSignal] == 1)
	{
	    PlayerPlaySound(playerid, 21000, 0.0, 0.0, 0.0);
	    VehInfo[vId][vSignal] = 0;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	return true;
}

CMD:sl(playerid)
{
	if(!IsPlayerInAnyVehicle(playerid)) return SendClientMessage(playerid, COLOR_LGREY, "Вы не за рулём");
	new vId = GetPlayerVehicleID(playerid);
	new Float:vVelocity[3];
	GetVehicleVelocity(vId, vVelocity[0], vVelocity[1], vVelocity[2]);
	if(VehInfo[vId][vLimiter] == 0)
	{
	    PlayerPlaySound(playerid, 21000, 0.0, 0.0, 0.0);
	    VehInfo[vId][vLimiter] = 1;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	if(VehInfo[vId][vLimiter] == 1)
	{
	    PlayerPlaySound(playerid, 21000, 0.0, 0.0, 0.0);
	    VehInfo[vId][vLimiter] = 0;
	    return SetVehicleParamsEx(vId, VehInfo[vId][vEngine], VehInfo[vId][vLight], 0, VehInfo[vId][vLock], 0, 0, 0);
	}
	return true;
}

CMD:v(playerid, params[])
{
    if(PlayerInfo[playerid][pVip] == 0) return SendClientMessage(playerid, COLOR_LGREY, "Данная функция доступна только VIP игрокам");
	if(sscanf(params, "s[116]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /v [сообщение]");
	new str[144];
	format(str, sizeof(str), "[V] %s[%d]: %s", PlayerInfo[playerid][pName], playerid, params[0]);
	return SendVipMessage(0xCCCC00AA, str);
}

CMD:ans(playerid, params[])
{
    if(PlayerInfo[playerid][pAdmin] == 0) return true;
	if(sscanf(params, "is[100]", params[0], params[1])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /ans [id игрока] [сообщение]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	new str[144];
	format(str, sizeof(str), "Администратор %s[%d] для %s[%d]: %s", PlayerInfo[playerid][pName], playerid, PlayerInfo[params[0]][pName], params[0], params[1]);
	SendAdminMessage(0xFF9945AA, str, 1);
	PlayerPlaySound(params[0], 1085, 0.0, 0.0, 0.0);
	return SendClientMessage(params[0], 0xFF9945AA, str);
}

CMD:pm(playerid, params[])
{
    if(PlayerInfo[playerid][pMute] > 0) return SendClientMessage(playerid, COLOR_ORANGE, "Вы не можете использовать это");
	if(sscanf(params, "is[100]", params[0], params[1])) return SendClientMessage(playerid, COLOR_LGREY, "Используйте /pm [id игрока] [текст]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(togPM{params[0]} == 0) return SendClientMessage(playerid, COLOR_LGREY, "Игрок отключил приём личных сообщений");
	new str[144];
	format(str, sizeof(str), "PM: %s | Отправитель: %s[%d]", params[1], PlayerInfo[playerid][pName], playerid);
	SendClientMessage(params[0], COLOR_YELLOW, str);
	PlayerPlaySound(params[0], 1085, 0.0, 0.0, 0.0);
	format(str, sizeof(str), "PM: %s | Получатель: %s[%d]", params[1], PlayerInfo[params[0]][pName], params[0]);
	SendClientMessage(playerid, COLOR_YELLOW, str);
	if(ears == 1)
	{
	    format(str, sizeof(str), "[A][PM]: %s | Отправил %s[%d] для %s[%d]", params[1], PlayerInfo[playerid][pName], playerid, PlayerInfo[params[0]][pName], params[0]);
		return SendAdminMessage(COLOR_YELLOW, str, 1);
	}
	return true;
}




CMD:admins(playerid, params[])
{
    if(PlayerInfo[playerid][pAdmin] == 0 && PlayerInfo[playerid][pVip]) return SendClientMessage(playerid, COLOR_LGREY, "Данная функция доступна только VIP игрокам");
    new str[52];
    SendClientMessage(playerid, COLOR_GREEN, "Админы онлайн:");
    foreach(new i:Player)
    {
        if(PlayerInfo[i][pAdmin] >= 1)
        {
            format(str, sizeof(str), "%s[%d] (%d lvl)", PlayerInfo[i][pName], i, PlayerInfo[i][pAdmin]);
	        if(PlayerInfo[i][pAdmin] == 5) format(str, sizeof(str), "Гл. администратор");
	        if(PlayerInfo[i][pAFK] > 3) strcat(str, " {FF0000}AFK");
			if(GetPlayerState(i) == PLAYER_STATE_SPECTATING) format(str, sizeof(str), "%s {33CC00} > /sp %d", str, currIDspec[i]);
			SendClientMessage(playerid, COLOR_YELLOW, str);
        }
    }
    return true;
}

CMD:vips(playerid, params[])
{
    if(PlayerInfo[playerid][pVip] == 0) return SendClientMessage(playerid, COLOR_LGREY, "Данная функция доступна только VIP игрокам");
    new str[52];
    SendClientMessage(playerid, COLOR_GREEN, "VIP игроки онлайн:");
    foreach(new i:Player)
    {
        if(PlayerInfo[i][pVip] == 1)
        {
            format(str, sizeof(str), "%s[%d]", PlayerInfo[i][pName], i);
	        if(PlayerInfo[i][pAFK] > 3) strcat(str, " {FF0000}AFK");
			SendClientMessage(playerid, COLOR_YELLOW, str);
        }
    }
    return true;
}

CMD:lego(playerid)
{
	if(PlayerInfo[playerid][pAdmin] < 5) return true;
	if(lego != playerid && lego >= 0) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла неизвестная ошибка");
	if(lego == -1)
	{
	    SendClientMessage(playerid, COLOR_GREEN, "Режим редактирования объектов активирован");
	    SendClientMessage(playerid, COLOR_YELLOW, "Доступные команды:");
	    SendClientMessage(playerid, 0xCC9900AA, "Объекты:  /newobj  /dellast  /editobj  /newactor  /editactor");
	    return lego = playerid;
	}
	if(lego != -1)
	{
	    SendClientMessage(playerid, COLOR_ORANGE, "Режим редактирования объектов деактивирован");
	    return lego = -1;
	}
	return true;
}

CMD:newobj(playerid)
{
	if(PlayerInfo[playerid][pAdmin] != 5) return true;
	if(lego == -1) return true;
	if(lego != playerid) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла неизвестная ошибка");
	return ShowPlayerDialog(playerid, dObjectNew, DIALOG_STYLE_INPUT, "{CC9900}Добавление объекта", "{ffffff}Введите ID объекта, который вы хотите установить\n\nСписок объектов можно найти тут: {6699FF}www.samp-ru.org/forum/6-21-1", "Далее", "Закрыть");
}

CMD:dellast(playerid)
{
    if(PlayerInfo[playerid][pAdmin] != 5) return true;
	if(lego == -1) return true;
	if(lego != playerid) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла неизвестная ошибка");
	if(lastobj == 0) return SendClientMessage(playerid, COLOR_ORANGE, "Вы не ставили объект либо вы уже удалили предыдущий");
	SendClientMessage(playerid, COLOR_GREEN, "Предыдущий объект был удалён");
	DestroyObject(lastobj);
	return lastobj = 0;
}

CMD:editobj(playerid)
{
    if(PlayerInfo[playerid][pAdmin] != 5) return true;
	if(lego == -1) return true;
	if(lego != playerid) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла неизвестная ошибка");
	SelectObject(playerid);
	return SendClientMessage(playerid, COLOR_GREEN, "Выберите объект указателем");
}

CMD:newactor(playerid)
{
	if(PlayerInfo[playerid][pAdmin] != 5) return true;
	if(lego == -1) return true;
	if(lego != playerid) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла неизвестная ошибка");
	return ShowPlayerDialog(playerid, dActorNew, DIALOG_STYLE_INPUT, "{CC9900}Добавление актёра", "{ffffff}Введите ID скина актёра, который вы хотите установить\n\nID скинов можно найти тут: {6699FF}www.samp-ru.org/forum/6-21-1", "Далее", "Закрыть");
}

CMD:editactor(playerid, params[])
{
    if(PlayerInfo[playerid][pAdmin] != 5) return true;
	if(lego == -1) return true;
	if(lego != playerid) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла неизвестная ошибка");
	if(sscanf(params, "i", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используй /editactor [id актёра]");
	if(actorids[params[0]] == -1) return SendClientMessage(playerid, COLOR_LGREY, "Не найден актёр с таким ID");
	new str[10];
	curractor = params[0];
	format(str, sizeof(str), "ID: %d", params[0]);
	return ShowPlayerDialog(playerid, dActorEdit, DIALOG_STYLE_LIST, str, "1. Изменить расположение\n2. Изменить внешность\n3. Изменить анимацию\n4. Убрать инфо об актёре\n5. Удалить актёра", "Выбрать", "Закрыть");
}

CMD:arena(playerid)
{
    if(PlayerInfo[playerid][pJail] > 0) return SendClientMessage(playerid, COLOR_LGREY, "Аррестованым не разрешено покидать камеру");
	if(PlayerInfo[playerid][pArena] != 0) return SendClientMessage(playerid, COLOR_LGREY, "Вам необходимо выйти из арены");
	if(PlayerInfo[playerid][pRoom] != -1) return SendClientMessage(playerid, COLOR_LGREY, "Вам необходимо выйти из комнаты");
	new str[256];
	new tempstr[64];
	strcat(str, "Тип\tКарта\tОнлайн\n");
	for(new i = 1; i != sizeof(onlinearena); i++)
	{
	    if(onlinearena[i] == 0) format(tempstr, sizeof(tempstr), "%s\t{FF5C33}%d\n", namesarena[i], onlinearena[i]);
	    else format(tempstr, sizeof(tempstr), "%s\t{00CC99}%d\n", namesarena[i], onlinearena[i]);
	    strcat(str, tempstr);
	}
	return ShowPlayerDialog(playerid, dArena, DIALOG_STYLE_TABLIST_HEADERS, "{ffdd00}Арена", str, "Зайти", "Закрыть");
}

CMD:rooms(playerid)
{
    if(PlayerInfo[playerid][pJail] > 0) return SendClientMessage(playerid, COLOR_LGREY, "Аррестованым не разрешено покидать камеру");
    if(PlayerInfo[playerid][pArena] != 0) return SendClientMessage(playerid, COLOR_LGREY, "Вам необходимо выйти из арены");
    if(PlayerInfo[playerid][pRoom] != -1) return SendClientMessage(playerid, COLOR_LGREY, "Вам необходимо выйти из комнаты");
    new map[48];
	new str[1024];
	new tempstr[64];
	new a;
	strcat(str, "Создал\tКарта\tОнлайн\n");
	for(new i = 0; i != sizeof(RoomInfo); i++)
	{
	    if(RoomInfo[i][rID] != -1)
	    {
	        if(RoomInfo[i][rMap] == 1) map = "Заброшеная деревня";
			if(RoomInfo[i][rOnline] == 0) format(tempstr, sizeof(tempstr), "%s\t%s\t{FF5C33}0\n", PlayerInfo[RoomInfo[i][rCreateID]][pName], map);
			else format(tempstr, sizeof(tempstr), "%s\t%s\t{00CC99}%d\n", PlayerInfo[RoomInfo[i][rCreateID]][pName], map, RoomInfo[i][rOnline]);
			strcat(str, tempstr);
			roomids[a] = RoomInfo[i][rID];
	        a++;
	    }
	}
 	return ShowPlayerDialog(playerid, dRooms, DIALOG_STYLE_TABLIST_HEADERS, "{ffdd00}Список комнат", str, "Инфо", "Закрыть");
}

CMD:pvp(playerid, params[])
{
	if(PlayerInfo[playerid][pJail] > 0) return SendClientMessage(playerid, COLOR_LGREY, "Аррестованым не разрешено покидать камеру");
	if(sscanf(params, "d", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используйте /pvp [id игрока]");
	if(PlayerInfo[params[0]][pAR] != 0 || !IsPlayerConnected(params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Такого игрока нет");
	if(playerid == params[0]) return SendClientMessage(playerid, COLOR_LGREY, "Нельзя предложить дуэль самому себе");
	if(startPVP{playerid} == 1) return SendClientMessage(playerid, COLOR_LGREY, "Вам необходимо закончить дуэль");
	if(startPVP{params[0]} == 1) return SendClientMessage(playerid, COLOR_LGREY, "Соперник на дуэли");
	if(isOffered{params[0]} == 1) return SendClientMessage(playerid, COLOR_LGREY, "Игроку необходимо принять или отклонить предложение");
	if(isOfferedTo{params[0]} == 1) return SendClientMessage(playerid, COLOR_LGREY, "Игроку необходимо отозвать своё предложение");
	if(isOffered{playerid} == 1) return SendClientMessage(playerid, COLOR_LGREY, "Необходимо принять или отклонить предыдущее предложение");
	if(isOfferedTo{playerid} == 1) return SendClientMessage(playerid, COLOR_WHITE, "Используйте {FF9933}/cancel{ffffff} для отмены предыдущего предложения");
	offerID[playerid] = params[0];
	return ShowPlayerDialog(playerid, dPvp, DIALOG_STYLE_TABLIST_HEADERS, "{ffdd00}PVP", "{00cc66}Выберите оружие для PVP\n1. Desert Eagle", "Выбрать", "Отмена");
}

CMD:cancel(playerid)
{
    if(isOfferedTo{playerid} == 0) return SendClientMessage(playerid, COLOR_LGREY, "В данный момент нет активных предложений");
    new str[128];
    format(str, sizeof(str), "%s отозвал своё предложение", PlayerInfo[playerid][pName]);
    SendClientMessage(offerID[playerid], COLOR_ORANGE, str);
    SendClientMessage(playerid, COLOR_GREEN, "Вы отозвали своё предложение");
    return ClearOffersVars(playerid);
}

CMD:yes(playerid)
{
	if(isOffered{playerid} == 0) return SendClientMessage(playerid, COLOR_LGREY, "В данный момент нет активных предложений");
	if(typeOffer{playerid} == 1)
	{
	    if(isOfferedTo{offerID[playerid]} == 0) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла неизвестная ошибка");
	    new str[128];
    	format(str, sizeof(str), "%s принял ваше предложение", PlayerInfo[playerid][pName]);
    	SendClientMessage(offerID[playerid], COLOR_GREEN, str);
	    return SetPlayersSpawnPvp(playerid, offerID[playerid]);
	}
	return true;
}

CMD:no(playerid)
{
    if(isOffered{playerid} == 0) return SendClientMessage(playerid, COLOR_LGREY, "В данный момент нет активных предложений");
	if(typeOffer{playerid} == 1)
	{
	    if(isOfferedTo{offerID[playerid]} == 0) return SendClientMessage(playerid, COLOR_ORANGE, "Произошла неизвестная ошибка");
	    new str[128];
	    format(str, sizeof(str), "%s отклонил Ваше предложение", PlayerInfo[playerid][pName]);
	    SendClientMessage(offerID[playerid], COLOR_ORANGE, str);
	    ClearOffersVars(playerid);
	    return SendClientMessage(playerid, COLOR_ORANGE, "Вы отклонили предложение");
	}
	return true;
}




CMD:bug(playerid, params[])
{
	if(sscanf(params, "s[256]", params[0])) return SendClientMessage(playerid, COLOR_LGREY, "Используйте /bug [сообщение о баге]");
	new str[256];
	mysql_format(mysql_connection, str, sizeof(str), "INSERT INTO `bugs`(`name`, `text`, `date`) VALUES ('%s','%s',NOW())", PlayerInfo[playerid][pName], params[0]);
	mysql_tquery(mysql_connection, str, "", "");
	return SendClientMessage(playerid, COLOR_GREEN, "Сообщение было успешно отправлено!");
}
