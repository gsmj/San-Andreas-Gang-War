from dataclasses import dataclass
from random import randint
import samp # type: ignore


@dataclass
class ServerInfo:
    name: str = "San Andreas Gang War | 1 | Reborn"
    name_timer = [
        "San Andreas Gang War | 1 | Reborn",
        "San Andreas Gang War | 1 | Reborn | Client: 0.3.7 / 0.3DL",
        "SAGW | 1 | Reborn | Grand Opening",
        "SAGW | 1 | Reborn | Gangs, Drift and more",
    ]
    name_short: str = "SAGW"
    gamemode: str = "DM/TDM/GW/TURFS/Drift/Freeroam"
    language: str = "Russian"
    map: str = "San Andreas"
    CAPTURE_LIMIT: int = 2


@dataclass
class Colors:
    dark_orange: int = 0xFF6600FF
    light_grey: int = 0xB4B5B7FF
    blue: int = 0x319AFFFF
    red: int = 0xFF6347AA
    yellow: int = 0xFFFF00AA
    grove: int = 0x009900AA
    ballas: int = 0xCC00FFAA
    aztecas: int = 0x00b4e1AA
    vagos: int = 0xffcd00AA
    rifa: int = 0x6666ffAA
    white: int = 0xFFFFFFFF
    mask: int = 0x22222200
    textdraw: int = 0xFFFF00AA
    sms: int = 0xEDFF21FF
    bronze_vip: int = 0x2596BEAA
    silver_vip: int = 0x808080AA
    gold_vip: int = 0xFFD700AA
    game_text_groove: str = "~g~"
    game_text_ballas: str = "~p~"
    game_text_vagos: str = "~h~~h~"
    game_text_rifa: str = "~b~~h~"
    game_text_aztecas: str = "~b~~h~~h~"
    game_text_time_date: str = "~y~"
    game_text_time_time: str = "~g~~h~"
    grove_hex: str = "008000"
    ballas_hex: str = "8B00FF"
    vagos_hex: str = "FFA500"
    aztecas_hex: str = "00bfff"
    rifa_hex: str = "1560BD"
    white_hex: str = "FFFFFF"
    error_hex: str = "ff6347"
    cmd_hex: str = "FFCD00"
    vip_hex: str = "EDFF21"
    dialog_hex: str = "A9C4E4"
    green_hex: str = "008000"
    bronze_hex: int = "2596BE"
    silver_hex: int = "808080"
    gold_hex: int = "FFD700"


@dataclass
class ZoneNames:
    names = (
        "Bayside Marina",
        "Bayside",
        "Battery Point",
        "Paradiso",
        "Santa Flora",
        "Palisades",
        "City Hall",
        "Ocean Flats",
        "Foster Valley",
        "Hashbury",
        "Juniper Hollow",
        "Esplanade North",
        "Financial",
        "Calton Heights",
        "Downtown",
        "Juniper Hill",
        "Chinatown",
        "Kings",
        "Garcia",
        "Doherty",
        "Easter Bay Airport",
        "Easter Basin",
        "Esplanade East",
        "Angel Pine",
        "Shady Cabin",
        "Back o Beyond",
        "Leafy Hollow",
        "Flint Range",
        "Fallen Tree",
        "The Farm",
        "El Quebrados",
        "Aldea Malvada",
        "The Sherman Dam",
        "Las Barrancas",
        "Fort Carson",
        "Hunter Quarry",
        "Octane Springs",
        "Green Palms",
        "Regular Tom",
        "Las Brujas",
        "Verdant Meadows",
        "Las Payasadas",
        "Arco del Oeste",
        "Hankypanky Point",
        "Palomino Creek",
        "North Rock",
        "Montgomery",
        "Hampton Barns",
        "Fern Ridge",
        "Dillimore",
        "Hilltop Farm",
        "Blueberry",
        "The Panopticon",
        "Frederick Bridge",
        "The Mako Span",
        "Blueberry Acres",
        "Martin Bridge",
        "Fallow Bridge",
        "Shady Creeks",
        "Queens",
        "Gant Bridge",
        "Easter Bay Chemicals",
        "Los Santos International",
        "Verdant Bluffs",
        "El Corona",
        "Willowfield",
        "Ocean Docks",
        "Marina",
        "Verona Beach",
        "Conference Center",
        "Commerce",
        "Pershing Square",
        "Little Mexico",
        "Idlewood",
        "Glen Park",
        "Jefferson",
        "Las Colinas",
        "Ganton",
        "East Beach",
        "East Los Santos",
        "Los Flores",
        "Downtown Los Santos",
        "Mulholland Intersection",
        "Mulholland",
        "Market",
        "Vinewood",
        "Temple",
        "Santa Maria Beach",
        "Rodeo",
        "Richman",
        "The Strip",
        "The Four Dragons Casino",
        "The Pink Swan",
        "The High Roller",
        "Pirates in Mens Pants",
        "The Visage",
        "Julius Thruway South",
        "Julius Thruway West",
        "Rockshore East",
        "Come-A-Lot",
        "The Camels Toe",
        "Royal Casino",
        "Caligulas Palace",
        "Pilgrim",
        "Starfish Casino",
        "The Emerald Isle",
        "Old Venturas Strip",
        "K.A.C.C. Military Fuels",
        "Creek",
        "Sobell Rail Yards",
        "Linden Station",
        "Julius Thruway East",
        "Linden Side",
        "Julius Thruway North",
        "Harry Gold Parkway",
        "Redsands East",
        "Redsands West",
        "Las Venturas Airport",
        "LVA Freight Depot",
        "Blackfield Intersection",
        "Greenglass College",
        "Blackfield",
        "Roca Escalante",
        "Last Dime Motel",
        "Rockshore West",
        "Randolph Industrial Estate",
        "Blackfield Chapel",
        "Pilson Intersection",
        "Whitewood Estates",
        "Prickle Pine",
        "Spinybed",
        "San Andreas Sound",
        "Fishers Lagoon",
        "Garver Bridge",
        "Kincaid Bridge",
        "Los Santos Inlet",
        "Sherman Reservoir",
        "Flint Water",
        "Easter Tunnel",
        "Bayside Tunnel",
        "The Big Ear",
        "Lil Probe Inn",
        "Valle Ocultado",
        "Unity Station",
        "Market Station",
        "Cranberry Station",
        "Yellow Bell Station",
        "San Fierro Bay",
        "El Castillo del Diablo",
        "Restricted Area",
        "Montgomery Intersection",
        "Robada Intersection",
        "Flint Intersection",
        "Avispa Country Club",
        "Missionary Hill",
        "Mount Chiliad",
        "Yellow Bell Golf Course",
        "Beacon Hill",
        "Playa del Seville",
        "The Clowns Pocket",
        "Los Santos",
        "Las Venturas",
        "Bone County",
        "Tierra Robada",
        "San Fierro",
        "Red County",
        "Flint County",
        "Whetstone")


@dataclass
class MonthsConverter:
    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }


@dataclass
class ServerWorldIDs:
    default_world: int = 0
    gangwar_world: int = 1
    gangwar_world_interior: int = 2
    deathmatch_world: int = 3
    deathmatch_world_interior: int = 4
    freeroam_world: int = 5
    freeroam_world_interior = 6
    freeroam_class_selector: int = 10 + randint(1, 999)


@dataclass
class WeatherIDs:
    weather_i: int = 0
    weather = (
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22
    )


@dataclass
class VIPData:
    names = {
        0: "BRONZE",
        1: "SILVER",
        2: "GOLD"
    }

    colors = {
        0: Colors.bronze_hex,
        1: Colors.silver_hex,
        2: Colors.gold_hex
    }


@dataclass
class FreeroamSkins:
    skins = (
        1,
        2,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        68,
        69,
        70,
        71,
        72,
        73,
        75,
        76,
        78,
        79,
        80,
        81,
        82,
        83,
        84,
        85,
        87,
        88,
        89,
        91,
        92,
        93,
        95,
        96,
        97,
        98,
        99,
        269,
        270,
        271,
        272)


@dataclass
class RandomSpawns:
    spawns = [
        [1751.1097,-2106.4529,13.5469,183.1979], # El-Corona - Outside random house
    ]


def convert_seconds(seconds: int):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds

def get_center(min_x: float, max_x: float, min_y: float, max_y: float) -> tuple[float, float]:
    x = (min_x + max_x) / 2.0
    y = (min_y + max_y) / 2.0
    return x, y

def encode():
   return samp.config(encoding="cp1251")
