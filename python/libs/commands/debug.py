import importlib

from pysamp import call_native_function, call_remote_function
from pysamp.commands import cmd
from pysamp.dialog import Dialog

from ...player import Player
from ...vehicle import Vehicle
from ..gang.gang import gangzone_pool
from ..house.house import houses
from ..squad.squad import squad_gangzone_pool
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

        player.send_notification_message(f"{attr} {value}")
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

        player.send_notification_message(f"{attr} {value}")

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
    player.send_notification_message(f"{player_.player_vehicle}")
