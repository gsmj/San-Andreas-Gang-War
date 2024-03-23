import importlib

from pysamp.commands import cmd
from pysamp.dialog import Dialog

from ...player import Player
from ...vehicle import Vehicle
from ..gang.gang import gangzone_pool
from ..house.house import houses
from ..squad.squad import squad_gangzone_pool
from ..utils.data import ZoneNames
from .cmd_ex import CommandType, cmd_ex


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
    return player.send_message("Кэш обновлён!")

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
    return player.send_message(f"Всего домов: {len(houses)}")

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
    return player.send_message(f"Всего гангзон: {len(gangzone_pool)}")


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

        player.send_message(f"{attr} {value}")
        print(f"{attr} | {value}")

@cmd_ex(
    cmd,
    description="Отладочная информация об авто на сервере",
    mode=CommandType.admin_type
)
@Player.using_registry
def vdata(player: Player):
    if not player.admin.check_command_access(7):
        return

    vehicles = Vehicle._registry
    content = ""
    for attr, value in vehicles.items():
        content += f"{attr}: {value}\n"

        player.send_message(f"{attr} {value}")

@cmd_ex(
    cmd,
    description="Отладочная информация об авто игрока на сервере",
    mode=CommandType.admin_type
)
@Player.using_registry
def pvdata(player: Player, player_id: int):
    if not player.admin.check_command_access(7):
        return

    player_ = Player.from_registry_native(int(player_id))
    player.send_message(f"{player_.player_vehicle}")

@cmd_ex(
    cmd,
    description="Сохранение позиции и ID гангзоны",
    mode=CommandType.admin_type
)
@Player.using_registry
def sgz(player: Player):
    player.send_debug_message("Используйте команду только когда Вы находитесь в гангзоне", 2)
    for gz_id, gangzone in squad_gangzone_pool.items():
        if player.is_in_area(gangzone.min_x, gangzone.min_y, gangzone.max_x, gangzone.max_y):
            break

    x, y, z = player.get_pos()
    with open("squadpositions.txt", mode="a") as f:
        f.write(f"{x}, {y}, {z} | ID: {gz_id} | Name: {ZoneNames.names[gz_id]}\n")

    return player.send_message(f"ID гангзоны: {gz_id} | Название: {ZoneNames.names[gz_id]}")
