from pysamp.player import Player as BasePlayer
from pysamp.playertextdraw import PlayerTextDraw
from pysamp.textdraw import TextDraw
from pystreamer.dynamicpickup import DynamicPickup
from pystreamer.dynamiccp import DynamicCheckpoint
from pysamp.timer import set_timer, kill_timer
from pysamp.dialog import Dialog
from pysamp import (
    send_client_message,
    create_player_3d_text_label,
    delete_player_3d_text_label,
    call_remote_function,
    send_client_message_to_all,
    kick
)
from .libs.utils.data import *
from .libs.utils.consts import *
from functools import wraps
from datetime import datetime
from zoneinfo import ZoneInfo
from .libs.gang.gang import gangs, Gang, gangzone_pool
from .libs.static import textdraws
from .libs import __version__
from .libs.database.database import DataBase
from .vehicle import Vehicle, VehicleData, VehicleTypes, VehicleComponents
from .libs.misc.playerdata import *
from .libs.modes.modes import Freeroam, DeathMatch, GangWar
from .libs.dynamic.objects import remove_objects_for_player
from .libs.commands.cmd_ex import commands, CommandType
from .libs.house.house import (
    House,
    houses_by_pickup,
    interiors,
    houses_by_owner
)
from .libs.squad.squad import Squad
from .libs.fun.math import MathTest
from math import sqrt
import time
from samp import INVALID_PLAYER_ID, PLAYER_STATE_ONFOOT, PLAYER_STATE_DRIVER, PLAYER_STATE_SPECTATING # type: ignore


class Player(BasePlayer):
    _registry: dict = {}
    def __init__(self, player_id):
        super().__init__(player_id)
        self.cache: dict = {}
        self.name = self.get_name()
        self.password: str = None
        self.email: str = None
        self.pin: int = None
        self.registration_ip: str = None
        self.last_ip: str = self.get_ip()
        self.registration_data: datetime = None
        self.score: int = 0
        self.money: int = 0
        self.donate: int = 0
        self.dm_rating: int = 0
        self.kills: int = 0
        self.deaths: int = 0
        self.heals: int = 0
        self.masks: int = 0
        self.skin: int = 0
        self.color: int = 0 # Цвет сохраняется только когда необходимо иметь разделение или возврат к обычному (цвет банды, т.д)
        self.gang_id: int = -1 # No gang
        self.gang: Gang = gangs[self.gang_id]
        self.mode: int = 0
        self.vehicle_speedometer: dict = {}
        self.drift_counter: dict = {}
        self.timers: PlayerTimers = PlayerTimers()
        self.checks: PlayerChecks = PlayerChecks()
        self.time: PlayerTime = PlayerTime()
        self.drift: PlayerDrift = PlayerDrift()
        self.vip: PlayerVIP = PlayerVIP()
        self.gun_slots: PlayerFreeroamGunSlots = PlayerFreeroamGunSlots()
        self.admin: PlayerAdmin = PlayerAdmin()
        self.vehicle: PlayerVehicle = PlayerVehicle()
        self.settings: PlayerSettings = PlayerSettings()
        self.house: House = None
        self.squad: Squad = None

    @classmethod
    def from_registry_native(cls, player: BasePlayer) -> "Player":
        if isinstance(player, int):
            player_id = player

        if isinstance(player, BasePlayer):
            player_id = player.id

        player = cls._registry.get(player_id)
        if not player:
            cls._registry[player_id] = player = cls(player_id)

        return player

    @classmethod
    def using_registry(cls, func):
        @wraps(func)
        def from_registry(*args, **kwargs):
            args = list(args)
            args[0] = cls.from_registry_native(args[0])
            return func(*args, **kwargs)

        return from_registry

    @classmethod
    def delete_registry(cls, player: BasePlayer) -> None:
        del cls._registry[player.id]

    def set_skin_ex(self, skin_id: int) -> None:
        self.set_skin(skin_id)
        self.skin = skin_id

    def set_color_ex(self, color: int) -> None:
        self.set_color(color)
        self.color = self.get_color()

    def set_money_ex(self, amount: int, increase: bool = True, show_text: bool = True) -> None:
        if increase:
            self.money += amount
            self.give_money(amount)
            string = f"~g~+{amount}$"

        else:
            self.money -= amount
            self.give_money(-amount)
            string = f"~r~-{amount}$"

        if show_text:
            self.game_text(string, 1500, 1)

    def set_dm_rating(self, amount: int, increase: bool = True, show_text: bool = True) -> None:
        if increase:
            self.dm_rating += amount
            string = f"~b~+{amount}"

        else:
            if (self.dm_rating - amount) < 0:
                self.dm_rating = 0
                return

            else:
                self.dm_rating -= amount
                string = f"~r~-{amount}"

        if show_text:
            self.game_text(string, 1500, 3)

    def take_money_ex(self, amount: int, show_text: bool = True) -> None:
        self.money -= amount
        self.set_money(self.money)
        if show_text:
            self.game_text(f"~r~-{amount}$", 1500, 1)

    def set_mode(self, mode: int) -> None:
        self.set_virtual_world(mode)
        self.mode = mode

    def update_vehicle_inst(self, vehice: Vehicle) -> None:
        self.vehicle.inst = vehice
        return

    def kick_player(self, player: "Player") -> None:
        player = self.from_registry_native(player)
        Dialogs.show_kick_dialog(player)
        player.send_error_message("Введите /q (/quit) чтобы выйти!")
        return set_timer(kick, 1000, False, player.id)

    def mute_timer(self) -> None:
        self.send_notification_message("Время муто вышло.")
        self.checks.muted = False
        self.time.mute = 0
        self.timers.mute_id = TIMER_ID_NONE

    def every_second(self) -> None:
        self.time.afk += 1
        if self.time.afk >= 3:
            self.set_chat_bubble(f"AFK: {self.time.afk} секунд", -1, 20.0, 1100)

        if not self.settings.disabled_ping_td:
            return textdraws.fps_and_ping[0].set_string(f"Ping: {self.get_ping()}")

    def jail_timer(self) -> None:
        self.send_notification_message("Вас выпустили из деморгана.")
        self.checks.jailed = False
        self.time.jail = 0
        self.timers.jail_id = TIMER_ID_NONE
        self.force_class_selection()
        self.toggle_spectating(True)
        self.toggle_spectating(False)

    def create_speedometer(self) -> dict[int, "PlayerTextDraw"]:
        self.vehicle_speedometer[0] = PlayerTextDraw.create(self, 625.000000, 385.000000, "usebox")
        self.vehicle_speedometer[0].letter_size(0.000000, 5.905555)
        self.vehicle_speedometer[0].text_size(430.799987, 0.000000)
        self.vehicle_speedometer[0].alignment(1)
        self.vehicle_speedometer[0].use_box(True)
        self.vehicle_speedometer[0].box_color(50)
        self.vehicle_speedometer[0].color(102)
        self.vehicle_speedometer[0].set_shadow(0)
        self.vehicle_speedometer[0].set_outline(0)
        self.vehicle_speedometer[0].font(0)
        self.vehicle_speedometer[1] = PlayerTextDraw.create(self, 600.000000, 385.000000, "LD_SPAC:white")
        self.vehicle_speedometer[1].letter_size(0.000000, 0.000000)
        self.vehicle_speedometer[1].text_size(21.250000, 57.166625)
        self.vehicle_speedometer[1].alignment(1)
        self.vehicle_speedometer[1].color(255)
        self.vehicle_speedometer[1].set_shadow(0)
        self.vehicle_speedometer[1].set_outline(0)
        self.vehicle_speedometer[1].font(4)
        self.vehicle_speedometer[2] = PlayerTextDraw.create(self, 440.000000, 385.000000, "SPEED: 0 km/h")
        self.vehicle_speedometer[2].letter_size(0.401249, 1.430832)
        self.vehicle_speedometer[2].alignment(1)
        self.vehicle_speedometer[2].color(-1)
        self.vehicle_speedometer[2].set_shadow(0)
        self.vehicle_speedometer[2].set_outline(1)
        self.vehicle_speedometer[2].background_color(51)
        self.vehicle_speedometer[2].font(1)
        self.vehicle_speedometer[2].set_proportional(True)
        self.vehicle_speedometer[3] = PlayerTextDraw.create(self, 610.000000, 385.000000, "L")
        self.vehicle_speedometer[3].letter_size(0.449999, 1.600000)
        self.vehicle_speedometer[3].alignment(1)
        self.vehicle_speedometer[3].color(-1)
        self.vehicle_speedometer[3].set_shadow(0)
        self.vehicle_speedometer[3].set_outline(1)
        self.vehicle_speedometer[3].background_color(51)
        self.vehicle_speedometer[3].font(1)
        self.vehicle_speedometer[3].set_proportional(True)
        self.vehicle_speedometer[4] = PlayerTextDraw.create(self, 610.000000, 415.000000, "E")
        self.vehicle_speedometer[4].letter_size(0.449999, 1.600000)
        self.vehicle_speedometer[4].alignment(1)
        self.vehicle_speedometer[4].color(-1)
        self.vehicle_speedometer[4].set_shadow(0)
        self.vehicle_speedometer[4].set_outline(1)
        self.vehicle_speedometer[4].font(1)
        self.vehicle_speedometer[4].set_proportional(True)
        return self.vehicle_speedometer

    def show_speedometer(self) -> None:
        self.vehicle_speedometer[0].show()
        self.vehicle_speedometer[1].show()
        self.vehicle_speedometer[2].show()
        self.vehicle_speedometer[3].show()
        self.vehicle_speedometer[4].show()

    def hide_speedometer(self) -> None:
        self.vehicle_speedometer[0].destroy()
        self.vehicle_speedometer[1].destroy()
        self.vehicle_speedometer[2].destroy()
        self.vehicle_speedometer[3].destroy()
        self.vehicle_speedometer[4].destroy()

    def update_speedometer_sensors(self, vehicle: Vehicle):
        if vehicle.engine == 1:
            self.vehicle_speedometer[4].set_string("~b~E")

        else:
            self.vehicle_speedometer[4].set_string("~w~E")

        if vehicle.lights == 1:
            self.vehicle_speedometer[3].set_string("~b~L")

        else:
            self.vehicle_speedometer[3].set_string("~w~L")

    def update_speedometer_velocity(self, vehicle: Vehicle):
        return self.vehicle_speedometer[2].set_string(f"SPEED: {self.get_speed_in_vehicle(vehicle)} km/h")

    def get_speed_in_vehicle(self, vehicle: Vehicle):
        x, y, z = vehicle.get_velocity()
        x_res = abs(x)**2.0
        y_res = abs(y)**2.0
        z_res = abs(z)**2.0

        res = sqrt(x_res + y_res + z_res) * 100.3
        return int(res)

    def create_drift_counter(self) -> dict[int, "PlayerTextDraw"]:
        self.drift_counter[1] = PlayerTextDraw.create(self, 320.000000, 375.000000, "Drift Counter")
        self.drift_counter[1].alignment(2)
        self.drift_counter[1].background_color(255)
        self.drift_counter[1].letter_size(0.500000, 1.000000)
        self.drift_counter[1].font(3)
        self.drift_counter[1].color(-1)
        self.drift_counter[1].set_outline(1)
        self.drift_counter[1].set_proportional(True)
        self.drift_counter[2] = PlayerTextDraw.create(self, 250.000000, 385.000000, "Cash: ~g~0")
        self.drift_counter[2].background_color(255)
        self.drift_counter[2].font(2)
        self.drift_counter[2].letter_size(0.200000, 1.000000)
        self.drift_counter[2].color(-1)
        self.drift_counter[2].set_outline(1)
        self.drift_counter[2].set_proportional(True)
        self.drift_counter[3] = PlayerTextDraw.create(self, 250.000000, 395.000000, "Score: ~y~0")
        self.drift_counter[3].background_color(255)
        self.drift_counter[3].font(2)
        self.drift_counter[3].letter_size(0.200000, 1.000000)
        self.drift_counter[3].color(-1)
        self.drift_counter[3].set_outline(1)
        self.drift_counter[3].set_outline(1)
        self.drift_counter[3].set_proportional(True)
        self.drift_counter[4] = PlayerTextDraw.create(self, 250.000000, 405.000000, "Combo: ~r~x1")
        self.drift_counter[4].background_color(255)
        self.drift_counter[4].font(2)
        self.drift_counter[4].letter_size(0.200000, 1.000000)
        self.drift_counter[4].color(-1)
        self.drift_counter[4].set_outline(1)
        self.drift_counter[4].set_proportional(True)
        return self.drift_counter

    def show_drift_counter(self) -> None:
        self.drift_counter[1].show()
        self.drift_counter[2].show()
        self.drift_counter[3].show()
        self.drift_counter[4].show()

    def destroy_drift_counter(self) -> None:
        self.drift_counter[1].destroy()
        self.drift_counter[2].destroy()
        self.drift_counter[3].destroy()
        self.drift_counter[4].destroy()

    def hide_drift_counter(self) -> None:
        self.drift_counter[1].hide()
        self.drift_counter[2].hide()
        self.drift_counter[3].hide()
        self.drift_counter[4].hide()
        self.give_drift_money()

    def give_drift_money(self) -> None:
        self.score += self.drift.score * self.drift.combo
        self.drift_counter[2].set_string(f"Cash: ~g~0$")
        self.drift_counter[3].set_string(f"Score: ~y~0")
        self.drift_counter[4].set_string(f"Combo: ~r~x1")
        self.set_money_ex(self.drift.money)
        if self.drift.score != 0:
            self.set_score(self.score)

        self.drift.money = 0
        self.drift.score = 0
        self.drift.combo = 1

    def update_drift_counter(self, value: int) -> None:
        self.drift.money += value
        self.drift.score += int(value / 100)
        self.drift.combo += int(self.drift.score / 100)
        self.drift_counter[2].set_string(f"Cash: ~g~{self.drift.money}$")
        self.drift_counter[3].set_string(f"Score: ~y~{self.drift.score}")
        self.drift_counter[4].set_string(f"Combo: ~r~x{self.drift.combo}")

    def send_error_message(self, message: str) -> None:
        return self.send_client_message(Colors.red, f"[ОШИБКА] {message}")

    def send_notification_message(self, message: str) -> None:
        return self.send_client_message(Colors.white, f"{message}")

    def send_debug_message(self, event: str, message: str) -> bool:
        if DEBUG:
            self.send_client_message(Colors.blue, f"{event}")
            self.send_client_message(Colors.light_grey, f"{message}")

    def send_report_message(self, author: "Player", message: str) -> None:
        for player in self._registry.values():
            if player.admin.level != 0:
                player.send_client_message(Colors.red, f"[REPORT] Репорт от {{{Colors.cmd_hex}}}{author.name}({author.id}):{{{Colors.red_hex}}} {message}.")

    def get_gang_rang(self):
        for key, value in self.gang.rangs.items():
            if self.kills <= key:
                return key, value

    def get_dm_color(self) -> None:
        for key, value in DMRatingColors.colors.items():
            if self.dm_rating <= key:
                break

        if not value:
            value = "FFD700"

        return value

    def remove_unused_vehicle(self, mode: int):
        if self.vehicle.inst and self.mode == mode:
            Vehicle.remove_unused_player_vehicle(self.vehicle.inst)
            # self.vehicle.inst = None

    def get_zone_name(self, x: float, y: float):
        return call_remote_function("GetMapZoneAtPoint2D", x, y)

    def get_pos_zone_name(self):
        return call_remote_function("GetPlayerMapZone", self.id)

    def check_player_mode(self, modes: list[int]) -> int:
        if not self.get_virtual_world() in modes:
            self.send_error_message("Это команда недоступна в Вашем режиме!")
            return False

        return True

    def show_server_logotype(self):
        for td in textdraws.logo.values():
            td.show_for_player(self)

    def show_bottom_commands(self):
        self.hide_bottom_commands()
        if self.mode == ServerMode.gangwar_world:
            for td in textdraws.commands_bottom_gw.values():
                td.show_for_player(self)

        if self.mode == ServerMode.freeroam_world:
            for td in textdraws.commands_bottom.values():
                td.show_for_player(self)

    def hide_bottom_commands(self):
        for td in textdraws.commands_bottom_gw.values():
            td.hide_for_player(self)

        for td in textdraws.commands_bottom.values():
            td.hide_for_player(self)

    def show_ping_textdraw(self):
        for td in textdraws.fps_and_ping.values():
            td.show_for_player(self)

    def hide_ping_textdraw(self):
        for td in textdraws.fps_and_ping.values():
            td.hide_for_player(self)

    def check_cooldown(self, unix_seconds: float) -> bool:
        if self.time.cooldown is not None:
            if (time.time() - self.time.cooldown) < unix_seconds:
                return False

        self.time.cooldown = time.time()
        return True

    def check_pickup_cooldown(self, unix_seconds: float) -> bool:
        if self.time.pickup_cooldown is not None:
            if (time.time() - self.time.pickup_cooldown) < unix_seconds:
                return False

        self.time.pickup_cooldown = time.time()
        return True

    def set_random_color(self) -> None:
        return self.set_color(randint(0, 16777215))

    def set_random_color_ex(self) -> None:
        self.color = randint(0, 16777215)
        return self.set_color(self.color)

    def set_rainbow_color(self) -> None:
        if self.vip.random_clist_iterator == len(RainbowColors.colors):
            self.vip.random_clist_iterator = 0

        self.set_color(RainbowColors.colors[self.vip.random_clist_iterator])
        self.vip.random_clist_iterator += 1

    def kick_if_not_logged(self) -> None:
        if not self.checks.logged:
            Dialogs.show_kick_dialog(self)
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.kick, 1000, False)

    def kick_if_not_logged_or_jailed(self) -> None:
        if not self.checks.logged or self.checks.jailed:
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.kick, 1000, False)

    def kick_teamkill(self) -> None:
        Dialogs.show_kick_teamkill(self)
        self.send_error_message("Введите /q (/quit) чтобы выйти!")
        return set_timer(self.kick, 1000, False)

    def ban_from_server(self, reason: str) -> None:
        if self.checks.banned:
            Dialogs.show_banned_dialog(self)
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.ban_ex, 1000, False, reason)

    def is_in_area(self, min_x: float, min_y: float, max_x: float, max_y: float) -> bool:
        x, y, _z = self.get_pos()
        if ((x <= max_x and x >= min_x) and (y <= max_y and y >= min_y)):
            return True

        return False

    def set_jail_spawn_info(self):
        self.set_spawn_info(
            254, # 254 Команда для игроков в ДМГ, чтобы не было урона
            167,
            5509.365234,
            1245.812866,
            8.000000,
            0.0,
            0, 0, 0, 0, 0, 0)

    def enable_jail_mode(self):
        self.remove_unused_vehicle(ServerMode.freeroam_world)
        self.set_skin(167)
        self.set_team(254)
        self.set_color_ex(Colors.jail)
        GangWar.disable_gangzones_for_player(self)
        GangWar.hide_capture_textdraws(self)
        DeathMatch.hide_gangzones_for_player(self)
        self.set_pos(5509.365234, 1245.812866, 8.000000)
        self.set_jail_spawn_info()
        self.reset_weapons()
        self.send_notification_message(f"Вы выйдите из деморгана через {{{Colors.cmd_hex}}}{self.time.jail}{{{Colors.white_hex}}} минут.")
        if self.timers.jail_id == TIMER_ID_NONE:
            self.timers.jail_id = set_timer(self.jail_timer, int(self.time.jail * 60000), False)

        DeathMatch.disable_timer_for_player(self)

    def prox_detector(self, max_range: float, color: int, message: str, max_ratio: float = 1.6) -> None:
        if not self.get_pos():
            return

        color_r = float(color >> 24 & 0xFF)
        color_g = float(color >> 16 & 0xFF)
        color_b = float(color >> 8 & 0xFF)
        range_with_ratio = max_range * max_ratio
        for player in self._registry.values():
            if not self.is_streamed_in(player):
                continue

            range = player.distance_from_point(*self.get_pos())
            if range > max_range:
                continue

            range_ratio = (range_with_ratio - range) / range_with_ratio
            clr_r = int(range_ratio * color_r)
            clr_g = int(range_ratio * color_g)
            clr_b = int(range_ratio * color_b)
            send_client_message(player.id, (color & 0xFF) | (clr_b << 8) | (clr_g << 16) | (clr_r << 24), f"- {self.get_name()}[{self.id}]:{{{Colors.white_hex}}} {message}")

    def preload_all_anim_libs(self) -> None:
        self.apply_animation("shop", "null", 0.0, False, False, False, False, 0)
        self.apply_animation("ped", "null", 0.0, False, False, False, False, 0)

    def set_max_gun_skill(self):
        self.set_skill_level(0, 999)
        self.set_skill_level(1, 999)
        self.set_skill_level(2, 999)
        self.set_skill_level(3, 999)
        self.set_skill_level(4, 999)
        self.set_skill_level(5, 999)
        self.set_skill_level(6, 999)
        self.set_skill_level(7, 999)
        self.set_skill_level(8, 999)
        self.set_skill_level(9, 999)
        self.set_skill_level(10, 999)

    def set_checkpoint_to_gangzone(self, x, y, z) -> None:
        return self.set_checkpoint(x, y, z, 1.0)

    def set_data_after_login(self, player_db: "Player") -> None: # Login
        player_settings = DataBase.get_player_settings(self)
        self.password = player_db.password
        self.email = player_db.email
        self.pin = player_db.pin
        self.registration_ip = player_db.registration_ip
        self.registration_data = player_db.registration_data
        self.score = player_db.score
        self.money = player_db.money
        self.donate = player_db.donate
        self.dm_rating = player_db.dm_rating
        self.kills = player_db.kills
        self.deaths = player_db.deaths
        self.heals = player_db.heals
        self.masks = player_db.masks
        self.gang_id = player_db.gang_id
        self.gang = gangs[self.gang_id]
        self.vip.level=player_db.vip_level
        self.admin.level=player_db.admin_level
        self.checks.muted=player_db.is_muted
        self.checks.jailed=player_db.is_jailed
        self.checks.logged=True
        self.checks.banned=player_db.is_banned
        self.time.jail=player_db.jail_time
        self.time.mute=player_db.mute_time
        self.settings.disabled_ping_td=player_settings.disabled_ping_td
        self.settings.disabled_global_chat_gw=player_settings.disabled_global_chat_gw
        self.settings.spawn_in_house=player_settings.spawn_in_house
        if houses_by_owner[self.name]:
            self.house = houses_by_owner[self.name]

        self.set_max_gun_skill()
        self.reset_money()
        self.give_money(self.money)
        self.set_score(self.score)
        Freeroam.update_gun_slots_for_player(self, DataBase.get_player_freeroam_gun_slots(self))
        send_client_message_to_all(Colors.white, f"Игрок {{{Colors.cmd_hex}}}{self.name}[{self.id}]{{{Colors.white_hex}}} зашёл на сервер!")
        if not self.checks.jailed:
            self.force_class_selection()
            self.toggle_spectating(False)

        self.set_mode(ServerMode.jail_world)
        return self.toggle_spectating(False)

    def _get_tab_list_header(self, start: int, stop: int = None) -> str:
        gangzone_tab_list_header = ""
        for gangzone in list(gangzone_pool.values())[start:stop]:
            hours, minutes, seconds = convert_seconds(gangzone.capture_cooldown)
            gangzone_tab_list_header += f"{{{gangs[gangzone.gang_id].color_hex}}}{gangs[gangzone.gang_id].gang_name}{{{Colors.white_hex}}}\t{gangzone.id}\t{hours}:{minutes}:{seconds}\n"

        return gangzone_tab_list_header

    # Handle блок.

    def on_text_handle(self, text: str) -> False:
        self.kick_if_not_logged()
        if MathTest.correct_answer != ID_NONE:
            try:
                answer = int(text)
            except:
                pass
            else:
                if answer == MathTest.correct_answer:
                    return MathTest.send_winner_message(self)

        if self.checks.muted:
            self.set_chat_bubble("Пытается что-то сказать.", Colors.red, 20.0, 10000)
            return self.send_error_message("Доступ в чат заблокирован!")

        if self.mode == ServerMode.freeroam_world or self.mode in ServerMode.deathmatch_worlds:
            return send_client_message_to_all(self.color, f"{self.get_name()}[{self.id}]:{{{Colors.white_hex}}} {text}")

        if self.mode == ServerMode.gangwar_world and self.settings.disabled_global_chat_gw:
            return send_client_message_to_all(self.color, f"{self.get_name()}[{self.id}]:{{{Colors.white_hex}}} {text}")

        self.set_chat_bubble(text, -1, 20.0, 10000)
        return self.prox_detector(20.0, self.color, text)

    def on_pick_up_pickup_handle(self, pickup: DynamicPickup) -> None:
        self.kick_if_not_logged()
        self.send_debug_message("on_pick_up_pickup_handle", f"Player: {self} | Pickup.id: {pickup.id}")
        if not self.check_pickup_cooldown(5):
            return

        if pickup.id == gangs[0].enter_exit[0].id: # Grove enter
            if not self.gang_id == gangs[0].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(2466.2649, -1698.4724, 1013.5078)
            self.set_facing_angle(90.0)
            self.set_camera_behind()
            self.set_interior(2)

        if pickup.id == gangs[0].enter_exit[1].id: # Grove exit
            if not self.gang_id == gangs[0].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2495.3022, -1688.5438, 13.8722)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_interior(0)

        if pickup.id == gangs[1].enter_exit[0].id: # Ballas enter
            if not self.gang_id == gangs[1].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(-42.6860, 1408.4878, 1084.4297)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_interior(8)

        if pickup.id == gangs[1].enter_exit[1].id: # Ballas exit
            if not self.gang_id == gangs[1].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2022.9169, -1122.7472, 26.2329)
            self.set_camera_behind()
            self.set_interior(0)

        if pickup.id == gangs[2].enter_exit[0].id: # Vagos enter
            if not self.gang_id == gangs[2].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(318.564971, 1118.209960, 1083.882812)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_interior(5)

        if pickup.id == gangs[2].enter_exit[1].id: # Vagos exit
            if not self.gang_id == gangs[2].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2756.1492, -1180.2386, 69.3978)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_interior(0)

        if pickup.id == gangs[3].enter_exit[0].id: # Aztecas enter
            if not self.gang_id == gangs[3].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(223.0174, 1240.1416, 1082.1406)
            self.set_facing_angle(270.0)
            self.set_camera_behind()
            self.set_interior(2)

        if pickup.id == gangs[3].enter_exit[1].id: # Aztecas exit
            if not self.gang_id == gangs[3].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2185.6555, -1812.5112, 13.5650)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_interior(0)

        if pickup.id == gangs[4].enter_exit[0].id: # Rifa enter
            if not self.gang_id == gangs[4].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(-68.9146, 1353.8420, 1080.2109)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_interior(6)

        if pickup.id == gangs[4].enter_exit[1].id: # Rifa exit
            if not self.gang_id == gangs[4].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2784.5544, -1926.1563, 13.5469)
            self.set_facing_angle(90.0)
            self.set_camera_behind()
            self.set_interior(0)

        if pickup.id in houses_by_pickup:
            house = houses_by_pickup[pickup.id]
            if not self.house and house.is_locked:
                return self.send_error_message("Дом закрыт!")

            return Dialogs.show_house_info_dialog(self, pickup.id)

    def on_enter_checkpoint_handle(self, checkpoint: DynamicCheckpoint) -> None:
        self.kick_if_not_logged()
        if checkpoint.id == gangs[0].warehouse.id: # Grove
            return Dialogs.show_warehouse_dialog(self)

        if checkpoint.id == gangs[1].warehouse.id: # Ballas
            return Dialogs.show_warehouse_dialog(self)

        if checkpoint.id == gangs[2].warehouse.id: # Vagos
            return Dialogs.show_warehouse_dialog(self)

        if checkpoint.id == gangs[3].warehouse.id: # Aztecas
            return Dialogs.show_warehouse_dialog(self)

        if checkpoint.id == gangs[4].warehouse.id: # Rifa
            return Dialogs.show_warehouse_dialog(self)

    def on_update_handle(self) -> None:
        self.time.afk = 0
        return True

    def on_damage_handler(self, issuer: "Player", amount: float, weapon_id: int, body_part) -> None:
        self.play_sound(17802, 0.0, 0.0, 0.0)
        x, y, z, to_x, to_y, to_z = self.get_last_shot_vectors()
        damage_informer = create_player_3d_text_label(self.id, f"{int(amount)}", Colors.white, to_x, to_y, to_z, 150)
        return set_timer(delete_player_3d_text_label, 1000, False, self.id, damage_informer)

    def on_key_state_change_handle(self, new_keys: int, old_keys: int) -> None:
        self.kick_if_not_logged()
        if (old_keys == 65536) and (new_keys == 0):
            return Dialogs.show_mn_dialog(self)

        if self.get_state() == PLAYER_STATE_DRIVER and old_keys == 1:
            if self.vehicle.inst.is_car:
                if self.vehicle.inst.engine == 1:
                    self.vehicle.inst.engine = 0
                else:
                    self.vehicle.inst.engine = 1

                self.update_speedometer_sensors(self.vehicle.inst)
                return self.vehicle.inst.set_params_ex(
                    self.vehicle.inst.engine,
                    self.vehicle.inst.lights,
                    0,
                    0,
                    0,
                    0,
                    0
                )

        if self.get_state() == PLAYER_STATE_DRIVER and old_keys == 4:
            if self.vehicle.inst.is_car:
                if self.vehicle.inst.lights == 1:
                    self.vehicle.inst.lights = 0
                else:
                    self.vehicle.inst.lights = 1

                self.update_speedometer_sensors(self.vehicle.inst)
                return self.vehicle.inst.set_params_ex(
                    self.vehicle.inst.engine,
                    self.vehicle.inst.lights,
                    0,
                    0,
                    0,
                    0,
                    0
                )

        if self.get_state() == PLAYER_STATE_DRIVER and self.mode == ServerMode.freeroam_world:
            if new_keys == 1 or new_keys == 9 or new_keys == 33 and old_keys != 1 or old_keys != 9 or old_keys != 33:
                if self.vehicle.inst.is_car:
                    self.vehicle.inst.add_component(1010)

        if new_keys == 1024 and old_keys != 1024:
            if self.checks.in_house:
                if self.house.owner == self.name:
                    return Dialogs.show_house_menu_dialog(self)

                self.checks.in_house = False
                self.set_mode(ServerMode.freeroam_world)
                self.set_interior(0)
                return self.set_pos(
                    self.house.pos_x,
                    self.house.pos_y,
                    self.house.pos_z
                )

    def on_state_change_handle(self, new_state: int, old_state: int) -> None:
        if new_state == PLAYER_STATE_DRIVER:
            self.send_notification_message(f"Чтобы завести авто используйте {{{Colors.cmd_hex}}}LCTRL{{{Colors.white_hex}}}.")
            vehicle = Vehicle.get_from_registry(self.get_vehicle_id())
            self.update_vehicle_inst(vehicle)
            self.send_debug_message("on_state_change_handle", f"Player: {self} | Vehicle: {self.vehicle.inst.id} | In")
            if self.vehicle.inst.is_car:
                self.create_speedometer()
                self.show_speedometer()
                self.vehicle_speedometer[5] = set_timer(self.update_speedometer_velocity, 200, True, self.vehicle.inst)
                if self.mode == ServerMode.freeroam_world:
                    self.create_drift_counter()
            else:
                return self.vehicle.inst.set_params_ex(
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                )

        if new_state == PLAYER_STATE_ONFOOT and old_state == PLAYER_STATE_DRIVER:
            self.send_debug_message("on_state_change_handle", f"Player: {self} | Vehicle: {self.vehicle.inst.id} | Out")
            if self.vehicle.inst.is_car:
                kill_timer(self.vehicle_speedometer[5])
                self.hide_speedometer()
                if self.mode == ServerMode.freeroam_world:
                    self.destroy_drift_counter()

            else:
                return self.vehicle.inst.set_params_ex(
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                )

    def on_start_drift_handle(self) -> None:
        if self.mode == ServerMode.freeroam_world:
            return self.show_drift_counter()

    def on_drift_update_handle(self, value: int, combo: int, flag_id: int, distance: float, speed: float) -> None:
        if self.mode == ServerMode.freeroam_world:
            if not self.time.afk >= 1 and self.vehicle.inst.is_car:
                return self.update_drift_counter(value)
    def on_end_drift_handle(self, value: int, combo: int, reason: int) -> None:
        if self.mode == ServerMode.freeroam_world:
            return self.hide_drift_counter()


@Player.on_connect
@Player.using_registry
def on_player_connect(player: Player) -> None:
    player.send_debug_message("on_player_connect", f"Player: {player}")
    if player.is_connected():
        DataBase.update_analytics()
        remove_objects_for_player(player)
        for i in range(25):
            player.send_notification_message(" ")

        player.toggle_clock(False)
        player.send_notification_message(f"Добро пожаловать на сервер {{{Colors.cmd_hex}}}{ServerInfo.name_short}{{{Colors.white_hex}}}!")
        player.send_notification_message(f"Версия: {{{Colors.cmd_hex}}}{__version__}{{{Colors.white_hex}}}!")
        player.send_notification_message(f"Created by: {{{Colors.vagos_hex}}}Ykpauneu{{{Colors.white_hex}}} & {{{Colors.rifa_hex}}}Rein.{{{Colors.white_hex}}}!")
        player.send_notification_message(f"Сервер посетили: {{{Colors.cmd_hex}}}{DataBase.get_analytics()}{{{Colors.white_hex}}} игроков.")
        player.show_server_logotype()
        player.show_ping_textdraw()
        player.timers.every_sec = set_timer(player.every_second, 1000, True)
        player.toggle_spectating(True)
        player_db = DataBase.get_player(player)
        if not player_db:
            return Dialogs.show_registration_dialog(player)

        if not player_db.is_banned:
            if player.get_ip() == player_db.registration_ip:
                player.send_notification_message("Вы автоматически авторизовались!")
                return player.set_data_after_login(player_db)

            return Dialogs.show_login_dialog(player)

        return player.ban_from_server()

@Player.on_disconnect
@Player.using_registry
def on_player_disconnect(player: Player, reason: int) -> None:
    if player.vip.is_random_clist_enabled:
        kill_timer(player.vip.random_clist_timer_id)

    if player.vehicle.inst:
        player.vehicle.inst.set_owner(NO_VEHICLE_OWNER)

    DeathMatch.disable_timer_for_player(player)
    kill_timer(player.timers.every_sec)
    if player.checks.logged:
        DataBase.save_player(
            player,
            password=player.password,
            email=player.email,
            pin=player.pin,
            last_ip=player.last_ip,
            score=player.score,
            money=player.money,
            donate=player.donate,
            dm_rating=player.dm_rating,
            kills=player.kills,
            deaths=player.deaths,
            heals=player.heals,
            masks=player.masks,
            gang_id=player.gang_id,
            vip_level=player.vip.level,
            admin_level=player.admin.level,
            is_muted=player.checks.muted,
            is_jailed=player.checks.jailed,
            is_banned=player.checks.banned,
            jail_time=player.time.jail,
            mute_time=player.time.mute
            )

        DataBase.save_freeroam_gun_slots(
            player,
            slot_melee=player.gun_slots.melee,
            slot_pistol=player.gun_slots.pistol,
            slot_shotgun=player.gun_slots.shotgun,
            slot_machine_gun=player.gun_slots.machine_gun,
            slot_assault_rifle=player.gun_slots.assault_rifle,
            slot_long_rifle=player.gun_slots.long_rifle,
        )

        DataBase.save_player_settings(
            player,
            disabled_ping_td=player.settings.disabled_ping_td,
            disabled_global_chat_gw=player.settings.disabled_global_chat_gw,
            spawn_in_house=player.settings.spawn_in_house
        )

    return Player.delete_registry(player)

@Player.on_request_class
@Player.using_registry
def on_player_request_class(player: Player, class_id: int) -> None:
    player.send_debug_message("on_request_class_handle", f"Player: {player} | Class: {class_id}")
    player.kick_if_not_logged()
    if player.checks.selected_skin:
        return player.spawn()

    player.set_mode(ServerMode.default_world)
    player.set_mode(randint(100, 500))
    player.toggle_controllable(False)
    player.set_pos(204.6633, -6.5563, 1001.2109)
    player.set_facing_angle(299.4084)
    player.set_camera_position(208.7765, -3.9595, 1001.2178)
    player.set_camera_look_at(204.6633, -6.5563, 1001.2109)
    player.set_interior(5)
    player.set_mode(ServerMode.any())
    DeathMatch.disable_timer_for_player(player)
    player.cache["CLASS_ID"] = class_id
    return True

@Player.on_request_spawn
@Player.using_registry
def on_player_request_spawn(player: Player) -> None:
    player.kick_if_not_logged()
    player.checks.selected_skin = True
    player.set_mode(ServerMode.freeroam_world)
    player.set_skin_ex(player.cache["CLASS_ID"])
    del player.cache["CLASS_ID"]


@Player.on_spawn
@Player.using_registry
def on_player_spawn(player: Player) -> None:
    player.send_debug_message("on_spawn_handle", f"Player: {player} | Mode: {player.get_virtual_world()} | Interior {player.get_interior()}")
    if player.mode == ServerMode.gangwar_world:
        return GangWar.enable_mode_for_player(player)

    if player.mode == ServerMode.freeroam_world:
        return Freeroam.enable_mode_for_player(player)

    if player.mode == ServerMode.jail_world:
        return player.enable_jail_mode()

    if player.mode in ServerMode.deathmatch_worlds:
        return DeathMatch.enable_mode_for_player(player)

@Player.on_click_map
@Player.using_registry
def on_player_click_map(player: Player, x: float, y: float, z: float) -> None:
    if player.mode == ServerMode.freeroam_world and player.vip.level >= 1:
        return player.set_pos(x, y, z)


@Player.on_death
@Player.using_registry
def on_player_death(player: Player, killer: Player, reason: int) -> None:
    killer = Player.from_registry_native(killer)
    player.send_debug_message("on_death_handle", f"Player: {player} | Killer: {killer}")
    player.kick_if_not_logged()
    player.deaths += 1
    if player.mode == ServerMode.gangwar_world or player.mode == ServerMode.gangwar_world:
        player.masks = 0
        player.heals = 0
        GangWar.set_spawn_info_for_player(player)

    if player.mode == ServerMode.freeroam_world:
        if player.checks.in_house:
            player.checks.in_house = False

        Freeroam.set_spawn_info_for_player(player)
        player.send_death_message(killer, player, reason)
        killer.send_death_message(killer, player, reason)

    if player.mode in ServerMode.deathmatch_worlds:
        DeathMatch.disable_timer_for_player(player)
        DeathMatch.set_spawn_info_for_player(player)
        player.send_death_message(killer, player, reason)
        player.set_dm_rating(randint(1, 15), increase=False)
        killer.send_death_message(killer, player, reason)
        need_restore = 100 - killer.get_health()
        if need_restore != 0.0:
            killer.set_health(killer.get_health() + need_restore)

        killer.set_dm_rating(randint(1, 15))
        DeathMatch.give_guns_for_player(killer)

    if player.mode == ServerMode.jail_world:
        return player.set_jail_spawn_info()

    if killer.id == INVALID_PLAYER_ID:
        return player.delete_registry(killer)

    killer.kills += 1
    killer.set_money_ex(1000)
    killer.set_score(killer.kills)
    if killer.gang.is_capturing:
        if killer.gang.capture_id == player.gang.capture_id:
            gz = gangzone_pool[killer.gang.capture_id]
            if killer.gang.gang_id == gz.gang_atk_id:
                gz.gang_atk_score += 1
            else:
                gz.gang_def_score += 1
            killer.send_death_message(killer, player, reason)
            player.send_death_message(killer, player, reason)



































class Dialogs:
    @classmethod
    def show_kick_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(0, "[ОШИБКА]", "Для игры на сервере необходимо пройти регистрацию/авторизацию.", "Закрыть", "").show(player)

    @classmethod
    def show_kick_teamkill(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(0, "[ОШИБКА]", "Вы были кикнуты. Убийство союзников - запрещено!.", "Закрыть", "").show(player)

    @classmethod
    def show_banned_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(0, "[ОШИБКА]", "Вы забанены на этом сервере!", "Закрыть", "").show(player)

    @classmethod
    def show_credits_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(
            0,
            "О проекте",
            f"San Andreas {{{Colors.red_hex}}}Gang War\n\n{{{Colors.dialog_hex}}}Разработчик:\t{{{Colors.vagos_hex}}}Ykpauneu\n{{{Colors.dialog_hex}}}Тестировщик:\t{{{Colors.rifa_hex}}}Rein.{{{Colors.dialog_hex}}}\n\nВерсия:\t{{{Colors.cmd_hex}}}{__version__}",
            "Закрыть",
            ""
        ).show(player)

    @classmethod
    def show_warehouse_dialog(cls, player) -> int:
        player = Player.from_registry_native(player)
        return Dialog.create(2, f"Склад банды {player.gang.gang_name}.", "1. Аптечка\n2. Маска\n3. Оружие", "Ок", "Закрыть", on_response=cls.warehouse_response).show(player)

    @classmethod
    def warehouse_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if list_item == 0: # Heals
            if player.heals < 3:
                player.heals = 3
                player.send_notification_message(f"Вы взяли {{{Colors.cmd_hex}}}3{{{Colors.white_hex}}} аптечки. Используйте {{{Colors.cmd_hex}}}/healme{{{Colors.white_hex}}} для применения аптечки.")
                return cls.show_warehouse_dialog(player)

            else:
                return player.send_error_message("У Вас уже есть аптечки!")

        if list_item == 1: # Masks
            if player.masks < 3:
                player.masks = 3
                player.send_notification_message(f"Вы взяли {{{Colors.cmd_hex}}}3{{{Colors.white_hex}}} маски. Используйте {{{Colors.cmd_hex}}}/mask{{{Colors.white_hex}}} для применения маски.")
                return cls.show_warehouse_dialog(player)

            else:
                return player.send_error_message("У Вас уже есть маски!")

        if list_item == 2: # Guns
            return Dialog.create(
                2, "Выбор оружия",
                "1. Desert Eagle\n2. Shotgun\n3. AK-47\n4. M4\n5. Rifle\n6. Бита",
                "Ок",
                "Закрыть",
                on_response=cls.warehouse_gun_response
                ).show(player)

    @classmethod
    def warehouse_gun_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_warehouse_dialog(player)

        if list_item == 0:
            _weapon, ammo = player.get_weapon_data(2)
            if ammo == 300:
                return player.send_error_message("Вы не можете взять больше!")

            player.give_weapon(24, 100)
            player.send_notification_message(f"Вы взяли {{{Colors.cmd_hex}}}Desert Eagle{{{Colors.white_hex}}}.")

        if list_item == 1:
            _weapon, ammo = player.get_weapon_data(3)
            if ammo == 300:
                return player.send_error_message("Вы не можете взять больше!")

            player.give_weapon(25, 100)
            player.send_notification_message(f"Вы взяли {{{Colors.cmd_hex}}}Shotgun{{{Colors.white_hex}}}.")

        if list_item == 2:
            _weapon, ammo = player.get_weapon_data(5)
            if ammo == 300:
                return player.send_error_message("Вы не можете взять больше!")

            player.give_weapon(30, 100)
            player.send_notification_message(f"Вы взяли {{{Colors.cmd_hex}}}AK-47{{{Colors.white_hex}}}.")

        if list_item == 3:
            _weapon, ammo = player.get_weapon_data(5)
            if ammo == 300:
                return player.send_error_message("Вы не можете взять больше!")

            player.give_weapon(31, 100)
            player.send_notification_message(f"Вы взяли {{{Colors.cmd_hex}}}M4{{{Colors.white_hex}}}.")

        if list_item == 4:
            _weapon, ammo = player.get_weapon_data(6)
            if ammo == 300:
                return player.send_error_message("Вы не можете взять больше!")

            player.give_weapon(33, 100)
            player.send_notification_message(f"Вы взяли {{{Colors.cmd_hex}}}Rifle{{{Colors.white_hex}}}.")

        if list_item == 5:
            player.give_weapon(5, 1)
            player.send_notification_message(f"Вы взяли {{{Colors.cmd_hex}}}Baseball Bat{{{Colors.white_hex}}}.")

        return cls.show_warehouse_dialog(player)

    @classmethod
    def show_login_dialog(cls, player: Player) -> int:
        player = Player.from_registry_native(player)
        player.cache["LOGIN_ATTEMPTS"] = 0
        return Dialog.create(
            1, f"{ServerInfo.name_short} | Авторизация",
            f"{player.get_name()}, добро пожаловать!\nВведите пароль:",
            "Ок",
            "",
            on_response=cls.login_response
            ).show(player)

    @classmethod
    def login_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return player.kick_if_not_logged()

        if player.cache["LOGIN_ATTEMPTS"] == 3:
            return player.kick_if_not_logged()

        if len(input_text) < 6 or len(input_text) > 32:
            player.cache["LOGIN_ATTEMPTS"] += 1
            player.send_error_message("Длина пароля должна быть от 6 и до 32 символов!")
            return cls.show_login_dialog(player)

        player_db = DataBase.get_player(player)
        if input_text != player_db.password:
            player.cache["LOGIN_ATTEMPTS"] += 1
            player.send_error_message(f"Вы указали неверный пароль ({player.cache['LOGIN_ATTEMPTS']}/3)")
            return cls.show_login_dialog(player)

        del player.cache["LOGIN_ATTEMPTS"]
        if player_db.pin:
            return cls.show_pin_dialog(player)

        return player.set_data_after_login(player_db)

    @classmethod
    def show_pin_dialog(cls, player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            3,
            f"{ServerInfo.name_short} | Авторизация",
            "Вы указали дополнитулью защиту, введите PIN код:",
            "Ок",
            "",
            on_response=cls.pin_response
        ).show(player)


    @classmethod
    def pin_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return player.kick_if_not_logged()

        return player.set_data_after_login(DataBase.get_player(player))

    @classmethod
    def show_registration_dialog(cls, player) -> int:
        player = Player.from_registry_native(player)
        return Dialog.create(1, f"{ServerInfo.name_short} | Регистрация", f"{player.get_name()}, добро пожаловать на проект {ServerInfo.name_short}\nДля игры необходимо пройти регистрацию\nПридумайте пароль:", "Ок", "", on_response=cls.registration_response).show(player)

    @classmethod
    def registration_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return player.kick_if_not_logged()

        if len(input_text) < 6 or len(input_text) > 32:
            player.send_error_message("Длина пароля должна быть от 6 и до 32 символов!")
            return cls.show_registration_dialog(player)

        player.password = input_text
        return cls.show_email_dialog(player)

    @classmethod
    def show_email_dialog(cls, player) -> int:
        player = Player.from_registry_native(player)
        return Dialog.create(1, f"{ServerInfo.name_short} | E-mail", f"Вы можете указать Ваш e-mail\nВ случае потери доступа к аккаунту, Вы сможете получить код восстановления\nВведите почту:", "Ок", "Позже",on_response=cls.email_response).show(player)

    @classmethod
    def email_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None: # Register
        player = Player.from_registry_native(player)
        if not response:
            player.email = ""
            player.send_notification_message("Вы пропустили этот шаг.")

        else:
            if len(input_text) < 6 or len(input_text) > 32:
                player.send_error_message("Длина почты должна быть от 6 и до 32 символов!")
                return cls.show_email_dialog(player)

            player.email = input_text

        player.play_sound(1052, x=0.0, y=0.0, z=0.0)
        player.pin = ""
        player.checks.logged = True
        player.registration_ip = player.get_ip()
        player.registration_data = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        player.reset_money()
        player.set_money_ex(100000, show_text=False)
        DataBase.create_player(player)
        return cls.show_select_mode_dialog(player)

    @classmethod
    def show_gang_choice_dialog(cls, player: Player) -> int:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2, f"{ServerInfo.name_short} | Банда",
            "Grove Street Families\nThe Ballas\nLos Santos Vagos\nVarrios Los Aztecas\nLos Santos Rifa",
            "Ок",
            "",
            on_response=cls.gang_choice_response
            ).show(player)

    @classmethod
    def gang_choice_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            player.send_error_message("Необходимо выбрать группировку!")
            return cls.show_gang_choice_dialog(player)

        player.gang_id = list_item
        player.gang = gangs[player.gang_id]
        player.spawn()

    @classmethod
    def show_select_deathmatch_dialog(cls, player: Player) -> int:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Выбор карты",
            "Деревня (CJ + Sawn-off)\nДеревня (Deagle)\nДеревня\nФерма\nЗаброшенная деревня\nЗавод КАСС",
            "Ок",
            "",
            on_response=cls.select_deathmatch_response
        ).show(player)

    @classmethod
    def select_deathmatch_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            player.send_error_message("Необходимо выбрать карту!")
            return cls.show_select_deathmatch_dialog(player)

        if list_item == 0:
            list_mode = ServerMode.deathmatch_world_shotgun

        if list_item == 1:
            list_mode = ServerMode.deathmatch_world_oc_deagle

        if list_item == 2:
            list_mode = ServerMode.deathmatch_world_old_country

        if list_item == 3:
            list_mode = ServerMode.deathmatch_world_farm

        if list_item == 4:
            list_mode = ServerMode.deathmatch_world_abandoned_country

        if list_item == 5:
            list_mode = ServerMode.deathmatch_world_kass

        player.set_mode(list_mode)
        player.spawn()
        if list_mode == ServerMode.deathmatch_world_shotgun:
            player.set_skin_ex(0)
            return DeathMatch.enable_mode_for_player(player)

        return DeathMatch.enable_mode_for_player(player)

    @classmethod
    def show_command_gang_choice_dialog(cls, player) -> int:
        player = Player.from_registry_native(player)
        return Dialog.create(2, f"{ServerInfo.name_short} | Банда", "Grove Street Families\nThe Ballas\nLos Santos Vagos\nVarrios Los Aztecas\nLos Santos Rifa", "Ок", "", on_response=cls.command_gang_choice_response).show(player)

    @classmethod
    def command_gang_choice_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        player.gang_id = list_item
        player.gang = gangs[player.gang_id]
        player.set_mode(ServerMode.gangwar_world)
        return GangWar.enable_mode_for_player(player)

    @classmethod
    def show_stats_dialog(cls, show_to: Player, player_id: int = None) -> Dialog:
        player_stats = Player.from_registry_native(player_id)
        key, value = player_stats.get_gang_rang()
        ratio = player_stats.kills / player_stats.deaths if player_stats.kills and player_stats.deaths != 0 else 0.0
        level = int(sqrt(player_stats.score) / 2)
        next_lvl_exp = int((2 * ((level + 1))) ** 2)
        return Dialog.create(
            0,
            f"Статистика игрока {player_stats.get_name()}",
            (
                f"Ник:\t\t\t\t{{{Colors.cmd_hex}}}{player_stats.get_name()}{{{Colors.dialog_hex}}}\n"
                f"DM-Рейтинг:\t\t\t{{{player_stats.get_dm_color()}}}{player_stats.dm_rating:,} {{{Colors.dialog_hex}}}\n"
                f"Уровень:\t\t\t{{{Colors.cmd_hex}}}{level}{{{Colors.dialog_hex}}} ({player_stats.score}/{next_lvl_exp})\n"
                f"Счёт:\t\t\t\t{{{Colors.cmd_hex}}}{player_stats.score}{{{Colors.dialog_hex}}}\n"
                f"Баланс:\t\t\t{{{Colors.green_hex}}}{player_stats.money}${{{Colors.dialog_hex}}}\n"
                f"Донат:\t\t\t\t{{{Colors.cmd_hex}}}{player_stats.donate}{{{Colors.dialog_hex}}}\n"
                f"Ранг:\t\t\t\t{value} ({{{Colors.green_hex}}}{player_stats.kills}{{{Colors.dialog_hex}}}/{key})\n"
                f"Группировка:\t\t\t{{{player_stats.gang.color_hex}}}{player_stats.gang.gang_name}{{{Colors.dialog_hex}}}\n"
                f"Убийств:\t\t\t{{{Colors.green_hex}}}{player_stats.kills}{{{Colors.dialog_hex}}}\n"
                f"Смертей:\t\t\t{{{Colors.red_hex}}}{player_stats.deaths}{{{Colors.dialog_hex}}}\n"
                f"K/D:\t\t\t\t{{{Colors.cmd_hex}}}{round(ratio, 00)}{{{Colors.dialog_hex}}}\n"
                f"Аптечек:\t\t\t{{{Colors.cmd_hex}}}{player_stats.heals}{{{Colors.dialog_hex}}}\n"
                f"Масок:\t\t\t\t{{{Colors.cmd_hex}}}{player_stats.masks}{{{Colors.dialog_hex}}}\n"
                f"Есть VIP:\t\t\t{{{Colors.cmd_hex}}}{'Есть' if player_stats.vip.level != -1 else 'Нет'}{{{Colors.dialog_hex}}}\n"
                f"Выдан мут:\t\t\t{{{Colors.cmd_hex}}}{'Да' if player_stats.checks.muted else 'Нет'}{{{Colors.dialog_hex}}}"
            ),
            "Закрыть",
            "").show(Player.from_registry_native(show_to))

    @classmethod
    def show_gangzone_choice_dialog(cls, player: Player, turf_id: int) -> Dialog:
        player = Player.from_registry_native(player)
        player._gz_choice = turf_id
        return Dialog.create(2, f"Список территорий", "Проложить GPS", "Ок", "Закрыть", on_response=cls.gangzone_choice_response).show(player)

    @classmethod
    def gangzone_choice_response(cls, player: Player, response: int, list_item: int, input_text: str) -> Dialog:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_gangzones_dialog_page_one(player)

        if player.get_virtual_world() == ServerMode.gangwar_world:
            return player.send_error_message("Использовать команду можно только вне дома!")

        gangzone = DataBase.load_gangzone(player._gz_choice)
        x, y = get_center(gangzone.min_x, gangzone.max_x, gangzone.min_y, gangzone.max_y)
        player.send_notification_message(f"Маршрут GPS построен. Используйте {{{Colors.cmd_hex}}}/gps{{{Colors.white_hex}}}, для отключения.")
        return player.set_checkpoint_to_gangzone(x, y, 0)

    @classmethod
    def show_gangzones_dialog_page_one(cls, player) -> Dialog:
        player = Player.from_registry_native(player)
        tab_list = player._get_tab_list_header(0, 91)
        return Dialog.create(
            5,
            "Список территорий",
            f"Владелец\tID\tДо атаки\n{tab_list}\n>>>",
            "Выбрать",
            "Закрыть",
            on_response=cls.show_gangzones_response_page_one
        ).show(player)

    @classmethod
    def show_gangzones_response_page_one(cls, player: Player, response: int, list_item: int, input_text: str) -> Dialog:
        player = Player.from_registry_native(player)
        if not response: # List item: id, input_text = gang name
            return

        if input_text == ">>>":
            tab_list = player._get_tab_list_header(91)
            return Dialog.create(
                5,
                "Список территорий",
                f"Владелец\tID\tДо атаки\n{tab_list}\n<<<",
                "Выбрать",
                "Закрыть",
                on_response=cls.show_gangzones_response_page_two
            ).show(player)

        return cls.show_gangzone_choice_dialog(player, list_item)

    @classmethod
    def show_gangzones_response_page_two(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if input_text == "<<<":
            return cls.show_gangzones_dialog_page_one(player)

        return cls.show_gangzone_choice_dialog(player, list_item)

    @classmethod
    def show_start_capture_dialog(cls, player: Player, atk_id: int, def_id: int, gangzone_id: int):
        player = Player.from_registry_native(player)
        zone_id = player.get_pos_zone_name()
        GangWar.capture_dict[player.name] = (player.name, atk_id, def_id, gangzone_id, ZoneNames.names[zone_id])
        return Dialog.create(
            0,
            "Захват территории",
            f"Владелец:\t{{{gangs[def_id].color_hex}}}{gangs[def_id].gang_name}\n{{{Colors.dialog_hex}}}Территория:\t{{{Colors.cmd_hex}}}{ZoneNames.names[zone_id]}",
            "Ок",
            "Закрыть",
            on_response=cls.start_capture_response).show(player)

    @classmethod
    def start_capture_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            del GangWar.capture_dict[player.name]
            return player.send_notification_message("Вы отменили захват территории.")

        gangs[GangWar.capture_dict[player.name][1]].capture_id = GangWar.capture_dict[player.name][3]
        gangs[GangWar.capture_dict[player.name][2]].capture_id = GangWar.capture_dict[player.name][3]
        gangs[GangWar.capture_dict[player.name][1]].is_capturing = True
        gangs[GangWar.capture_dict[player.name][2]].is_capturing = True
        _capture = GangWar.capture_dict[player.name]

        player.send_debug_message("start_capture_response", f"{Player._registry.values()}")
        for player_reg in Player._registry.values():
            if player_reg.mode != ServerMode.gangwar_world:
                continue

            if player_reg.gang_id == gangs[_capture[1]].gang_id or player_reg.gang_id == gangs[_capture[2]].gang_id:
                GangWar.send_capture_message(player, player_reg)

        return GangWar.start_capture(player, player._registry)

    @classmethod
    def show_mn_dialog(cls, player) -> Dialog:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Меню игрока",
            f"1. Статистика\n2. Список команд\n3. Выбрать режим\n4. Настройки аккаунта\n5. Связь с администрацией\n6. Донат\n7. О проекте",
            "Ок",
            "Закрыть",
            on_response=cls.mn_response).show(player)

    @classmethod
    def mn_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if list_item == 0:
            return cls.show_stats_dialog(player, player_id=player.id)

        if list_item == 1:
            return cls.show_commands_list_dialog(player)

        if list_item == 2:
            return cls.show_select_mode_dialog(player)

        if list_item == 3:
            return cls.show_account_settings_dialog(player)

        if list_item == 4:
            return cls.show_admin_ask_dialog(player)

        if list_item == 5:
            return cls.show_donation_dialog(player)

        if list_item == 6:
            return cls.show_credits_dialog(player)

    @classmethod
    def show_commands_list_dialog(cls, player: Player) -> Dialog:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Список команд",
            "1. Общие команды\n2. GangWar команды\n3. Freeroam команды\n4. VIP команды",
            "Ок",
            "Назад",
            on_response=cls.commands_list_response
        ).show(player)

    @classmethod
    def commands_list_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_mn_dialog(player)

        commands_str = ""
        if list_item == 0:
            for command_name, command_params in commands.items():
                if command_params[1] == CommandType.all_types:
                    commands_str += f"{{{Colors.cmd_hex}}}{command_name}\t{{{Colors.dialog_hex}}}{command_params[0]}\n"

        if list_item == 1:
            for command_name, command_params in commands.items():
                if command_params[1] == CommandType.gangwar_type:
                    commands_str += f"{{{Colors.cmd_hex}}}{command_name}\t{{{Colors.dialog_hex}}}{command_params[0]}\n"

        if list_item == 2:
            for command_name, command_params in commands.items():
                if command_params[1] == CommandType.freeroam_type:
                    commands_str += f"{{{Colors.cmd_hex}}}{command_name}\t{{{Colors.dialog_hex}}}{command_params[0]}\n"

        if list_item == 3:
            for command_name, command_params in commands.items():
                if command_params[1] == CommandType.vip_type:
                    commands_str += f"{{{Colors.cmd_hex}}}{command_name}\t{{{Colors.dialog_hex}}}{command_params[0]}\n"

        return Dialog.create(
            5, "Список команд",
            f"Команда\tОписание\n{commands_str}",
            "Закрыть",
            "").show(player)

    @classmethod
    def show_select_mode_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Выбрать режим",
            "GangWar\nFreeroam\nDeathmatch",
            "Ок",
            "",
            on_response=cls.select_mode_response,
        ).show(player)

    @classmethod
    def select_mode_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            player.send_error_message("Необходимо выбрать режим!")
            return cls.show_select_mode_dialog(player)

        if list_item == 0:
            if player.mode == ServerMode.gangwar_world:
                return player.send_error_message("Вы уже выбрали этот режим!")

            player.set_mode(ServerMode.gangwar_world)
            player.send_notification_message(f"Вы выбрали режим {{{Colors.cmd_hex}}}GangWar{{{Colors.white_hex}}}!")
            return cls.show_gang_choice_dialog(player)

        if list_item == 1:
            if player.mode == ServerMode.freeroam_world:
                return player.send_error_message("Вы уже выбрали этот режим!")

            player.checks.selected_skin = False
            player.force_class_selection()
            player.toggle_spectating(True)
            player.toggle_spectating(False)
            player.send_notification_message(f"Вы выбрали режим {{{Colors.cmd_hex}}}Freeroam{{{Colors.white_hex}}}!")

        if list_item == 2:
            if player.mode in ServerMode.deathmatch_worlds:
                return cls.show_select_deathmatch_dialog(player)

            player.send_notification_message(f"Вы выбрали режим {{{Colors.cmd_hex}}}Deathmatch{{{Colors.white_hex}}}!")
            return cls.show_select_deathmatch_dialog(player)

    @classmethod
    def show_account_settings_dialog(cls, player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Настройки аккаунта",
            (
                f"1. Изменить e-mail\n"
                f"2. Изменить PIN код\n"
                f"3. {'Включить' if player.settings.disabled_ping_td else 'Отключить'} показание пинга\n"
                f"4. {'Отключить' if player.settings.disabled_global_chat_gw else 'Включить'} глобальный чат в режиме GangWar по умолчанию\n"
                f"5. {'Отключить' if player.settings.spawn_in_house else 'Включить'} спавн в доме по умолчанию\n"

            ),
            "Ок",
            "Назад",
            on_response=cls.privacy_settings_response
        ).show(player)

    @classmethod
    def privacy_settings_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_mn_dialog(player)

        if list_item == 0:
            return cls.show_email_privacy_dialog(player)

        if list_item == 1:
            return cls.show_pin_privacy_dialog(player)

        if list_item == 2:
            if player.settings.disabled_ping_td:
                player.settings.disabled_ping_td = False
                player.show_ping_textdraw()

            else:
                player.settings.disabled_ping_td = True
                player.hide_ping_textdraw()

            return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}{'отключили' if player.settings.disabled_ping_td else 'включили'}{{{Colors.white_hex}}} показание пинга.")

        if list_item == 3:
            if player.settings.disabled_global_chat_gw:
                player.settings.disabled_global_chat_gw = False

            else:
                player.settings.disabled_global_chat_gw = True

            return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}{'включили' if player.settings.disabled_global_chat_gw else 'отключили'}{{{Colors.white_hex}}} глобальный чат по умолчанию в режиме {{{Colors.cmd_hex}}}GangWar{{{Colors.white_hex}}}.")

        if list_item == 4:
            if player.settings.spawn_in_house:
                player.settings.spawn_in_house = False

            else:
                player.settings.spawn_in_house = True

            return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}{'включили' if player.settings.spawn_in_house else 'отключили'}{{{Colors.white_hex}}} спавн в доме по умолчанию.")

    @classmethod
    def show_email_privacy_dialog(cls, player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            1,
            "Изменение e-mail",
            "Укажите новый e-mail:",
            "Ок",
            "Назад",
            on_response=cls.email_privacy_response
        ).show(player)

    @classmethod
    def email_privacy_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_mn_dialog(player)

        if len(input_text) < 6 or len(input_text) > 32:
            return player.send_error_message("Длина почты должна быть от 6 и до 32 символов!")

        player.email = input_text
        return player.send_notification_message("Вы успешно изменили свой e-mail!")

    @classmethod
    def show_pin_privacy_dialog(cls, player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            1,
            "Изменение PIN кода",
            "Укажите новый PIN код:",
            "Ок",
            "Назад",
            on_response=cls.pin_privacy_response
        ).show(player)

    @classmethod
    def pin_privacy_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_mn_dialog(player)

        if len(input_text) > 6:
            return player.send_error_message("Длина PIN кода должна быть от до 6 символов!")

        player.pin = input_text
        return player.send_notification_message("Вы успешно изменили свой PIN код!")

    @classmethod
    def show_admin_ask_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(
            1,
            "Связь с Администрацией",
            "Введите Ваш вопрос/жалобу:",
            "Ок",
            "Закрыть",
            on_response=cls.admin_ask_response
        ).show(player)

    @classmethod
    def admin_ask_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_mn_dialog(player)

        if not input_text:
            return player.send_error_message("Вы не указали сообщение!")

        player.send_report_message(player, input_text)
        return player.send_notification_message("Ваше сообщение было отправлено!")

    @classmethod
    def show_donation_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Донат",
            (
                f"Остаток на счету: {{{Colors.cmd_hex}}}{player.donate}{{{Colors.dialog_hex}}}\n"
                f"Купить {{{VIPData.colors[0]}}}BRONZE VIP{{{Colors.dialog_hex}}} (50)\n"
                f"Купить {{{VIPData.colors[1]}}}SILVER VIP{{{Colors.dialog_hex}}} (100)\n"
                f"Купить {{{VIPData.colors[2]}}}GOLD VIP{{{Colors.dialog_hex}}} (200)\n"
            ),
            "Ок",
            "Закрыть",
            on_response=cls.donation_response
        ).show(player)

    @classmethod
    def donation_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_mn_dialog(player)

        if list_item == 0:
            return cls.show_mn_dialog(player)

        if list_item == 1:
            if player.donate < 50:
                return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{50 - player.donate}{{{Colors.red_hex}}} донат очков!")

            if player.vip.level != -1 and player.vip.level >= 0:
                return player.send_error_message("У Вас уже есть VIP-статус!")

            player.donate -= 50
            player.vip.level = 0
            return player.send_notification_message(f"Вы купили {{{VIPData.colors[player.vip.level]}}}BRONZE VIP{{{Colors.white_hex}}}!")

        if list_item == 2:
            if player.donate < 100:
                return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{100 - player.donate}{{{Colors.red_hex}}} донат очков!")

            if player.vip.level != -1 and player.vip.level >= 1:
                return player.send_error_message("У Вас уже есть VIP-статус!")

            player.donate -= 100
            player.vip.level = 1
            return player.send_notification_message(f"Вы купили {{{VIPData.colors[player.vip.level]}}}SILVER VIP{{{Colors.white_hex}}}!")

        if list_item == 3:
            if player.donate < 200:
                return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{200 - player.donate}{{{Colors.red_hex}}} донат очков!")

            if player.vip.level != -1 and player.vip.level >= 2:
                return player.send_error_message("У Вас уже есть VIP-статус!")

            player.donate -= 200
            player.vip.level = 2
            return player.send_notification_message(f"Вы купили {{{VIPData.colors[player.vip.level]}}}GOLD VIP{{{Colors.white_hex}}}!")

    @classmethod
    def show_skin_gang_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        skins_str = ""
        for i in player.gang.skins:
            skins_str += f"{i}\n"

        return Dialog.create(
            2,
            "Новый скин",
            skins_str,
            "Ок",
            "Закрыть",
            on_response=cls.skin_gang_response
        ).show(player)

    @classmethod
    def skin_gang_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        player.set_skin_ex(int(input_text))
        return player.send_notification_message(f"Ваш скин был изменён на модель {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}.")

    @classmethod
    def show_weapons_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        gun_string = ""
        for key, value in GunData.guns.items():
            gun_string += f"{{{Colors.cmd_hex}}}{key}\t{{{Colors.green_hex}}}{value[2]}$\n"

        return Dialog.create(
            5, "Покупка оружия",
            (
                "Оружие\tСтоимость\n"
                f"{gun_string}"
            ),
            "Купить",
            "Закрыть",
            on_response=cls.weapons_response
        ).show(player)


    @classmethod
    def weapons_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        gun = GunData.guns[input_text]
        if player.money - gun[2] < 0:
            return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{gun[2] - player.money}${{{Colors.red_hex}}}!")

        if gun[1] == 1: # Слот
            player.gun_slots.melee == gun[0] # ID оружия

        if gun[1] == 2:
            player.gun_slots.pistol == gun[0]

        if gun[1] == 3:
            player.gun_slots.shotgun == gun[0]

        if gun[1] == 4:
            player.gun_slots.assault_rifle == gun[0]

        if gun[1] == 5:
            player.gun_slots.long_rifle == gun[0]

        player.set_money_ex(gun[2], increase=False)
        player.give_weapon(gun[0], 100)
        return player.send_notification_message(f"Вы купили {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}.")

    @classmethod
    def show_vehicles_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Покупка транспорта",
            (
                f"{VehicleTypes.LOWRIDER}\n{VehicleTypes.OFFROAD}\n{VehicleTypes.SERVICES}\n{VehicleTypes.SEDAN}\n{VehicleTypes.SPORT}\n{VehicleTypes.UNIVERSAL}\n{VehicleTypes.UNIQE}"
            ),
            "Ок",
            "Закрыть",
            on_response=cls.vehicles_response
        ).show(player)


    @classmethod
    def vehicles_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        veh_str = ""
        veh_type = VehicleTypes.LOWRIDER
        if list_item == 0: # Lowrider
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.LOWRIDER:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}$\n"

        if list_item == 1: # Offroad
            veh_type = VehicleTypes.OFFROAD
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.OFFROAD:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}$\n"

        if list_item == 2: # Services
            veh_type = VehicleTypes.SERVICES
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.SERVICES:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}$\n"

        if list_item == 3: # Sedan
            veh_type = VehicleTypes.SEDAN
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.SEDAN:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}$\n"

        if list_item == 4: # Sport
            veh_type = VehicleTypes.SPORT
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.SPORT:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}$\n"

        if list_item == 5: # Universal
            veh_type = VehicleTypes.UNIVERSAL
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.UNIVERSAL:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}$\n"

        if list_item == 6: # Uniqe
            veh_type = VehicleTypes.UNIQE
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.UNIQE:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}$\n"

        return Dialog.create(
            5, veh_type,
            (
                "ID\tНазвание\tСтоимость\n"
                f"{veh_str}"
            ),
            "Купить",
            "Назад",
            on_response=cls.buy_vehicle_response
        ).show(player)

    @classmethod
    def buy_vehicle_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_vehicles_dialog(player)

        veh_data = VehicleData.data[int(input_text)]
        if player.money - veh_data[2] < 0:
            return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{veh_data[2] - player.money}${{{Colors.red_hex}}}!")

        player.remove_unused_vehicle(ServerMode.freeroam_world)
        player.set_money_ex(veh_data[2], increase=False)
        player_veh = Vehicle.create(
            int(input_text),
            *player.get_pos(),
            player.get_facing_angle(),
            1,
            1,
            -1,
            player.mode
        )
        player_veh.set_info(owner=player.get_name())
        player.update_vehicle_inst(player_veh)
        player.put_in_vehicle(player.vehicle.inst.id, 0)

    @classmethod
    def show_teleports_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        teleports = ""
        for name in FreeroamTeleports.teleports.keys():
            teleports += f"{name}\n"

        return Dialog.create(
            2,
            "Телепорт",
            teleports,
            "Ок",
            "Закрыть",
            on_response=cls.teleport_response
        ).show(player)

    @classmethod
    def teleport_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        x, y, z, rotation = FreeroamTeleports.teleports[input_text]
        if player.is_in_any_vehicle():
            player.vehicle.inst.set_position(x, y, z)
            player.vehicle.inst.set_z_angle(rotation)
        else:
            player.set_facing_angle(rotation)
            player.set_pos(x, y, z)
            player.set_camera_behind()

        return player.send_notification_message(f"Вы были перемещены на позицию {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}.")

    @classmethod
    def show_positions_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Меню позиций Администратора",
            "Создать позицию\nУдалить позицию\nСписок позиций",
            "Ок",
            "Закрыть",
            on_response=cls.position_response
        ).show(player)

    @classmethod
    def position_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if list_item == 0:
            return cls.show_create_position_dialog(player)

        if list_item == 1:
            return cls.show_delete_position_dialog(player)

        if list_item == 2:
            return cls.show_list_position_dialog(player)

    @classmethod
    def show_create_position_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            1,
            "Создании позиции",
            "Введите название позиции:",
            "Ок",
            "Назад",
            on_response=cls.create_position_response
        ).show(player)

    @classmethod
    def create_position_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_positions_dialog(player)

        if len(input_text) == 0 or len(input_text) > 32:
            player.send_error_message("Название позиции должно быть больше 0 и меньше 32 символов!")
            return cls.show_positions_dialog(player)

        if DataBase.load_admin_position(player, input_text):
            player.send_error_message("Позиция с таким названием уже существует!")
            return cls.show_positions_dialog(player)

        DataBase.create_admin_pos(player, input_text, *player.get_pos(), player.get_facing_angle())
        return player.send_notification_message(f"Вы создали позицию: {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}.")

    @classmethod
    def show_delete_position_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            1,
            "Удаление позиции",
            "Введите название позиции:",
            "Ок",
            "Назад",
            on_response=cls.delete_position_response
        ).show(player)

    @classmethod
    def delete_position_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_positions_dialog(player)

        pos_id = DataBase.load_admin_position(player, input_text)
        if not pos_id:
            player.send_error_message("Не удалось найти позицию!")
            return cls.show_delete_position_dialog(player)

        player.send_notification_message(f"Вы удалили позицию: {{{Colors.cmd_hex}}}{pos_id.name}{{{Colors.white_hex}}}.")
        return DataBase.delete_admin_position(player, pos_id.name)

    @classmethod
    def show_list_position_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        dialog_pos = ""
        for pos in DataBase.load_admin_positions(player):
            dialog_pos += f"{pos.name}\n"

        return Dialog.create(
            2,
            "Список позиций",
            f"{dialog_pos}",
            "Телепорт",
            "Назад",
            on_response=cls.list_position_response
        ).show(player)

    @classmethod
    def list_position_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_positions_dialog(player)

        pos = DataBase.load_admin_position(player, input_text)
        player.set_pos(pos.x, pos.y, pos.z)
        player.set_facing_angle(pos.rotation)
        player.set_camera_behind()
        player.send_notification_message(f"Вы переместились в позицию: {{{Colors.cmd_hex}}}{pos.name}{{{Colors.white_hex}}}.")

    @classmethod
    def show_tuning_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2, "Тюнинг транспорта",
            (
                "1. Покраска\n"
                "2. Закись азота\n"
                "3. Диски\n"
                "4. Покрасочные работы\n"
                "5. Спойлер\n"
                "6. Передний бампер\n"
                "7. Задний бампер\n"
                "8. Гидравлика"
            ),
            "Ок",
            "Закрыть",
            on_response=cls.tuning_response
        ).show(player)

    @classmethod
    def tuning_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if list_item == 0:
            player.send_notification_message("Укажите числа от 0 до 255 через запятую (17, 18)")
            return Dialog.create(
                1, "Покраска",
                "Укажите цвета:",
                "Ок",
                "Назад",
                on_response=cls.tuning_paint_response
            ).show(player)

        if list_item == 1:
            return Dialog.create(
                2, "Закись азота",
                "Nitro X2\nNitro X5\nNitro X10",
                "Ок",
                "Назад",
                on_response=cls.tuning_nitro_response
            ).show(player)

        if list_item == 2:
            wheels_str = ""
            for disk in VehicleComponents.wheels.keys():
                wheels_str += f"{disk}\n"

            return Dialog.create(
                2, "Диски",
                wheels_str,
                "Ок",
                "Назад",
                on_response=cls.tuning_wheels_response
            ).show(player)

        if list_item == 3:
            if player.vehicle.inst.get_model() not in VehicleComponents.paint_jobs:
                player.send_error_message("Покрасочные работы недоступны для этого транспорта!")
                return cls.show_tuning_dialog(player)

            paint_str = ""
            for paint_id in VehicleComponents.paint_jobs[player.vehicle.inst.get_model()]:
                paint_str += f"Расцветка {paint_id}\n"

            return Dialog.create(
                2, "Покрасочные работы",
                paint_str,
                "Ок",
                "Назад",
                on_response=cls.tuning_paint_job_response
            ).show(player)

        if list_item == 4:
            if player.vehicle.inst.get_model() not in VehicleComponents.spoilers:
                player.send_error_message("Для этого транспорта нельзя установить спойлер!")
                return cls.show_tuning_dialog(player)

            spoiler_str = ""
            for spoiler in VehicleComponents.spoilers[player.vehicle.inst.get_model()].keys():
                spoiler_str += f"{spoiler}\n"

            return Dialog.create(
                2, "Спойлер",
                spoiler_str,
                "Ок",
                "Назад",
                on_response=cls.tuning_spoiler_response
            ).show(player)

        if list_item == 5:
            if player.vehicle.inst.get_model() not in VehicleComponents.front_bumper:
                player.send_error_message("Для этого транспорта нельзя установить передний бампер!")
                return cls.show_tuning_dialog(player)

            front_bumper_str = ""
            for front_bumper in VehicleComponents.front_bumper[player.vehicle.inst.get_model()].keys():
                front_bumper_str += f"{front_bumper}\n"

            return Dialog.create(
                2, "Передний бампер",
                front_bumper_str,
                "Ок",
                "Назад",
                on_response=cls.tuning_front_bumper_response
            ).show(player)

        if list_item == 6:
            if player.vehicle.inst.get_model() not in VehicleComponents.rear_bumper:
                player.send_error_message("Для этого транспорта нельзя установить задний бампер!")
                return cls.show_tuning_dialog(player)

            rear_bumper_str = ""
            for rear_bumper in VehicleComponents.rear_bumper[player.vehicle.inst.get_model()].keys():
                rear_bumper_str += f"{rear_bumper}\n"

            return Dialog.create(
                2, "Задний бампер",
                rear_bumper_str,
                "Ок",
                "Назад",
                on_response=cls.tuning_rear_bumper_response
            ).show(player)

        if list_item == 7:
            return Dialog.create(
                2, "Гидравлика",
                "Установить\nУдалить",
                "Ок",
                "Назад",
                on_response=cls.tuning_hydraulics_response
            ).show(player)

    @classmethod
    def tuning_paint_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_tuning_dialog(player)

        if not input_text:
            player.send_error_message("Необходимо указать числа через запятую (17, 18)!")
            return cls.show_tuning_dialog(player)

        try:
            input_text = input_text.split(", ")
        except:
            player.send_error_message("Необходимо указать числа через запятую (17, 18)!")
            return cls.show_tuning_dialog(player)

        try:
            input_text[1]

        except:
            player.send_error_message("Укажите второй цвет от 0 до 255")
            return cls.show_tuning_dialog(player)

        if len(input_text[0]) < 0 or len(input_text[0]) > 255:
            player.send_error_message("Укажите первый цвет от 0 до 255")
            return cls.show_tuning_dialog(player)

        if len(input_text[1]) < 0 or len(input_text[1]) > 255:
            player.send_error_message("Укажите второй цвет от 0 до 255")
            return cls.show_tuning_dialog(player)

        try:
            color_one = int(input_text[0])
            color_two = int(input_text[1])
        except:
            player.send_error_message("Укажите целые числа!")
            return cls.show_tuning_dialog(player)

        player.vehicle.inst.change_color(color_one, color_two)
        player.play_sound(1052, x=0.0, y=0.0, z=0.0)
        return player.send_notification_message("Цвет успешно изменён!")

    @classmethod
    def tuning_nitro_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_tuning_dialog(player)

        if list_item == 0:
            player.vehicle.inst.add_component(VehicleComponents.nitro_x2)

        if list_item == 1:
            player.vehicle.inst.add_component(VehicleComponents.nitro_x5)

        if list_item == 2:
            player.vehicle.inst.add_component(VehicleComponents.nitro_x10)

        player.play_sound(1052, x=0.0, y=0.0, z=0.0)
        return player.send_notification_message(f"Установлено {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}!")

    @classmethod
    def tuning_wheels_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_tuning_dialog(player)

        player.vehicle.inst.add_component(VehicleComponents.wheels[input_text])
        player.play_sound(1052, x=0.0, y=0.0, z=0.0)
        return player.send_notification_message(f"Установлены диски {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}!")

    @classmethod
    def tuning_paint_job_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_tuning_dialog(player)

        model = player.vehicle.inst.get_model()
        pj_int = int(input_text.split(" ")[1])
        player.vehicle.inst.change_color(1, 1)
        player.vehicle.inst.change_paintjob(VehicleComponents.paint_jobs[model][pj_int])
        player.play_sound(1052, x=0.0, y=0.0, z=0.0)
        return player.send_notification_message(f"Установлена покрасночная работа {{{Colors.cmd_hex}}}{pj_int}{{{Colors.white_hex}}}!")

    @classmethod
    def tuning_spoiler_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_tuning_dialog(player)

        player.vehicle.inst.add_component(VehicleComponents.spoilers[player.vehicle.inst.get_model()][input_text])
        player.play_sound(1052, x=0.0, y=0.0, z=0.0)
        return player.send_notification_message(f"Установлен спойлер {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}!")

    @classmethod
    def tuning_front_bumper_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_tuning_dialog(player)

        player.vehicle.inst.add_component(VehicleComponents.front_bumper[player.vehicle.inst.get_model()][input_text])
        player.play_sound(1052, x=0.0, y=0.0, z=0.0)
        return player.send_notification_message(f"Установлен передний бампер {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}!")

    @classmethod
    def tuning_rear_bumper_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_tuning_dialog(player)

        player.vehicle.inst.add_component(VehicleComponents.rear_bumper[player.vehicle.inst.get_model()][input_text])
        player.play_sound(1052, x=0.0, y=0.0, z=0.0)
        return player.send_notification_message(f"Установлен задний бампер {{{Colors.cmd_hex}}}{input_text}{{{Colors.white_hex}}}!")

    @classmethod
    def tuning_hydraulics_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_tuning_dialog(player)

        if list_item == 0:
            player.vehicle.inst.add_component(VehicleComponents.hydraulics)
            return player.send_notification_message(f"Гидравлика была {{{Colors.cmd_hex}}}установлена{{{Colors.white_hex}}}!")

        if list_item == 1:
            player.vehicle.inst.remove_component(VehicleComponents.hydraulics)
            return player.send_notification_message(f"Гидравлика была {{{Colors.cmd_hex}}}удалена{{{Colors.white_hex}}}!")

        player.play_sound(1052, x=0.0, y=0.0, z=0.0)

    @classmethod
    def show_vbuy_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2, "VIP транспорт",
            "Hunter\nHydra\nAndromada\nRhino",
            "Ок",
            "Закрыть",
            on_response=cls.vbuy_response
        ).show(player)

    @classmethod
    def vbuy_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if list_item == 0:
            model_id = 425

        if list_item == 1:
            model_id = 520

        if list_item == 2:
            model_id = 592

        if list_item == 3:
            model_id = 432

        player.remove_unused_vehicle(ServerMode.freeroam_world)
        player_veh = Vehicle.create(
            model_id,
            *player.get_pos(),
            player.get_facing_angle(),
            1,
            1,
            -1,
            player.mode
        )
        player_veh.set_info(owner=player.get_name())
        player.update_vehicle_inst(player_veh)
        player.put_in_vehicle(player.vehicle.inst.id, 0)

    @classmethod
    def show_clist_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        color_str = ""
        for key, value in Colors.clist_hex.items():
            color_str += f"{key} | {{{value}}}{player.name}\n"

        return Dialog.create(
            2, "Изменение цвета",
            color_str,
            "Ок",
            "Закрыть",
            on_response=cls.clist_response
        ).show(player)

    @classmethod
    def clist_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        player.set_color_ex(Colors.clist_rgba[list_item])
        return player.send_notification_message(f"{{{Colors.clist_hex[list_item]}}}Цвет изменён!")

    @classmethod
    def show_house_info_dialog(cls, player: Player, pickup_id: int) -> None:
        player = Player.from_registry_native(player)
        house = houses_by_pickup[pickup_id]
        player.cache["HOUSE_PICKUP_ID"] = pickup_id
        return Dialog.create(
            0,
            f"Дом №{house.uid}",
            (
                f"Владелец:\t{{{Colors.cmd_hex}}}{house.owner}{{{Colors.dialog_hex}}}\n"
                f"Стоимость:\t{{{Colors.cmd_hex}}}{house.price}{{{Colors.dialog_hex}}}\n"
                f"Интерьер:\t{{{Colors.cmd_hex}}}{house.interior_id}{{{Colors.dialog_hex}}}\n"
            ),
            "Войти",
            "Закрыть",
            on_response=cls.house_info_response,
        ).show(player)

    @classmethod
    def house_info_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        player.house = houses_by_pickup[player.cache["HOUSE_PICKUP_ID"]]
        player.checks.in_house = True
        x, y, z = interiors[player.house.interior_id]
        player.set_interior(player.house.interior_id)
        player.set_pos(x, y, z)
        player.set_mode(player.house.interior_id + 1000)
        if player.house.owner == NO_HOUSE_OWNER:
            player.send_notification_message(f"Для покупки дома используйте {{{Colors.cmd_hex}}}/buyhouse{{{Colors.white_hex}}}.")

        del player.cache["HOUSE_PICKUP_ID"]

    @classmethod
    def show_house_create_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2, "Интерьер",
            (
                f"{{{Colors.bronze_hex}}}Маленький дом (LOW)\n"
                f"{{{Colors.bronze_hex}}}Средний дом (LOW)\n"
                f"{{{Colors.bronze_hex}}}Большой дом (LOW)\n"
                f"{{{Colors.silver_hex}}}Маленький дом (MEDIUM)\n"
                f"{{{Colors.silver_hex}}}Средний дом (MEDIUM)\n"
                f"{{{Colors.silver_hex}}}Большой дом (MEDIUM)\n"
                f"{{{Colors.gold_hex}}}Маленький дом (HIGH)\n"
                f"{{{Colors.gold_hex}}}Средний дом (HIGH)\n"
                f"{{{Colors.gold_hex}}}Большой дом (HIGH)\n"
                f"{{{Colors.cmd_hex}}}Трейлер (SPECIAL)\n"
            ),
            "Ок",
            "Закрыть",
            on_response=cls.create_house_response
        ).show(player)


    @classmethod
    def create_house_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if list_item == 0:
            interior_id = 1

        if list_item == 1:
            interior_id = 10

        if list_item == 2:
            interior_id = 6

        if list_item == 3:
            interior_id = 11

        if list_item == 4:
            interior_id = 12

        if list_item == 5:
            interior_id = 8

        if list_item == 6:
            interior_id = 4

        if list_item == 7:
            interior_id = 5

        if list_item == 8:
            interior_id = 9

        if list_item == 9:
            interior_id = 2

        if interior_id == 2:
            price = 50000

        if interior_id in (1, 10, 6):
            price = 100000

        if interior_id in (11, 12, 8):
            price = 500000

        if interior_id in (4, 5, 9):
            price = 1000000

        house = DataBase.create_house(interior_id, price, *player.get_pos())
        House(
            house.uid,
            house.owner,
            house.interior_id,
            house.price,
            house.pos_x,
            house.pos_y,
            house.pos_z,
            house.is_locked
        )

    @classmethod
    def show_house_menu_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Меню дома",
            (
                "Выйти\n"
                "Открыть/Закрыть\n"
                "Продать\n"
            ),
            "Ок",
            "Закрыть",
            on_response=cls.house_menu_response
        ).show(player)

    @classmethod
    def house_menu_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if list_item == 0:
            player.checks.in_house = False
            player.set_mode(ServerMode.freeroam_world)
            player.set_interior(0)
            return player.set_pos(
                player.house.pos_x,
                player.house.pos_y,
                player.house.pos_z
            )

        if list_item == 1:
            if player.house.is_locked:
                text = "~g~Unlocked"
                player.house.change_door_status(False)

            else:
                text = "~r~Locked"
                player.house.change_door_status(True)

            return player.game_text(text, 1250, 0)

        if list_item == 2:
            amount = int(player.house.price / 2)
            player.set_money_ex(amount)
            player.house.remove_owner()
            player.send_notification_message(
                f"Вы продали дом {{{Colors.cmd_hex}}}№{player.house.uid}{{{Colors.white_hex}}} за {{{Colors.cmd_hex}}}{amount}${{{Colors.white_hex}}}."
            )
            player.set_mode(ServerMode.freeroam_world)
            player.set_interior(0)
            player.set_pos(
                player.house.pos_x,
                player.house.pos_y,
                player.house.pos_z
            )
            player.house = None
            player.checks.in_house = False

    @classmethod
    def show_squad_create_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            1, "Создание фракции",
            "Введите название:",
            "Ок",
            "Закрыть",
            on_response=cls.create_squad_response
        ).show(player)

    @classmethod
    def create_squad_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return

        if len(input_text) < 6 or len(input_text) > 32:
            player.send_error_message("Название должно быть от 6 и до 32 символов!")
            return cls.show_squad_create_dialog(player)

        player.cache["CREATE_SQUAD_DATA"] = []
        player.cache["CREATE_SQUAD_DATA"].append({"name": input_text})
        return cls.show_squad_create_tag_dialog(player)


    @classmethod
    def show_squad_create_tag_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            1, "Создание фракции",
            "Введите тег:",
            "Ок",
            "Закрыть",
            on_response=cls.create_squad_tag_response
        ).show(player)

    @classmethod
    def create_squad_tag_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            del player.cache["CREATE_SQUAD_DATA"]
            return

        if len(input_text) < 0 or len(input_text) > 6:
            player.send_error_message("Длина тега должна быть от 0 и до 6 символов!")
            return cls.show_squad_create_tag_dialog(player)

        player.cache["CREATE_SQUAD_DATA"].append({"tag": input_text})
        return cls.show_squad_create_type_dialog(player)


    @classmethod
    def show_squad_create_type_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2, "Тип фракции",
            (
                "Фракция\n"
                "Организция\n"
                "Группировка\n"
                "Семья\n"
                "Синдикат\n"
                "Сообщество\n"
                "RP-Соощество\n"
            ),
            "Ок",
            "Закрыть",
            on_response=cls.create_squad_type_response
        ).show(player)

    @classmethod
    def create_squad_type_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            del player.cache["CREATE_SQUAD_DATA"]
            return

        player.cache["CREATE_SQUAD_DATA"].append({"classification": input_text})
        return cls.show_squad_create_color_dialog(player)

    @classmethod
    def show_squad_create_color_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)
        color_str = ""
        for key, value in Colors.clist_hex.items():
            color_str += f"{{{value}}}{player.name}\n"

        return Dialog.create(
            2, "Выбор цвета",
            color_str,
            "Ок",
            "Закрыть",
            on_response=cls.squad_create_color_response
        ).show(player)

    @classmethod
    def squad_create_color_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            del player.cache["CREATE_SQUAD_DATA"]
            return

        player.cache["CREATE_SQUAD_DATA"].append({"color": Colors.clist_rgba[list_item]})
        player.cache["CREATE_SQUAD_DATA"].append({"color_hex": Colors.clist_hex[list_item]})
        squad = Squad.create(
            player.cache["CREATE_SQUAD_DATA"][0]["name"],
            player.cache["CREATE_SQUAD_DATA"][1]["tag"],
            player.name,
            player.cache["CREATE_SQUAD_DATA"][2]["classification"],
            player.cache["CREATE_SQUAD_DATA"][3]["color"],
            player.cache["CREATE_SQUAD_DATA"][4]["color_hex"]
        )
        del player.cache["CREATE_SQUAD_DATA"]
        player.squad = squad
        return player.send_notification_message(f"Вы успешно создали сквад: {{{squad.color}}}{squad.name}{{{Colors.white_hex}}}!")

    @classmethod
    def show_squad_info_dialog(cls, player: Player) -> None:
        player = Player.from_registry_native(player)

        # return Dialog.create(
        #     2, "Выбор цвета",
        #     color_str,
        #     "Ок",
        #     "Закрыть",
        #     on_response=cls.squad_create_color_response
        # ).show(player)
