from ..database.database import DataBase
from ..utils.data import ServerMode, Colors
from dataclasses import dataclass, field
from pysamp.player import Player


squad_permissions: tuple = (
    "all"
    "invite",
    "uninvite",
    "settings"
    "startwar",
    "giverank",
    "takerank",
)

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

@dataclass(repr=False)
class SquadGangZone:
    id: int
    squad_id: int
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

from pprint import pprint # TODO: Убрать на релизе

@dataclass(repr=False)
class SquadMembers:
    """
    squad - squad name\n
    memmber = player name\n
    rank = squad rank\n
    """
    squad: str
    member: str
    rank: str

@dataclass(repr=False)
class SquadRanks:
    squad: str
    rank: str
    permissions: str


@dataclass(repr=False)
class Squad:
    name: str
    tag: str
    leader: str
    classification: str
    color: int
    color_hex: str
    members: list["SquadMembers"] = field(default_factory=lambda: [])
    ranks: list["SquadRanks"] = field(default_factory=lambda: [])

    def __post_init__(self) -> None:
        members_db = DataBase.load_squad_members(self.name)
        if members_db:
            for i in members_db:
                self.members.append(SquadMembers(self.name, i.member, i.rank))

        ranks_db = DataBase.load_squad_ranks(self.name)
        if ranks_db:
            for i in ranks_db:
                self.ranks.append(SquadRanks(self.name, i.rank, i.permissions))

        pprint(f"Загружен Squad:\n{self}\nMembers: {self.members}\nRanks: {self.ranks}")

    @classmethod
    def create(cls, name: str, tag: str, leader: str, classification: str, color: int, color_hex: str) -> "Squad":
        squad = DataBase.create_squad(name, tag, leader, classification, color, color_hex)
        ranks = DataBase.load_squad_ranks(squad.name)
        inst = cls(name, tag, leader, classification, color, color_hex)
        for i in ranks:
            inst.ranks.append(SquadRanks(name, i.rank, i.permissions))

        return inst

    def is_leader(self, player: "Player") -> bool:
        return True if player.name == self.leader else False


