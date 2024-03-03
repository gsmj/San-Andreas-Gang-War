from pysamp import (
    send_rcon_command,
    set_game_mode_text,
    enable_stunt_bonus_for_all,
    manual_vehicle_engine_and_lights,
    disable_interior_enter_exits,
    show_player_markers,
    set_world_time,
    send_client_message_to_all,
    show_name_tags,
    add_player_class,
    use_player_ped_anims
)
from datetime import datetime
from zoneinfo import ZoneInfo
from pysamp.timer import set_timer
from pystreamer import register_callbacks
from pystreamer.dynamiccp import DynamicCheckpoint
from pystreamer.dynamicpickup import DynamicPickup
from pydpc.driftcounter.callbacks import register as register_drift_callbacks
from pydpc.driftcounter.drift import Drift
from pydpc.driftcounter import *
from .libs.modes.modes import GangWar
from .libs.gang.gang import GangZoneData, gangzone_pool
from .libs.squad.squad import Squad, SquadGangZone, squad_gangzone_pool
from .player import Player
from .vehicle import Vehicle
from .libs.utils.data import *
from .libs.database.database import DataBase
from .libs.commands.commands import *
from .libs.static.textdraws import create_textdraws
from .libs.static.gangzones import create_gangzones
from .libs.static.labels import create_labels
from .libs.dynamic.objects import create_objects
from .libs.utils.consts import NO_HOUSE_OWNER
from .libs.house.house import House, houses
from .libs import __version__
from .core import Core
from .libs.fun.math import MathTest
import random
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
    manual_vehicle_engine_and_lights()
    use_player_ped_anims()
    disable_interior_enter_exits()
    show_name_tags(True)
    show_player_markers(1)
    send_rcon_command(f"name {ServerInfo.name}")
    send_rcon_command(f"language {ServerInfo.language}")
    send_rcon_command(f"game.map {ServerInfo.map}")
    set_game_mode_text(ServerInfo.gamemode)
    DataBase.create_gangzones()
    DataBase.create_squad_gangzones()
    create_textdraws()
    create_objects()
    create_labels()
    create_gangzones()
    gangzones = DataBase.load_gangzones_order_by()
    if gangzones:
        for gangzone in gangzones:
            GangZoneData(
                gangzone.id,
                gangzone.gang_id,
                gangzone.color,
                gangzone.min_x,
                gangzone.min_y,
                gangzone.min_x,
                gangzone.max_y,
                gangzone.capture_cooldown,
            )
    squad_gangzones = DataBase.load_squad_gangzones_order_by()
    if squad_gangzones:
        for squad_gz in squad_gangzones:
            SquadGangZone(
                squad_gz.id,
                squad_gz.squad_id,
                squad_gz.min_x,
                squad_gz.min_y,
                squad_gz.min_x,
                squad_gz.max_y,
                squad_gz.capture_cooldown,
            )

    squads = DataBase.load_squads()
    if squads:
        for squad in squads:
            Squad(
                squad.name,
                squad.tag,
                squad.leader,
                squad.classification,
                squad.color,
                squad.color_hex,
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
                # GangWar.update_capture_textdraw(gangzone)

            else:
                ...
                # GangWar.end_capture(gangzone, Player._registry)

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

    if ServerInfo.change_name_and_adverb != 0:
        ServerInfo.change_name_and_adverb -= 1

    else:
        send_rcon_command(f"name {random.choice(ServerInfo.name_timer)}")
        ServerInfo.change_name_and_adverb = 7200

    if ServerInfo.send_math != 0:
        ServerInfo.send_math -= 1

    else:
        MathTest.send_math_test()
        ServerInfo.send_math = 1800

@Player.on_text
@Player.using_registry
def on_player_text(player: Player, text: str) -> None:
    player.on_text_handle(text)
    return False

@DynamicPickup.on_player_pick_up
@Player.using_registry
def on_player_pick_up_pickup(player: Player, pickup: DynamicPickup) -> None:
    player.on_pick_up_pickup_handle(pickup)

@DynamicCheckpoint.on_player_enter
@Player.using_registry
def on_player_enter_checkpoint(player: Player, checkpoint: DynamicCheckpoint) -> None:
    player.on_enter_checkpoint_handle(checkpoint)

@Player.on_update
@Player.using_registry
def on_player_update(player: Player) -> None:
    player.on_update_handle()

@Player.on_give_damage
@Player.using_registry
def on_player_give_damage(player: Player, issuer: Player, amount: float, weapon_id: int, body_part) -> None:
    issuer = Player.from_registry_native(issuer)
    player.on_damage_handler(issuer, amount, weapon_id, body_part)

@Player.on_key_state_change
@Player.using_registry
def on_player_key_state_change(player: Player, new_keys: int, old_keys: int) -> None:
    player.on_key_state_change_handle(new_keys, old_keys)

@Player.on_state_change
@Player.using_registry
def on_player_state_change(player: Player, new_state: int, old_state: int) -> None:
    player.on_state_change_handle(new_state, old_state)

@Drift.on_start
@Player.using_registry
def on_player_start_drift(player: Player) -> None:
    player.on_start_drift_handle()

@Drift.on_update
@Player.using_registry
def on_player_drift_update(player: Player, value: int, combo: int, flag_id: int, distance: float, speed: float) -> None:
    player.on_drift_update_handle(value, combo, flag_id, distance, speed)

@Drift.on_end
@Player.using_registry
def on_player_end_drift(player: Player, value: int, combo: int, reason: int) -> None:
    player.on_end_drift_handle(value, combo, reason)

@Vehicle.on_death
@Vehicle.using_registry
def on_vehicle_death(vehicle: Vehicle, killer: Player) -> None:
    killer = Player.from_registry_native(killer)
    vehicle.on_death_handle(killer)

@Vehicle.on_damage_status_update
@Vehicle.using_registry
def on_vehicle_damage_status_update(vehicle: Vehicle, player: Player) -> None:
    player = Player.from_registry_native(player)
    vehicle.on_damage_status_handle(player)
