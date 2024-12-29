import random
from datetime import datetime
from zoneinfo import ZoneInfo

from driftcounter.driftcounter import *
from driftcounter.driftcounter.callbacks import register as register_drift_callbacks
from pysamp import (
    add_player_class,
    disable_interior_enter_exits,
    enable_stunt_bonus_for_all,
    send_client_message_to_all,
    gang_zone_create,
    set_world_time,
    show_name_tags,
    show_player_markers,
    use_player_ped_anims
)
from pysamp.timer import set_timer
from pystreamer import register_callbacks

from .core import Core
from .libs import __version__
from .libs.commands.commands import *
from .libs.commands.debug import *
from .libs.database.database import DataBase
from .libs.dynamic.objects import create_objects
from .libs.fun.math import MathTest
from .libs.gang.gang import GangZoneData, gangzone_pool
from .libs.house.house import House, houses
from .libs.modes.modes import GangWar
from .libs.squad.squad import Squad, SquadGangZone, squad_gangzone_pool, squad_pool_id
from .libs.static.gangzones import create_gangzones
from .libs.static.labels import create_labels
from .libs.static.textdraws import create_textdraws
from .libs.static.vehicles import create_gang_vehicles
from .libs.utils.consts import NO_VEHICLE_OWNER
from .libs.utils.data import *
from .player import Player
from .vehicle import Vehicle
encode()

@Core.on_init
def on_ready():
    DataBase.create_metadata()
    register_callbacks()
    register_drift_callbacks()
    drift_set_global_check()
    drift_set_update_delay(8)
    drift_set_start_end_delay(60)
    drift_set_minimal_angle(15.5)
    drift_set_minimal_speed(25.5)
    drift_set_divider(1000)
    drift_set_damage_check()
    enable_stunt_bonus_for_all(False)
    use_player_ped_anims()
    disable_interior_enter_exits()
    show_name_tags(True)
    show_player_markers(1)
    DataBase.create_gangzones(gang_zone_create)
    DataBase.create_squad_gangzones(gang_zone_create)
    create_textdraws()
    create_objects()
    create_labels()
    create_gangzones()
    create_gang_vehicles()
    gangzones = DataBase.load_gangzones_order_by()
    if gangzones:
        for gangzone in gangzones:
            if gangzone.gang_id != -1:
                color = gangs[gangzone.gang_id].color

            else:
                color = gangzone.color

            GangZoneData(
                gangzone.id,
                gangzone.gang_id,
                color,
                gangzone.min_x,
                gangzone.min_y,
                gangzone.min_x,
                gangzone.max_y,
                gangzone.capture_cooldown,
            )
    Squad.create_all()
    squad_gangzones = DataBase.load_squad_gangzones_order_by()
    if squad_gangzones:
        for squad_gz in squad_gangzones:
            if squad_gz.squad_id != -1:
                color = squad_pool_id[squad_gz.squad_id].color
            else:
                color = 0xFFFFFFAA

            SquadGangZone(
                squad_gz.id,
                squad_gz.squad_id,
                color,
                squad_gz.min_x,
                squad_gz.min_y,
                squad_gz.max_x,
                squad_gz.max_y,
                squad_gz.capture_cooldown,
            )
    vehicles = DataBase.load_vehicles_order_by()
    if vehicles:
        for vehicle in vehicles:
            if vehicle.virtual_world != ServerMode.freeroam_world:
                veh = Vehicle.create(
                    vehicle.model_id,
                    vehicle.x,
                    vehicle.y,
                    vehicle.z,
                    vehicle.rotation,
                    vehicle.color1,
                    vehicle.color2,
                    vehicle.delay,
                    vehicle.virtual_world,
                    add_siren=vehicle.add_siren,
                )
                veh.set_info(
                    owner=vehicle.owner,
                    engine=vehicle.engine,
                    lights=vehicle.lights,
                    doors=vehicle.doors
                )
    houses_ = DataBase.load_houses_order_by()
    if houses_:
        for house in houses_:
            House(
                house.uid,
                house.owner,
                house.interior_id,
                house.price,
                house.pos_x,
                house.pos_y,
                house.pos_z,
                house.is_locked
            )

    analytics = DataBase.get_any_analytics()
    if not analytics:
        DataBase.create_analytics()
        print("Created: Analytics (database)")

    for i in range(312):
        if i == 74:
            continue

        add_player_class(i, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0)

    print(f"Loaded: {len(gangzone_pool)} gangzones")
    print(f"Loaded: {len(squad_gangzone_pool)} squad gangzones")
    print(f"Loaded: {len(squad_pool_id)} squads")
    print(f"Loaded: {len(Vehicle._registry.items())} vehicles")
    print(f"Loaded: {len(houses)} houses")
    print("--------------------------------------------------")
    print(f"Running: {ServerInfo.name_short} (v{__version__})\nCreated by: Ykpauneu & Rein.")
    print("--------------------------------------------------")
    time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
    ServerInfo.current_time = time
    set_world_time(ServerInfo.current_time.hour)
    set_timer(every_second, 1000, True)

def every_second():
    for gangzone in gangzone_pool.values():
        if gangzone.capture_cooldown != 0:
            gangzone.capture_cooldown -= 1

            if gangzone.capture_cooldown == 0:
                DataBase.save_gangzone(
                    gangzone.id,
                    capture_cooldown=0
                )

        if gangzone.is_capture:
            if gangzone.capture_time != 0:
                gangzone.capture_time -= 1
                GangWar.update_capture_textdraw(gangzone)

            else:
                GangWar.end_capture(gangzone, Player._registry)

    for squad_gangzone in squad_gangzone_pool.values():
        if squad_gangzone.capture_cooldown != 0:
            squad_gangzone.capture_cooldown -= 1

            if squad_gangzone.capture_cooldown == 0:
                DataBase.save_squad_gangzone(
                    squad_gangzone.id,
                    capture_cooldown=0
                )

        if squad_gangzone.is_capture:
            if squad_gangzone.capture_time != 0:
                squad_gangzone.capture_time -= 1
                squad_gangzone.update_capture_textdraw()

            else:
                squad_gangzone.end_war(Player._registry)

    if ServerInfo.current_time.hour != datetime.now(tz=ZoneInfo("Europe/Moscow")).hour:
        ServerInfo.current_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        if ServerInfo.current_time.hour == 0:
            DataBase.disable_current_analytics()
            DataBase.create_analytics()

        set_world_time(ServerInfo.current_time.hour)
        send_client_message_to_all(Colors.ad, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        send_client_message_to_all(Colors.ad, f"Наш сайт: {{{Colors.link_hex}}}sanandreasonline.github.io")
        send_client_message_to_all(Colors.ad, f"Наш Discord: {{{Colors.link_hex}}}discord.gg/yn2EcNJywH")
        send_client_message_to_all(Colors.ad, f"Наш IP: {{{Colors.cmd_hex}}}213.226.126.237:7777")
        send_client_message_to_all(Colors.ad, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if ServerInfo.send_math != 0:
        ServerInfo.send_math -= 1

    else:
        MathTest.send_math_test()
        ServerInfo.send_math = 1800

@Vehicle.on_death
@Vehicle.using_registry
def on_vehicle_death(vehicle: Vehicle, killer: Player) -> None:
    killer = Player.from_registry_native(killer)
    if vehicle.owner != NO_VEHICLE_OWNER:
        killer.remove_player_vehicle()
        return Vehicle.delete_registry(vehicle)
