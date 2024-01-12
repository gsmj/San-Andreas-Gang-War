from pysamp.commands import cmd
from pysamp.dialog import Dialog
from pysamp.timer import set_timer
from .player import Player
from .gang import gangs
from .utils import Colors, MonthsConverter
from .database import DataBase
from datetime import datetime as dt
from zoneinfo import ZoneInfo


@cmd(aliases=("mm", "menu", "help"))
@Player.using_registry
def mn(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(3.0):
        return player.send_error_message("Не флудите!")

    return player.show_mn_dialog()


@cmd
@Player.using_registry
def stats(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(3.0):
        return player.send_error_message("Не флудите!")

    return player.show_stats_dialog()


@cmd(aliases=("usedrugs", "heal"))
@Player.using_registry
def healme(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(3.0):
        return player.send_error_message("Не флудите!")

    if player.heals == 0:
        return player.send_error_message("У Вас нет аптечек!")

    health = player.get_health()
    if health + 25.0 <= 100.0:
        player.apply_animation("SMOKING", "M_smk_drag", 4.1, False, False, False, False, 0)
        player.heals -= 1
        player.set_health(health + 25.0)
        player.set_chat_bubble("Использует аптечку..", Colors.white, 20.0, 5000)
        return player.send_notification_message(f"Вы использовали аптечку. Здоровье восстановлено на {{FF0000}}25HP{{FFFFFF}}.")

    else:
        return player.send_error_message("Вы не можете использовать аптечку сейчас!")


@cmd
@Player.using_registry
def mask(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(3.0):
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
    return player.send_notification_message(f"Ваше местоположение на карте скрыто. Используйте {{FFCD00}}/maskoff{{FFFFFF}}, чтобы снять маску.")


@cmd(aliases=("maskend", "end"))
@Player.using_registry
def maskoff(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(3.0):
        return player.send_error_message("Не флудите!")

    if not player.is_wearing_mask:
        return player.send_error_message("У Вас нет маски!")

    if player.is_attached_object_slot_used(2):
        player.remove_attached_object(2)

    player.is_wearing_mask = False
    player.set_color(gangs[player.gang_id].color)
    return player.send_notification_message("Вы сняли маску.")


@cmd(aliases=("newband", "changegang"))
@Player.using_registry
def newgang(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(3.0):
        return player.send_error_message("Не флудите!")

    if gangs[player.gang_id].is_capture:
        return player.send_error_message("Вы не можете сменить банду сейчас!")

    if player.is_wearing_mask:
        player.is_wearing_mask = False
        player.set_color(gangs[player.gang_id].color)

    if player.is_attached_object_slot_used(2):
        player.remove_attached_object(2)

    player.heals = 0
    player.masks = 0
    player.reset_weapons()
    player.reset_money()
    return player.show_command_gang_choice_dialog()


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


@cmd(aliases=("r"), split_args=False)
@Player.using_registry
def f(player: Player, message: str):
    player.kick_if_not_logged()
    if not player.check_cooldown(3.0):
        return player.send_error_message("Не флудите!")

    if len(message) == 0:
        return player.send_error_message("[ОШИБКА] Использование команды: /f message")

    if player.is_muted:
        return player.send_error_message("Доступ в чат ограничен!")

    for player_in_registry in player._registry:
        player_in_registry = Player.from_registry_native(player_in_registry)
        if player.gang_id == player_in_registry.gang_id:
            key, value = player.get_gang_rang()
            player_in_registry.send_client_message(gangs[player.gang_id].color, f"[F] {value} {player.get_name()}: {message}")

    return


@cmd
@Player.using_registry
def members(player: Player):
    player.kick_if_not_logged()
    if not player.check_cooldown(3.0):
        return player.send_error_message("Не флудите!")

    members_dict = {}
    for player_in_registry in player._registry:
        player_in_registry = Player.from_registry_native(player_in_registry)
        if player.gang_id == player_in_registry.gang_id:
            members_dict[player_in_registry.get_name()] = player_in_registry.kills

    sorted_members = dict(sorted(members_dict.items(), key=lambda item: item[1], reverse=True))
    members_string = ""
    for key, value in sorted_members.items():
        members_string += f"Игрок: {key}\t\t\tУбийств: {value}\n"

    return Dialog.create(0, f"Онлайн в банде {gangs[player.gang_id].gang_name}", f"{members_string}", "Закрыть", "").show(player)





# TODO Доделать:
# Команды []
# Система авто (запуск, /lock, и т.д) []
# Система каптов []
# Доработать команды, если надо []
# Система администрирования []
# Сделать привязку к мирам. (0 - GW, 1 - DM, и т.д) []
# Система мута (доделать) []




# @cmd
# @Player.using_registry
# def setturf(player: Player, set_gang_id: int):
#     gangzones = DataBase.load_gangzones()
#     for gangzone in gangzones:
#         if player.is_in_area(gangzone.min_x, gangzone.min_y, gangzone.max_x, gangzone.max_y):
#             gangzone_id = gangzone.id
#             player.send_notification_message(f"Вы находитесь в гангзоне {gangzone_id}!")
#             break

#     player.send_notification_message(f"Обновляется: {gangzone_id}!")
#     DataBase.save_gangzone(gangzone_id, gang_id=int(set_gang_id), color=gangs[int(set_gang_id)].color)
#     player.reload_gangzones_for_player()
