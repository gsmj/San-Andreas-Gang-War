from dataclasses import dataclass, field
from typing import Any, Union

from pysamp.player import Player
from pysamp import gang_zone_show_for_player, gang_zone_hide_for_player, gang_zone_flash_for_player, gang_zone_stop_flash_for_player
from pystreamer import create_dynamic_map_icon, destroy_dynamic_map_icon

from ..database.database import DataBase
from ..utils.data import Colors, ServerMode, get_center, convert_seconds
from ..static.textdraws import squad_capture_td

squad_capture_dict: dict[str, tuple[str, "Squad", "Squad", int, str]] = {}
"""
Key: Инициатор войны
Values: Инициатор войны, Атака, Защита, GangZone Id, Название зоны
"""

squad_permissions: dict[str, str] = {
    "Все разрешения": "all",
    "Приглашать участников": "invite",
    "Выгонять участников": "uninvite",
    "Управлять фракцией": "manage",
    "Начинать войну": "startwar",
    "Повышать участников": "giverank",
    "Понижать участников": "takerank",
    "Ничего": "none"
}
squad_permissions_converter: dict[str, str] = {
    "all": "Все разрешения",
    "invite": "Приглашать участников",
    "uninvite": "Выгонять участников",
    "manage": "Управлять фракцией",
    "startwar": "Начинать войну",
    "giverank": "Повышать участников",
    "takerank": "Понижать участников",
    "none": "Ничего"
}

squad_gangzone_pool: dict[int, "SquadGangZone"] = {}
"""
Key: Gangzone id
Value: SquadGangZone dataclass
"""
squad_pool: dict[str, "Squad"] = {}
"""
Key: Squad name
Value: Squad dataclass
"""
squad_pool_id: dict[int, "Squad"] = {}
"""
Key: Squad id
Value: Squad dataclass
"""
map_icons: list = []


@dataclass(repr=False)
class SquadGangZone:
    id: int
    squad_id: int
    color: int
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    capture_cooldown: int
    gang_atk_id: int = -1
    gang_def_id: int = -1
    gang_atk_score: int = 0
    gang_def_score: int = 0
    capture_time: int = 0
    is_capture: bool = False

    def __post_init__(self) -> None:
        squad_gangzone_pool[self.id] = self

    def restore_to_defaults(self) -> None:
        self.capture_cooldown = 900
        self.gang_atk_id = -1
        self.gang_def_id = -1
        self.gang_atk_score = 0
        self.gang_def_score = 0
        self.capture_time = 0
        self.is_capture = False

    def show_for_player(self, player: Player) -> None:
        gang_zone_show_for_player(player.id, self.id, self.color)

    def disable_for_player(self, player: Player) -> None:
        gang_zone_hide_for_player(player.id, self.id)

    def start_war(self, player: Player, squad_atk: "Squad", squad_def: "Squad") -> None:
        self.gang_atk_id = squad_atk.uid
        self.gang_def_id = squad_def.uid
        self.capture_cooldown = 0
        self.capture_time = 900
        self.is_capture = True
        self.update_capture_textdraw()
        # Set params for Squads:
        Squad.send_war_message(player, player._registry)
        squad_atk.start_war(self.id, player, player._registry)
        squad_def.start_war(self.id, player, player._registry)
        for i in player._registry.values():
            i: Player
            if i.mode != ServerMode.freeroam_world:
                continue

            if not i.squad:
                continue

            if not i.squad.uid == squad_atk.uid or not i.squad.uid == squad_def.uid:
                continue

            Squad.show_capture_textdraws_for_player(i)
            i.set_team(i.squad.uid)
            i.send_notification_message("Во время войны урон по своим был отключён!")
            Squad.give_guns_for_player(i)
            gang_zone_flash_for_player(i.id, self.id, squad_atk.color)

        map_icons.append(create_dynamic_map_icon(
            *get_center(self.min_x, self.max_x, self.min_y, self.max_y),
            0.0,
            23,
            0,
            world_id=ServerMode.gangwar_world,
            interior_id=0,
            style=1
            ))
        del squad_capture_dict[player.name]

    def end_war(self, registry: dict[int, "Player"]) -> None:
        win = False
        if self.gang_atk_score >= self.gang_def_score:
            win = True
            self.squad_id = self.gang_atk_id
            self.color = squad_pool_id[self.gang_atk_id].color

        s_atk = squad_pool_id[self.gang_atk_id]
        s_def = s_atk = squad_pool_id[self.gang_def_id]
        DataBase.save_squad_gangzone(
            id=self.id,
            squad_id=self.squad_id,
            color=self.color,
            capture_cooldown=900,
        )
        for player in registry.values():
            player: Player
            if player.mode != ServerMode.freeroam_world:
                continue

            if not player.squad:
                continue

            if not player.squad.uid == self.gang_atk_id or not player.squad.uid == self.gang_def_id:
                continue

            player.set_team(255)
            player.send_notification_message(f"{s_atk.classification} {{{s_atk.color_hex}}}{s_atk.name}{{{Colors.white_hex}}} {'захватила' if win else 'не смогла захватить'} территорию!")
            player.send_notification_message(f"Счёт: {{{s_atk}}}{self.gang_atk_score}{{{Colors.white_hex}}} - {{{s_def.color_hex}}}{self.gang_def_score}{{{Colors.white_hex}}}.")
            Squad.hide_capture_textdraws(player)
            gang_zone_stop_flash_for_player(player.id, self.id)
            Squad.reload_gangzones_for_player(player)

        for icon in map_icons:
            destroy_dynamic_map_icon(icon)

        s_atk.stop_war()
        s_def.stop_war()
        self.restore_to_defaults()

    def update_capture_textdraw(self) -> None:
        _, m, s = convert_seconds(self.capture_time)
        squad_atk = squad_pool_id[self.gang_atk_id] # It's bad to get inst every N secs
        squad_def = squad_pool_id[self.gang_def_id]
        squad_capture_td[0].set_string(f"Time: {m}:{s}")
        squad_capture_td[1].set_string(f"{squad_atk.tag} ~r~{self.gang_atk_score}")
        squad_capture_td[1].color(squad_atk.color)
        squad_capture_td[2].set_string(f"{squad_def.tag} ~r~{self.gang_def_score}")
        squad_capture_td[2].color(squad_def.color)

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        DataBase.save_squad_gangzone(self.id, **kwargs)


@dataclass(repr=False)
class Squad:
    uid: int
    name: str
    tag: str
    classification: str
    color: int
    color_hex: str
    members: dict[str, str] = field(default_factory=lambda: {})
    """
    Key: Member name
    Values: Rank name
    """
    ranks: dict[str, list[str]] = field(default_factory=lambda: {})
    """
    Key: Rank name
    Values: Rank permissions
    """
    is_capturing: bool = False
    capture_id: int = -1

    def __post_init__(self) -> None:
        members_db = DataBase.load_squad_members(self.uid)
        if members_db:
            for i in members_db:
                self.members[i.member] = i.rank

        ranks_db = DataBase.load_squad_ranks(self.uid)
        if ranks_db:
            for i in ranks_db:
                self.ranks[i.rank] = DataBase.load_squad_permissions_for_rank(self.uid, i.uid)

        squad_pool[self.name] = self
        squad_pool_id[self.uid] = self
        print("Members:")
        print(f"\t{self.members}\n")
        print("Ranks:")
        print(f"\t{self.ranks}\n")

    @classmethod
    def create(cls, name: str, tag: str, leader: str, classification: str, color: int, color_hex: str) -> "Squad":
        squad = DataBase.create_squad(name, tag, leader, classification, color, color_hex)
        return cls(squad.uid, name, tag, classification, color, color_hex)

    @classmethod
    def create_all(cls) -> None:
        squads = DataBase.load_squads()
        if squads:
            for squad in squads:
                Squad(
                    squad.uid,
                    squad.name,
                    squad.tag,
                    squad.classification,
                    squad.color,
                    squad.color_hex,
                )

    def has_permissions(self, player: "Player", *permissions: tuple[str]) -> bool:
        try:
            self.members[player.name]
        except:
            return False

        for rank in self.ranks[self.members[player.name]]:
            if rank in permissions:
                return True

        return True

    def update(self, **kwargs: dict[Any]) -> None:
        """
        Обновление датакласса и ORM-класса в БД
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        DataBase.save_squad(self.uid, **kwargs)

    def create_rank(self, rank: str, permissions: list) -> None:
        buffer: list = []
        for i in permissions:
            buffer.append(squad_permissions[i])

        DataBase.create_squad_rank(self.uid, rank, buffer)
        self.ranks[rank] = buffer

    def update_rank(self, rank_name: str, **kwargs: dict[Any]) -> None:
        for value in self.members.copy().values():
            if value == rank_name:
                self.ranks[value] = kwargs["rank"]

        for key, value in self.ranks.copy().items():
            if key == rank_name:
                del self.ranks[key]
                self.ranks[kwargs["rank"]] = value

        DataBase.save_squad_rank(self.uid, rank_name, **kwargs)

    def kick_member(self, member: Player) -> None:
        del self.members[member.name]
        DataBase.delete_squad_member(member.name)

    def delete_rank(self, rank: str) -> None:
        DataBase.delete_squad_rank(self.uid, rank)

    def create_member(self, member: str, rank: str) -> None:
        self.members[member] = rank
        DataBase.create_squad_member(self.uid, member, rank)

    def update_member_rank(self, member: str, rank: str) -> None:
        self.members[member] = rank
        DataBase.save_squad_member(member, rank=rank)

    def start_war(self, capture_id: int, initiator: Player, pool: dict) -> None:
        self.is_capturing = True
        self.capture_id = capture_id

    def stop_war(self) -> None:
        self.is_capturing = False
        self.capture_id = -1

    @staticmethod
    def send_war_message(initiator: Player, pool: dict) -> None:
        capture = squad_capture_dict[initiator.name]
        s_atk = capture[1]
        s_def = capture[2]
        gz_name = capture[3]
        for player in pool.values():
            if player.mode != ServerMode.freeroam_world:
                continue

            if not player.squad:
                continue

            if not player.squad.uid == s_atk.uid or not player.squad.uid.uid == s_def.uid:
                continue

            player.send_notification_message(
                f"{{{s_atk.color_hex}}}{initiator.name}{{{Colors.white_hex}}} инициировал захват территории {{{Colors.cmd_hex}}}{gz_name}{{{Colors.white_hex}}}!"
            )
            player.send_notification_message(
                f"Началась война между {{{s_atk.color_hex}}}{s_atk.name}{{{Colors.white_hex}}} и {{{s_def.color_hex}}}{s_def.name}{{{Colors.white_hex}}}!"
            )

    @staticmethod
    def show_squad_gangzones_for_player(player: Player) -> None:
        for gangzone in squad_gangzone_pool.values():
            gangzone.show_for_player(player)

    @staticmethod
    def disable_gangzones_for_player(player: Player):
        for gangzone in squad_gangzone_pool.values():
            gangzone.disable_for_player(player)

    @staticmethod
    def reload_gangzones_for_player(player: Player):
        for gangzone in squad_gangzone_pool.values():
            gangzone.disable_for_player(player)
            gangzone.show_for_player(player)

    @staticmethod
    def show_capture_textdraws_for_player(player: Player) -> None:
        for td in squad_capture_td.values():
            td.show_for_player(player)

    @staticmethod
    def hide_capture_textdraws(player: Player) -> None:
        for td in squad_capture_td.values():
            td.hide_for_player(player)

    @staticmethod
    def give_guns_for_player(player: Player) -> None:
        player.reset_weapons()
        player.give_weapon(24, 150)
        player.give_weapon(31, 500)
        player.set_armour(100.0)
