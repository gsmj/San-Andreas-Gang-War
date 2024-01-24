from pysamp.commands import cmd
from pysamp import send_client_message_to_all
from pysamp.dialog import Dialog
from pysamp.timer import set_timer
from .player import Player, Dialogs
from .gang import gangs, GangZoneData
from .utils import (
    Colors,
    MonthsConverter,
    ServerWorldIDs,
    WeatherIDs,
    convert_seconds,
    VIPData,
    ServerInfo)
from .database import DataBase
from datetime import datetime as dt
from zoneinfo import ZoneInfo
import random
from .vehicle import Vehicle

@cmd
@Player.using_registry
def mn(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_mn_dialog(player)

@cmd
@Player.using_registry
def stats(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_stats_dialog(player)

@cmd
@Player.using_registry
def healme(player: Player):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.heals == 0:
        return player.send_error_message("У Вас нет аптечек!")

    health = player.get_health()
    if health + 25.0 <= 100.0:
        player.apply_animation("SMOKING", "M_smk_drag", 4.1, False, False, False, False, 0)
        player.heals -= 1
        player.set_health(health + 25.0)
        player.set_chat_bubble("Использует аптечку..", Colors.white, 20.0, 5000)
        return player.send_notification_message(f"Вы использовали аптечку. Здоровье восстановлено на {{FF0000}}25HP{{{Colors.white_hex}}}.")

    else:
        return player.send_error_message("Вы не можете использовать аптечку сейчас!")

@cmd
@Player.using_registry
def mask(player: Player):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.is_wearing_mask:
        return player.send_error_message("Ваше местоположение уже скрыто!")

    if player.masks == 0:
        return player.send_error_message("У Вас нет масок!")

    if player.is_attached_object_slot_used(2):
        player.remove_attached_object(2)

    player.apply_animation("SHOP", "ROB_Shifty", 4.1, False, False, False, False, 0)
    player.masks -= 1
    player.is_wearing_mask = True
    player.set_attached_object(2, 19801, 2, offset_x=0.067, offset_y=0.026, offset_z=0.001000, rotation_x=0.30, rotation_y=85.600000, rotation_z=175.400000, scale_x=1.321000, scale_y=1.32700, scale_z=1.257000)
    player.set_color(Colors.mask)
    player.set_chat_bubble("Надевает маску..", Colors.white, 20.0, 5000)
    return player.send_notification_message(f"Ваше местоположение на карте скрыто. Используйте {{{Colors.cmd_hex}}}/maskoff{{{Colors.white_hex}}}, чтобы снять маску.")

@cmd
@Player.using_registry
def maskoff(player: Player):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.is_wearing_mask:
        return player.send_error_message("У Вас нет маски!")

    if player.is_attached_object_slot_used(2):
        player.remove_attached_object(2)

    player.is_wearing_mask = False
    player.set_color(player.gang.color)
    return player.send_notification_message("Вы сняли маску.")

@cmd
@Player.using_registry
def newgang(player: Player):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.gang.is_capturing:
        return player.send_error_message("Вы не можете сменить банду сейчас!")

    if player.is_wearing_mask:
        player.is_wearing_mask = False
        player.set_color(player.gang.color)

    if player.is_attached_object_slot_used(2):
        player.remove_attached_object(2)

    player.heals = 0
    player.masks = 0
    player.reset_weapons()
    player.reset_money()
    return Dialogs.show_command_gang_choice_dialog(player)

@cmd
@Player.using_registry
def changeskin(player: Player):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(10.0):
        return player.send_error_message("Не флудите!")

    if player.gang.is_capturing:
        return player.send_error_message("Вы не можете сменить банду сейчас!")

    if player.get_virtual_world() != ServerWorldIDs.gangwar_world_interior:
        return player.send_error_message("Вы можете изменить скин только в доме!")

    player.set_skin(random.choice(player.gang.skins))
    return player.send_notification_message("Ваш скин был изменён.")

@cmd
@Player.using_registry
def time(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(5.0):
        return player.send_error_message("Не флудите!")

    current_time = dt.now(tz=ZoneInfo("Europe/Moscow")).strftime("%H:%M")
    current_date = dt.now(tz=ZoneInfo("Europe/Moscow"))
    player.apply_animation("COP_AMBIENT", "Coplook_watch", 4.1, False, False, False, False, 0)
    return player.game_text(f"{Colors.game_text_time_date}{current_date.day} {MonthsConverter.months[current_date.month]}~n~{Colors.game_text_time_time}{current_time}", 3000, 1)

@cmd
@Player.using_registry
def f(player: Player, *message: str):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.is_muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /f message")

    for player_in_registry in Player._registry.values():
        if player.gang_id == player_in_registry.gang_id:
            key, value = player.get_gang_rang()
            player_in_registry.send_client_message(player.gang.color, f"[F] {value} {player.get_name()}: {message}")

    return

@cmd
@Player.using_registry
def o(player: Player, *message: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.is_muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /o message")

    return send_client_message_to_all(player.get_color(), f"{player.get_name()}{{{Colors.white_hex}}}: {message}")

@cmd
@Player.using_registry
def v(player: Player, *message: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.vip == 0:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.is_muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /v message")

    vip_status = VIPData.names[player.vip]
    vip_status_color = VIPData.colors[player.vip]
    for player_in_registry in Player._registry.values():
        if player_in_registry.vip != -1:
            player_in_registry.send_notification_message(f"{{{Colors.vip_hex}}}[VIP] {{{vip_status_color}}}[{vip_status}]{{{Colors.white_hex}}} {player_in_registry.get_name()}: {message}")

@cmd
@Player.using_registry
def members(player: Player):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    members_dict = {}
    for player_in_registry in Player._registry.values():
        if player.gang_id == player_in_registry.gang_id:
            members_dict[player_in_registry.get_name()] = player_in_registry.kills

    sorted_members = dict(sorted(members_dict.items(), key=lambda item: item[1], reverse=True))
    members_string = ""
    for key, value in sorted_members.items():
        members_string += f"Игрок: {key}\t\t\tУбийств: {value}\n"

    return Dialog.create(0, f"Онлайн в банде {player.gang.gang_name}", f"{members_string}", "Закрыть", "").show(player)

@cmd
@Player.using_registry
def gangzones(player: Player):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    player.send_notification_message("Вы можете выбрать территорию, нажав ЛКМ/Enter.")
    return Dialogs.show_gangzones_dialog_page_one(player)

@cmd
@Player.using_registry
def commands(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_commands_list_dialog(player)

@cmd
@Player.using_registry
def setweather(player: Player, weather_id: int):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if int(weather_id) not in WeatherIDs.weather:
        return player.send_error_message("Допустимый диапазон погоды: 0 - 22!")

    player.set_weather(int(weather_id))
    return player.send_notification_message(f"Погода была изменена на {weather_id} ID.")

@cmd
@Player.using_registry
def capture(player: Player):
    player.kick_if_not_logged()
    if not player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
        return

    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    for gangzone in DataBase.load_gangzones():
        if player.is_in_area(gangzone.min_x, gangzone.min_y, gangzone.max_x, gangzone.max_y):
            break

    gangzone = GangZoneData._registry[gangzone.id]
    if player.gang_id == gangzone.gang_id:
        return player.send_error_message("Вы не можете атаковать свою территорию!")

    if gangzone.capture_cooldown != 0:
        hours, minutes, seconds = convert_seconds(gangzone.capture_cooldown)
        return player.send_error_message(f"Захватить территорию можно будет только через {{{Colors.cmd_hex}}}{hours}{{{Colors.error_hex}}} часов, {{{Colors.cmd_hex}}}{minutes}{{{Colors.error_hex}}} минут, {{{Colors.cmd_hex}}}{seconds}{{{Colors.error_hex}}} секунд!")

    total_captures = 0
    gangzones = GangZoneData.get_all_from_registy()
    for i in gangzones.values():
        if i.is_capture:
            total_captures += 1

    if total_captures == ServerInfo.CAPTURE_LIMIT:
        return player.send_error_message("В данный момент на сервере достигнут лимит захвата!")

    if player.gang.is_capturing or gangs[gangzone.gang_id].is_capturing:
        return player.send_error_message("Одна из банд уже ведёт захват территории!")

    return Dialogs.show_start_capture_dialog(player, player.gang_id, gangzone.gang_id, gangzone.gangzone_id)

@cmd
@Player.using_registry
def gps(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return player.disable_checkpoint()

@cmd
@Player.using_registry
def credits(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_credits_dialog(player)

@cmd
@Player.using_registry
def setmode(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_select_mode_dialog(player)

@cmd
@Player.using_registry
def lock(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    lock_status = ["~b~Unlocked", "~r~Locked"]
    for veh_inst in Vehicle._registry.values():
        if veh_inst.get_distance_from_point(*player.get_pos()) < 3.0:
            if not veh_inst.owner or veh_inst.owner == player.get_name():
                if veh_inst.doors == 0:
                    veh_inst.doors = 1
                else:
                    veh_inst.doors = 0

                player.game_text(lock_status[veh_inst.doors], 2500, 0)
                veh_inst.set_params_ex(veh_inst.engine, veh_inst.lights, 0, veh_inst.doors, 0, 0, 0)
                break
            else:
                player.send_error_message("Это не Ваша машина!")
                break

@cmd
@Player.using_registry
def sms(player: Player, player_id: int, *message: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.is_muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /sms message")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    target = Player.from_registry_native(target_id)
    return target.send_client_message(Colors.sms, f"[SMS] {message}. Отправитель: {player.get_name()}.")

@cmd
@Player.using_registry
def id(player: Player, nickname: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    found = ""
    for player_in_registry in Player._registry.values():
        if nickname in player_in_registry.name:
            found += f"{player_in_registry.name}{{{Colors.white_hex}}}[{player_in_registry.get_id()}] "

    if not found:
        return player.send_error_message("Игроков не найдено!")

    return player.send_notification_message(f"Найдено игроков: {{{Colors.cmd_hex}}}{found}")

@cmd
@Player.using_registry
def donate(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_donation_dialog(player)

@cmd
@Player.using_registry
def report(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_admin_ask_dialog(player)

# TODO:
# Добавить загрузку машин для Freeroam из базы данных
# Добавить новые режимы, постепенно
# Изменить выбор скина на GangWar моде