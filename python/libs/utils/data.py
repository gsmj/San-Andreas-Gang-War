from dataclasses import dataclass
from random import randint
import matplotlib
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
    gamemode: str = "GW/Freeroam"
    language: str = "Russian"
    map: str = "San Andreas"
    CAPTURE_LIMIT: int = 2
    current_time = None
    time = None
    change_name_and_adverb: int = 7200
    send_math: int = 1800


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
    admin_pm: int = 0xFBC3B1AA
    admin: int = 0xC0392BAA
    jail: int = 0xC0C0C0AA
    dark_green: int = 0x34C924AA
    ad: int = 0xF44336AA
    deathmatch: int = 0x434B4DAA
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
    red_hex: str = "ff6347"
    # cmd_hex: str = "FFCD00"
    cmd_hex: str = "D53032"
    vip_hex: str = "EDFF21"
    dialog_hex: str = "A9C4E4"
    green_hex: str = "008000"
    bronze_hex: str = "cd7f32"
    silver_hex: str = "808080"
    gold_hex: str = "FFD700"
    admin_hex: str = "8B0000"
    admin_pm_hex: str = "FBCEB1"
    link_hex: str = "2986cc"
    dark_green_hex: str = "34C924"
    ad_hex = "F44336"
    clist_hex = {
        0: "F0F8FF",
        1: "FAEBD7",
        2: "00FFFF",
        3: "7FFFD4",
        4: "F0FFFF",
        5: "F5F5DC",
        6: "FFE4C4",
        7: "000000",
        8: "FFEBCD",
        9: "0000FF",
        10: "8A2BE2",
        11: "A52A2A",
        12: "DEB887",
        13: "5F9EA0",
        14: "7FFF00",
        15: "D2691E",
        16: "FF7F50",
        17: "6495ED",
        18: "FFF8DC",
        19: "DC143C",
        20: "00FFFF",
        21: "00008B",
        22: "008B8B",
        23: "B8860B",
        24: "A9A9A9",
        25: "006400",
        26: "A9A9A9",
        27: "BDB76B",
        28: "8B008B",
        29: "556B2F",
        30: "FF8C00",
        31: "9932CC",
        32: "8B0000",
        33: "E9967A",
        34: "8FBC8F",
        35: "483D8B",
        36: "2F4F4F",
        37: "2F4F4F",
        38: "00CED1",
        39: "9400D3",
        40: "FF1493",
        41: "00BFFF",
        42: "696969",
        43: "696969",
        44: "1E90FF",
        45: "B22222",
        46: "FFFAF0",
        47: "228B22",
        48: "FF00FF",
        49: "DCDCDC",
        50: "F8F8FF",
        51: "FFD700",
        52: "DAA520",
        53: "808080",
        54: "008000",
        55: "ADFF2F",
        56: "808080",
        57: "F0FFF0",
        58: "FF69B4",
        59: "CD5C5C",
        60: "4B0082",
        61: "FFFFF0",
        62: "F0E68C",
        63: "E6E6FA",
        64: "FFF0F5",
        65: "7CFC00",
        66: "FFFACD",
        67: "ADD8E6",
        68: "F08080",
        69: "E0FFFF",
        70: "FAFAD2",
        71: "D3D3D3",
        72: "90EE90",
        73: "D3D3D3",
        74: "FFB6C1",
        75: "FFA07A",
        76: "20B2AA",
        77: "87CEFA",
        78: "778899",
        79: "778899",
        80: "B0C4DE",
        81: "FFFFE0",
        82: "00FF00",
        83: "32CD32",
        84: "FAF0E6",
        85: "FF00FF",
        86: "800000",
        87: "66CDAA",
        88: "0000CD",
        89: "BA55D3",
        90: "9370DB",
        91: "3CB371",
        92: "7B68EE",
        93: "00FA9A",
        94: "48D1CC",
        95: "C71585",
        96: "191970",
        97: "F5FFFA",
        98: "FFE4E1",
        99: "FFE4B5",
        100: "FFDEAD",
        101: "000080",
        102: "FDF5E6",
        103: "808000",
        104: "6B8E23",
        105: "FFA500",
        106: "FF4500",
        107: "DA70D6",
        108: "EEE8AA",
        109: "98FB98",
        110: "AFEEEE",
        111: "DB7093",
        112: "FFEFD5",
        113: "FFDAB9",
        114: "CD853F",
        115: "FFC0CB",
        116: "DDA0DD",
        117: "B0E0E6",
        118: "800080",
        119: "663399",
        120: "FF0000",
        121: "BC8F8F",
        122: "4169E1",
        123: "8B4513",
        124: "FA8072",
        125: "F4A460",
        126: "2E8B57",
        127: "FFF5EE",
        128: "A0522D",
        129: "C0C0C0",
        130: "87CEEB",
        131: "6A5ACD",
        132: "708090",
        133: "708090",
        134: "FFFAFA",
        135: "00FF7F",
        136: "4682B4",
        137: "D2B48C",
        138: "008080",
        139: "D8BFD8",
        140: "FF6347",
        141: "40E0D0",
        142: "EE82EE",
        143: "F5DEB3",
        144: "FFFFFF",
        145: "F5F5F5",
        146: "FFFF00",
        147: "9ACD32"
    }
    clist_rgba = {
        0: 0xF0F8FFAA,
        1: 0xFAEBD7AA,
        2: 0x00FFFFAA,
        3: 0x7FFFD4AA,
        4: 0xF0FFFFAA,
        5: 0xF5F5DCAA,
        6: 0xFFE4C4AA,
        7: 0x000000AA,
        8: 0xFFEBCDAA,
        9: 0x0000FFAA,
        10: 0x8A2BE2AA,
        11: 0xA52A2AAA,
        12: 0xDEB887AA,
        13: 0x5F9EA0AA,
        14: 0x7FFF00AA,
        15: 0xD2691EAA,
        16: 0xFF7F50AA,
        17: 0x6495EDAA,
        18: 0xFFF8DCAA,
        19: 0xDC143CAA,
        20: 0x00FFFFAA,
        21: 0x00008BAA,
        22: 0x008B8BAA,
        23: 0xB8860BAA,
        24: 0xA9A9A9AA,
        25: 0x006400AA,
        26: 0xA9A9A9AA,
        27: 0xBDB76BAA,
        28: 0x8B008BAA,
        29: 0x556B2FAA,
        30: 0xFF8C00AA,
        31: 0x9932CCAA,
        32: 0x8B0000AA,
        33: 0xE9967AAA,
        34: 0x8FBC8FAA,
        35: 0x483D8BAA,
        36: 0x2F4F4FAA,
        37: 0x2F4F4FAA,
        38: 0x00CED1AA,
        39: 0x9400D3AA,
        40: 0xFF1493AA,
        41: 0x00BFFFAA,
        42: 0x696969AA,
        43: 0x696969AA,
        44: 0x1E90FFAA,
        45: 0xB22222AA,
        46: 0xFFFAF0AA,
        47: 0x228B22AA,
        48: 0xFF00FFAA,
        49: 0xDCDCDCAA,
        50: 0xF8F8FFAA,
        51: 0xFFD700AA,
        52: 0xDAA520AA,
        53: 0x808080AA,
        54: 0x008000AA,
        55: 0xADFF2FAA,
        56: 0x808080AA,
        57: 0xF0FFF0AA,
        58: 0xFF69B4AA,
        59: 0xCD5C5CAA,
        60: 0x4B0082AA,
        61: 0xFFFFF0AA,
        62: 0xF0E68CAA,
        63: 0xE6E6FAAA,
        64: 0xFFF0F5AA,
        65: 0x7CFC00AA,
        66: 0xFFFACDAA,
        67: 0xADD8E6AA,
        68: 0xF08080AA,
        69: 0xE0FFFFAA,
        70: 0xFAFAD2AA,
        71: 0xD3D3D3AA,
        72: 0x90EE90AA,
        73: 0xD3D3D3AA,
        74: 0xFFB6C1AA,
        75: 0xFFA07AAA,
        76: 0x20B2AAAA,
        77: 0x87CEFAAA,
        78: 0x778899AA,
        79: 0x778899AA,
        80: 0xB0C4DEAA,
        81: 0xFFFFE0AA,
        82: 0x00FF00AA,
        83: 0x32CD32AA,
        84: 0xFAF0E6AA,
        85: 0xFF00FFAA,
        86: 0x800000AA,
        87: 0x66CDAAAA,
        88: 0x0000CDAA,
        89: 0xBA55D3AA,
        90: 0x9370DBAA,
        91: 0x3CB371AA,
        92: 0x7B68EEAA,
        93: 0x00FA9AAA,
        94: 0x48D1CCAA,
        95: 0xC71585AA,
        96: 0x191970AA,
        97: 0xF5FFFAAA,
        98: 0xFFE4E1AA,
        99: 0xFFE4B5AA,
        100: 0xFFDEADAA,
        101: 0x000080AA,
        102: 0xFDF5E6AA,
        103: 0x808000AA,
        104: 0x6B8E23AA,
        105: 0xFFA500AA,
        106: 0xFF4500AA,
        107: 0xDA70D6AA,
        108: 0xEEE8AAAA,
        109: 0x98FB98AA,
        110: 0xAFEEEEAA,
        111: 0xDB7093AA,
        112: 0xFFEFD5AA,
        113: 0xFFDAB9AA,
        114: 0xCD853FAA,
        115: 0xFFC0CBAA,
        116: 0xDDA0DDAA,
        117: 0xB0E0E6AA,
        118: 0x800080AA,
        119: 0x663399AA,
        120: 0xFF0000AA,
        121: 0xBC8F8FAA,
        122: 0x4169E1AA,
        123: 0x8B4513AA,
        124: 0xFA8072AA,
        125: 0xF4A460AA,
        126: 0x2E8B57AA,
        127: 0xFFF5EEAA,
        128: 0xA0522DAA,
        129: 0xC0C0C0AA,
        130: 0x87CEEBAA,
        131: 0x6A5ACDAA,
        132: 0x708090AA,
        133: 0x708090AA,
        134: 0xFFFAFAAA,
        135: 0x00FF7FAA,
        136: 0x4682B4AA,
        137: 0xD2B48CAA,
        138: 0x008080AA,
        139: 0xD8BFD8AA,
        140: 0xFF6347AA,
        141: 0x40E0D0AA,
        142: 0xEE82EEAA,
        143: 0xF5DEB3AA,
        144: 0xFFFFFFAA,
        145: 0xF5F5F5AA,
        146: 0xFFFF00AA,
        147: 0x9ACD32AA,
    }

@dataclass
class RainbowColors:
    colors = {
        0: 0xe8141AA,
        1: 0xffa500AA,
        2: 0xfaeb36AA,
        3: 0x79c314AA,
        4: 0x487de7AA,
        5: 0x4b369dAA,
        6: 0x70369dAA
    }


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
class NoEngineVehicleIDs:
    ids = (1, 2)


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


@dataclass(frozen=True)
class ServerMode:
    default_world: int = 0
    gangwar_world: int = 1
    freeroam_world: int = 3
    deathmatch_world_oc_deagle: int = 4
    deathmatch_world_old_country: int = 5
    deathmatch_world_farm: int = 6
    deathmatch_world_abandoned_country: int = 7
    deathmatch_world_kass: int = 8
    deathmatch_worlds = (
        deathmatch_world_oc_deagle,
        deathmatch_world_old_country,
        deathmatch_world_farm,
        deathmatch_world_abandoned_country,
        deathmatch_world_kass
    )


    jail_world: int = 100


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
    skins = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311)


@dataclass
class FreeroamTeleports:
    """
    Key: name
    Value: pos (x, y, z, rot)
    """
    teleports = {
        "Groove Street": (2494.5181, -1666.6481, 13.3438, 90.0000),
        "Airport LS": (1817.4248, -2422.3840, 13.5547, 180.0000),
        "Drift parking": (1639.6705, -1100.6979, 23.9063, 0.0000),
        "Vinewood": (1241.3738, -743.3031, 95.2668, 20.0000),
        "Casino Four Dragons": (2026.8141, 1008.0557, 10.8203, 270.0000),
        "Airport LV": (1318.9250, 1256.5140, 10.8203, 0.0000),
        "Big Ear": (-331.1712,  1524.3041, 75.3570, 265.0000),
        "Zone 69": (213.8135, 1866.4119, 13.1406, 0.0000),
        "Paleto-Bay": (-2227.4087, 2326.8154, 7.5469, 90.0000),
        "San-Fierro": (-1980.1105, 883.3474, 45.2031, 270.0000),
        "Airport SF": (-1256.3604, 36.3511, 14.1405, 135.0000),
        "Angel Pine": (-2197.0686, -2260.1377, 30.6551, 145.0000),
        "Los Santos": (1128.6122, -1425.6549, 15.7969, 360.0000),
        "Las Venturas": (2025.8014, 1343.0096, 10.8203, 270.0000),
        "Santa Maria Beach": (341.2572, -1799.4027, 4.7396, 360.0000),
        "Verdant Meadows": (418.0660,2502.5620,16.4844, 90.0000)
    }


@dataclass(frozen=True)
class RandomSpawns:
    spawns = [
        [1751.1097,-2106.4529,13.5469,183.1979], # El-Corona - Outside random house
        [2652.6418,-1989.9175,13.9988,182.7107], # Random house in willowfield - near playa de seville and stadium
        [2489.5225,-1957.9258,13.5881,2.3440], # Hotel in willowfield - near cluckin bell
        [2689.5203,-1695.9354,10.0517,39.5312], # Outside stadium - lots of cars
        [2770.5393,-1628.3069,12.1775,4.9637], # South in east beach - north of stadium - carparks nearby
        [2807.9282,-1176.8883,25.3805,173.6018], # North in east beach - near apartments
        [2552.5417,-958.0850,82.6345,280.2542], # Random house north of Las Colinas
        [2232.1309,-1159.5679,25.8906,103.2939], # Jefferson motel
        [2388.1003,-1279.8933,25.1291,94.3321], # House south of pig pen
        [2481.1885,-1536.7186,24.1467,273.4944], # East LS - near clucking bell and car wash
        [2495.0720,-1687.5278,13.5150,359.6696], # Outside CJ's house - lots of cars nearby
        [2306.8252,-1675.4340,13.9221,2.6271], # House in ganton - lots of cars nearby
        [2191.8403,-1455.8251,25.5391,267.9925], # House in south jefferson - lots of cars nearby
        [1830.1359,-1092.1849,23.8656,94.0113], # Mulholland intersection carpark
        [2015.3630,-1717.2535,13.5547,93.3655], # Idlewood house
        [1654.7091,-1656.8516,22.5156,177.9729], # Right next to PD
        [1219.0851,-1812.8058,16.5938,190.0045], # Conference Center
        [1508.6849,-1059.0846,25.0625,1.8058], # Across the street of BANK - lots of cars in intersection carpark
        [1421.0819,-885.3383,50.6531,3.6516], # Outside house in viod
        [1133.8237,-1272.1558,13.5469,192.4113], # Near hospital
        [1235.2196,-1608.6111,13.5469,181.2655], # Backalley west of mainstreet
        [590.4648,-1252.2269,18.2116,25.0473], # Outside "BAnk of San Andreas"
        [842.5260,-1007.7679,28.4185,213.9953], # North of Graveyard
        [911.9332,-1232.6490,16.9766,5.2999], # LS Film Studio
        [477.6021,-1496.6207,20.4345,266.9252], # Rodeo Place
        [255.4621,-1366.3256,53.1094,312.0852], # Outside propery in richman
        [281.5446,-1261.4562,73.9319,305.0017], # Another richman property
        [790.1918,-839.8533,60.6328,191.9514], # Mulholland house
        [1299.1859,-801.4249,84.1406,269.5274], # Maddoggs
        [1240.3170,-2036.6886,59.9575,276.4659], # Verdant Bluffs
        [2215.5181,-2627.8174,13.5469,273.7786], # Ocean docks 1
        [2509.4346,-2637.6543,13.6453,358.3565], # Ocean Docks spawn 2
        [1435.8024,2662.3647,11.3926,1.1650], #  Northern train station
        [1457.4762,2773.4868,10.8203,272.2754], #  Northern golf club
        [1739.6390,2803.0569,14.2735,285.3929], #  Northern housing estate 1
        [1870.3096,2785.2471,14.2734,42.3102], #  Northern housing estate 2
        [1959.7142,2754.6863,10.8203,181.4731], #  Northern house 1
        [2314.2556,2759.4504,10.8203,93.2711], #  Northern industrial estate 1
        [2216.5674,2715.0334,10.8130,267.6540], #  Northern industrial estate 2
        [2101.4192,2678.7874,10.8130,92.0607], #  Northern near railway line
        [1951.1090,2660.3877,10.8203,180.8461], #  Northern house 2
        [1666.6949,2604.9861,10.8203,179.8495], #  Northern house 3
        [2808.3367,2421.5107,11.0625,136.2060], #  Northern shopping centre
        [2633.3203,2349.7061,10.6719,178.7175], #  V-Rock
        [2606.6348,2161.7490,10.8203,88.7508], #  South V-Rock
        [2616.5286,2100.6226,10.8158,177.7834], #  North Ammunation 1
        [2491.8816,2397.9370,10.8203,266.6003], #  North carpark 1
        [2531.7891,2530.3223,21.8750,91.6686], #  North carpark 2
        [2340.6677,2530.4324,10.8203,177.8630], #  North Pizza Stack
        [2097.6855,2491.3313,14.8390,181.8117], #  Emerald Isle
        [1893.1000,2423.2412,11.1782,269.4385], #  Souvenir shop
        [1698.9330,2241.8320,10.8203,357.8584], #  Northern casino
        [1479.4559,2249.0769,11.0234,306.3790], #  Baseball stadium 1
        [1298.1548,2083.4016,10.8127,256.7034], #  Baseball stadium 2
        [1117.8785,2304.1514,10.8203,81.5490], #  North carparks
        [1108.9878,1705.8639,10.8203,0.6785], #  Dirtring racing 1
        [1423.9780,1034.4188,10.8203,90.9590], #  Sumo
        [1537.4377,752.0641,11.0234,271.6893], #  Church
        [1917.9590,702.6984,11.1328,359.2682], #  Southern housing estate
        [2089.4785,658.0414,11.2707,357.3572], #  Southern house 1
        [2489.8286,928.3251,10.8280,67.2245], #  Wedding chapel
        [2697.4717,856.4916,9.8360,267.0983], #  Southern construction site
        [2845.6104,1288.1444,11.3906,3.6506], #  Southern train station
        [2437.9370,1293.1442,10.8203,86.3830], #  Wedding chapel (near Pyramid)
        [2299.5430,1451.4177,10.8203,269.1287], #  Carpark (near Pyramid)
        [2214.3008,2041.9165,10.8203,268.7626], #  Central parking lot
        [2005.9174,2152.0835,10.8203,270.1372], #  Central motel
        [2222.1042,1837.4220,10.8203,88.6461], #  Clowns Pocket
        [2025.6753,1916.4363,12.3382,272.5852], #  The Visage
        [2087.9902,1516.5336,10.8203,48.9300], #  Royal Casino
        [2172.1624,1398.7496,11.0625,91.3783], #  Auto Bahn
        [2139.1841,987.7975,10.8203,0.2315], #  Come-a-lot
        [1860.9672,1030.2910,10.8203,271.6988], #  Behind 4 Dragons
        [1673.2345,1316.1067,10.8203,177.7294], #  Airport carpark
        [1412.6187,2000.0596,14.7396,271.3568], #  South baseball stadium houses
        [-2723.4639,-314.8138,7.1839,43.5562],  # golf course spawn
        [-2694.5344,64.5550,4.3359,95.0190],  # in front of a house
        [-2458.2000,134.5419,35.1719,303.9446],  # hotel
        [-2796.6589,219.5733,7.1875,88.8288],  # house
        [-2706.5261,397.7129,4.3672,179.8611],  # park
        [-2866.7683,691.9363,23.4989,286.3060],  # house
        [-2764.9543,785.6434,52.7813,357.6817],  # donut shop
        [-2660.9402,883.2115,79.7738,357.4440],  # house
        [-2861.0796,1047.7109,33.6068,188.2750], #  parking lot
        [-2629.2009,1383.1367,7.1833,179.7006],  # parking lot at the bridge
        [-2079.6802,1430.0189,7.1016,177.6486],  # pier
        [-1660.2294,1382.6698,9.8047,136.2952], #  pier 69
        [-1674.1964,430.3246,7.1797,226.1357],  # gas station]
        [-1954.9982,141.8080,27.1747,277.7342],  # train station
        [-1956.1447,287.1091,35.4688,90.4465],  # car shop
        [-1888.1117,615.7245,35.1719,128.4498],  # random
        [-1922.5566,886.8939,35.3359,272.1293],  # random
        [-1983.3458,1117.0645,53.1243,271.2390],  # church
        [-2417.6458,970.1491,45.2969,269.3676],  # gas station
        [-2108.0171,902.8030,76.5792,5.7139],  # house
        [-2097.5664,658.0771,52.3672,270.4487],  # random
        [-2263.6650,393.7423,34.7708,136.4152],  # random
        [-2287.5027,149.1875,35.3125,266.3989],  # baseball parking lot
        [-2039.3571,-97.7205,35.1641,7.4744],  # driving school
        [-1867.5022,-141.9203,11.8984,22.4499],  # factory
        [-1537.8992,116.0441,17.3226,120.8537],  # docks ship
        [-1708.4763,7.0187,3.5489,319.3260],  # docks hangar
        [-1427.0858,-288.9430,14.1484,137.0812],  # airport
        [-2173.0654,-392.7444,35.3359,237.0159],  # stadium
        [-2320.5286,-180.3870,35.3135,179.6980],  # burger shot
        [-2930.0049,487.2518,4.9141,3.8258]  # harbor
    ]

@dataclass(frozen=True)
class DeathMatchSpawns:
    spawns = {
        ServerMode.deathmatch_world_oc_deagle: (
            (-397.1293, 2250.9568, 42.4297, 290.0000),
            (-367.7202, 2255.0208, 42.4844, 195.0000) ,
            (-347.1474, 2230.7024, 42.4885, 100.0000),
            (-360.3025, 2201.7686, 42.4844, 15.0000),
            (-391.4041, 2195.4341, 42.4163, 5.0000),
            (-428.4577, 2204.6074, 42.4297, 280.0000),
            (-417.8091, 2236.6167, 42.4297, 280.0000),
        ),

        ServerMode.deathmatch_world_old_country: (
            (-397.1293, 2250.9568, 42.4297, 290.0000),
            (-367.7202, 2255.0208, 42.4844, 195.0000) ,
            (-347.1474, 2230.7024, 42.4885, 100.0000),
            (-360.3025, 2201.7686, 42.4844, 15.0000),
            (-391.4041, 2195.4341, 42.4163, 5.0000),
            (-428.4577, 2204.6074, 42.4297, 280.0000),
            (-417.8091, 2236.6167, 42.4297, 280.0000),
        ),
        ServerMode.deathmatch_world_farm: (
            (1055.6105, -366.2527, 73.9922,  90.0000),
            (1019.3500, -302.0771, 73.9931, 180.0000),
            (1045.9434, -296.9352, 73.9931, 180.0000),
            (1113.2708, -319.7141, 73.9922, 90.0000),
        ),
        ServerMode.deathmatch_world_abandoned_country: (
            (-1309.9337, 2487.3464, 87.1753, 360.0000),
            (-1283.0154, 2515.2380, 87.1064, 85.0000),
            (-1304.1638, 2557.9167, 86.8784, 85.0000),
        ),
        ServerMode.deathmatch_world_kass: (
            (2546.1135, 2837.3240, 10.8203, 0.0000),
            (2543.4514, 2810.3254, 10.8203, 270.0000),
            (2592.6772, 2847.3723, 10.8203, 185.0000),
            (2606.2842, 2807.8652, 10.8203, 0.0000),
        ),
    }




@dataclass
class GunData:
    """
    Key: name
    Value: (id, slot, price)
    """
    guns = {
        # "Brass Knuckles": (1, 1, 500),
        "Golf Club": (2, 1, 500),
        "Nite Stick": (3, 1, 500),
        "Baseball Bat": (5, 1, 500),
        "Shovel": (6, 1, 500),
        "Pool Cue": (7, 1, 500),
        "Katana": (8, 1, 500),
        "Chainsaw": (9, 1, 500),
        "Cane": (15, 1, 500),
        # 16: "Grenade",
        # 18: "Molotov Cocktail",
        "Colt 45": (22, 2, 1000),
        "Silenced Pistol": (23, 2, 1000),
        "Desert Eagle": (24, 2, 5000),
        "Shotgun": (25, 3, 10000),
        "Sawn-off Shotgun": (26, 3, 10000),
        "Combat Shotgun": (27, 3, 10000),
        "TEC9": (32, 4, 20000),
        "UZI": (28, 4, 20000),
        "MP5": (29, 4, 20000),
        "AK-47": (30, 5, 30000),
        "M4": (31, 5, 30000),
        "Rifle": (33, 6, 50000),
        "Sniper Rifle": (34, 6, 50000)
    }


@dataclass(frozen=True)
class DMRatingColors:
    colors = {
        0: Colors.white_hex,
        1000: "808080",
        2000: "00ffff",
        5000: "0047AB",
        10000: "800080",
        20000: "FFC0CB",
        30000: "FF0000",
        50000: "ffff00"
    }


@dataclass
class AdminData:
    """
    Key: level
    Value: (name)
    """
    data = {
        1: "Администратор 1 Уровня",
        2: "Администратор 2 Уровня",
        3: "Администратор 3 Уровня",
        4: "Администратор 4 Уровня",
        5: "Заместитель Главного Администратора",
        6: "Главный Администратор",
        7: "Разработчик"
    }


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