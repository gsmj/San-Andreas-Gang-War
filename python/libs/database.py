from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    String,
    Integer,
    Column,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    insert,
    select,
    SmallInteger,
    values,
    Identity,
    Float,
    and_,
    func,
    delete
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker
)
from .gang import DefaultGangZones, gangs
from pysamp.gangzone import Gangzone
from .utils import Colors
from datetime import datetime
from zoneinfo import ZoneInfo
import secrets
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
    money = Column(Integer(), default=100000)
    donate = Column(Integer(), default=0)
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
    gang_atk_id = Column(Integer(), default=-1)
    gang_def_id = Column(Integer(), default=-1)
    gang_atk_score = Column(Integer(), default=0)
    gang_def_score = Column(Integer(), default=0)
    capture_time = Column(Integer(), default=0)
    capture_cooldown = Column(Integer(), default=0)
    is_capture = Column(Boolean(), default=False)


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


class DataBase():
    @classmethod
    def create_metadata(cls):
        engine = create_engine("sqlite:///sqlite3.db")
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

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
    def save_player(cls, player: "Player", **kwargs) -> None:
        with cls.Session() as session:
            result = session.execute(select(Player).where(Player.name == player.get_name()))
            player_db = result.scalar()
            for key, value in kwargs.items():
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
            for i, gz in enumerate(DefaultGangZones.zones):
                DataBase.create_gangzone(i, -1, Colors.white, gz[0], gz[1], gz[2], gz[3])

            print(f"Created: GangZones (database)")

        for gz in DefaultGangZones.zones:
            Gangzone.create(gz[0], gz[1], gz[2], gz[3])

        print(f"Created: GangZones (server)")
        for gz in DataBase.load_gangzones():
            if gz.gang_id != -1:
                gangs[gz.gang_id].turfs.append(gz.id)

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
