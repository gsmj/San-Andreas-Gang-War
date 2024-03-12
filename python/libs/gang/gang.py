from dataclasses import dataclass

from pystreamer.dynamiccp import DynamicCheckpoint
from pystreamer.dynamicpickup import DynamicPickup

from ..utils.data import Colors, ServerMode


@dataclass(repr=False)
class Gang:
    skins: list[int]
    gang_name: str
    gang_id: int
    rangs: dict[int, str]
    color: int
    game_text_color: str
    color_hex: str
    map_icon: int
    warehouse: DynamicCheckpoint
    enter_exit: list[DynamicPickup]
    spawn_pos: list[float, float, float]
    interior_id: int
    capture_id: int = -1,
    is_capturing: bool = False

gangzone_pool: dict[int, "GangZoneData"] = {}
"""
Key: Gangzone id
Value: GangZoneData dataclass
"""

@dataclass(repr=False)
class GangZoneData:
    id: int
    gang_id: int
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
        gangzone_pool[self.id] = self

gangs = { # ID: Gang inst
    -1: Gang(
        [0],
        "Нет",
        -1,
        {50: "Нет", 100: "Нет", 150: "Нет", 200: "Нет", 250: "Нет", 300: "Нет", 350: "Нет", 400: "Нет", 450: "Нет", 500: "Нет"},
        -1,
        "",
        Colors.dialog_hex,
        0,
        None,
        None,
        [0.0],
        0,
    ),
    0: Gang(
        [86, 105, 106, 107, 149, 195, 269, 270, 271], # Grove skins
        "The Families",
        0, # Grove id
        {50: "Newman", 100: "Hustla", 150: "Huckster", 200: "True", 250: "Warrior", 300: "Gangsta", 350: "O.G", 400: "Big Bro", 450: "Legend", 500: "Daddy"}, # Grove rangs
        Colors.grove,
        Colors.game_text_groove,
        Colors.grove_hex,
        62,
        DynamicCheckpoint.create(2455.5740, -1706.3229, 1013.5078, 1.0, world_id=ServerMode.gangwar_world, interior_id=2, stream_distance=25.0), # Grove warehouse
        [
            DynamicPickup.create(1318, 23, 2495.4265, -1691.1404, 14.7656, world_id=ServerMode.gangwar_world, interior_id=0), # Grove enter
            DynamicPickup.create(1318, 23, 2468.8428, -1698.2579, 1013.5078, world_id=ServerMode.gangwar_world) # Grove exit
        ],
        [2452.0325, -1700.2831, 1013.5078], # Spawn pos
        2 # Interior id
        ),
    1: Gang(
        [102, 103, 104, 195],
        "The Ballas",
        1,
        {50: "Baby", 100: "Tested", 150: "Cracker", 200: "Nigga", 250: "Big Nigga", 300: "Gangster", 350: "Defender", 400: "Shooter", 450: "Star", 500: "Big Daddy"},
        Colors.ballas,
        Colors.game_text_ballas,
        Colors.ballas_hex,
        59,
        DynamicCheckpoint.create(-42.5511, 1412.5063, 1084.4297, 1.0, world_id=ServerMode.gangwar_world, interior_id=8, stream_distance=25.0),
        [
            DynamicPickup.create(1318, 23, 2022.8790, -1120.2637, 26.4210, world_id=ServerMode.gangwar_world, interior_id=0),
            DynamicPickup.create(1318, 23, -42.6055, 1405.7949, 1084.4297, world_id=ServerMode.gangwar_world)
        ],
        [-49.8575, 1408.5522, 1084.4297],
        8
    ),
    2: Gang(
        [108, 109, 110, 190],
        "Los Santos Vagos",
        2,
        {50: "Mamarracho", 100: "Compinche", 150: "Bandito", 200: "Vato Loco", 250: "Chaval", 300: "Forajido", 350: "Veterano", 400: "Elite", 450: "El Orgullo", 500: "Padre"},
        Colors.vagos,
        Colors.game_text_vagos,
        Colors.vagos_hex,
        60,
        DynamicCheckpoint.create(333.0990,1118.9160,1083.8903, 1.0, world_id=ServerMode.gangwar_world, interior_id=5, stream_distance=25.0),
        [
            DynamicPickup.create(1318, 23, 2756.2825, -1182.4691, 69.3998, world_id=ServerMode.gangwar_world, interior_id=0),
            DynamicPickup.create(1318, 23, 318.6152, 1114.8966, 1083.8828, world_id=ServerMode.gangwar_world)
        ],
        [321.0667, 1123.1947, 1083.8828],
        5
    ),
    3: Gang(
        [114, 115, 116, 193, 292],
        "Varrios Los Aztecas",
        3,
        {50: "Novato", 100: "Amigo", 150: "Asistente", 200: "Asesino", 250: "Latinos", 300: "Mejor", 350: "Empresa", 400: "Aproximado", 450: "Diputado", 500: "Padre"},
        Colors.aztecas,
        Colors.game_text_aztecas,
        Colors.aztecas_hex,
        58,
        DynamicCheckpoint.create(223.0524, 1249.5559, 1082.1406, 1.0, world_id=ServerMode.gangwar_world, interior_id=2, stream_distance=25.0),
        [
            DynamicPickup.create(1318, 23, 2185.8176, -1814.6786, 13.5469, world_id=ServerMode.gangwar_world, interior_id=0),
            DynamicPickup.create(1318, 23, 225.756989, 1240.000000, 1082.149902, world_id=ServerMode.gangwar_world)
        ],
        [219.6040, 1241.9434, 1082.1406],
        2
    ),
    4: Gang(
        [173, 174, 175, 226, 273],
        "Los Santos Rifa",
        4,
        {50: "Amigo", 100: "Macho", 150: "Junior", 200: "Ermanno", 250: "Bandido", 300: "Autoridad", 350: "Adjunto", 400: "Veterano", 450: "Vato Loco", 500: "Padre"},
        Colors.rifa,
        Colors.game_text_rifa,
        Colors.rifa_hex,
        61,
        DynamicCheckpoint.create(-71.8009, 1366.5933, 1080.2185, 1.0, world_id=ServerMode.gangwar_world, interior_id=6, stream_distance=25.0),
        [
            DynamicPickup.create(1318, 23, 2787.0759, -1926.1780, 13.5469, world_id=ServerMode.gangwar_world, interior_id=0),
            DynamicPickup.create(1318, 23, -68.8279, 1351.3553, 1080.2109, world_id=ServerMode.gangwar_world)
        ],
        [-59.1456, 1364.5851, 1080.2109],
        6
    )
}
