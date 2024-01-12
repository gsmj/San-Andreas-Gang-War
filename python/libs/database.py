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
    Float
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker
)
from datetime import datetime
from zoneinfo import ZoneInfo
from pysamp import gang_zone_show_for_all
from pysamp.gangzone import Gangzone
from pysamp import gang_zone_show_for_player
Base = declarative_base()


class Player(Base):
    __tablename__ = "Player"
    uid = Column(Integer, Identity(), primary_key=True)
    name = Column(String(32))
    password = Column(String(32))
    email = Column(String(32))
    pin = Column(Integer, default=0)
    registration_ip = Column(String(32))
    last_ip = Column(String(32))
    registration_data = Column(DateTime(timezone=ZoneInfo("Europe/Moscow")))
    kills = Column(Integer(), default=0)
    deaths = Column(Integer(), default=0)
    heals = Column(Integer(), default=0)
    masks = Column(Integer(), default=0)
    gang_id = Column(Integer())
    is_muted = Column(Boolean(), default=False)
    is_jailed = Column(Boolean(), default=False)
    is_banned = Column(Boolean(), default=False)


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
    is_capture = Column(Boolean(), default=False)


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
            session.commit()


    @classmethod
    def get_player(cls, player: "Player") -> "Player":
        with cls.Session() as session:
            result = session.execute(select(Player).where(Player.name == player.get_name()))
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
    def create_gangzone(cls, id: int, gang_id: int, color: int, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        with cls.Session() as session:
            session.add(GangZone(id=id, gang_id=gang_id, color=color, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y))
            session.commit()


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

