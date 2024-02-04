from dataclasses import dataclass
from .consts import TIMER_ID_NONE, SLOT_ID_NONE


@dataclass
class PlayerDriftData:
    money: int = 0
    score: int = 0
    combo: int = 1
    timer_id: int = TIMER_ID_NONE


@dataclass
class PlayerFreeroamGunSlots:
    slots = {
        0: SLOT_ID_NONE, # Not used
        1: SLOT_ID_NONE, # Melee
        2: SLOT_ID_NONE, # Pistol
        3: SLOT_ID_NONE, # Shotgun
        4: SLOT_ID_NONE, # Machine gun
        5: SLOT_ID_NONE, # Assault rifle
        6: SLOT_ID_NONE  # Long rifle
    }

@dataclass
class PlayerVIP:
    level: int = -1
    is_random_clist_enabled: bool = False
    random_clist_timer_id: int = TIMER_ID_NONE
    gangwar_template = ("0, 0, 0")


@dataclass
class PlayerAdmin():
    """
    Level 2:
    /jail, /unjail, /mute, /unmute, /hp, /goto, /gethere\n
    Level 3:
    /setnick, /slap, /freeze, /unfreeze, /ban, /unban\n
    Level 4:
    /settime, /getip, /bantime, /givegun, /sethp\n
    Level 5:
    /amusic, /obj\n
    Level 6:
    /deleteaccount, /vipcode, /givevip, /setgangzone, /setvw, /setemail, /setpassword\n
    /debug_python, /debug_events, /debug_players, /debug_player_attrs
    """
    level: int = 6
    pos_x_spec: float = 0.0
    pos_y_spec: float = 0.0
    pos_z_spec: float = 0.0
    world_id_before_spec: int = -1
    interior_id_before_spec: int = -1
    on_spawn_state_spectating: bool = False


    def check_command_access(self, level: int) -> bool:
        if self.level < level:
            return False

        return True
