from pysamp import (
    on_gamemode_init,
    on_gamemode_exit,
    send_rcon_command,
    set_game_mode_text,
    set_name_tag_draw_distance,
    enable_stunt_bonus_for_all,
    manual_vehicle_engine_and_lights,
    disable_interior_enter_exits,
    allow_interior_weapons,
    limit_global_chat_radius,
    limit_player_marker_radius,
    show_player_markers,
    create_3d_text_label
)
from pysamp.gangzone import Gangzone
from pysamp.timer import set_timer
from pystreamer import register_callbacks
from pystreamer.dynamiccp import DynamicCheckpoint
from pystreamer.dynamicpickup import DynamicPickup
from .libs.gang import gangs, DefaultGangZones
from .libs.player import Player
from .libs.vehicles import Vehicles
from .libs.utils import Colors, ServerInfo
from .libs.database import DataBase
from .libs.commands import *
from .libs.textdraws import TextDraws
import random


import psutil # TODO Debug функция. Убрать на релизе
process = psutil.Process()

@on_gamemode_init
def on_ready() -> None:
    DataBase.create_metadata()
    register_callbacks()
    if not DataBase.get_gangzone():
        i = 0
        for gz in DefaultGangZones.zones:
            DataBase.create_gangzone(i, -1, Colors.white, gz[0], gz[1], gz[2], gz[3])
            print(f"Created: GangZone (database) -> ID: {i}")
            i += 1

    for gz in DefaultGangZones.zones:
        i = Gangzone.create(gz[0], gz[1], gz[2], gz[3])
        print(f"Created: GangZone (server) -> ID: {i.id}")

    for gz in DataBase.load_gangzones():
        if gz.gang_id != -1:
            gangs[gz.gang_id].turfs.append(gz.id)
            print(f"Created: GangZone (gang) -> ID: {gz.id} ({gangs[gz.gang_id].gang_name})")

    enable_stunt_bonus_for_all(False)
    manual_vehicle_engine_and_lights()
    disable_interior_enter_exits()
    send_rcon_command(f"name {ServerInfo.name}")
    send_rcon_command(f"language {ServerInfo.language}")
    send_rcon_command(f"game.map {ServerInfo.map}")
    set_game_mode_text(ServerInfo.gamemode)
    set_name_tag_draw_distance(30.0)
    allow_interior_weapons(False)
    limit_global_chat_radius(16.0)
    limit_player_marker_radius(14.0)
    show_player_markers(2)
    create_3d_text_label("Grove Street Families", 0x009900FF, 2514.3403, -1691.5911, 14.0460, 10, 0, test_line_of_sight=True)
    create_3d_text_label("The Ballas", 0xCC00FFFF, 2022.9318, -1120.2645, 26.4210+1, 10, 0, test_line_of_sight=True)
    create_3d_text_label("Los Santos Vagos", 0xffcd00FF, 2756.3645,-1182.8091, 69.4035+1, 10, 0, test_line_of_sight=True)
    create_3d_text_label("Varios Los Aztecas", 0x00B4E1FF, 2185.7717, -1815.2280, 13.5469, 10, 0, test_line_of_sight=True)
    create_3d_text_label("The Rifa", 0x6666FFFF, 2787.0764,-1926.1918, 13.5469+1, 10, 0, test_line_of_sight=True)
    TextDraws.load()
    Vehicles.load()
    set_timer(every_second, 1000, True)
    set_timer(change_name, 15000, True)


def every_second():
    memory = process.memory_full_info().uss / 1024**2
    cpu = process.cpu_percent() / psutil.cpu_count()
    print(f"CPU usage: {cpu} | Memory: {memory}")


def change_name():
    return send_rcon_command(f"name {random.choice(ServerInfo.name_timer)}")


@on_gamemode_exit
def on_exit() -> None:
    return print("Exit!")


@Player.on_connect
@Player.using_registry
def on_player_connect(player: Player) -> None:
    player.on_connect_handle()


@Player.on_disconnect
@Player.using_registry
def on_player_disconnect(player: Player, reason: int) -> None:
    player.on_disconnect_handle()


@Player.on_spawn
@Player.using_registry
def on_player_spawn(player: Player) -> None:
    player.on_spawn_handle()


@Player.on_death
@Player.using_registry
def on_player_death(player: Player, killer: Player, reason: int) -> None:
    killer = Player.from_registry_native(killer)
    player.on_death_handle(killer, reason)


@Player.on_text
@Player.using_registry
def on_player_text(player: Player, text: str) -> None:
    player.on_text_handle(text)


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
