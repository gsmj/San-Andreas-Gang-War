from pysamp.player import Player
from pysamp.playertextdraw import PlayerTextDraw
from pysamp.timer import kill_timer, set_timer

from ...vehicle import Vehicle

drift_counter_pool: dict[int, list["PlayerTextDraw"]] = {}
"""
Key: Player Id
Value: PlayerTextDraw
"""

def create_drift_counter(player: Player) -> None:
    drift_counter_pool[player.id] = []
    drift_counter_pool[player.id].append(PlayerTextDraw.create(player, 320.000000, 375.000000, "Drift Counter"))
    drift_counter_pool[player.id][0].alignment(2)
    drift_counter_pool[player.id][0].background_color(255)
    drift_counter_pool[player.id][0].letter_size(0.500000, 1.000000)
    drift_counter_pool[player.id][0].font(3)
    drift_counter_pool[player.id][0].color(-1)
    drift_counter_pool[player.id][0].set_outline(1)
    drift_counter_pool[player.id][0].set_proportional(True)
    drift_counter_pool[player.id].append(PlayerTextDraw.create(player, 250.000000, 385.000000, "Cash: ~g~0"))
    drift_counter_pool[player.id][1].background_color(255)
    drift_counter_pool[player.id][1].font(2)
    drift_counter_pool[player.id][1].letter_size(0.200000, 1.000000)
    drift_counter_pool[player.id][1].color(-1)
    drift_counter_pool[player.id][1].set_outline(1)
    drift_counter_pool[player.id][1].set_proportional(True)
    drift_counter_pool[player.id].append(PlayerTextDraw.create(player, 250.000000, 395.000000, "Score: ~y~0"))
    drift_counter_pool[player.id][2].background_color(255)
    drift_counter_pool[player.id][2].font(2)
    drift_counter_pool[player.id][2].letter_size(0.200000, 1.000000)
    drift_counter_pool[player.id][2].color(-1)
    drift_counter_pool[player.id][2].set_outline(1)
    drift_counter_pool[player.id][2].set_outline(1)
    drift_counter_pool[player.id][2].set_proportional(True)
    drift_counter_pool[player.id].append(PlayerTextDraw.create(player, 250.000000, 405.000000, "Combo: ~r~x1"))
    drift_counter_pool[player.id][3].background_color(255)
    drift_counter_pool[player.id][3].font(2)
    drift_counter_pool[player.id][3].letter_size(0.200000, 1.000000)
    drift_counter_pool[player.id][3].color(-1)
    drift_counter_pool[player.id][3].set_outline(1)
    drift_counter_pool[player.id][3].set_proportional(True)

def give_drift_money(player: Player) -> None:
    player.score += player.drift.score * player.drift.combo
    drift_counter_pool[player.id][1].set_string("Cash: ~g~0$")
    drift_counter_pool[player.id][2].set_string("Score: ~y~0")
    drift_counter_pool[player.id][3].set_string("Combo: ~r~x1")
    player.set_money_ex(player.drift.money)
    if player.drift.score != 0:
        player.set_score(player.score)

    player.drift.money = 0
    player.drift.score = 0
    player.drift.combo = 1

def update_drift_counter(player: Player, value: int) -> None:
    player.drift.money += value
    player.drift.score += int(value / 100)
    player.drift.combo += int(player.drift.score / 100)
    drift_counter_pool[player.id][1].set_string(f"Cash: ~g~{player.drift.money}$")
    drift_counter_pool[player.id][2].set_string(f"Score: ~y~{player.drift.score}")
    drift_counter_pool[player.id][3].set_string(f"Combo: ~r~x{player.drift.combo}")

def show_drift_counter(player: Player) -> None:
    for textdraw in drift_counter_pool[player.id]:
        textdraw.show()

def hide_drift_counter(player: Player, destroy: bool = False) -> None:
    if not player.id in drift_counter_pool:
        return

    for textdraw in drift_counter_pool[player.id]:
        if isinstance(textdraw, PlayerTextDraw):
            textdraw.hide()

    give_drift_money(player)
    if destroy:
        del drift_counter_pool[player.id]
