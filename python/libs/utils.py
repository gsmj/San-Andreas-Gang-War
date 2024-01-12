from dataclasses import dataclass
import samp # type: ignore

@dataclass
class ServerInfo:
    name: str = "San Andreas Gang War | 1 | Reborn"
    name_timer = [
        "San Andreas Gang War | 1 | Reborn",
        "San Andreas Gang War | 1 | Reborn | Client: 0.3.7 / 0.3DL",
        "SAGW | 1 | Reborn | Grand Opening!",
        "SAGW | 1 | Reborn | Gangs, Drift and more!",
    ]
    name_short: str = "SAGW"
    gamemode: str = "DM/TDM/GW/TURFS/Drift/Freeroam"
    language: str = "Russian"
    map: str = "San Andreas"


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
    game_text_groove: str = "~g~"
    game_text_ballas: str = "~p~"
    game_text_vagos: str = "~h~~h~"
    game_text_rifa: str = "~b~~h~"
    game_text_aztecas: str = "~b~~h~~h~"
    game_text_time_date: str = "~y~"
    game_text_time_time: str = "~g~~h~"


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


def convert_seconds(seconds: int):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds


def encode():
    return samp.config(encoding="cp1251")
