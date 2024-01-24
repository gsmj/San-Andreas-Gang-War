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
    create_3d_text_label,
    add_player_class
)
from pysamp.gangzone import Gangzone
from pysamp.textdraw import TextDraw
from pysamp.timer import set_timer
from pystreamer import register_callbacks
from pystreamer.dynamiccp import DynamicCheckpoint
from pystreamer.dynamicpickup import DynamicPickup
from .libs.gang import gangs, DefaultGangZones, GangZoneData
from .libs.player import Player
from .libs.vehicle import Vehicle
from .libs.utils import Colors, ServerInfo
from .libs.database import DataBase
from .libs.commands import *
from .libs.textdraws import TextDraws
import random


@on_gamemode_init
def on_ready() -> None:
    register_callbacks()
    DataBase.create_metadata()
    DataBase.create_gangzones()
    print(f"Created: GangZone (gang)")
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
    gangzones = DataBase.load_gangzones_order_by()
    if gangzones:
        for gangzone in gangzones:
            GangZoneData(
                gangzone.id,
                gangzone.gang_id,
                gangzone.color,
                gangzone.gang_atk_id,
                gangzone.gang_def_id,
                gangzone.gang_atk_score,
                gangzone.gang_def_score,
                gangzone.capture_cooldown,
                gangzone.is_capture,
                gangzone.capture_time).using_registry(gangzone.id)

    vehicles = DataBase.load_vehicles_order_by()
    if vehicles:
        for vehicle in vehicles:
            veh = Vehicle(
                vehicle.model_id,
                vehicle.owner,
                vehicle.engine,
                vehicle.lights,
                vehicle.doors
            ).create(
                vehicle.model_id,
                vehicle.x,
                vehicle.y,
                vehicle.z,
                vehicle.rotation,
                vehicle.color1,
                vehicle.color2,
                vehicle.delay,
                add_siren=vehicle.add_siren).add_to_registry()
            veh.set_virtual_world(vehicle.virtual_world)

    set_timer(every_second, 1000, True)


@on_gamemode_exit
def on_exit() -> None:
    print("EXITED")

def every_second():
    change_name_cd = 15000
    for gangzone in GangZoneData._registry.values():
        if gangzone.capture_cooldown != 0:
            gangzone.capture_cooldown -= 1

        if gangzone.is_capture:
            if gangzone.capture_time != 0:
                gangzone.capture_time -= 1
                Player.update_capture_textdraw(gangzone)

            else:
                Player.end_capture(gangzone)

    if change_name_cd != 0:
        change_name_cd -= 1

    else: send_rcon_command(f"name {random.choice(ServerInfo.name_timer)}")
    change_name_cd = 15000

@Player.on_connect
@Player.using_registry
def on_player_connect(player: Player) -> None:
    player.on_connect_handle()


@Player.on_disconnect
@Player.using_registry
def on_player_disconnect(player: Player, reason: int) -> None:
    player.on_disconnect_handle()

@Player.on_request_class
@Player.using_registry
def on_player_request_class(player: Player, class_id: int) -> None:
    player.on_request_class_handle(class_id)

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

@Player.on_key_state_change
@Player.using_registry
def on_player_key_state_change(player: Player, new_keys: int, old_keys: int) -> None:
    player.on_key_state_change_handle(new_keys, old_keys)

@Player.on_state_change
@Player.using_registry
def on_player_state_change(player: Player, new_state: int, old_state: int) -> None:
    player.on_state_change_handle(new_state, old_state)


@Player.on_click_textdraw
@Player.using_registry
def on_player_click_textdraw(player: Player, clicked: TextDraw) -> None:
    player.on_click_textdraw_handle(clicked)
