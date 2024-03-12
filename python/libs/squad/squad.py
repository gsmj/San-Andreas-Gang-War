from dataclasses import dataclass, field
from typing import Any, Union

from pysamp.player import Player

from ..database.database import DataBase
from ..utils.data import Colors, ServerMode

squad_permissions: dict[str, str] = {
    "Все разрешения": "all",
    "Приглашать участников": "invite",
    "Выгонять участников": "uninvite",
    "Управлять фракцией": "manage",
    "Начинать войну": "startwar",
    "Повышать участников": "giverank",
    "Понижать участников": "takerank",
}
squad_permissions_converter: dict[str, str] = {
    "all": "Все разрешения",
    "invite": "Приглашать участников",
    "uninvite": "Выгонять участников",
    "manage": "Управлять фракцией",
    "startwar": "Начинать войну",
    "giverank": "Повышать участников",
    "takerank": "Понижать участников",
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
    ranks: dict[str, str] = field(default_factory=lambda: {})
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
        print(self.ranks)

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

    def is_leader(self, player: "Player") -> bool:
        try:
            self.members[player.name]
        except:
            return False

        for rank in self.ranks[self.members[player.name]]:
            if rank == "all":
                return True

        return True

    def is_member(self, player: "Player") -> bool:
        try:
            self.members[player.name]
        except:
            return False

        return True

    def has_permissions(self, player: "Player", *permissions: tuple[str]) -> Union[str, bool]:
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
        DataBase.create_squad_rank(self.uid, self.rank, permissions)
        self.ranks[rank] = permissions

    def kick_member(self, member: Player) -> None:
        del self.members[member.name]
        DataBase.delete_squad_member(member.name)
