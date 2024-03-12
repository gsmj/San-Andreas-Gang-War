from pysamp.player import Player
from pysamp.playertextdraw import PlayerTextDraw
from pysamp.timer import kill_timer, set_timer

from ...vehicle import Vehicle

vehicle_speedometer_pool: dict[int, list["PlayerTextDraw"]] = {}
"""
Key: Player Id
Value: PlayerTextDraw
"""
drift_counter_pool: dict[int, list["PlayerTextDraw"]] = {}
"""
Key: Player Id
Value: PlayerTextDraw
"""


def create_speedometer(player: Player):
    vehicle_speedometer_pool[player.id] = []
    vehicle_speedometer_pool[player.id].append(PlayerTextDraw.create(player, 625.000000, 385.000000, "usebox")) # type: ignore
    vehicle_speedometer_pool[player.id][0].letter_size(0.000000, 5.905555)
    vehicle_speedometer_pool[player.id][0].text_size(430.799987, 0.000000)
    vehicle_speedometer_pool[player.id][0].alignment(1)
    vehicle_speedometer_pool[player.id][0].use_box(True)
    vehicle_speedometer_pool[player.id][0].box_color(50)
    vehicle_speedometer_pool[player.id][0].color(102)
    vehicle_speedometer_pool[player.id][0].set_shadow(0)
    vehicle_speedometer_pool[player.id][0].set_outline(0)
    vehicle_speedometer_pool[player.id][0].font(0)

    vehicle_speedometer_pool[player.id].append(PlayerTextDraw.create(player, 600.000000, 385.000000, "LD_SPAC:white")) # type: ignore
    vehicle_speedometer_pool[player.id][1].letter_size(0.000000, 0.000000)
    vehicle_speedometer_pool[player.id][1].text_size(21.250000, 57.166625)
    vehicle_speedometer_pool[player.id][1].alignment(1)
    vehicle_speedometer_pool[player.id][1].color(255)
    vehicle_speedometer_pool[player.id][1].set_shadow(0)
    vehicle_speedometer_pool[player.id][1].set_outline(0)
    vehicle_speedometer_pool[player.id][1].font(4)

    vehicle_speedometer_pool[player.id].append(PlayerTextDraw.create(player, 440.000000, 385.000000, "SPEED: 0 km/h")) # type: ignore
    vehicle_speedometer_pool[player.id][2].letter_size(0.401249, 1.430832)
    vehicle_speedometer_pool[player.id][2].alignment(1)
    vehicle_speedometer_pool[player.id][2].color(-1)
    vehicle_speedometer_pool[player.id][2].set_shadow(0)
    vehicle_speedometer_pool[player.id][2].set_outline(1)
    vehicle_speedometer_pool[player.id][2].background_color(51)
    vehicle_speedometer_pool[player.id][2].font(1)
    vehicle_speedometer_pool[player.id][2].set_proportional(True)

    vehicle_speedometer_pool[player.id].append(PlayerTextDraw.create(player, 610.000000, 385.000000, "L")) # type: ignore
    vehicle_speedometer_pool[player.id][3].letter_size(0.449999, 1.600000)
    vehicle_speedometer_pool[player.id][3].alignment(1)
    vehicle_speedometer_pool[player.id][3].color(-1)
    vehicle_speedometer_pool[player.id][3].set_shadow(0)
    vehicle_speedometer_pool[player.id][3].set_outline(1)
    vehicle_speedometer_pool[player.id][3].background_color(51)
    vehicle_speedometer_pool[player.id][3].font(1)
    vehicle_speedometer_pool[player.id][3].set_proportional(True)

    vehicle_speedometer_pool[player.id].append(PlayerTextDraw.create(player, 610.000000, 415.000000, "E")) # type: ignore
    vehicle_speedometer_pool[player.id][4].letter_size(0.449999, 1.600000)
    vehicle_speedometer_pool[player.id][4].alignment(1)
    vehicle_speedometer_pool[player.id][4].color(-1)
    vehicle_speedometer_pool[player.id][4].set_shadow(0)
    vehicle_speedometer_pool[player.id][4].set_outline(1)
    vehicle_speedometer_pool[player.id][4].font(1)
    vehicle_speedometer_pool[player.id][4].set_proportional(True)


def update_speedometer_velocity(player: Player, vehicle: Vehicle):
    return vehicle_speedometer_pool[player.id][2].set_string(f"SPEED: {vehicle.get_speed()} km/h")

def update_speedometer_sensors(player: Player, vehicle: Vehicle):
    if vehicle.engine == 1:
        vehicle_speedometer_pool[player.id][4].set_string("~b~E")

    else:
        vehicle_speedometer_pool[player.id][4].set_string("~w~E")

    if vehicle.lights == 1:
        vehicle_speedometer_pool[player.id][3].set_string("~b~L")

    else:
        vehicle_speedometer_pool[player.id][3].set_string("~w~L")


def show_speedometer(player: Player, vehicle: Vehicle) -> None:
    for textdraw in vehicle_speedometer_pool[player.id]:
        textdraw.show()

    timer = set_timer(update_speedometer_velocity, 250, True, player, vehicle)
    vehicle_speedometer_pool[player.id].append(timer) # Index 5

def hide_speedometer(player: Player) -> None:
    try:
        vehicle_speedometer_pool[player.id]
    except:
        return

    for textdraw in vehicle_speedometer_pool[player.id]:
        if isinstance(textdraw, PlayerTextDraw):
            textdraw.hide()

    kill_timer(vehicle_speedometer_pool[player.id][5])
    del vehicle_speedometer_pool[player.id]
