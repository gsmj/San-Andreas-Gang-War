from dataclasses import dataclass, field
from .consts import TIMER_ID_NONE, SLOT_ID_NONE, ID_NONE
from .vehicle import Vehicle

@dataclass
class PlayerDrift:
    money: int = 0
    score: int = 0
    combo: int = 1
    timer_id: int = TIMER_ID_NONE


@dataclass
class PlayerFreeroamGunSlots:
    fist: int = SLOT_ID_NONE # Fist. Not used
    melee: int = SLOT_ID_NONE # Melee
    pistol: int = SLOT_ID_NONE # Pistol
    shotgun: int = SLOT_ID_NONE # Shotgun
    machine_gun: int = SLOT_ID_NONE # Machine gun
    assault_rifle: int = SLOT_ID_NONE # Assault rifle
    long_rifle: int = SLOT_ID_NONE # Long rifle

@dataclass
class PlayerVIP:
    level: int = -1
    is_random_clist_enabled: bool = False
    random_clist_timer_id: int = TIMER_ID_NONE
    gangwar_template = ("0, 0, 0")


@dataclass
class PlayerAdmin:
    level: int = 0
    world_id_before_spec: int = -1
    interior_id_before_spec: int = -1

    def check_command_access(self, level: int) -> bool:
        if self.level < level:
            return False

        return True


@dataclass
class PlayerIs:
    muted: bool = False
    jailed: bool = False
    logged: bool = False
    banned: bool = False
    selecting_skin: bool = False
    wearing_mask: bool = False
    saw_bottom_textdraw: bool = False


@dataclass
class PlayerTime:
    cooldown: float = 0.0
    jail: int = 0
    mute: int = 0
    afk: int = 0


@dataclass
class PlayerSettings:
    disabled_ping_td: bool = True # Чтобы при коннекте не показывать
    disabled_global_chat_gw: bool = False


@dataclass
class PlayerTimers:
    jail_id: int = TIMER_ID_NONE
    mute_id: int = TIMER_ID_NONE
    every_sec: int = TIMER_ID_NONE


@dataclass
class PlayerTemp:
    capture_tuple = None
    login_attempts = 1


@dataclass
class PlayerVehicle:
    inst: "Vehicle" = None
