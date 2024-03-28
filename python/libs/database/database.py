import platform
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import (Boolean, Column, DateTime, Float, Identity, Integer,
                        String, and_, create_engine, delete, select)
from sqlalchemy.orm import declarative_base, sessionmaker

# import pysamp.gangzone as py_gangzone

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
    (2816.37451171875, -2561.1746826171875, 2861.37451171875, -2323.1746826171875),
    (2214.393310546875, -2730.180908203125, 2812.393310546875, -2272.180908203125),
    (2145.193359375, -178.1749267578125, 2619.193359375, 215.8250732421875),
    (1859.193359375, 106.81256103515625, 2046.193359375, 263.81256103515625),
    (1506.193359375, -33.18743896484375, 1606.193359375, 66.81256103515625),
    (996.593505859375, -463.18743896484375, 1142.593505859375, -274.18743896484375),
    (-619.2064208984375, -213.18743896484375, -397.2064208984375, -15.18743896484375),
    (-631.2064208984375, -571.1871948242188, -459.2064208984375, -460.18719482421875),
    (-410.2064208984375, -1097.1871948242188, -310.2064208984375, -997.1871948242188),
    (-1144.806396484375, -1731.1871948242188, -957.806396484375, -1607.1871948242188),
    (-1956.8063473701477, -1797.9869995117188, -1715.8063473701477, -1498.9869995117188),
    (-1484.8063473701477, -1622.9872436523438, -1384.8063473701477, -1429.9872436523438),
    (-1210.8063473701477, -1275.9872436523438, -998.8063473701477, -1061.9872436523438),
    (-986.8063473701477, -572.9872436523438, -886.8063473701477, -472.98724365234375),
    (-2283.0125579833984, -1761.98095703125, -2205.0125579833984, -1696.98095703125),
    (-2531.0562591552734, 1518.0501403808594, -2293.0562591552734, 1571.0501403808594),
    (-1488.018783569336, 1460.0126342773438, -1355.018783569336, 1512.0126342773438),
    (-1633.6188354492188, 2473.0187644958496, -1344.6188354492188, 2715.0187644958496),
    (-471.61260986328125, 2186.018798828125, -312.61260986328125, 2294.018798828125),
    (-958.6314086914062, 1955.0375671386719, -454.63140869140625, 2159.037567138672),
    (-1878.6375427246094, 1260.0314331054688, -1740.6375427246094, 1332.0314331054688),
    (394.39361572265625, 705.0314331054688, 799.3936157226562, 1027.0314331054688),
    (-123.0252685546875, 1629.0375671386719, 442.9747314453125, 2153.037567138672),
    (-97.01904296875, 2386.0250205993652, 450.98095703125, 2667.0250205993652),
    (2776.393310546875, 826.0126342773438, 2896.393310546875, 1022.0126342773438),
    (2233.3494873046875, 2701.0500450134277, 2464.3494873046875, 2830.0500450134277),
    (662.193603515625, 223.01275634765625, 825.193603515625, 398.01275634765625),
    (1848.79345703125, -1266.9872436523438, 2067.79345703125, -1128.9872436523438),
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
    outdated_version_warning = Column(Boolean(), default=False)
    use_squad_tag_in_text = Column(Boolean(), default=False)


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
    classification = Column(String(32))
    color = Column(Integer())
    color_hex = Column(String(16))


class SquadMember(Base):
    __tablename__ = "SquadMember"
    uid = Column(Integer, Identity(), primary_key=True)
    squad_id = Column(Integer)
    member = Column(String(32))
    rank = Column(String(32))


class SquadRank(Base):
    __tablename__ = "SquadRank"
    uid = Column(Integer, Identity(), primary_key=True)
    squad_id = Column(Integer)
    rank = Column(String(32), default="Лидер")


class SquadRankPermissions(Base):
    __tablename__ = "SquadRankPermissions"
    uid = Column(Integer, Identity(), primary_key=True)
    squad_id = Column(Integer)
    rank_id = Column(Integer)
    permissions = Column(String(16))


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
        cls.Session = sessionmaker(bind=engine, expire_on_commit=False)
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
    def create_gangzone(cls, id: int, gang_id: int, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        with cls.Session() as session:
            session.add(GangZone(id=id, gang_id=gang_id, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y))
            session.commit()

    @classmethod
    def create_gangzones(cls):
        create = False
        if not cls.get_gangzone():
            create = True

        # for gz in default_gang_zones:
        #     i = py_gangzone.Gangzone.create(gz[0], gz[1], gz[2], gz[3])
        #     if create:
        #         cls.create_gangzone(i.id, -1, gz[0], gz[1], gz[2], gz[3])

        print(f"Created: GangZones (database & server)")

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
    def load_gangzone(cls, gangzone_id: int) -> SquadGangZones:
        with cls.Session() as session:
            result = session.execute(select(SquadGangZones).where(SquadGangZones.id == gangzone_id))
            return result.scalar()

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
        create = False
        if not cls.get_squad_gangzone(): # Чтобы не делать по 158 запросов в бд
            create = True

        # for gz in default_squad_zones:
        #     i = py_gangzone.Create.create(gz[0], gz[1], gz[2], gz[3])
        #     if create:
        #         cls.create_squad_gangzone(i.id, -1, gz[0], gz[1], gz[2], gz[3])

        print(f"Created: SquadGangZones (database & server)")


    @classmethod
    def create_squad(cls, name: str, tag: str, leader: str, classification: str, color: int, color_hex: str) -> Squad:
        with cls.Session() as session:
            session.add(Squad(name=name, tag=tag, classification=classification, color=color, color_hex=color_hex))
            squad_ = session.execute(select(Squad).where(Squad.name == name)).scalar()

            session.add(SquadRank(squad_id=squad_.uid))
            session.add(SquadMember(squad_id=squad_.uid, member=leader, rank="Лидер"))
            rank_ = session.execute(select(SquadRank).where(SquadRank.squad_id == squad_.uid)).scalar()
            session.add(SquadRankPermissions(squad_id=squad_.uid, rank_id=rank_.uid, permissions="all"))
            session.commit()
            return squad_

    @classmethod
    def load_squad_by_name(cls, squad_name: str) -> Squad:
        with cls.Session() as session:
            result = session.execute(select(Squad).where(Squad.name == squad_name))
            return result.scalar()

    @classmethod
    def load_squad_by_tag(cls, squad_tag: str) -> Squad:
        with cls.Session() as session:
            result = session.execute(select(Squad).where(Squad.tag == squad_tag))
            return result.scalar()

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
    def delete_squad(cls, squad_id: int) -> Squad:
        with cls.Session() as session:
            session.execute(delete(Squad).where(Squad.uid == squad_id))
            session.execute(delete(SquadMember).where(SquadMember.squad_id == squad_id))
            session.execute(delete(SquadRank).where(SquadRank.squad_id == squad_id))
            session.execute(delete(SquadRankPermissions).where(SquadRankPermissions.squad_id == squad_id))
            session.commit()

        with cls.Session() as session:
            gangzones = session.execute(select(SquadGangZones).where(SquadGangZones.squad_id == squad_id)).scalars().all()
            for gangzone in gangzones:
                gangzone.squad_id = -1

            session.commit()

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
    def create_squad_member(cls, squad_id: int, member: str, rank: str) -> None:
        with cls.Session() as session:
            session.add(SquadMember(squad_id=squad_id, member=member, rank=rank))
            session.commit()

    @classmethod
    def load_squad_member(cls, player: Player) -> SquadMember:
        with cls.Session() as session:
            result = session.execute(select(SquadMember).where(SquadMember.member == player.name))
            return result.scalar()

    @classmethod
    def load_squad_members(cls, squad_id: int) -> SquadMember:
        with cls.Session() as session:
            result = session.execute(select(SquadMember).where(SquadMember.squad_id == squad_id))
            return result.scalars().all()

    @classmethod
    def save_squad_member(cls, member: str, **kwargs: dict) -> None:
        with cls.Session() as session:
            result = session.execute(select(SquadMember).where(SquadMember.member == member))
            squad_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(squad_db, key):
                    setattr(squad_db, key, value)

            session.commit()

    @classmethod
    def delete_squad_member(cls, member: str) -> None:
        with cls.Session() as session:
            session.execute(delete(SquadMember).where(SquadMember.member == member))
            session.commit()

    @classmethod
    def delete_squad_rank(cls, squad_id: int, rank: str) -> None:
        rank_db = DataBase.load_squad_rank_by_name(squad_id, rank)
        with cls.Session() as session:
            session.execute(delete(SquadRank).where(SquadRank.rank == rank))
            session.execute(delete(SquadRankPermissions).where(SquadRankPermissions.rank_id == rank_db.uid))
            session.commit()

        members = DataBase.load_squad_members(squad_id)
        DataBase.create_squad_rank(squad_id, "Нет", "none")
        rank_none = DataBase.load_squad_rank_by_name(squad_id, "Нет")
        for member in members:
            if member.rank_id == rank_db.uid:
                DataBase.save_squad_member(member.name, rank=rank_none.rank)

    @classmethod
    def create_squad_rank(cls, squad_id: str, rank: str, permissions: list) -> None:
        with cls.Session() as session:
            session.add(SquadRank(squad_id=squad_id, rank=rank))
            rank_ = session.execute(select(SquadRank).where(and_(SquadRank.squad_id == squad_id, SquadRank.rank == rank))).scalar()
            for permission in permissions:
                session.add(SquadRankPermissions(squad_id=squad_id, rank_id=rank_.uid, permissions=permission))

            session.commit()

    @classmethod
    def load_squad_ranks(cls, squad_id: int) -> SquadRank:
        with cls.Session() as session:
            result = session.execute(select(SquadRank).where(SquadRank.squad_id == squad_id))
            return result.scalars().all()

    @classmethod
    def load_squad_rank_by_name(cls, squad_id: int, rank_name: str) -> SquadRank:
        with cls.Session() as session:
            result = session.execute(select(SquadRank).where(and_(SquadRank.squad_id == squad_id, SquadRank.rank == rank_name)))
            return result.scalar()

    @classmethod
    def load_squad_permissions_for_rank(cls, squad_id: int, rank_id: int) -> list[str]:
        l: list = []
        with cls.Session() as session:
            permissions = session.execute(
                select(SquadRankPermissions).where(
                    and_(
                        SquadRankPermissions.squad_id == squad_id,
                        SquadRankPermissions.rank_id == rank_id
                    )
                )
            ).scalars().all()

            for i in permissions:
                l.append(i.permissions)

        return l

    @classmethod
    def save_squad_rank(cls, squad_id: int, rank_name: str, **kwargs: dict) -> None:
        with cls.Session() as session:
            result = session.execute(select(SquadRank).where(and_(SquadRank.squad_id == squad_id, SquadRank.rank == rank_name)))
            rank_db = result.scalar()
            for key, value in kwargs.items():
                if hasattr(rank_db, key):
                    setattr(rank_db, key, value)

            session.commit()

        members = DataBase.load_squad_members(squad_id)
        for i in members:
            if i.rank == rank_name:
                DataBase.save_squad_member(i.member, rank=kwargs["rank"])
