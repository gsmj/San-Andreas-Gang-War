from pysamp.commands import cmd
from pysamp import send_client_message_to_all, set_world_time
from pysamp.dialog import Dialog
from pysamp.timer import set_timer, kill_timer
from ...player import Player, Dialogs
from ..gang.gang import gangs, gangzone_pool
from ..house.house import houses
from ..utils.data import (
    Colors,
    MonthsConverter,
    ServerMode,
    WeatherIDs,
    convert_seconds,
    VIPData,
    ServerInfo,
)
from ..utils.consts import TIMER_ID_NONE, NO_HOUSE_OWNER
from .cmd_ex import cmd_ex, CommandType
from ..database.database import DataBase
from datetime import datetime as dt
from zoneinfo import ZoneInfo
import random
from ...vehicle import Vehicle
from samp import SPECIAL_ACTION_USEJETPACK, PLAYER_STATE_SPECTATING # type: ignore
from typing import Literal


@cmd_ex(
    cmd(aliases=("menu", "mm", "help", "m")),
    description="Меню игрока"
)
@Player.using_registry
def mn(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_mn_dialog(player)

@cmd_ex(
    cmd,
    description="Статистика игрока"
)
@Player.using_registry
def stats(player: Player, player_id: int = None):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player_id:
        try:
            target_id = int(player_id)

        except:
            return player.send_error_message("Игрок не найден!")

    else:
        target_id = player.id

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    return Dialogs.show_stats_dialog(player, player_id=target_id)

@cmd_ex(
    cmd,
    description="Использование аптечки",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def healme(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

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

@cmd_ex(
    cmd,
    description="Использование маски",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def mask(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    if player.checks.wearing_mask:
        return player.send_error_message("Ваше местоположение уже скрыто!")

    if player.masks == 0:
        return player.send_error_message("У Вас нет масок!")

    if player.is_attached_object_slot_used(2):
        player.remove_attached_object(2)

    player.apply_animation("SHOP", "ROB_Shifty", 4.1, False, False, False, False, 0)
    player.masks -= 1
    player.checks.wearing_mask = True
    player.set_attached_object(2, 19801, 2, offset_x=0.067, offset_y=0.026, offset_z=0.001000, rotation_x=0.30, rotation_y=85.600000, rotation_z=175.400000, scale_x=1.321000, scale_y=1.32700, scale_z=1.257000)
    player.set_color(Colors.mask)
    player.set_chat_bubble("Надевает маску..", Colors.white, 20.0, 5000)
    return player.send_notification_message(f"Ваше местоположение на карте скрыто. Используйте {{{Colors.cmd_hex}}}/maskoff{{{Colors.white_hex}}}, чтобы снять маску.")

@cmd_ex(
    cmd,
    description="Снятие маски",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def maskoff(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    if not player.checks.wearing_mask:
        return player.send_error_message("У Вас нет маски!")

    if player.is_attached_object_slot_used(2):
        player.remove_attached_object(2)

    player.checks.wearing_mask = False
    player.set_color(player.gang.color)
    return player.send_notification_message("Вы сняли маску.")

@cmd_ex(
    cmd(aliases=("changegang", "g")),
    description="Смена банды",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def newgang(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    if player.gang.is_capturing:
        return player.send_error_message("Вы не можете сменить банду сейчас!")

    if player.checks.wearing_mask:
        player.checks.wearing_mask = False
        player.set_color(player.gang.color)

    if player.is_attached_object_slot_used(2):
        player.remove_attached_object(2)

    player.heals = 0
    player.masks = 0
    player.reset_weapons()
    return Dialogs.show_command_gang_choice_dialog(player)

@cmd_ex(
    cmd,
    description="Случайный скин",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def randomskin(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    if player.gang.is_capturing:
        return player.send_error_message("Вы не можете сменить скин сейчас!")

    if player.get_virtual_world() != ServerMode.gangwar_world:
        return player.send_error_message("Вы можете изменить скин только в доме!")

    player.set_skin_ex(random.choice(player.gang.skins))
    return player.send_notification_message("Ваш скин был изменён.")

@cmd_ex(
    cmd,
    description="Новый скин",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def changeskin(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    if player.gang.is_capturing:
        return player.send_error_message("Вы не можете сменить скин сейчас!")

    if player.get_virtual_world() != ServerMode.gangwar_world:
        return player.send_error_message("Вы можете изменить скин только в доме!")

    return Dialogs.show_skin_gang_dialog(player)

@cmd_ex(
    cmd,
    description="Точное время",
)
@Player.using_registry
def time(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(5.0):
        return player.send_error_message("Не флудите!")

    current_time = dt.now(tz=ZoneInfo("Europe/Moscow")).strftime("%H:%M")
    current_date = dt.now(tz=ZoneInfo("Europe/Moscow"))
    player.apply_animation("COP_AMBIENT", "Coplook_watch", 4.1, False, False, False, False, 0)
    return player.game_text(f"{Colors.game_text_time_date}{current_date.day} {MonthsConverter.months[current_date.month]}~n~{Colors.game_text_time_time}{current_time}", 3000, 1)

@cmd_ex(
    cmd,
    description="Чат банды",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def f(player: Player, *message: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    if player.checks.muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /f message")

    for player_in_registry in Player._registry.values():
        if player.gang_id == player_in_registry.gang_id:
            key, value = player.get_gang_rang()
            player_in_registry.send_client_message(player.gang.color, f"[F] {value} {player.get_name()}: {message}")

    return

@cmd_ex(
    cmd,
    description="Общий чат",
)
@Player.using_registry
def o(player: Player, *message: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.checks.muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /o message")

    return send_client_message_to_all(player.color, f"{player.get_name()}({player.get_id()}):{{{Colors.white_hex}}} {message}")

@cmd_ex(
    cmd,
    description="Информация о VIP статусах",
    mode=CommandType.vip_type
)
@Player.using_registry
def vipinfo(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    return Dialog.create(
        0,
        "Информация о VIP статусах",
        (
            f"{{{Colors.bronze_hex}}}BRONZE VIP{{{Colors.dialog_hex}}}:\n"
            f"{{{Colors.cmd_hex}}}/vc\t\t{{{Colors.dialog_hex}}}VIP чат\n"
            f"{{{Colors.cmd_hex}}}/rclist\t\t{{{Colors.dialog_hex}}}Переливающийся цвет игрока\n"
            f"{{{Colors.cmd_hex}}}/jp\t\t{{{Colors.dialog_hex}}}Покупка джетпака\n\n"
            f"{{{Colors.silver_hex}}}SILVER VIP{{{Colors.dialog_hex}}}:\n"
            f"{{{Colors.cmd_hex}}}/vbuy\t\t{{{Colors.dialog_hex}}}VIP транспорт\n\n"
            f"{{{Colors.gold_hex}}}GOLD VIP{{{Colors.dialog_hex}}}:\n"
            "Все возможности других статусов\n"
            "Телепорт по метке"
        ),
        "Закрыть",
        ""
    ).show(player)

@cmd_ex(
    cmd,
    description="VIP чат",
    mode=CommandType.vip_type
)
@Player.using_registry
def vc(player: Player, *message: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.checks.muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /v message")

    vip_status = VIPData.names[player.vip.level]
    vip_status_color = VIPData.colors[player.vip.level]
    for player_in_registry in Player._registry.values():
        if player_in_registry.vip.level != -1:
            player_in_registry.send_notification_message(f"{{{Colors.vip_hex}}}[VIP] {{{vip_status_color}}}[{vip_status}]{{{Colors.white_hex}}} {player.get_name()}[{player.id}]: {message}")

@cmd_ex(
    cmd,
    description="VIP транспорт",
    mode=CommandType.vip_type
)
@Player.using_registry
def vbuy(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.vip.level < 1:
        return player.send_error_message(f"Вам необходимо приобрести {{{Colors.silver_hex}}}SILVER VIP{{{Colors.red_hex}}} и выше!")

    return Dialogs.show_vbuy_dialog(player)

@cmd_ex(
    cmd,
    description="Переливающийся цвет игрока",
    mode=CommandType.vip_type
)
@Player.using_registry
def rclist(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.vip.is_random_clist_enabled:
        player.vip.is_random_clist_enabled = False
        kill_timer(player.vip.random_clist_timer_id)
        if player.color != 0:
            player.set_color(player.color)
        else:
            player.set_random_color_ex()

        return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}выключили{{{Colors.white_hex}}} переливающийся цвет игрока.")

    player.vip.is_random_clist_enabled = True
    player.vip.random_clist_timer_id = set_timer(player.set_rainbow_color, 1000, True)
    return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}включили{{{Colors.white_hex}}} переливающийся цвет игрока.")

@cmd_ex(
    cmd,
    description="Покупка Jetpack",
    mode=CommandType.vip_type
)
@Player.using_registry
def jp(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.money - 10000 < 0:
        return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{10000 - player.money}${{{Colors.red_hex}}}!")

    player.set_special_action(SPECIAL_ACTION_USEJETPACK)
    return player.send_notification_message(f"Вы купили {{{Colors.cmd_hex}}}Jetpack{{{Colors.white_hex}}}.")


@cmd_ex(
    cmd,
    description="Онлайн в банде",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def members(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    members_dict = {}
    for player_in_registry in Player._registry.values():
        if player.gang_id == player_in_registry.gang_id:
            members_dict[player_in_registry.get_name()] = player_in_registry.kills

    sorted_members = dict(sorted(members_dict.items(), key=lambda item: item[1], reverse=True))
    members_string = ""
    for key, value in sorted_members.items():
        members_string += f"Игрок: {key}\t\t\tУбийств: {value}\n"

    return Dialog.create(0, f"Онлайн в банде {player.gang.gang_name}", f"{members_string}", "Закрыть", "").show(player)

@cmd_ex(
    cmd,
    description="Список территорий",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def gangzones(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    player.send_notification_message("Вы можете выбрать территорию, нажав ЛКМ/Enter.")
    return Dialogs.show_gangzones_dialog_page_one(player)

@cmd_ex(
    cmd,
    description="Список команд",
)
@Player.using_registry
def cmds(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_commands_list_dialog(player)

@cmd_ex(
    cmd,
    description="Изменение погоды",
)
@Player.using_registry
def weather(player: Player, weather_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if int(weather_id) not in WeatherIDs.weather:
        return player.send_error_message("Допустимый диапазон погоды: 0 - 22!")

    player.set_weather(int(weather_id))
    return player.send_notification_message(f"Погода была изменена на {weather_id} ID.")

@cmd_ex(
    cmd(aliases=("capt", "c")),
    description="Захват территории",
    mode=CommandType.gangwar_type
)
@Player.using_registry
def capture(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    for gz_id, gangzone in gangzone_pool.items():
        if player.is_in_area(gangzone.min_x, gangzone.min_y, gangzone.max_x, gangzone.max_y):
            break

    gangzone = gangzone_pool[gz_id]
    if player.gang_id == gangzone.gang_id:
        return player.send_error_message("Вы не можете атаковать свою территорию!")

    if gangzone.capture_cooldown != 0:
        hours, minutes, seconds = convert_seconds(gangzone.capture_cooldown)
        return player.send_error_message(f"Захватить территорию можно будет только через {{{Colors.cmd_hex}}}{hours}{{{Colors.red_hex}}} часов, {{{Colors.cmd_hex}}}{minutes}{{{Colors.red_hex}}} минут, {{{Colors.cmd_hex}}}{seconds}{{{Colors.red_hex}}} секунд!")

    total_captures = 0
    for i in gangzone_pool.values():
        if i.is_capture:
            total_captures += 1

    if total_captures == ServerInfo.CAPTURE_LIMIT:
        return player.send_error_message("В данный момент на сервере достигнут лимит захвата!")

    if player.gang.is_capturing or gangs[gangzone.gang_id].is_capturing:
        return player.send_error_message("Одна из банд уже ведёт захват территории!")

    return Dialogs.show_start_capture_dialog(player, player.gang_id, gangzone.gang_id, gangzone.id)

# @cmd
# @Player.using_registry
# def gps(player: Player):
#     player.kick_if_not_logged_or_jailed()
#     if not player.check_cooldown(1.5):
#         return player.send_error_message("Не флудите!")

#     return player.disable_checkpoint()

@cmd_ex(
    cmd,
    description="Список разработчиков",
)
@Player.using_registry
def credits(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_credits_dialog(player)

@cmd_ex(
    cmd(aliases=("changemode", "sm")),
    description="Список режима",
)
@Player.using_registry
def setmode(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.is_in_any_vehicle():
        return player.send_error_message("Выйдите из транспорта!")

    if player.gang.is_capturing:
        return player.send_error_message("Вы не можете сменить режим во время войны за территорию")

    if player.get_interior() != 0:
        return player.send_error_message("Вы не можете сменить режим находясь в интерьере!")

    return Dialogs.show_select_mode_dialog(player)

@cmd_ex(
    cmd,
    description="Закрытие транспорта",
)
@Player.using_registry
def lock(player: Player):
    player.kick_if_not_logged_or_jailed()
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

@cmd_ex(
    cmd,
    description="Отправка SMS",
)
@Player.using_registry
def sms(player: Player, player_id: int, *message: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.checks.muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /sms message")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    player.play_sound(1052, x=0.0, y=0.0, z=0.0)
    target.play_sound(1052, x=0.0, y=0.0, z=0.0)
    player.send_client_message(Colors.sms, f"[SMS] {message}. Получатель: {target.get_name()}[{target.id}].")
    return target.send_client_message(Colors.sms, f"[SMS] {message}. Отправитель: {player.get_name()}[{player.id}].")

@cmd_ex(
    cmd,
    description="Поиск игрока по нику",
)
@Player.using_registry
def id(player: Player, nickname: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    found = ""
    for player_in_registry in Player._registry.values():
        if nickname in player_in_registry.name:
            found += f"{player_in_registry.name}[{player_in_registry.id}] "

    if not found:
        return player.send_error_message("Игроков не найдено!")

    return player.send_notification_message(f"Найдено игроков: {{{Colors.cmd_hex}}}{found}")

@cmd_ex(
    cmd,
    description="Донат",
)
@Player.using_registry
def donate(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_donation_dialog(player)

@cmd_ex(
    cmd,
    description="Отправка жалобы/вопроса",
)
@Player.using_registry
def report(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    return Dialogs.show_admin_ask_dialog(player)


@cmd_ex(
    cmd(aliases=("guns", "weapon", "w")),
    description="Покупка оружия",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def weapons(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    return Dialogs.show_weapons_dialog(player)

@cmd
@Player.using_registry
def ahelp(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    return Dialog.create(
        5,
        "Список команд для администрации",
        (
            "Команда\tУровень\tОписание\n"
            f"{{{Colors.cmd_hex}}}/spawn\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Заспавнить себя/игрока\n"
            f"{{{Colors.cmd_hex}}}/ahelp\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Список команд для администрации\n"
            f"{{{Colors.cmd_hex}}}/pm\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Ответ на /report\n"
            f"{{{Colors.cmd_hex}}}/admins\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Список администраторов в сети\n"
            f"{{{Colors.cmd_hex}}}/aad\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Сообщение от имени администратора\n"
            f"{{{Colors.cmd_hex}}}/spec\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Слежка за игроком\n"
            f"{{{Colors.cmd_hex}}}/specoff\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Отключение слежки за игроком\n"
            f"{{{Colors.cmd_hex}}}/jail\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Посадить игрока в деморган\n"
            f"{{{Colors.cmd_hex}}}/unjail\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Выпустить игрока из деморгана\n"
            f"{{{Colors.cmd_hex}}}/mute\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Выдача мута игроку\n"
            f"{{{Colors.cmd_hex}}}/unmute\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Снятие мута с игрока\n"
            f"{{{Colors.cmd_hex}}}/hp\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Восстановление HP до 100\n"
            f"{{{Colors.cmd_hex}}}/goto\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Перемещение к игроку\n"
            f"{{{Colors.cmd_hex}}}/gethere\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Перемещение игрока к себе\n"
            f"{{{Colors.cmd_hex}}}/slap\t{{{Colors.red_hex}}}3\t{{{Colors.dialog_hex}}}Подбросить игрока\n"
            f"{{{Colors.cmd_hex}}}/freeze\t{{{Colors.red_hex}}}3\t{{{Colors.dialog_hex}}}Заморозить игрока\n"
            f"{{{Colors.cmd_hex}}}/unfreeze\t{{{Colors.red_hex}}}3\t{{{Colors.dialog_hex}}}Разморозить игрока\n"
            f"{{{Colors.cmd_hex}}}/ban\t{{{Colors.red_hex}}}3\t{{{Colors.dialog_hex}}}Забанить игрока\n"
            f"{{{Colors.cmd_hex}}}/unban\t{{{Colors.red_hex}}}3\t{{{Colors.dialog_hex}}}Разбанить игрока\n"
            f"{{{Colors.cmd_hex}}}/settime\t{{{Colors.red_hex}}}4\t{{{Colors.dialog_hex}}}Изменение времени\n"
            f"{{{Colors.cmd_hex}}}/getip\t{{{Colors.red_hex}}}4\t{{{Colors.dialog_hex}}}Получение IP-адреса игрока\n"
            f"{{{Colors.cmd_hex}}}/givegun\t{{{Colors.red_hex}}}4\t{{{Colors.dialog_hex}}}Выдача оружия игроку\n"
            f"{{{Colors.cmd_hex}}}/sethp\t{{{Colors.red_hex}}}4\t{{{Colors.dialog_hex}}}Изменение HP игрока\n"
            f"{{{Colors.cmd_hex}}}/amusic\t{{{Colors.red_hex}}}5\t{{{Colors.dialog_hex}}}Включение аудио для игрока\n"
            f"{{{Colors.cmd_hex}}}/stopamusic\t{{{Colors.red_hex}}}5\t{{{Colors.dialog_hex}}}Отключение аудио для игрока\n"
            f"{{{Colors.cmd_hex}}}/deleteplayer\t{{{Colors.red_hex}}}6\t{{{Colors.dialog_hex}}}Удаление аккаунта\n"
            f"{{{Colors.cmd_hex}}}/setvip\t{{{Colors.red_hex}}}6\t{{{Colors.dialog_hex}}}Изменение VIP статуса для игрока\n"
            f"{{{Colors.cmd_hex}}}/setgangzone\t{{{Colors.red_hex}}}6\t{{{Colors.dialog_hex}}}Изменение владельца территории\n"
            f"{{{Colors.cmd_hex}}}/spawnveh\t{{{Colors.red_hex}}}6\t{{{Colors.dialog_hex}}}Спавн транспорта\n"
            f"{{{Colors.cmd_hex}}}/positions\t{{{Colors.red_hex}}}6\t{{{Colors.dialog_hex}}}Меню позиций Администратора\n"
            f"{{{Colors.cmd_hex}}}/createhouse\t{{{Colors.red_hex}}}6\t{{{Colors.dialog_hex}}}Создание дома\n"
        ),
        "Закрыть",
        ""
    ).show(player)

@cmd
@Player.using_registry
def spawn(player: Player, player_id: int = None):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    if not player_id:
        return player.spawn()

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    return target.spawn()

@cmd
@Player.using_registry
def pm(player: Player, player_id: int, *message: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /pm player_id message")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    player.play_sound(1052, x=0.0, y=0.0, z=0.0)
    target.play_sound(1052, x=0.0, y=0.0, z=0.0)
    target.send_client_message(Colors.admin_pm, f"[REPORT] Ответ от {player.name}[{player.id}]: {message}.")
    return player.send_client_message(Colors.admin_pm, f"[REPORT] Ваш ответ: {message}.")

@cmd_ex(
    cmd,
    description="Список администраторов в сети",
)
@Player.using_registry
def admins(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    admins_str = ""
    for player_in_registry in Player._registry.values():
        if player_in_registry.admin.level != 0:
            admins_str += f"{player_in_registry.name}[{player_in_registry.id}] - {player_in_registry.admin.level} "

    return player.send_notification_message(f"Список администраторов: {{{Colors.cmd_hex}}}{admins_str}")

@cmd
@Player.using_registry
def aad(player: Player, *message: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /add message")

    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}[{player.id}]: {message}.")

@cmd
@Player.using_registry
def spec(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == target_id:
        return player.send_error_message("Вы не можете наблюдать за собой!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    if player.get_state() == PLAYER_STATE_SPECTATING:
        return player.send_error_message("Вы уже за кем-то наблюдаете!")

    if target.is_in_any_vehicle():
        veh = Vehicle.from_registry_native(target.get_vehicle_id())
        player.spectate_vehicle(veh)

    else:
        player.spectate_player(target)

    player.toggle_spectating(True)
    player.set_interior(target.get_interior())
    player.set_virtual_world(target.mode)
    return player.send_notification_message(f"Вы наблюдаете за игроком: {{{Colors.cmd_hex}}}{target.name}{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def specoff(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    if not player.get_state() == PLAYER_STATE_SPECTATING:
        return player.send_error_message("Вы не ведёте наблюдение!")

    player.toggle_spectating(False)
    return player.send_notification_message("Наблюдение прекращено.")

@cmd
@Player.using_registry
def jail(player: Player, player_id: int, minutes: int, *reason: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    try:
        target_time = int(minutes)

    except:
        return player.send_error_message("Укажите время в минутах!")

    reason = " ".join(reason)
    if len(reason) == 0:
        return player.send_error_message("Использование команды: /jail player_id minutes [reason]")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    if target.checks.jailed:
        player.send_error_message("Игрок уже в деморгане!")

    target.checks.jailed = True
    target.time.jail = target_time
    target.set_mode(ServerMode.jail_world)
    target.enable_jail_mode()
    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}[{player.id}] посадил игрока {target.name}[{target.id}] в деморган на {minutes} минут. Причина: {reason}.")

@cmd
@Player.using_registry
def unjail(player: Player, player_id: int):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    if not target.checks.jailed:
        player.send_error_message("Игрок не в деморгане!")

    target.send_notification_message(f"Администратор {{{Colors.cmd_hex}}}{player.name}[{player.id}]{{{Colors.white_hex}}} выпустил Вас выпустили из деморгана.")
    kill_timer(target.timers.jail_id)
    target.checks.jailed = False
    target.time.jail = 0
    target.timers.jail_id = TIMER_ID_NONE
    target.set_mode(ServerMode.freeroam_world)
    target.enable_skin_selector()
    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}[{player.id}] выпустил игрока {target.name}[{target.id}] из деморгана.")

@cmd
@Player.using_registry
def mute(player: Player, player_id: int, minutes: int, *reason: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    try:
        target_time = int(minutes)

    except:
        return player.send_error_message("Укажите время в минутах!")

    reason = " ".join(reason)
    if len(reason) == 0:
        return player.send_error_message("Использование команды: /mute player_id minutes [reason]")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    if target.checks.muted:
        player.send_error_message("Игрок уже в муте!")

    target.checks.muted = True
    target.time.mute = target_time
    target.timers.mute_id = set_timer(target.mute_timer, target_time * 60000, False)
    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}[{player.id}] выдал мут игроку {target.name}[{target.id}] на {minutes} минут. Причина: {reason}.")

@cmd
@Player.using_registry
def unmute(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    if not target.checks.muted:
        player.send_error_message("Игрок не в муте!")

    target.send_notification_message(f"Администратор {{{Colors.cmd_hex}}}{player.name}[{player.id}]{{{Colors.white_hex}}} снял с Вас мут.")
    kill_timer(target.timers.mute_id)
    target.checks.muted = False
    target.time.mute = 0
    target.timers.mute_id = TIMER_ID_NONE
    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}[{player.id}] снял мут с игрока {target.name}[{target.id}].")

@cmd_ex(
    cmd,
    description="Восстановление HP",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def heal(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(120.0):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    player.set_health(100.0)
    return player.send_notification_message(f"Значение HP восстановлено до {{{Colors.cmd_hex}}}100{{{Colors.white_hex}}}.")

@cmd_ex(
    cmd,
    description="Восстановление AR",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def armour(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(120.0):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    player.set_armour(100.0)
    return player.send_notification_message(f"Значение AR восстановлено до {{{Colors.cmd_hex}}}100{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def goto(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    x, y, z = target.get_pos()
    player.set_pos(x+5.0, y+5.0, z)
    player.set_interior(target.get_interior())
    player.set_virtual_world(target.mode)
    return player.send_notification_message(f"Вы были перемещены к игроку {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def gethere(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    x, y, z = player.get_pos()
    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.set_pos(x+5.0, y+5.0, z)
    target.set_interior(player.get_interior())
    target.set_virtual_world(player.mode)
    return player.send_notification_message(f"Вы переместили игрока {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def slap(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(3):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    x, y, z = target.get_pos()
    target.set_pos(x, y, z+5.0)
    return player.send_notification_message(f"Вы подбросили игрока {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def freeze(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(3):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.toggle_controllable(False)
    return player.send_notification_message(f"Вы заморозили игрока {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def unfreeze(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(3):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.toggle_controllable(True)
    return player.send_notification_message(f"Вы разморозили игрока {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def ban(player: Player, player_id: int, *reason: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(3):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    reason = " ".join(reason)
    if len(reason) == 0:
        return player.send_error_message("Использование команды: /ban player_id [reason]")

    if player.id == target_id:
        return player.send_error_message("Вы не можете указать себя!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.checks.banned = True
    target.ban_from_server(reason)
    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}[{player.id}] забанил игрока {target.name}[{target.id}]. Причина: {reason}.")

@cmd
@Player.using_registry
def unban(player: Player, player_name: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(3):
        return player.send_error_message("Вам недоступна эта команда!")

    target = DataBase.get_player_name(player_name)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    if not target.checks.banned:
        return player.send_error_message("Игрок не находится в бане!")

    DataBase.save_player_name(player_name, is_banned=False)
    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}[{player.id}] разбанил игрока {target.name}[{target.id}].")

@cmd
@Player.using_registry
def settime(player: Player, hour: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(4):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_hour = int(hour)

    except:
        return player.send_error_message("Укажите время!")

    set_world_time(target_hour)
    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}[{player.id}] изменил время на {hour} часов.")

@cmd
@Player.using_registry
def getip(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(4):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    return player.send_notification_message(f"IP игрока {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}} - {{{Colors.cmd_hex}}}{target.get_ip()}{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def givegun(player: Player, player_id: int, weapon_id: int, ammo: int = 100):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(4):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    try:
        target_weapon_id = int(weapon_id)

    except:
        return player.send_error_message("Оружие не найдено!")

    try:
        target_ammo = int(ammo)

    except:
        return player.send_error_message("Укажите количество патронов!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.give_weapon(target_weapon_id, target_ammo)
    target.send_notification_message(f"Администратор {{{Colors.cmd_hex}}}{player.name}[{player.id}]{{{Colors.white_hex}}} выдал Вам оружие.")
    return player.send_notification_message(f"Вы выдали оружие игроку {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def sethp(player: Player, player_id: int, health: float):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(4):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    try:
        target_health = float(health)

    except:
        return player.send_error_message("Укажите количество HP!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.set_health(target_health)
    target.send_notification_message(f"Администратор {{{Colors.cmd_hex}}}{player.name}[{player.id}]{{{Colors.white_hex}}} изменил Вам значение HP.")
    return player.send_notification_message(f"Вы изменили значение HP игроку {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def amusic(player: Player, player_id: int, url: str, distance: float = 5.0):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(5):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    try:
        target_distance = float(distance)

    except:
        return player.send_error_message("Укажите дистанцию!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.play_audio_stream(url, *target.get_pos(), distance=target_distance)
    return player.send_notification_message(f"Вы включили аудио для игрока {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def stopamusic(player: Player, player_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(5):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.stop_audio_stream()
    return player.send_notification_message(f"Вы выключили аудио для игрока {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def deleteplayer(player: Player, player_name: str):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(6):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_name = str(player_name)

    except:
        return player.send_error_message("Игрок не найден!")

    player_db = DataBase.get_player_name(target_name)
    if not player_db:
        return player.send_error_message("Игрок не найден!")

    DataBase.save_player_name(target_name, is_banned=True)
    return player.send_notification_message(f"Вы удалили аккаунт игрока {{{Colors.cmd_hex}}}{target_name}{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def setvip(player: Player, player_id: int, level: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(6):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    try:
        target_level = int(level)

    except:
        return player.send_error_message("Укажите уровень VIP!")

    if target_level not in (1, 2, 3):
        return player.send_error_message("Укажите уровень от 1 до 3")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    target.vip.level = target_level - 1
    target.send_notification_message(
        f"Администратор {{{Colors.cmd_hex}}}{player.name}[{player.id}]{{{Colors.white_hex}}} изенил Ваш уровень VIP на {{{VIPData.colors[target.vip.level]}}}{VIPData.names[target.vip.level]}{{{Colors.white_hex}}}."
    )
    send_client_message_to_all(Colors.ad, f"{target.name}[{target.id}] получил {{{VIPData.colors[target.vip.level]}}}{VIPData.names[target.vip.level]} VIP{{{Colors.ad_hex}}}!")
    return player.send_notification_message(f"Вы изменили значение VIP игроку {{{Colors.cmd_hex}}}{target.name}[{target.id}]{{{Colors.white_hex}}} на {{{VIPData.colors[target.vip.level]}}}{VIPData.names[target.vip.level]}{{{Colors.white_hex}}}.")

@cmd
@Player.using_registry
def setgangzone(player: Player, gangzone_id: int, gang_id: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(6):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_gangzone = int(gangzone_id)
        gangzone = gangzone_pool[target_gangzone]

    except:
        return player.send_error_message("Гангзона не найдена (используйте /gangzones)!")

    try:
        target_gang = int(gang_id)

    except:
        player.send_error_message(f"Укажите ID!")

    if not target_gang in gangs.keys():
        player.send_error_message(f"Банда не найдена!")
        gangs_str = ""
        for key, value in gangs.values():
            gangs_str += f"ID: {key} - Name: {value.gang_name}"
            player.send_error_message(f"{gangs_str}!")
        return

    gangzone.gang_id = target_gang
    gangzone.color = gangs[target_gang].color
    gangzone.gang_atk_id = 0
    gangzone.gang_def_id = 0
    gangzone.gang_atk_score = 0
    gangzone.gang_def_score = 0
    gangzone.capture_cooldown = 120
    gangzone.capture_time = 0
    gangzone.is_capture = False
    for player_gw in Player._registry.values():
        if player_gw.mode == ServerMode.gangwar_world:
            player_gw.reload_gangzones_for_player()

    return player.send_notification_message(f"Гангзона обновлена!")

@cmd
@Player.using_registry
def spawnveh(player: Player, vehicle_id: int, color_one: int, color_two: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(6):
        return player.send_error_message("Вам недоступна эта команда!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    try:
        target_vehicle_id = int(vehicle_id)

    except:
        player.send_error_message(f"Укажите ID!")

    player.remove_unused_vehicle(ServerMode.freeroam_world)
    player_veh = Vehicle.create(
        target_vehicle_id,
        *player.get_pos(),
        player.get_facing_angle(),
        color_one,
        color_two,
        -1,
        player.mode
    )
    player_veh.set_info(owner=player.get_name())
    player.update_vehicle_inst(player_veh)
    player.put_in_vehicle(player.vehicle.inst.id, 0)

@cmd
@Player.using_registry
def positions(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(6):
        return player.send_error_message("Вам недоступна эта команда!")

    return Dialogs.show_positions_dialog(player)

@cmd_ex(
    cmd(aliases=("veh", "vehicle", "v")),
    description="Покупка транспорта",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def vehicles(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    return Dialogs.show_vehicles_dialog(player)

@cmd_ex(
    cmd,
    description="Передача денег игроку",
)
@Player.using_registry
def pay(player: Player, player_id: int, amount: int):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    try:
        target_amount = int(amount)

    except:
        return player.send_error_message("Укажите количество!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок не найден!")

    if target_amount < 0:
        return player.send_error_message("Укажите число больше 0!")

    if player.money - target_amount < 0:
        return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{target_amount - player.money}${{{Colors.red_hex}}}!")

    if player.distance_from_point(*target.get_pos) > 3.0:
        return player.send_error_message("Игрок слишком далеко!")

    player.set_money_ex(target_amount, increase=False)
    target.set_money_ex(target_amount)
    target.send_notification_message(f"Игрок {{{Colors.cmd_hex}}}{player.name}[{player.id}]{{{Colors.white_hex}}} передал Вам {{{Colors.green_hex}}}{amount}${{{Colors.white_hex}}}.")
    return player.send_notification_message(f"Вы передали {{{Colors.green_hex}}}{target_amount}${{{Colors.white_hex}}} игроку {{{Colors.cmd_hex}}}{player.name}[{player.id}]{{{Colors.white_hex}}}.")

@cmd_ex(
    cmd,
    description="Покупка Elegy",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def elegy(player: Player, color_one: int, color_two: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if player.money - 5000 < 0:
        return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{5000 - player.money}${{{Colors.red_hex}}}!")

    try:
        target_color_one = int(color_one)

    except:
        target_color_one = 1

    try:
        target_color_two = int(color_two)

    except:
        target_color_two = 1

    player.remove_unused_vehicle(ServerMode.freeroam_world)
    player_veh = Vehicle.create(
        562,
        *player.get_pos(),
        player.get_facing_angle(),
        target_color_one,
        target_color_two,
        -1,
        player.mode
    )
    player_veh.set_info(owner=player.get_name())
    player.update_vehicle_inst(player_veh)
    player.put_in_vehicle(player.vehicle.inst.id, 0)

@cmd_ex(
    cmd,
    description="Покупка Infernus",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def infernus(player: Player, color_one: int, color_two: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if player.money - 5000 < 0:
        return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{5000 - player.money}${{{Colors.red_hex}}}!")

    try:
        target_color_one = int(color_one)

    except:
        target_color_one = 1

    try:
        target_color_two = int(color_two)

    except:
        target_color_two = 1

    player.remove_unused_vehicle(ServerMode.freeroam_world)
    player_veh = Vehicle.create(
        411,
        *player.get_pos(),
        player.get_facing_angle(),
        target_color_one,
        target_color_two,
        -1,
        player.mode
    )
    player_veh.set_info(owner=player.get_name())
    player.update_vehicle_inst(player_veh)
    player.put_in_vehicle(player.vehicle.inst.id, 0)

@cmd_ex(
    cmd,
    description="Покупка Bullet",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def bullet(player: Player, color_one: int, color_two: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if player.money - 5000 < 0:
        return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{5000 - player.money}${{{Colors.red_hex}}}!")

    try:
        target_color_one = int(color_one)

    except:
        target_color_one = 1

    try:
        target_color_two = int(color_two)

    except:
        target_color_two = 1

    player.remove_unused_vehicle(ServerMode.freeroam_world)
    player_veh = Vehicle.create(
        541,
        *player.get_pos(),
        player.get_facing_angle(),
        target_color_one,
        target_color_two,
        -1,
        player.mode
    )
    player_veh.set_info(owner=player.get_name())
    player.update_vehicle_inst(player_veh)
    player.put_in_vehicle(player.vehicle.inst.id, 0)

@cmd_ex(
    cmd,
    description="Покупка Sultan",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def sultan(player: Player, color_one: int, color_two: int):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if player.money - 5000 < 0:
        return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{5000 - player.money}${{{Colors.red_hex}}}!")

    try:
        target_color_one = int(color_one)

    except:
        target_color_one = 1

    try:
        target_color_two = int(color_two)

    except:
        target_color_two = 1

    player.remove_unused_vehicle(ServerMode.freeroam_world)
    player_veh = Vehicle.create(
        560,
        *player.get_pos(),
        player.get_facing_angle(),
        target_color_one,
        target_color_two,
        -1,
        player.mode
    )
    player_veh.set_info(owner=player.get_name())
    player.update_vehicle_inst(player_veh)
    player.put_in_vehicle(player.vehicle.inst.id, 0)

@cmd_ex(
    cmd(aliases=("tp", "t")),
    description="Телепорт",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def teleport(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    return Dialogs.show_teleports_dialog(player)

@cmd_ex(
    cmd,
    description="Перевернуть транспорт",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def flip(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if not player.is_in_any_vehicle():
        return player.send_error_message("Вы должны находиться в транспорте!")

    veh = Vehicle.from_registry_native(player.vehicle.id)
    x, y, z = veh.get_position()
    angle = veh.get_z_angle()
    veh.set_position(x, y, z+1.5)
    veh.set_z_angle(angle)
    return player.send_notification_message("Транспорт был перевёрнут.")

@cmd_ex(
    cmd(aliases=("vt", "tune")),
    description="Тюнинг транспорта",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def tuning(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if not player.is_in_any_vehicle():
        return player.send_error_message("Вы должны находиться в транспорте!")

    return Dialogs.show_tuning_dialog(player)

@cmd_ex(
    cmd,
    description="Изменение клиста",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def clist(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    return Dialogs.show_clist_dialog(player)

@cmd_ex(
    cmd,
    description="Создание дома",
    mode=CommandType.admin_type
)
@Player.using_registry
def createhouse(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(6):
        return player.send_error_message("Вам недоступна эта команда!")

    return Dialogs.show_house_create_dialog(player)

@cmd_ex(
    cmd,
    description="Покупка дома",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def buyhouse(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    if not player.checks.in_house:
        return player.send_error_message("Вы не находитесь в доме!")

    if player.house.owner != NO_HOUSE_OWNER:
        return player.send_error_message("Этот дом уже занят!")

    if (player.money - player.house.price) < 0:
        return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{player.house.price - player.money}{{{Colors.white_hex}}}!")

    player.money -= player.house.price
    player.settings.spawn_in_house = True
    player.house.set_owner(player.name)
    return player.send_notification_message(f"Вы купили дом {{{Colors.cmd_hex}}}№{player.house.uid}{{{Colors.white_hex}}}!")

@cmd_ex(
    cmd,
    description="Меню дома",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def house(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.gangwar_world]):
        return

    if not player.checks.in_house:
        return player.send_error_message("Вы не находитесь в доме!")

    if not player.house:
        return player.send_error_message("У Вас нет дома!")

    return Dialogs.show_house_menu_dialog(player)

@cmd_ex(
    cmd,
    description="Поздороваться со всеми игроками",
    mode=CommandType.all_types
)
@Player.using_registry
def qq(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.checks.muted:
        return player.send_error_message("Доступ в чат ограничен!")

    return send_client_message_to_all(Colors.cmd, f"{player.name}[{player.id}] приветствует всех игроков!")

@cmd_ex(
    cmd,
    description="Попрощаться со всеми игроками",
    mode=CommandType.all_types
)
@Player.using_registry
def bb(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.checks.muted:
        return player.send_error_message("Доступ в чат ограничен!")

    return send_client_message_to_all(Colors.cmd, f"{player.name}[{player.id}] прощается со всеми игроками!")

@cmd_ex(
    cmd,
    description="Отладочная информация об игроке",
    mode=CommandType.admin_type
)
@Player.using_registry
def pdata(player: Player, player_id: int):
    if not player.admin.check_command_access(7):
        return

    player_ = Player.from_registry_native(int(player_id))
    content = ""
    for attr, value in vars(player_).items():
        content += f"{attr}: {value}\n"

    return Dialog.create(
        0,
        "Отладочная информация об игроке",
        content,
        "Закрыть",
        ""
    ).show(player)

@cmd_ex(
    cmd(use_function_name=False, aliases="class"),
    description="Выбор класса",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def class_(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if player.is_in_any_vehicle():
        return player.send_error_message("Выйдите из транспорта!")

    if player.get_interior() != 0:
        return player.send_error_message("Вы не можете сменить режим находясь в интерьере!")

    player.checks.selected_skin = False
    player.force_class_selection()
    player.toggle_spectating(True)
    player.toggle_spectating(False)
    return player.send_notification_message("Выберите скин.")

@cmd_ex(
    cmd,
    description="Меню фракции",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def squad(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if not player.squad:
        return player.send_error_message("У Вас нет фракции!")

@cmd_ex(
    cmd,
    description="Создание фракции",
    mode=CommandType.freeroam_type
)
@Player.using_registry
def createsquad(player: Player):
    player.kick_if_not_logged_or_jailed()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerMode.freeroam_world]):
        return

    if player.squad:
        return player.send_error_message("У Вас уже есть фракция!")

    return Dialogs.show_squad_create_dialog(player)


@cmd_ex(
    cmd,
    description="Запись в кэш игрока",
    mode=CommandType.admin_type
)
@Player.using_registry
def pcache(player: Player, player_id: int, key: str, value: str):
    if not player.admin.check_command_access(7):
        return

    player_ = Player.from_registry_native(int(player_id))
    player_.cache[key] = value
    return player.send_notification_message("Кэш обновлён!")

@cmd_ex(
    cmd,
    description="Отладочная информация о домах",
    mode=CommandType.admin_type
)
@Player.using_registry
def hdata(player: Player):
    if not player.admin.check_command_access(7):
        return

    content = ""
    for house in houses.values():
        content += f"House: {house[0]} | Pickup: {house[1]}\n"

    Dialog.create(
        0,
        "Отладочная информация о домах",
        content,
        "Закрыть",
        ""
    ).show(player)
    return player.send_notification_message(f"Всего домов: {len(houses)}")

@cmd_ex(
    cmd,
    description="Отладочная информация о гангзонах",
    mode=CommandType.admin_type
)
@Player.using_registry
def gdata(player: Player):
    if not player.admin.check_command_access(7):
        return

    content = ""
    for gangzone in gangzone_pool.values():
        content += f"{gangzone}\n"

    Dialog.create(
        0,
        "Отладочная информация о гангзонах",
        content,
        "Закрыть",
        ""
    ).show(player)
    return player.send_notification_message(f"Всего гангзон: {len(gangzone_pool)}")