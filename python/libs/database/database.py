from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Column,
    DateTime,
    Boolean,
    select,
    Identity,
    Float,
    and_,
    delete,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)
from dataclasses import dataclass
from pysamp.gangzone import Gangzone
from datetime import datetime
from zoneinfo import ZoneInfo
import platform


default_gang_zones = [
    (1642.710571,-2174.567871,1770.710571,-2073.567871),
    (1770.710571,-2174.567871,1898.710571,-2073.567871),
    (1898.710571,-2174.567871,2026.710571,-2073.567871),
    (2026.710571,-2174.567871,2154.710449,-2073.567871),
    (2154.710449,-2174.567871,2282.710449,-2073.567871),
    (2282.710449,-2174.567871,2410.710449,-2073.567871),
    (2410.710449,-2174.567871,2538.710449,-2073.567871),
    (2538.710449,-2174.567871,2666.710449,-2073.567871),
    (2666.710449,-2174.567871,2794.710449,-2073.567871),
    (2794.710449,-2174.567871,2922.710449,-2073.567871),
    (1642.710571,-2073.567871,1770.710571,-1972.567871),
    (1770.710571,-2073.567871,1898.710571,-1972.567871),
    (1898.710571,-2073.567871,2026.710571,-1972.567871),
    (2026.710571,-2073.567871,2154.710449,-1972.567871),
    (2154.710449,-2073.567871,2282.710449,-1972.567871),
    (2282.710449,-2073.567871,2410.710449,-1972.567871),
    (2410.710449,-2073.567871,2538.710449,-1972.567871),
    (2538.710449,-2073.567871,2666.710449,-1972.567871),
    (2666.710449,-2073.567871,2794.710449,-1972.567871),
    (2794.710449,-2073.567871,2922.710449,-1972.567871),
    (1642.710571,-1972.567871,1770.710571,-1871.567871),
    (1770.710571,-1972.567871,1898.710571,-1871.567871),
    (1898.710571,-1972.567871,2026.710571,-1871.567871),
    (2026.710571,-1972.567871,2154.710449,-1871.567871),
    (2154.710449,-1972.567871,2282.710449,-1871.567871),
    (2282.710449,-1972.567871,2410.710449,-1871.567871),
    (2410.710449,-1972.567871,2538.710449,-1871.567871),
    (2538.710449,-1972.567871,2666.710449,-1871.567871),
    (2666.710449,-1972.567871,2794.710449,-1871.567871),
    (2794.710449,-1972.567871,2922.710449,-1871.567871),
    (1642.710571,-1871.567871,1770.710571,-1770.567871),
    (1770.710571,-1871.567871,1898.710571,-1770.567871),
    (1898.710571,-1871.567871,2026.710571,-1770.567871),
    (2026.710571,-1871.567871,2154.710449,-1770.567871),
    (2154.710449,-1871.567871,2282.710449,-1770.567871),
    (2282.710449,-1871.567871,2410.710449,-1770.567871),
    (2410.710449,-1871.567871,2538.710449,-1770.567871),
    (2538.710449,-1871.567871,2666.710449,-1770.567871),
    (2666.710449,-1871.567871,2794.710449,-1770.567871),
    (2794.710449,-1871.567871,2922.710449,-1770.567871),
    (1642.710571,-1770.567871,1770.710571,-1669.567871),
    (1770.710571,-1770.567871,1898.710571,-1669.567871),
    (1898.710571,-1770.567871,2026.710571,-1669.567871),
    (2026.710571,-1770.567871,2154.710449,-1669.567871),
    (2154.710449,-1770.567871,2282.710449,-1669.567871),
    (2282.710449,-1770.567871,2410.710449,-1669.567871),
    (2410.710449,-1770.567871,2538.710449,-1669.567871),
    (2538.710449,-1770.567871,2666.710449,-1669.567871),
    (2666.710449,-1770.567871,2794.710449,-1669.567871),
    (2794.710449,-1770.567871,2922.710449,-1669.567871),
    (1642.710571,-1669.567871,1770.710571,-1568.567871),
    (1770.710571,-1669.567871,1898.710571,-1568.567871),
    (1898.710571,-1669.567871,2026.710571,-1568.567871),
    (2026.710571,-1669.567871,2154.710449,-1568.567871),
    (2154.710449,-1669.567871,2282.710449,-1568.567871),
    (2282.710449,-1669.567871,2410.710449,-1568.567871),
    (2410.710449,-1669.567871,2538.710449,-1568.567871),
    (2538.710449,-1669.567871,2666.710449,-1568.567871),
    (2666.710449,-1669.567871,2794.710449,-1568.567871),
    (2794.710449,-1669.567871,2922.710449,-1568.567871),
    (1642.710571,-1568.567871,1770.710571,-1467.567871),
    (1770.710571,-1568.567871,1898.710571,-1467.567871),
    (1898.710571,-1568.567871,2026.710571,-1467.567871),
    (2026.710571,-1568.567871,2154.710449,-1467.567871),
    (2154.710449,-1568.567871,2282.710449,-1467.567871),
    (2282.710449,-1568.567871,2410.710449,-1467.567871),
    (2410.710449,-1568.567871,2538.710449,-1467.567871),
    (2538.710449,-1568.567871,2666.710449,-1467.567871),
    (2666.710449,-1568.567871,2794.710449,-1467.567871),
    (2794.710449,-1568.567871,2922.710449,-1467.567871),
    (1642.710571,-1467.567871,1770.710571,-1366.567871),
    (1770.710571,-1467.567871,1898.710571,-1366.567871),
    (1898.710571,-1467.567871,2026.710571,-1366.567871),
    (2026.710571,-1467.567871,2154.710449,-1366.567871),
    (2154.710449,-1467.567871,2282.710449,-1366.567871),
    (2282.710449,-1467.567871,2410.710449,-1366.567871),
    (2410.710449,-1467.567871,2538.710449,-1366.567871),
    (2538.710449,-1467.567871,2666.710449,-1366.567871),
    (2666.710449,-1467.567871,2794.710449,-1366.567871),
    (2794.710449,-1467.567871,2922.710449,-1366.567871),
    (1642.710571,-1366.567871,1770.710571,-1265.567871),
    (1770.710571,-1366.567871,1898.710571,-1265.567871),
    (1898.710571,-1366.567871,2026.710571,-1265.567871),
    (2026.710571,-1366.567871,2154.710449,-1265.567871),
    (2154.710449,-1366.567871,2282.710449,-1265.567871),
    (2282.710449,-1366.567871,2410.710449,-1265.567871),
    (2410.710449,-1366.567871,2538.710449,-1265.567871),
    (2538.710449,-1366.567871,2666.710449,-1265.567871),
    (2666.710449,-1366.567871,2794.710449,-1265.567871),
    (2794.710449,-1366.567871,2922.710449,-1265.567871),
    (1642.710571,-1265.567871,1770.710571,-1164.567871),
    (1770.710571,-1265.567871,1898.710571,-1164.567871),
    (1898.710571,-1265.567871,2026.710571,-1164.567871),
    (2026.710571,-1265.567871,2154.710449,-1164.567871),
    (2154.710449,-1265.567871,2282.710449,-1164.567871),
    (2282.710449,-1265.567871,2410.710449,-1164.567871),
    (2410.710449,-1265.567871,2538.710449,-1164.567871),
    (2538.710449,-1265.567871,2666.710449,-1164.567871),
    (2666.710449,-1265.567871,2794.710449,-1164.567871),
    (2794.710449,-1265.567871,2922.710449,-1164.567871),
    (1642.710571,-1164.567871,1770.710571,-1063.567871),
    (1770.710571,-1164.567871,1898.710571,-1063.567871),
    (1898.710571,-1164.567871,2026.710571,-1063.567871),
    (2026.710571,-1164.567871,2154.710449,-1063.567871),
    (2154.710449,-1164.567871,2282.710449,-1063.567871),
    (2282.710449,-1164.567871,2410.710449,-1063.567871),
    (2410.710449,-1164.567871,2538.710449,-1063.567871),
    (2538.710449,-1164.567871,2666.710449,-1063.567871),
    (2666.710449,-1164.567871,2794.710449,-1063.567871),
    (2794.710449,-1164.567871,2922.710449,-1063.567871),
    (1642.710571,-1063.567871,1770.710571,-962.567871),
    (1770.710571,-1063.567871,1898.710571,-962.567871),
    (1898.710571,-1063.567871,2026.710571,-962.567871),
    (2026.710571,-1063.567871,2154.710449,-962.567871),
    (2154.710449,-1063.567871,2282.710449,-962.567871),
    (2282.710449,-1063.567871,2410.710449,-962.567871),
    (2410.710449,-1063.567871,2538.710449,-962.567871),
    (2538.710449,-1063.567871,2666.710449,-962.567871),
    (2666.710449,-1063.567871,2794.710449,-962.567871),
    (2794.710449,-1063.567871,2922.710449,-962.567871),
    (1642.710571,-962.567871,1770.710571,-861.567871),
    (1770.710571,-962.567871,1898.710571,-861.567871),
    (1898.710571,-962.567871,2026.710571,-861.567871),
    (2026.710571,-962.567871,2154.710449,-861.567871),
    (2154.710449,-962.567871,2282.710449,-861.567871),
    (2282.710449,-962.567871,2410.710449,-861.567871),
    (2410.710449,-962.567871,2538.710449,-861.567871),
    (2538.710449,-962.567871,2666.710449,-861.567871),
    (2666.710449,-962.567871,2794.710449,-861.567871),
    (2794.710449,-962.567871,2922.710449,-861.567871)
]

default_squad_zones = [
    (79.800048828125, 1303.5, 357.800048828125, 1514.5),
    (-134.199951171875, 1623.7999877929688, 471.800048828125, 2162.7999877929688),
    (-973, 1913.7999877929688, -439, 2165.7999877929688),
    (-1647, 2485.7999992370605, -1356, 2736.7999992370605),
    (-2725, 2184.800003051758, -2166, 2550.800003051758),
    (-103.199951171875, 2380.7999992370605, 486.800048828125, 2664.7999992370605),
    (374.7333984375, 707.7665710449219, 841.7333984375, 1038.7665710449219),
    (-2534.800001144409, 1496.4332580566406, -2289.800001144409, 1596.4332580566406),
    (-1493.333251953125, 1456.4332580566406, -1346.333251953125, 1526.4332580566406),
    (-1137.8665771484375, -774.9001770019531, -961.8665771484375, -576.9001770019531),
    (-636.8665771484375, -583.9001770019531, -456.8665771484375, -451.9001770019531),
    (-1978.5332641601562, -1788.9004211425781, -1685.5332641601562, -1482.9004211425781),
    (-1487.2666625976562, -1622.9004211425781, -1387.2666625976562, -1432.9004211425781),
    (-1153.3999633789062, -1717.9003295898438, -960.3999633789062, -1599.9003295898438),
    (-1250.3999633789062, -1374.2335205078125, -924.3999633789062, -883.2335205078125),
    (-2573.000015258789, -727.2334899902344, -2473.000015258789, -574.2334899902344),
    (-350.8125, -138.59375, 116.1875, 188.40625),
    (680, 213, 839, 395),
    (991, -465, 1159, -264),
    (2213, -2779, 2816, -2291),
    (2816, -2550, 2861, -2311),
    (-1894, 1263, -1738, 1337),
    (117, -1985, 191, -1742),
    (1078, -2083, 1308, -1983),
    (2771, 824, 2901, 1028),
    (2230, 2713, 2476, 2832),
    (-466, 1265, -165, 1654),
    (-464, 2179, -336, 2279),
    (-812, 2393, -763, 2443),
    (-1665, -2799, -1496, -2675),
    (-632, -1545, -532, -1445),
    (-433, -1483, -333, -1383),
    (-409, -1093, -309, -993),
    (-986, -569, -886, -469),
    (-632, -226, -392, -14),
    (-1770.4063720703125, -206.98724365234375, -1458.4063720703125, 244.01275634765625),
    (2399.393310546875, -1006.9872436523438, 2654.393310546875, -906.9872436523438),
    (2310.393310546875, -696.9872436523438, 2410.393310546875, -596.9872436523438),
    (1855.393310546875, 96.01275634765625, 2050.393310546875, 285.01275634765625),
    (-2611.599998474121, -223, -2511.599998474121, -123),
]


Base = declarative_base()
class Player(Base):
    __tablename__ = "Player"
    uid = Column(Integer, Identity(), primary_key=True)
    name = Column(String(32))
    password = Column(String(32))
    email = Column(String(32))
    pin = Column(String(6), default="")
    registration_ip = Column(String(32))
    last_ip = Column(String(32))
    registration_data = Column(DateTime(timezone=ZoneInfo("Europe/Moscow")))
    score = Column(Integer(), default=0)
    money = Column(Integer(), default=0)
    donate = Column(Integer(), default=0)
    dm_rating = Column(Integer(), default=0)
    kills = Column(Integer(), default=0)
    deaths = Column(Integer(), default=0)
    heals = Column(Integer(), default=0)
    masks = Column(Integer(), default=0)
    gang_id = Column(Integer())
    vip_level = Column(Integer(), default=-1)
    admin_level = Column(Integer(), default=0)
    vip_gangwar_template = Column(String(16), default="0, 0, 0")
    is_muted = Column(Boolean(), default=False)
    is_jailed = Column(Boolean(), default=False)
    is_banned = Column(Boolean(), default=False)
    jail_time = Column(Integer, default=0)
    mute_time = Column(Integer, default=0)


class PlayerFreeroamGunSlots(Base):
    __tablename__ = "PlayerFreeroamGunSlots"
    uid = Column(Integer, Identity(), primary_key=True)
    name = Column(String(32))
    slot_melee = Column(Integer(), default=-1)
    slot_pistol = Column(Integer(), default=-1)
    slot_shotgun = Column(Integer(), default=-1)
    slot_machine_gun = Column(Integer(), default=-1)
    slot_assault_rifle = Column(Integer(), default=-1)
    slot_long_rifle = Column(Integer(), default=-1)


class PlayerSettings(Base):
    __tablename__ = "PlayerSettings"
    uid = Column(Integer, Identity(), primary_key=True)
    name = Column(String(32))
    disabled_ping_td = Column(Boolean(), default=False)
    disabled_global_chat_gw = Column(Boolean(), default=False)
    spawn_in_house = Column(Boolean(), default=False)


class GangZone(Base):
    __tablename__ = "GangZone"
    uid = Column(Integer, Identity(), primary_key=True)
    id = Column(Integer())
    gang_id = Column(Integer())
    color = Column(Integer())
    min_x = Column(Float())
    min_y = Column(Float())
    max_x = Column(Float())
    max_y = Column(Float())
    capture_cooldown = Column(Integer(), default=0)


class Vehicle(Base):
    __tablename__ = "Vehicle"
    uid = Column(Integer, Identity(), primary_key=True)
    id = Column(Integer)
    owner = Column(String(32), default="")
    engine = Column(Integer(), default=0)
    lights = Column(Integer(), default=0)
    doors = Column(Integer(), default=0)
    model_id = Column(Integer())
    x = Column(Float())
    y = Column(Float())
    z = Column(Float())
    rotation = Column(Float())
    color1 = Column(Integer())
    color2 = Column(Integer())
    delay = Column(Integer())
    virtual_world = Column(Integer())
    add_siren = Column(Boolean(), default=False)


class AdminLog(Base):
    __tablename__ = "AdminLog"
    uid = Column(Integer, Identity(), primary_key=True)
    admin = Column(String(32))
    action = Column(Integer)
    target = Column(String(32))
    reason = Column(String(252))


class AdminSavedPositions(Base):
    __tablename__ = "AdminSavedPositions"
    uid = Column(Integer, Identity(), primary_key=True)
    admin = Column(String(32))
    name = Column(String(32))
    x = Column(Float())
    y = Column(Float())
    z = Column(Float())
    rotation = Column(Float())


class ServerAnalytics(Base):
    __tablename__ = "ServerAnalytics"
    uid = Column(Integer, Identity(), primary_key=True)
    date = Column(DateTime(timezone=ZoneInfo("Europe/Moscow")), default=datetime.now(tz=ZoneInfo("Europe/Moscow")))
    online = Column(Integer(), default=0)
    current = Column(Boolean(), default=True)


class House(Base):
    __tablename__ = "House"
    uid = Column(Integer, Identity(), primary_key=True)
    owner = Column(String(32), default=" ")
    interior_id = Column(Integer)
    price = Column(Integer())
    pos_x = Column(Float())
    pos_y = Column(Float())
    pos_z = Column(Float())
    is_locked = Column(Boolean(), default=False)


class Squad(Base):
    __tablename__ = "Squad"
    uid = Column(Integer, Identity(), primary_key=True)
    name = Column(String(32))
    tag = Column(String(6))
    leader = Column(String(32))
    classification = Column(String(32))
    color = Column(Integer())
    color_hex = Column(String(16))


class SquadMembers(Base):
    __tablename__ = "SquadMembers"
    uid = Column(Integer, Identity(), primary_key=True)
    squad = Column(String(32))
    member = Column(String(32))
    rank = Column(String(32))


class SquadRanks(Base):
    __tablename__ = "SquadRanks"
    uid = Column(Integer, Identity(), primary_key=True)
    squad = Column(String(32))
    rank = Column(String(32), default="Лидер")
    permissions = Column(String(32), default="all")


class SquadGangZones(Base):
    __tablename__ = "SquadGangZones"
    uid = Column(Integer, Identity(), primary_key=True)
    id = Column(Integer())
    squad_id = Column(Integer(), default=-1)
    min_x = Column(Float())
    min_y = Column(Float())
    max_x = Column(Float())
    max_y = Column(Float())
    capture_cooldown = Column(Integer(), default=0)


class DataBase():
    @classmethod
    def create_metadata(cls):
        if platform.system() == "Windows":
            engine = create_engine(r"sqlite:///python\libs\database\sqlite3.db")
        else:
            engine = create_engine("sqlite:///python/libs/database/sqlite3.db")

        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)
        print(f"Loading: DataBase ({platform.system()})")

    @classmethod
    def create_player(cls, player: "Player") -> None:
        with cls.Session() as session:
            session.add(
                Player(
                    name=player.get_name(),
                    password=player.password,
                    email=player.email,
                    registration_ip=player.registration_ip,
                    last_ip=player.last_ip,
                    registration_data=player.registration_data,
                    gang_id=player.gang_id,
                )
            )
            session.add(PlayerFreeroamGunSlots(name=player.get_name()))
            session.add(PlayerSettings(name=player.get_name()))
            session.commit()

    @classmethod
    def get_player(cls, player: "Player") -> "Player":
        with cls.Session() as session:
            result = session.execute(select(Player).where(Player.name == player.get_name()))
            return result.scalar()

    @classmethod
    def get_player_name(cls, name: str) -> "Player":
        with cls.Session() as session:
            result = session.execute(select(Player).where(Player.name == name))
            return result.scalar()

    @classmethod
    def get_player_freeroam_gun_slots(cls, player: "Player") -> "PlayerFreeroamGunSlots":
        with cls.Session() as session:
            result = session.execute(select(PlayerFreeroamGunSlots).where(PlayerFreeroamGunSlots.name == player.get_name()))
            return result.scalar()

    @classmethod
    def get_player_settings(cls, player: "Player") -> "PlayerSettings":
        with cls.Session() as session:
            result = session.execute(select(PlayerSettings).where(PlayerSettings.name == player.get_name()))
            return result.scalar()

    @classmethod
    def save_player(cls, player: "Player", **attributes: dict) -> None:
        with cls.Session() as session:
            result = session.execute(select(Player).where(Player.name == player.get_name()))
            player_db = result.scalar()
            for key, value in attributes.items():
                if hasattr(player_db, key):
                    setattr(player_db, key, value)

            session.commit()

    @classmethod
    def save_player_name(cls, name: str, **kwargs) -> None:
        with cls.Session() as session:
            result = session.execute(select(Player).where(Player.name == name))
            player_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(player_db, key):
                    setattr(player_db, key, value)

            session.commit()

    @classmethod
    def save_freeroam_gun_slots(cls, player: "Player", **kwargs) -> None:
        with cls.Session() as session:
            result = session.execute(select(PlayerFreeroamGunSlots).where(PlayerFreeroamGunSlots.name == player.get_name()))
            player_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(player_db, key):
                    setattr(player_db, key, value)

            session.commit()

    @classmethod
    def save_player_settings(cls, player: "Player", **kwargs) -> None:
        with cls.Session() as session:
            result = session.execute(select(PlayerSettings).where(PlayerSettings.name == player.get_name()))
            player_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(player_db, key):
                    setattr(player_db, key, value)

            session.commit()

    @classmethod
    def create_gangzone(cls, id: int, gang_id: int, color: int, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        with cls.Session() as session:
            session.add(GangZone(id=id, gang_id=gang_id, color=color, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y))
            session.commit()

    @classmethod
    def create_gangzones(cls):
        if not cls.get_gangzone():
            for i, gz in enumerate(default_gang_zones):
                cls.create_gangzone(i, -1, 0xFFFFFFFF, gz[0], gz[1], gz[2], gz[3]) # Colors.white

            print(f"Created: GangZones (database)")

        for gz in default_gang_zones:
            Gangzone.create(gz[0], gz[1], gz[2], gz[3])

        print(f"Created: GangZones (server)")

    @classmethod
    def save_gangzone(cls, id: int, **kwargs) -> None:
        with cls.Session() as session:
            result = session.execute(select(GangZone).where(GangZone.id == id))
            gangzone_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(gangzone_db, key):
                    setattr(gangzone_db, key, value)

            session.commit()

    @classmethod
    def get_gangzone(cls):
        with cls.Session() as session:
            result = session.execute(select(GangZone))
            return result.scalar()

    @classmethod
    def load_gangzones(cls) -> GangZone:
        with cls.Session() as session:
            result = session.execute(select(GangZone))
            return result.scalars().all()

    @classmethod
    def load_gangzones_with_cooldown(cls) -> GangZone:
        with cls.Session() as session:
            result = session.execute(select(GangZone).where(GangZone.capture_cooldown != 0))
            return result.scalars().all()

    @classmethod
    def load_gangzone(cls, gangzone_id: int):
        with cls.Session() as session:
            result = session.execute(select(GangZone).where(GangZone.id == gangzone_id))
            return result.scalar()

    @classmethod
    def load_gangzones_order_by(cls) -> GangZone:
        with cls.Session() as session:
            result = session.execute(select(GangZone).order_by(GangZone.capture_cooldown))
            return result.scalars().all()

    @classmethod
    def create_vehicle(cls, id: int, model_id: int, x: float, y: float, z: float, rotation: float, color1: int, color2: int, delay: int, virtual_world: int) -> None:
        with cls.Session() as session:
            session.add(Vehicle(id=id, model_id=model_id, x=x, y=y, z=z, rotation=rotation, color1=color1, color2=color2, delay=delay, virtual_world=virtual_world))
            session.commit()

    @classmethod
    def save_vehicle(cls, id: int, **kwargs) -> None:
        with cls.Session() as session:
            result = session.execute(select(Vehicle).where(Vehicle.id == id))
            vehicle_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(vehicle_db, key):
                    setattr(vehicle_db, key, value)

            session.commit()

    @classmethod
    def load_vehicles_order_by(cls) -> Vehicle:
        with cls.Session() as session:
            result = session.execute(select(Vehicle).order_by(Vehicle.uid))
            return result.scalars().all()

    @classmethod
    def create_admin_pos(cls, player: "Player", name: str, x: float, y: float, z: float, rotation: float) -> None:
        with cls.Session() as session:
            session.add(
                AdminSavedPositions(
                    admin=player.get_name(),
                    name=name,
                    x=x,
                    y=y,
                    z=z,
                    rotation=rotation
                )
            )
            session.commit()

    @classmethod
    def load_admin_positions(cls, player: "Player") -> AdminSavedPositions:
        with cls.Session() as session:
            result = session.execute(select(AdminSavedPositions).where(AdminSavedPositions.admin == player.get_name()))
            return result.scalars().all()

    @classmethod
    def load_admin_position(cls, player: "Player", name: str) -> AdminSavedPositions:
        with cls.Session() as session:
            result = session.execute(select(AdminSavedPositions).where(and_(AdminSavedPositions.admin == player.get_name(), AdminSavedPositions.name == name)))
            return result.scalar()

    @classmethod
    def delete_admin_position(cls, player: "Player", name: str) -> AdminSavedPositions:
        with cls.Session() as session:
            session.execute(delete(AdminSavedPositions).where(and_(AdminSavedPositions.admin == player.get_name(), AdminSavedPositions.name == name)))
            session.commit()

    @classmethod
    def create_analytics(cls) -> None:
        with cls.Session() as session:
            session.add(ServerAnalytics())
            session.commit()

    @classmethod
    def update_analytics(cls) -> None:
        with cls.Session() as session:
            result = session.execute(select(ServerAnalytics).where(ServerAnalytics.current == True))
            analytics_db = result.scalar()
            analytics_db.online += 1
            session.commit()

    @classmethod
    def get_analytics(cls) -> int:
        with cls.Session() as session:
            result = session.execute(select(ServerAnalytics).where(ServerAnalytics.current == True))
            return result.scalar().online

    @classmethod
    def get_any_analytics(cls) -> int:
        with cls.Session() as session:
            result = session.execute(select(ServerAnalytics))
            return result.scalar()

    @classmethod
    def disable_current_analytics(cls) -> int:
        """
        Makes current ServerAnalytics disabled
        """
        with cls.Session() as session:
            result = session.execute(select(ServerAnalytics).where(ServerAnalytics.current == True))
            analytics = result.scalar()
            analytics.current = False
            session.commit()

    @classmethod
    def create_house(cls, interior_id: int, price: int, pos_x: float, pos_y: float, pos_z: float) -> House:
        """
        Create house and return it
        """
        with cls.Session() as session:
            session.add(House(interior_id=interior_id, price=price, pos_x=pos_x, pos_y=pos_y, pos_z=pos_z))
            session.commit()
            house = session.execute(select(House).where(and_(House.pos_x == pos_x, House.pos_y == pos_y, House.pos_z == pos_z)))
            return house.scalar()

    @classmethod
    def load_houses_order_by(cls) -> House:
        with cls.Session() as session:
            result = session.execute(select(House).order_by(House.uid))
            return result.scalars().all()

    @classmethod
    def load_house(cls, house_uid: int) -> House:
        with cls.Session() as session:
            result = session.execute(select(House).where(House.uid == house_uid))
            return result.scalar()

    @classmethod
    def save_house(cls, house_id: int, **kwargs: dict) -> None:
        with cls.Session() as session:
            result = session.execute(select(House).where(House.uid == house_id))
            house_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(house_db, key):
                    setattr(house_db, key, value)

            session.commit()

    @classmethod
    def load_squad_gangzones_order_by(cls) -> SquadGangZones:
        with cls.Session() as session:
            result = session.execute(select(SquadGangZones).order_by(SquadGangZones.capture_cooldown))
            return result.scalars().all()

    @classmethod
    def get_squad_gangzone(cls) -> SquadGangZones:
        with cls.Session() as session:
            result = session.execute(select(SquadGangZones))
            return result.scalar()

    @classmethod
    def create_squad_gangzone(cls, id: int, squad_id: int, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        with cls.Session() as session:
            session.add(SquadGangZones(id=id, squad_id=squad_id, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y))
            session.commit()

    @classmethod
    def save_squad_gangzone(cls, id: int, **kwargs) -> None:
        with cls.Session() as session:
            result = session.execute(select(SquadGangZones).where(SquadGangZones.id == id))
            gangzone_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(gangzone_db, key):
                    setattr(gangzone_db, key, value)

            session.commit()

    @classmethod
    def create_squad_gangzones(cls):
        if not cls.get_squad_gangzone():
            for i, gz in enumerate(default_squad_zones):
                cls.create_squad_gangzone(i, -1, gz[0], gz[1], gz[2], gz[3])

            print(f"Created: SquadGangZones (database)")

        for gz in default_squad_zones:
            Gangzone.create(gz[0], gz[1], gz[2], gz[3])

        print(f"Created: SquadGangZones (server)")

    @classmethod
    def create_squad(cls, name: str, tag: str, leader: str, classification: str, color: int, color_hex: str) ->Squad:
        with cls.Session() as session:
            session.add(Squad(name=name, tag=tag, leader=leader, classification=classification, color=color, color_hex=color_hex))
            session.add(SquadRanks(squad=name))
            session.commit()
            sq = session.execute(select(Squad).where(Squad.name == name))
            return sq.scalar()

    @classmethod
    def load_squad(cls, squad_uid: int) -> Squad:
        with cls.Session() as session:
            result = session.execute(select(Squad).where(Squad.uid == squad_uid))
            return result.scalar()

    @classmethod
    def load_squads(cls) -> Squad:
        with cls.Session() as session:
            result = session.execute(select(Squad))
            return result.scalars().all()

    @classmethod
    def delete_squad(cls, squad_name: int) -> Squad:
        with cls.Session() as session:
            session.execute(delete(Squad).where(Squad.name == squad_name))
            session.execute(delete(SquadMembers).where(SquadMembers.squad == squad_name))
            session.execute(delete(SquadRanks).where(SquadRanks.squad == squad_name))

    @classmethod
    def save_squad(cls, squad_uid: int, **kwargs: dict) -> None:
        with cls.Session() as session:
            result = session.execute(select(Squad).where(Squad.uid == squad_uid))
            squad_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(squad_db, key):
                    setattr(squad_db, key, value)

            session.commit()

    @classmethod
    def create_squad_member(cls, name: str, member: str, rank: str) -> None:
        with cls.Session() as session:
            session.add(SquadMembers(squad=name, member=member, rank=rank))
            session.commit()

    @classmethod
    def load_squad_member(cls, name: str) -> SquadMembers:
        with cls.Session() as session:
            result = session.execute(select(SquadMembers).where(Squad.name == name))
            return result.scalar()

    @classmethod
    def load_squad_members(cls, squad: str) -> SquadMembers:
        with cls.Session() as session:
            result = session.execute(select(SquadMembers).where(SquadMembers.squad == squad))
            return result.scalars().all()

    @classmethod
    def save_squad_member(cls, member: str, **kwargs: dict) -> None:
        with cls.Session() as session:
            result = session.execute(select(SquadMembers).where(SquadMembers.member == member))
            squad_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(squad_db, key):
                    setattr(squad_db, key, value)

            session.commit()

    @classmethod
    def create_squad_rank(cls, name: str, rank: str, permissions: str) -> None:
        with cls.Session() as session:
            session.add(SquadRanks(squad=name, rank=rank, permissions=permissions))
            session.commit()

    @classmethod
    def load_squad_ranks(cls, squad: str) -> SquadRanks:
        with cls.Session() as session:
            result = session.execute(select(SquadRanks).where(SquadRanks.squad == squad))
            return result.scalars().all()

    @classmethod
    def save_squad_rank(cls, squad: str, **kwargs: dict) -> None:
        with cls.Session() as session:
            result = session.execute(select(SquadRanks).where(SquadRanks.squad == squad))
            squad_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(squad_db, key):
                    setattr(squad_db, key, value)

            session.commit()

