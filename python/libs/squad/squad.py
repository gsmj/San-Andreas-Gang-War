from dataclasses import dataclass, field
from typing import Any
from pysamp.player import Player
from pysamp.timer import set_timer, kill_timer
from pysamp import gang_zone_show_for_player, gang_zone_hide_for_player, gang_zone_flash_for_player, gang_zone_stop_flash_for_player
from pystreamer import create_dynamic_map_icon, destroy_dynamic_map_icon
from transliterate import translit
from ..database.database import DataBase
from ..utils.data import Colors, ServerMode, get_center, convert_seconds, has_cyrillic
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
squad_pool_id: dict[int, "Squad"] = {}
"""
Key: Squad id
Value: Squad dataclass
"""
map_icons: list = []

squad_gangzone_positions: dict[int, tuple[tuple[float, float, float]]] = {
    131: (
        (2787.637451171875, -2485.85546875, 13.65046215057373),
        (2787.712646484375, -2447.54296875, 13.633682250976562),
        (2787.494384765625, -2409.679443359375, 13.633734703063965),
        (2650.052734375, -2427.734619140625, 13.6328125),
        (2710.692626953125, -2555.00244140625, 13.63265323638916)
        ),
    157: (
        (1972.56396484375, -1236.0860595703125, 20.055017471313477),
        (1968.8704833984375, -1156.31396484375, 20.966943740844727),
        (2052.04443359375, -1156.390625, 23.578725814819336),
        (1117.01611328125, -297.6885681152344, 73.9921875),
        (-1073.9674072265625, -1296.69580078125, 129.21875)
    ),
    140: (
        (-1849.32666015625, -1703.76904296875, 40.843994140625),
        (-1860.013427734375, -1546.4088134765625, 21.75),
        (-1820.68994140625, -1614.494873046875, 23.015625),
        (-1903.07080078125, -1672.23486328125, 23.021526336669922),
        (-1892.3404541015625, -1618.53466796875, 21.756410598754883)
    ),
    135: (
        (1045.4622802734375, -294.7304382324219, 73.99308013916016),
        (1019.6592407226562, -292.3092041015625, 73.99308013916016),
        (1070.51318359375, -365.40472412109375, 73.9921875)
    ),
    141: (
        (-1426.845947265625, -1577.690673828125, 101.7578125),
        (-1458.7061767578125, -1546.117919921875, 101.7578125),
        (-1465.251708984375, -1510.9854736328125, 101.75132751464844),
        (-1458.2471923828125, -1475.5030517578125, 101.7578125),
        (-1422.91748046875, -1503.036376953125, 105.0390625),
        (-1446.6553955078125, -1445.0894775390625, 101.7578125)
    ),
    134: (
        (1549.5611572265625, 13.212623596191406, 24.145244598388672),
        (1521.2900390625, 20.61304473876953, 24.140625),
        (1589.8306884765625, 23.060819625854492, 24.108013153076172)
    ),
    139: (
        (-1111.935546875, -1674.0316162109375, 76.3671875),
        (-1110.30810546875, -1636.9847412109375, 76.3671875),
        (-1113.0001220703125, -1621.2020263671875, 76.37393951416016),
        (-1088.773681640625, -1674.780029296875, 76.37393951416016)
    ),
    133: (
        (1924.1995849609375, 158.87045288085938, 40.173858642578125),
        (1903.4754638671875, 165.77462768554688, 37.140625),
        (1946.12939453125, 153.23155212402344, 37.00267028808594)
    ),
    132: (
        (2240.248046875, -71.78141784667969, 26.508005142211914),
        (2254.71923828125, 72.65162658691406, 26.484375),
        (2315.622802734375, 2.1793484687805176, 26.484375),
        (2533.19677734375, 144.33546447753906, 26.60219383239746),
        (2424.769775390625, -57.732696533203125, 27.46770477294922)
    ),
    156: (
        (748.16552734375, 257.8209533691406, 27.0859375),
        (718.67626953125, 300.68133544921875, 20.234375),
        (758.611083984375, 375.0307312011719, 23.195844650268555),
        (812.0028076171875, 373.365234375, 19.319721221923828)
    ),
    143: (
        (-938.7965087890625, -487.7982482910156, 25.9609375),
        (-953.3414916992188, -494.5957946777344, 25.9609375),
        (-941.1228637695312, -545.2308349609375, 25.953638076782227),
        (-922.8872680664062, -540.7822265625, 25.953638076782227),
        (-909.603759765625, -533.0670776367188, 25.953638076782227),
        (-932.7783813476562, -519.5177001953125, 25.953638076782227)
    ),
    151: (
        (568.76318359375, 821.202880859375, -29.897293090820312),
        (625.3603515625, 898.8088989257812, -37.99587631225586),
        (679.4249267578125, 825.5299682617188, -42.9609375)
    ),
    150: (
        (-1797.91650390625, 1297.124755859375, 59.734375),
        (-1791.70166015625, 1309.2183837890625, 22.5625),
        (-1842.372314453125, 1301.6605224609375, 22.5625),
        (-1844.782958984375, 1284.178955078125, 31.858720779418945),
        (-1756.658203125, 1302.761474609375, 37.1484375),
        (-1757.1224365234375, 1302.19775390625, 46.4375),
        (-1779.8634033203125, 1301.7391357421875, 50.4453125)
    ),
    145: (
        (-2306.368408203125, 1544.8372802734375, 18.7734375),
        (-2338.786376953125, 1540.9588623046875, 23.140625),
        (-2388.87109375, 1546.25048828125, 26.046875),
        (-2417.306884765625, 1538.300048828125, 26.046875),
        (-2418.30029296875, 1554.2801513671875, 26.046875),
        (-2436.29541015625, 1529.581787109375, 17.335763931274414),
        (-2438.592041015625, 1546.159912109375, 8.3984375),
        (-2448.2216796875, 1546.4481201171875, 26.046875),
        (-2460.514404296875, 1551.1109619140625, 23.140625),
        (-2471.718505859375, 1540.4471435546875, 33.234375),
        (-2473.5654296875, 1551.82666015625, 33.227333068847656)
    ),
    153: (
        (413.72442626953125, 2536.839599609375, 19.1484375),
        (392.7745666503906, 2600.281494140625, 16.484375),
        (251.91238403320312, 2618.064697265625, 16.755599975585938),
        (256.52880859375, 2411.247802734375, 16.793251037597656)
    ),
    154: (
        (2818.0185546875, 892.2284545898438, 9.824094772338867),
        (2890.63623046875, 920.0973510742188, 10.8984375),
        (2786.205810546875, 964.8583984375, 10.75)
    ),
    149: (
        (-781.17626953125, 2105.37353515625, 60.3828125),
        (-776.6897583007812, 2033.7999267578125, 60.390625),
        (-650.7700805664062, 2111.45068359375, 60.3828125),
        (-845.5144653320312, 2000.2047119140625, 60.3818473815918),
        (-528.9474487304688, 1988.347900390625, 60.390625)
    ),
    155: (
        (2369.34375, 2797.51904296875, 10.8203125),
        (2293.77734375, 2821.64697265625, 10.8203125),
        (2386.35546875, 2758.7841796875, 10.8203125)
    ),
    147: (
        (-1473.75439453125, 2587.107666015625, 59.468353271484375),
        (-1480.2200927734375, 2629.09619140625, 58.78125),
        (-1472.8863525390625, 2620.0380859375, 58.78125),
        (-1463.2669677734375, 2701.49072265625, 55.8359375),
        (-1444.559814453125, 2643.44140625, 55.8359375),
        (-1470.559326171875, 2571.546630859375, 55.8359375),
        (-1447.5914306640625, 2553.462158203125, 55.8359375),
        (-1478.131103515625, 2541.458984375, 55.8359375),
        (-1532.46630859375, 2570.609375, 55.8359375)
    ),
    136: (
        (-588.0367431640625, -110.09642791748047, 67.52691650390625),
        (-541.1400756835938, -74.13179779052734, 62.859375),
        (-536.3555297851562, -61.234657287597656, 62.9921875),
        (-435.33331298828125, -61.12616729736328, 58.875),
        (-488.0637512207031, -174.71131896972656, 78.2109375),
        (-472.70733642578125, -175.99044799804688, 78.2109375)
    ),
}

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

    def start_war(self, player: Player, squad_atk: "Squad", squad_def: "Squad", pool: dict[int, "Player"]) -> None:
        self.gang_atk_id = squad_atk.uid
        self.gang_def_id = squad_def.uid
        self.capture_cooldown = 0
        self.capture_time = 900
        self.is_capture = True
        Squad.send_war_message(player, pool)
        squad_atk.start_war(self.id, player, pool)
        squad_def.start_war(self.id, player, pool)
        self.update_capture_textdraw()
        for i in pool.values():
            if i.mode != ServerMode.freeroam_world:
                continue

            if not i.squad:
                continue

            if i.squad.uid == squad_atk.uid or i.squad.uid == squad_def.uid:
                Squad.show_capture_textdraws_for_player(i)
                i.set_team(i.squad.uid)
                i.send_message("Во время войны урон по своим был отключён!")
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
            )),
        del squad_capture_dict[player.name]

    def end_war(self, registry: dict[int, "Player"]) -> None:
        win = False
        if self.gang_atk_score >= self.gang_def_score:
            win = True
            self.squad_id = self.gang_atk_id
            self.color = squad_pool_id[self.gang_atk_id].color

        s_atk = squad_pool_id[self.gang_atk_id]
        s_def  = squad_pool_id[self.gang_def_id]
        DataBase.save_squad_gangzone(
            id=self.id,
            squad_id=self.squad_id,
            color=self.color,
            capture_cooldown=900,
        )
        for player in registry.values():
            if player.mode != ServerMode.freeroam_world:
                continue

            if not player.squad:
                continue

            if player.squad.uid == self.gang_atk_id or player.squad.uid == self.gang_def_id:
                player.set_team(255)
                player.send_message(f"{s_atk.classification} {{{s_atk.color_hex}}}{s_atk.name}{{{Colors.white_hex}}} {'захватила' if win else 'не смогла захватить'} территорию!")
                player.send_message(f"Счёт: {{{s_atk.color_hex}}}{self.gang_atk_score}{{{Colors.white_hex}}} - {{{s_def.color_hex}}}{self.gang_def_score}{{{Colors.white_hex}}}.")
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
        a_name: str = squad_atk.name
        d_name: str = squad_def.name
        if has_cyrillic(squad_atk.name):
            a_name = translit(squad_atk.name, "ru", reversed=True, strict=True)

        if has_cyrillic(squad_def.name):
            d_name = translit(squad_def.name, "ru", reversed=True, strict=True)

        squad_capture_td[0].set_string(f"Time: {m}:{s}")
        squad_capture_td[1].set_string(f"{a_name}: ~r~{self.gang_atk_score}")
        squad_capture_td[1].color(squad_atk.color)
        squad_capture_td[2].set_string(f"{d_name}: ~r~{self.gang_def_score}")
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

        squad_pool_id[self.uid] = self

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
        if not player.name in self.members:
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
        for member, value in self.members.copy().items():
            if value == rank_name:
                self.members[member] = kwargs["rank"]

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
        gz_name = capture[4]
        for player in pool.values():
            if player.mode != ServerMode.freeroam_world:
                continue

            if not player.squad:
                continue

            if player.squad.uid == s_atk.uid or player.squad.uid == s_def.uid:
                player.send_message(
                    f"{{{s_atk.color_hex}}}{initiator.name}{{{Colors.white_hex}}} инициировал захват территории {{{Colors.cmd_hex}}}{gz_name}{{{Colors.white_hex}}}!"
                )
                player.send_message(
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
    def reload_gangzones_for_player(player: Player, squad_id: int = None, color: int = None, update_color: bool = False):
        for gangzone in squad_gangzone_pool.values():
            if update_color:
                if squad_id == gangzone.squad_id:
                    gangzone.color = color

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

    @staticmethod
    def delete_squad(squad: "Squad") -> None:
        DataBase.delete_squad(squad.uid)
        for gangzone in squad_gangzone_pool.values():
            if gangzone.squad_id == squad.uid:
                gangzone.squad_id = -1
                gangzone.color = 0xFFFFFFAA

        del squad_pool_id[squad.uid]
        del squad



# TODO: Запретить использовать freeroam / vip команды во время сквад капта