from pysamp.commands import cmd
from pysamp import send_client_message_to_all
from pysamp.dialog import Dialog
from pysamp.timer import set_timer, kill_timer
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
from samp import SPECIAL_ACTION_USEJETPACK, PLAYER_STATE_SPECTATING # type: ignore

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
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
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

@cmd
@Player.using_registry
def mask(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

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
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

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
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

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
def randomskin(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

    if player.gang.is_capturing:
        return player.send_error_message("Вы не можете сменить скин сейчас!")

    if player.get_virtual_world() != ServerWorldIDs.gangwar_world:
        return player.send_error_message("Вы можете изменить скин только в доме!")

    player.set_skin_ex(random.choice(player.gang.skins))
    return player.send_notification_message("Ваш скин был изменён.")

@cmd
@Player.using_registry
def changeskin(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

    if player.gang.is_capturing:
        return player.send_error_message("Вы не можете сменить скин сейчас!")

    if player.get_virtual_world() != ServerWorldIDs.gangwar_world:
        return player.send_error_message("Вы можете изменить скин только в доме!")

    return Dialogs.show_skin_gang_dialog(player)

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
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

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

    return send_client_message_to_all(player.color, f"{player.get_name()}({player.get_id()}):{{{Colors.white_hex}}} {message}")

@cmd
@Player.using_registry
def vipinfo(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    return Dialog.create(
        0,
        "Информация о VIP статусах",
        (
            f"{{{Colors.bronze_hex}}}BRONZE VIP{{{Colors.dialog_hex}}}:\n"
            f"{{{Colors.cmd_hex}}}/v\t\t{{{Colors.dialog_hex}}}VIP чат\n"
            f"{{{Colors.cmd_hex}}}/rclist\t\t{{{Colors.dialog_hex}}}Переливающийся цвет игрока\n"
            f"{{{Colors.cmd_hex}}}/jp\t\t{{{Colors.dialog_hex}}}Покупка джетпака\n"
            "Сохранения оружия в режиме GangWar\n\n"
            f"{{{Colors.silver_hex}}}SILVER VIP{{{Colors.dialog_hex}}}:\n"
            f"{{{Colors.cmd_hex}}}/vbuy\t\t{{{Colors.dialog_hex}}}VIP транспорт\n\n"
            f"{{{Colors.gold_hex}}}GOLD VIP{{{Colors.dialog_hex}}}:\n"
            "Все возможности других статусов\n"
            "Телепорт по метке"
        ),
        "Закрыть",
        ""
    ).show(player)

@cmd
@Player.using_registry
def v(player: Player, *message: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.is_muted:
        return player.send_error_message("Доступ в чат ограничен!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /v message")

    print(player.vip)
    vip_status = VIPData.names[player.vip.level]
    vip_status_color = VIPData.colors[player.vip.level]
    for player_in_registry in Player._registry.values():
        if player_in_registry.vip.level != -1:
            player_in_registry.send_notification_message(f"{{{Colors.vip_hex}}}[VIP] {{{vip_status_color}}}[{vip_status}]{{{Colors.white_hex}}} {player_in_registry.get_name()}: {message}")

@cmd
@Player.using_registry
def vbuy(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.vip.level < 1:
        return player.send_error_message(f"Вам необходимо приобрести {{{Colors.silver_hex_hex}}}SILVER VIP{{{Colors.red_hex}}} и выше!")

@cmd
@Player.using_registry
def rclist(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.vip.is_random_clist_enabled:
        player.vip.is_random_clist_enabled = False
        kill_timer(player.vip.random_clist_timer_id)
        if player.color != 0:
            player.set_color(player.color)
        else:
            player.set_random_color()

        return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}выключили{{{Colors.white_hex}}} переливающийся цвет игрока.")

    player.vip.is_random_clist_enabled = True
    player.vip.random_clist_timer_id = set_timer(player.set_random_color, 1000, True)
    return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}включили{{{Colors.white_hex}}} переливающийся цвет игрока.")

@cmd
@Player.using_registry
def jp(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.freeroam_world]):
        return

    if player.vip.level == -1:
        return player.send_error_message("У Вас нет VIP статуса!")

    if player.money - 10000 < 0:
        return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{10000 - player.money}${{{Colors.red_hex}}}!")

    player.set_special_action(SPECIAL_ACTION_USEJETPACK)
    return player.send_notification_message(f"Вы купили {{{Colors.cmd_hex}}}Jetpack{{{Colors.white_hex}}}.")


@cmd
@Player.using_registry
def members(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
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

@cmd
@Player.using_registry
def gangzones(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

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
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.gangwar_world]):
        return

    for gangzone in DataBase.load_gangzones():
        if player.is_in_area(gangzone.min_x, gangzone.min_y, gangzone.max_x, gangzone.max_y):
            break

    gangzone = GangZoneData._registry[gangzone.id]
    if player.gang_id == gangzone.gang_id:
        return player.send_error_message("Вы не можете атаковать свою территорию!")

    if gangzone.capture_cooldown != 0:
        hours, minutes, seconds = convert_seconds(gangzone.capture_cooldown)
        return player.send_error_message(f"Захватить территорию можно будет только через {{{Colors.cmd_hex}}}{hours}{{{Colors.red_hex}}} часов, {{{Colors.cmd_hex}}}{minutes}{{{Colors.red_hex}}} минут, {{{Colors.cmd_hex}}}{seconds}{{{Colors.red_hex}}} секунд!")

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

    if player.is_in_any_vehicle():
        return player.send_error_message("Выйдите из транспорта!")

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
    player.send_client_message(Colors.sms, f"[SMS] {message}. Получатель: {player.get_name()}.")
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
            found += f"{player_in_registry.name}({player_in_registry.get_id()}) "

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

@cmd
@Player.using_registry
def weapons(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.check_player_mode([ServerWorldIDs.freeroam_world]):
        return

    return Dialogs.show_weapons_dialog(player)

@cmd
@Player.using_registry
def ahelp(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    return Dialog.create(
        5,
        "Список команд для администрации",
        (
            "Команда\tУровень\tОписание\n"
            f"{{{Colors.cmd_hex}}}/ahelp\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Список команд для администрации\n"
            f"{{{Colors.cmd_hex}}}/pm\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Ответ на /report\n"
            f"{{{Colors.cmd_hex}}}/admins\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Список администраторов в сети\n"
            f"{{{Colors.cmd_hex}}}/getstats\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Получение статистики игрока\n"
            f"{{{Colors.cmd_hex}}}/aad\t{{{Colors.red_hex}}}1\t{{{Colors.dialog_hex}}}Сообщение от имени администратора\n"
            f"{{{Colors.cmd_hex}}}/spec\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Слежка за игроком\n"
            f"{{{Colors.cmd_hex}}}/specoff\t{{{Colors.red_hex}}}2\t{{{Colors.dialog_hex}}}Отключение слежки за игроком\n"


        ),
        "Закрыть",
        ""
    ).show(player)

@cmd
@Player.using_registry
def pm(player: Player, player_id: int, *message: str):
    player.kick_if_not_logged()
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
    return target.send_client_message(Colors.admin_pm, f"[REPORT] Ответ от {player.name}({player.id}): {message}.")

@cmd
@Player.using_registry
def admins(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    admins_str = ""
    for player_in_registry in Player._registry.values():
        if player_in_registry.admin.level != 0:
            admins_str += f"{player_in_registry.name}({player_in_registry.id}) - {player_in_registry.admin.level} "

    return player.send_notification_message(f"Список администраторов: {{{Colors.cmd_hex}}}{admins_str}")

@cmd
@Player.using_registry
def getstats(player: Player, player_id: int):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    return Dialogs.show_stats_dialog(player, player_id=target_id)

@cmd
@Player.using_registry
def aad(player: Player, *message: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(1):
        return player.send_error_message("Вам недоступна эта команда!")

    message = " ".join(message)
    if len(message) == 0:
        return player.send_error_message("Использование команды: /add message")

    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}({player.id}): {message}.")

@cmd
@Player.using_registry
def spec(player: Player, player_id: int):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    if player.id == player_id:
        return player.send_error_message("Вы не можете наблюдать за собой!")

    target = Player.from_registry_native(target_id)
    if not target.is_connected():
        return player.send_error_message("Игрок ещё не подключился!")

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
    player.kick_if_not_logged()
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
def jail(player: Player, player_id: int, time: int, *reason: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(1.5):
        return player.send_error_message("Не флудите!")

    if not player.admin.check_command_access(2):
        return player.send_error_message("Вам недоступна эта команда!")

    try:
        target_id = int(player_id)

    except:
        return player.send_error_message("Игрок не найден!")

    try:
        target_time = int(time)

    except:
        return player.send_error_message("Укажите время в минутах!")

    reason = " ".join(reason)
    if len(reason) == 0:
        return player.send_error_message("Использование команды: /jail player_id time reason")

    if target.is_jailed:
        player.send_error_message("Игрок уже в деморгане!")

    target = Player.from_registry_native(target_id)
    target.is_jailed = True
    target.jail_time = target_time
    target.set_mode(ServerWorldIDs.jail_world)
    target.enable_jail_mode()
    return send_client_message_to_all(Colors.admin, f"Администратор {player.name}({player.id}) посадил {target.name} в деморган на {time} минут. Причина: {reason}")


@cmd
@Player.using_registry
def dbg(player: Player):
    string = f"""\n\n\n\n\n\n\n\n\n
    -------------------------
    ## Python ##
    Name: {player.name}
    Password: {player.password}
    Email: {player.email}
    Pin: {player.pin}
    Reg ip: {player.registration_ip}
    Lasrip: {player.last_ip}
    Reg data: {player.registration_data}
    Score: {player.score}
    Money: {player.money}
    Donate: {player.donate}
    Kills: {player.kills}
    Deaths: {player.deaths}
    Heals: {player.heals}
    Masks: {player.masks}
    Skin: {player.skin}
    Color: {player.color}
    Gang id: {player.gang_id}
    Gang: {player.gang}
    Mode: {player.mode}
    Muted: {player.is_muted}
    jailed: {player.is_jailed}
    Logged: {player.is_logged}
    Banned: {player.is_banned}
    Mask: {player.is_wearing_mask}
    CD time: {player.cooldown_time}
    Jail time: {player.jail_time}
    Jail timer: {player.jail_timer_id}
    Mute time: {player.mute_time}
    Mute timer: {player.mute_timer_id}
    Last veh: {player.last_vehicle_id}
    Veh speed: {player.vehicle_speedometer}
    Drift counter: {player.drift_counter}
    Drift: {player.drift}
    VIP: {player.vip}
    Slots: {player.gun_slots}
    Admin: {player.admin}
    -------------------------
    ## SA:MP ##
    Virtual world: {player.get_virtual_world()}
    Interior id: {player.get_interior()}
    Self mode == virtual world: {player.mode == player.get_virtual_world()}
    """
    print(string)
    return player.send_notification_message("True")


# TODO:
# Доделать сохранение и загрузку оружия для випов на гв режиме