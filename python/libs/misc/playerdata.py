from dataclasses import dataclass, field

from pysamp.timer import kill_timer, set_timer

from ...vehicle import Vehicle
from ..house.house import House
from ..utils.consts import SLOT_ID_NONE, TIMER_ID_NONE


@dataclass(repr=False)
class PlayerDrift:
    money: int = 0
    score: int = 0
    combo: int = 1
    timer_id: int = TIMER_ID_NONE


@dataclass(repr=False)
class PlayerFreeroamGunSlots:
    fist: int = SLOT_ID_NONE # Fist. Not used
    melee: int = SLOT_ID_NONE # Melee
    pistol: int = SLOT_ID_NONE # Pistol
    shotgun: int = SLOT_ID_NONE # Shotgun
    machine_gun: int = SLOT_ID_NONE # Machine gun
    assault_rifle: int = SLOT_ID_NONE # Assault rifle
    long_rifle: int = SLOT_ID_NONE # Long rifle


@dataclass(repr=False)
class PlayerVIP:
    level: int = -1
    is_random_clist_enabled: bool = False
    random_clist_timer_id: int = TIMER_ID_NONE
    gangwar_template = ("0, 0, 0")
    random_clist_iterator: int = 0

    def disable_clist_timer_for_player(self) -> None:
        if self.random_clist_timer_id != TIMER_ID_NONE:
            kill_timer(self.random_clist_timer_id)

@dataclass(repr=False)
class PlayerAdmin:
    level: int = 0
    world_id_before_spec: int = -1
    interior_id_before_spec: int = -1

    def check_command_access(self, level: int) -> bool:
        if self.level < level:
            return False

        return True


@dataclass(repr=False)
class PlayerChecks:
    muted: bool = False
    jailed: bool = False
    logged: bool = False
    banned: bool = False
    selected_skin: bool = False
    wearing_mask: bool = False
    saw_bottom_textdraw: bool = False
    in_house: bool = False
    invulnerable: bool = False


@dataclass(repr=False)
class PlayerTime:
    cooldown: float = 0.0
    pickup_cooldown: float = 0.0
    jail: int = 0
    mute: int = 0
    afk: int = 0


@dataclass(repr=False)
class PlayerSettings:
    disabled_ping_td: bool = True # Чтобы при коннекте не показывать
    disabled_global_chat_gw: bool = False
    spawn_in_house: bool = False
    outdated_version_warning: bool = False
    use_squad_tag_in_text: bool = False


@dataclass(repr=False)
class PlayerTimers:
    jail_id: int = TIMER_ID_NONE
    mute_id: int = TIMER_ID_NONE
    every_sec: int = TIMER_ID_NONE
    deathmatch_in_area: int = TIMER_ID_NONE


@dataclass(repr=False)
class PlayerVehicle:
    inst: Vehicle = None
