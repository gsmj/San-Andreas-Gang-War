from pysamp.player import Player as BasePlayer
from pysamp.dialog import Dialog
from pysamp.playertextdraw import PlayerTextDraw
from pysamp.textdraw import TextDraw
from pystreamer.dynamicpickup import DynamicPickup
from pystreamer.dynamiccp import DynamicCheckpoint
from pystreamer.dynamicmapicon import create_dynamic_map_icon, destroy_dynamic_map_icon
from pysamp.timer import set_timer, kill_timer
from pysamp.dialog import Dialog
from pysamp import (
    send_client_message,
    create_player_3d_text_label,
    delete_player_3d_text_label,
    gang_zone_show_for_player,
    gang_zone_hide_for_player,
    text_draw_hide_for_player,
    gang_zone_flash_for_player,
    gang_zone_stop_flash_for_player,
    call_remote_function,
    select_text_draw,
    cancel_select_text_draw,
    send_client_message_to_all,
    kick
)
from .utils import *
from .consts import *
from functools import wraps
from datetime import datetime
from zoneinfo import ZoneInfo
from .gang import gangs, GangZoneData, Gang
from .textdraws import TextDraws
from .version import __version__
from .database import DataBase
from .vehicle import Vehicle, VehicleData, VehicleTypes
from .playerdata import *
from math import sqrt
import random
import time
from samp import INVALID_PLAYER_ID, PLAYER_STATE_ONFOOT, PLAYER_STATE_DRIVER, PLAYER_STATE_SPECTATING # type: ignore


class Player(BasePlayer):
    _registry: dict = {}
    def __init__(self, player_id):
        super().__init__(player_id)
        self.name = self.get_name()
        self.password: str = None
        self.email: str = None
        self.pin: int = None
        self.registration_ip: str = None
        self.last_ip: str = self.get_ip()
        self.registration_data: datetime = None
        self.score: int = 0
        self.money: int = 100000
        self.donate: int = 0
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
        self.is_data: PlayerIs = PlayerIs()
        self.time: PlayerTime = PlayerTime()
        self.drift: PlayerDrift = PlayerDrift()
        self.vip: PlayerVIP = PlayerVIP()
        self.gun_slots: PlayerFreeroamGunSlots = PlayerFreeroamGunSlots()
        self.admin: PlayerAdmin = PlayerAdmin()
        self.tmp: PlayerTemp = PlayerTemp()
        self.vehicle: PlayerVehicle = PlayerVehicle()
        self.settings: PlayerSettings = PlayerSettings()

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

    def take_money_ex(self, amount: int, show_text: bool = True) -> None:
        self.money -= amount
        self.set_money(self.money)
        if show_text:
            self.game_text(f"~r~-{amount}$", 1500, 1)

    def set_mode(self, mode: int) -> None:
        self.set_virtual_world(mode)
        self.mode = mode

    def update_freeroam_gun_slots(self, slots) -> None:
        self.gun_slots.melee = slots.slot_melee
        self.gun_slots.pistol = slots.slot_pistol
        self.gun_slots.shotgun = slots.slot_shotgun
        self.gun_slots.machine_gun = slots.slot_machine_gun
        self.gun_slots.assault_rifle = slots.slot_assault_rifle
        self.gun_slots.long_rifle = slots.slot_long_rifle

    def give_freeroam_guns(self) -> None:
        self.give_weapon(self.gun_slots.melee, 100)
        self.give_weapon(self.gun_slots.pistol, 100)
        self.give_weapon(self.gun_slots.shotgun, 100)
        self.give_weapon(self.gun_slots.machine_gun, 100)
        self.give_weapon(self.gun_slots.assault_rifle, 100)
        self.give_weapon(self.gun_slots.long_rifle, 100)

    def kick_player(self, player: "Player") -> None:
        player = self.from_registry_native(player)
        Dialogs.show_kick_dialog(player)
        player.send_error_message("Введите /q (/quit) чтобы выйти!")
        return set_timer(kick, 1000, False, player.id)

    def mute_timer(self) -> None:
        self.send_notification_message("Время муто вышло.")
        self.is_data.muted = False
        self.time.mute = 0
        self.timers.mute_id = TIMER_ID_NONE

    def every_second(self) -> None:
        self.time.afk += 1
        if self.time.afk >= 3:
            self.set_chat_bubble(f"AFK: {self.time.afk} секунд", -1, 20.0, 1100)

        if not self.settings.disabled_ping_td:
            return TextDraws.fps_and_ping[0].set_string(f"Ping: {self.get_ping()}")

    def jail_timer(self) -> None:
        self.send_notification_message("Вас выпустили из деморгана.")
        self.is_data.jailed = False
        self.time.jail = 0
        self.timers.jail_id = TIMER_ID_NONE
        self.set_mode(ServerWorldIDs.freeroam_world)
        return self.enable_freeroam_selector()

    def create_speedometer(self) -> dict[int, "PlayerTextDraw"]:
        self.vehicle_speedometer[0] = PlayerTextDraw.create(self, 626.000000, 384.540008, "usebox")
        self.vehicle_speedometer[0].letter_size(0.000000, 5.905555)
        self.vehicle_speedometer[0].text_size(430.799987, 0.000000)
        self.vehicle_speedometer[0].alignment(1)
        self.vehicle_speedometer[0].use_box(True)
        self.vehicle_speedometer[0].box_color(50)
        self.vehicle_speedometer[0].color(102)
        self.vehicle_speedometer[0].set_shadow(0)
        self.vehicle_speedometer[0].set_outline(0)
        self.vehicle_speedometer[0].font(0)
        self.vehicle_speedometer[1] = PlayerTextDraw.create(self, 601.875000, 383.250061, "LD_SPAC:white")
        self.vehicle_speedometer[1].letter_size(0.000000, 0.000000)
        self.vehicle_speedometer[1].text_size(21.250000, 57.166625)
        self.vehicle_speedometer[1].alignment(1)
        self.vehicle_speedometer[1].color(255)
        self.vehicle_speedometer[1].set_shadow(0)
        self.vehicle_speedometer[1].set_outline(0)
        self.vehicle_speedometer[1].font(4)
        self.vehicle_speedometer[2] = PlayerTextDraw.create(self, 442.399963, 386.026580, "SPEED: 0 km/h")
        self.vehicle_speedometer[2].letter_size(0.401249, 1.430832)
        self.vehicle_speedometer[2].alignment(1)
        self.vehicle_speedometer[2].color(-1)
        self.vehicle_speedometer[2].set_shadow(0)
        self.vehicle_speedometer[2].set_outline(1)
        self.vehicle_speedometer[2].background_color(51)
        self.vehicle_speedometer[2].font(1)
        self.vehicle_speedometer[2].set_proportional(True)
        self.vehicle_speedometer[3] = PlayerTextDraw.create(self, 608.125000, 386.166625, "L")
        self.vehicle_speedometer[3].letter_size(0.449999, 1.600000)
        self.vehicle_speedometer[3].alignment(1)
        self.vehicle_speedometer[3].color(-1)
        self.vehicle_speedometer[3].set_shadow(0)
        self.vehicle_speedometer[3].set_outline(1)
        self.vehicle_speedometer[3].background_color(51)
        self.vehicle_speedometer[3].font(1)
        self.vehicle_speedometer[3].set_proportional(True)
        self.vehicle_speedometer[4] = PlayerTextDraw.create(self, 609.125000, 413.416778, "E")
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
        self.drift_counter[1] = PlayerTextDraw.create(self, 320.000000, 395.000000, "Drift Counter")
        self.drift_counter[1].alignment(2)
        self.drift_counter[1].background_color(255)
        self.drift_counter[1].letter_size(0.500000, 1.000000)
        self.drift_counter[1].font(3)
        self.drift_counter[1].color(-1)
        self.drift_counter[1].set_outline(1)
        self.drift_counter[1].set_proportional(True)
        self.drift_counter[2] = PlayerTextDraw.create(self, 250.000000, 405.000000, "Cash: ~g~0")
        self.drift_counter[2].background_color(255)
        self.drift_counter[2].font(2)
        self.drift_counter[2].letter_size(0.200000, 1.000000)
        self.drift_counter[2].color(-1)
        self.drift_counter[2].set_outline(1)
        self.drift_counter[2].set_proportional(True)
        self.drift_counter[3] = PlayerTextDraw.create(self, 250.000000, 415.000000, "Score: ~y~0")
        self.drift_counter[3].background_color(255)
        self.drift_counter[3].font(2)
        self.drift_counter[3].letter_size(0.200000, 1.000000)
        self.drift_counter[3].color(-1)
        self.drift_counter[3].set_outline(1)
        self.drift_counter[3].set_outline(1)
        self.drift_counter[3].set_proportional(True)
        self.drift_counter[4] = PlayerTextDraw.create(self, 250.000000, 425.000000, "Combo: ~r~x1")
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
        self.drift.score += int(value / 1000)
        self.drift.combo += int(self.drift.score / 100)
        self.drift_counter[2].set_string(f"Cash: ~g~{self.drift.money}$")
        self.drift_counter[3].set_string(f"Score: ~y~{self.drift.score}")
        self.drift_counter[4].set_string(f"Combo: ~r~x{self.drift.combo}")

    def send_error_message(self, message: str) -> None:
        return self.send_client_message(Colors.red, f"[ОШИБКА] {message}")

    def send_notification_message(self, message: str) -> None:
        return self.send_client_message(Colors.white, f"{message}")

    def send_debug_message(self, message: str) -> None:
        return self.send_client_message(Colors.light_grey, f"DEBUG: {message}")

    def send_report_message(self, author: "Player", message: str) -> None:
        for player in self._registry.values():
            if player.admin.level != 0:
                player.send_client_message(Colors.red, f"Репорт от {{{Colors.cmd_hex}}}{author.name}({author.id}):{{{Colors.red_hex}}} {message}.")

    def send_capture_message(self, initiator: str, atk_id: int, def_id: int, gangzone_id: int, zone_name: str) -> None:
        self.send_client_message(Colors.white, f"{{{gangs[atk_id].color_hex}}}{initiator}{{{Colors.white_hex}}} инициировал захват территории {{{Colors.cmd_hex}}}{zone_name}{{{Colors.white_hex}}}!")
        return self.send_client_message(Colors.white, f"Началась война между {{{gangs[atk_id].color_hex}}}{gangs[atk_id].gang_name}{{{Colors.white_hex}}} и {{{gangs[def_id].color_hex}}}{gangs[def_id].gang_name}{{{Colors.white_hex}}}!")

    def get_gang_rang(self):
        for key, value in self.gang.rangs.items():
            if self.kills <= key:
                return key, value

    def remove_unused_vehicle(self):
        if self.vehicle.id != ID_NONE:
            veh = Vehicle.get_from_registry(self.vehicle.id)
            Vehicle.remove_unused_player_vehicle(veh)

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
        for td in TextDraws.logo.values():
            td.show_for_player(self)

    def show_bottom_commands(self):
        self.hide_bottom_commands()
        if self.mode == ServerWorldIDs.gangwar_world:
            for td in TextDraws.commands_bottom_gw.values():
                td.show_for_player(self)

        if self.mode == ServerWorldIDs.freeroam_world:
            for td in TextDraws.commands_bottom.values():
                td.show_for_player(self)

    def hide_bottom_commands(self):
        for td in TextDraws.commands_bottom_gw.values():
            td.hide_for_player(self)

        for td in TextDraws.commands_bottom.values():
            td.hide_for_player(self)

    def show_ping_textdraw(self):
        for td in TextDraws.fps_and_ping.values():
            td.show_for_player(self)

    def hide_ping_textdraw(self):
        for td in TextDraws.fps_and_ping.values():
            td.hide_for_player(self)

    def check_cooldown(self, unix_seconds: float) -> bool:
        if self.time.cooldown is not None:
            if (time.time() - self.time.cooldown) < unix_seconds:
                return False

        self.time.cooldown = time.time()
        return True

    def update_player_cooldown_time(self) -> float:
        self.time.cooldown = time.time()
        return self.time.cooldown

    def set_random_color(self) -> None:
        return self.set_color(randint(0, 16777215))

    def kick_if_not_logged(self) -> None:
        if not self.is_data.logged:
            Dialogs.show_kick_dialog(self)
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.kick, 1000, False)

    def kick_if_not_logged_or_jailed(self) -> None:
        if not self.is_data.logged or self.is_data.jailed:
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.kick, 1000, False)

    def kick_teamkill(self) -> None:
        Dialogs.show_kick_teamkill(self)
        self.send_error_message("Введите /q (/quit) чтобы выйти!")
        return set_timer(self.kick, 1000, False)

    def ban_from_server(self, reason: str) -> None:
        if self.is_data.banned:
            Dialogs.show_banned_dialog(self)
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.ban_ex, 1000, False, reason)

    def show_gangzones_for_player(self) -> None:
        gangzones = DataBase.load_gangzones()
        for i in gangzones:
            gang_zone_show_for_player(self.id, i.id, i.color)

    def reload_gangzones_for_player(self):
        gangzones = DataBase.load_gangzones()
        for i in gangzones:
            gang_zone_hide_for_player(self.id, i.id)
            gang_zone_show_for_player(self.id, i.id, i.color)

    def disable_gangzones_for_player(self):
        gangzones = DataBase.load_gangzones()
        for i in gangzones:
            gang_zone_hide_for_player(self.id, i.id)

    def is_in_area(self, min_x: float, min_y: float, max_x: float, max_y: float) -> bool:
        x, y, z = self.get_pos()
        if ((x <= max_x and x >= min_x) and (y <= max_y and y >= min_y)):
            return True

        return False

    def set_gangwar_spawn_info(self):
        self.set_spawn_info(
            255,
            self.skin,
            self.gang.spawn_pos[0],
            self.gang.spawn_pos[1],
            self.gang.spawn_pos[2],
            0.0, 0, 0, 0, 0, 0, 0)

    def enable_gangwar_mode(self, first_show: bool = True):
        self.show_bottom_commands()
        self.set_pos(self.gang.spawn_pos[0], self.gang.spawn_pos[1], self.gang.spawn_pos[2])
        self.set_camera_behind()
        self.set_interior(self.gang.interior_id)
        if first_show: # Если показывается первый раз
            self.set_health(100.0)
            self.set_skin_ex(random.choice(self.gang.skins))
            self.set_color_ex(self.gang.color)
            self.show_gangzones_for_player()
            if self.gang.is_capturing:
                gz = GangZoneData.get_from_registry(self.gang.capture_id)
                gz_db = DataBase.load_gangzone(gz.gangzone_id)
                x, y = get_center(gz_db.min_x, gz_db.max_x, gz_db.min_y, gz_db.max_y)
                gang_zone_flash_for_player(self.id, self.gang.capture_id, gangs[gz.gang_atk_id].color)
                self.show_capture_textdraws()
            self.game_text(f"Welcome~n~{self.gang.game_text_color}{self.get_name()}", 2000, 1)

        return self.set_spawn_info(
            255,
            self.skin,
            self.gang.spawn_pos[0],
            self.gang.spawn_pos[1],
            self.gang.spawn_pos[2],
            0.0, 0, 0, 0, 0, 0, 0)

    def enable_freeroam_selector(self):
        self.set_mode(randint(100, 500))
        self.toggle_controllable(False)
        self.set_skin_ex(FreeroamSkins.skins[0])
        self.set_pos(204.6633, -6.5563, 1001.2109)
        self.set_facing_angle(299.4084)
        self.set_camera_position(208.7765, -3.9595, 1001.2178)
        self.set_camera_look_at(204.6633, -6.5563, 1001.2109)
        self.set_interior(5)
        self._freeroam_selector = 0
        self.is_data.selecting_skin = True
        return self.show_class_selector_textdraws()

    def set_freeroam_spawn_info(self):
        i = randint(0, len(RandomSpawns.spawns))
        self.set_spawn_info(
            255,
            self.skin,
            RandomSpawns.spawns[i][0],
            RandomSpawns.spawns[i][1],
            RandomSpawns.spawns[i][2],
            RandomSpawns.spawns[i][3],
            0, 0, 0, 0, 0, 0)

    def enable_freeroam_mode(self):
        self.show_bottom_commands()
        self.set_camera_behind()
        self.set_interior(0)
        self.set_color_ex(randint(0, 16777215))
        self.disable_gangzones_for_player()
        i = randint(0, len(RandomSpawns.spawns))
        self.set_pos(RandomSpawns.spawns[i][0], RandomSpawns.spawns[i][1], RandomSpawns.spawns[i][2])
        self.set_facing_angle(RandomSpawns.spawns[i][3])
        self.set_freeroam_spawn_info()
        self.give_freeroam_guns()
        return self.game_text(f"Welcome~n~{self.get_name()}", 2000, 1)

    def set_jail_spawn_info(self):
        i = randint(0, len(RandomSpawns.spawns))
        self.set_spawn_info(
            254, # 254 Команда для игроков в ДМГ, чтобы не было урона
            167,
            5509.365234,
            1245.812866,
            8.000000,
            0.0,
            0, 0, 0, 0, 0, 0)

    def enable_jail_mode(self):
        self.set_skin(167)
        self.set_team(254)
        self.set_color_ex(Colors.jail)
        self.disable_gangzones_for_player()
        self.set_pos(5509.365234, 1245.812866, 8.000000)
        self.set_jail_spawn_info()
        self.reset_weapons()
        self.send_notification_message(f"Вы выйдите из деморгана через {{{Colors.cmd_hex}}}{self.time.jail}{{{Colors.white_hex}}} минут.")
        self.timers.jail_id = set_timer(self.jail_timer, int(self.time.jail * 60000), False)
        return self.game_text(f"Welcome~n~{self.get_name()}", 2000, 1)

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
            send_client_message(player.id, (color & 0xFF) | (clr_b << 8) | (clr_g << 16) | (clr_r << 24), f"- {self.get_name()}({self.get_id()}):{{{Colors.white_hex}}} {message}")

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

    def set_data_after_login(self, player_db: "Player") -> None:
        player_settings = DataBase.get_player_settings(self)
        self.password = player_db.password
        self.email = player_db.email
        self.pin = player_db.pin
        self.registration_ip = player_db.registration_ip
        self.registration_data = player_db.registration_data
        self.score = player_db.score
        self.money = player_db.money
        self.donate = player_db.donate
        self.kills = player_db.kills
        self.deaths = player_db.deaths
        self.heals = player_db.heals
        self.masks = player_db.masks
        self.gang_id = player_db.gang_id
        self.gang = gangs[self.gang_id]
        self.vip = PlayerVIP(
            level=player_db.vip_level
        )
        self.admin = PlayerAdmin(
            level=player_db.admin_level
        )
        self.is_data = PlayerIs(
            muted=player_db.is_muted,
            jailed=player_db.is_jailed,
            logged=True,
            banned=player_db.is_banned,
        )
        self.time = PlayerTime(
            jail=player_db.jail_time,
            mute=player_db.mute_time
        )
        self.settings = PlayerSettings(
            disabled_ping_td=player_settings.disabled_ping_td,
            disabled_global_chat_gw=player_settings.disabled_global_chat_gw
        )
        self.set_max_gun_skill()
        self.reset_money()
        self.set_score(self.score)
        self.give_money(self.money)
        self.update_freeroam_gun_slots(DataBase.get_player_freeroam_gun_slots(self))
        if not self.is_data.jailed:
            return Dialogs.show_select_mode_dialog(self)

        self.set_mode(ServerWorldIDs.jail_world)
        return self.toggle_spectating(False)


    def show_credits_dialog(self):
        return Dialogs.show_credits_dialog(self)

    def show_class_selector_textdraws(self):
        select_text_draw(self.id, Colors.textdraw)
        for td in TextDraws.class_selection_td.values():
            td.show_for_player(self)

    def hide_class_selector_textdraws(self):
        cancel_select_text_draw(self.id)
        text_draw_hide_for_player(self.id, 6)
        text_draw_hide_for_player(self.id, 7)
        text_draw_hide_for_player(self.id, 8)

    def show_capture_textdraws(self):
        for td in TextDraws.capture_td.values():
            td.show_for_player(self)

    def hide_capture_textdraws(self):
        text_draw_hide_for_player(self.id, 3)
        text_draw_hide_for_player(self.id, 4)
        text_draw_hide_for_player(self.id, 5)

    def start_capture(self, atk_id: int, def_id: int, gangzone_id) -> None: # self - Игрок, начавший захват
        gz_db = DataBase.load_gangzone(gangzone_id)
        x, y = get_center(gz_db.min_x, gz_db.max_x, gz_db.min_y, gz_db.max_y)
        gz = GangZoneData.get_from_registry(gangzone_id)
        gz.gang_atk_id = atk_id
        gz.gang_def_id = def_id
        gz.gang_atk_score = 0
        gz.gang_def_score = 0
        gz.capture_time = 900
        gz.capture_cooldown = 0
        gz.is_capture = True
        self.update_capture_textdraw(gz)
        for player in self._registry.values(): # Общий показ текстдрава капта для двух банд
            if (player.gang_id == atk_id) or (player.gang_id == def_id):
                player.set_team(player.gang_id)
                player.send_notification_message("Во время войны урон по своим был отключён!")
                gang_zone_flash_for_player(player.id, gz.gangzone_id, gangs[gz.gang_atk_id].color)
                player.show_capture_textdraws()

        return create_dynamic_map_icon(x, y, 0.0, gangs[gz.gang_atk_id].map_icon, 0, world_id=ServerWorldIDs.gangwar_world, interior_id=0, style=1)

    @staticmethod
    def end_capture(gangzone: GangZoneData):
        win = False
        if gangzone.gang_atk_score >= gangzone.gang_def_score:
            win = True
            gangzone.gang_id = gangzone.gang_atk_id
            gangzone.color = gangs[gangzone.gang_id].color

        DataBase.save_gangzone(
            id=gangzone.gangzone_id,
            gang_id=gangzone.gang_id,
            color=gangzone.color,
            gang_atk_id=-1,
            gang_def_id=-1,
            gang_atk_score=0,
            gang_def_score=0,
            capture_time=0,
            capture_cooldown=900,
            is_capture=False)
        for player in Player._registry:
            player = Player.from_registry_native(player)
            if (player.gang_id == gangzone.gang_atk_id) or (player.gang_id == gangzone.gang_atk_id):
                player.set_team(255)
                player.send_notification_message(f"Банда {{{gangs[gangzone.gang_atk_id].color_hex}}}{gangs[gangzone.gang_atk_id].gang_name}{{{Colors.white_hex}}} {'захватила' if win else 'не смогла захватить'} территорию!")
                player.send_notification_message(f"Счёт: {{{gangs[gangzone.gang_atk_id].color_hex}}}{gangzone.gang_atk_score}{{{Colors.white_hex}}} - {{{gangs[gangzone.gang_def_id].color_hex}}}{gangzone.gang_def_score}{{{Colors.white_hex}}}.")
                player.hide_capture_textdraws()
                gang_zone_stop_flash_for_player(player.id, gangzone.gangzone_id)
                player.reload_gangzones_for_player()

        destroy_dynamic_map_icon(0)
        destroy_dynamic_map_icon(1)
        gangzone.gang_atk_id = 0
        gangzone.gang_def_id = 0
        gangzone.gang_atk_score = 0
        gangzone.gang_def_score = 0
        gangzone.capture_time = 0
        gangzone.capture_cooldown = 900
        gangzone.is_capture = False

    @staticmethod
    def update_capture_textdraw(gz: GangZoneData):
        h, m, s = convert_seconds(gz.capture_time)
        TextDraws.capture_td[0].set_string(f"Time: {m}:{s}")
        TextDraws.capture_td[1].set_string(f"{gangs[gz.gang_atk_id].gang_name} ~r~{gz.gang_atk_score}")
        TextDraws.capture_td[1].color(gangs[gz.gang_atk_id].color)
        TextDraws.capture_td[2].set_string(f"{gangs[gz.gang_def_id].gang_name} ~r~{gz.gang_def_score}")
        TextDraws.capture_td[2].color(gangs[gz.gang_def_id].color)

    def _get_tab_list_header(self, start: int, stop: int = None) -> str:
        gangzone_tab_list_header = ""
        for gangzone in list(GangZoneData._registry.values())[start:stop]:
            hours, minutes, seconds = convert_seconds(gangzone.capture_cooldown)
            gangzone_tab_list_header += f"{{{gangs[gangzone.gang_id].color_hex}}}{gangs[gangzone.gang_id].gang_name}{{{Colors.white_hex}}}\t{gangzone.gangzone_id}\t{hours}:{minutes}:{seconds}\n"

        return gangzone_tab_list_header

    # Handle блок.

    def on_connect_handle(self) -> None:
        self.send_debug_message(f"on_connect_handle | Inst: {self}")
        if self.is_connected():
            for i in range(25):
                self.send_notification_message(" ")

            self.toggle_clock(False)
            self.send_notification_message(f"Добро пожаловать на сервер {{{Colors.cmd_hex}}}{ServerInfo.name_short}{{{Colors.white_hex}}}!")
            self.send_notification_message(f"Последняя версия: {{{Colors.cmd_hex}}}{__version__}{{{Colors.white_hex}}}!")
            self.send_notification_message(f"Created by: {{{Colors.vagos_hex}}}Ykpauneu{{{Colors.white_hex}}}& {{{Colors.rifa_hex}}}Rein.{{{Colors.white_hex}}}!")
            self.show_server_logotype()
            self.show_ping_textdraw()
            self.timers.every_sec = set_timer(self.every_second, 1000, True)
            self.toggle_spectating(True)
            player_db = DataBase.get_player(self)
            if not player_db:
                return Dialogs.show_registration_dialog(self)

            if not player_db.is_banned:
                return Dialogs.show_login_dialog(self)

            return self.ban_from_server()

    def on_disconnect_handle(self) -> None:
        if self.vip.is_random_clist_enabled:
            kill_timer(self.vip.random_clist_timer_id)

        if self.vehicle.id != ID_NONE:
            veh = Vehicle.get_from_registry(self.vehicle.id)
            veh.set_owner(NO_VEHICLE_OWNER)

        kill_timer(self.timers.every_sec)
        if self.is_data.logged:
            DataBase.save_player(
                self,
                password=self.password,
                email=self.email,
                pin=self.pin,
                last_ip=self.last_ip,
                score=self.score,
                money=self.money,
                donate=self.donate,
                kills=self.kills,
                deaths=self.deaths,
                heals=self.heals,
                masks=self.masks,
                gang_id=self.gang_id,
                vip_level=self.vip.level,
                admin_level=self.admin.level,
                vip_gangwar_template = "0, 0, 0",
                is_muted=self.is_data.muted,
                is_jailed=self.is_data.jailed,
                is_banned=self.is_data.banned,
                jail_time=self.time.jail,
                mute_time=self.time.mute
                )

            DataBase.save_freeroam_gun_slots(
                self,
                slot_melee=self.gun_slots.melee,
                slot_pistol=self.gun_slots.pistol,
                slot_shotgun=self.gun_slots.shotgun,
                slot_machine_gun=self.gun_slots.machine_gun,
                slot_assault_rifle=self.gun_slots.assault_rifle,
                slot_long_rifle=self.gun_slots.long_rifle,
            )

            DataBase.save_player_settings(
                self,
                disabled_ping_td=self.settings.disabled_ping_td,
                disabled_global_chat_gw=self.settings.disabled_global_chat_gw
            )

        return self.delete_registry(self)

    def on_request_class_handle(self, class_id: int) -> None:
        self.send_debug_message(f"on_request_class_handle | Inst: {self} | Class: {class_id}")
        self.kick_if_not_logged()
        self.spawn()
        return True

    def on_spawn_handle(self) -> None:
        self.send_debug_message(f"on_spawn_handle | Inst: {self} | Mode: {self.get_virtual_world()} | Int {self.get_interior()}")
        if self.mode == ServerWorldIDs.gangwar_world or self.mode == ServerWorldIDs.gangwar_world:
            return self.enable_gangwar_mode()

        if self.is_data.selecting_skin: # Если игрок выбирает скин во freeroam, то включить селектор. Так как игрок уже заспавнен
            return self.enable_freeroam_selector()

        if self.mode == ServerWorldIDs.freeroam_world: # Если игрок в обычном фрироме и выбрал скин, то просто ставить позицию т.д
            return self.enable_freeroam_mode()

        if self.mode == ServerWorldIDs.jail_world:
            return self.enable_jail_mode()

    def on_death_handle(self, killer: "Player", reason: int) -> None:
        self.send_debug_message(f"on_death_handle | Inst: {self} | Killer: {killer}")
        self.kick_if_not_logged()
        self.deaths += 1
        if self.mode == ServerWorldIDs.gangwar_world or self.mode == ServerWorldIDs.gangwar_world:
            self.masks = 0
            self.heals = 0
            self.set_gangwar_spawn_info()

        if self.mode == ServerWorldIDs.freeroam_world:
            self.set_freeroam_spawn_info()
            self.send_death_message(killer, self, reason)
            killer.send_death_message(killer, self, reason)

        if self.mode == ServerWorldIDs.jail_world:
            return self.set_jail_spawn_info()

        if killer.id == INVALID_PLAYER_ID:
            return self.delete_registry(killer.id)

        killer.kills += 1
        killer.set_money_ex(1000)
        killer.set_score(killer.kills)
        if killer.gang.is_capturing:
            if killer.gang.capture_id == self.gang.capture_id:
                gz = GangZoneData.get_from_registry(killer.gang.capture_id)
                if killer.gang.gang_id == gz.gang_atk_id:
                    gz.gang_atk_score += 1
                else:
                    gz.gang_def_score += 1
                killer.send_death_message(killer, self, reason)
                self.send_death_message(killer, self, reason)

    def on_text_handle(self, text: str) -> False:
        self.kick_if_not_logged()
        if self.is_data.muted:
            self.set_chat_bubble("Пытается что-то сказать.", Colors.red, 20.0, 10000)
            return self.send_error_message("Доступ в чат заблокирован!")

        if self.mode == ServerWorldIDs.freeroam_world:
            return send_client_message_to_all(self.color, f"{self.get_name()}({self.get_id()}):{{{Colors.white_hex}}} {text}")

        if self.mode == ServerWorldIDs.gangwar_world and self.settings.disabled_global_chat_gw:
            return send_client_message_to_all(self.color, f"{self.get_name()}({self.get_id()}):{{{Colors.white_hex}}} {text}")

        self.set_chat_bubble(text, -1, 20.0, 10000)
        return self.prox_detector(20.0, self.color, text)

    def on_pick_up_pickup_handle(self, pickup: DynamicPickup) -> None:
        self.kick_if_not_logged()
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
            vehicle = Vehicle.get_from_registry(self.get_vehicle_id())
            if vehicle.engine == 1:
                vehicle.engine = 0
            else:
                vehicle.engine = 1

            self.update_speedometer_sensors(vehicle)
            return vehicle.set_params_ex(
                vehicle.engine,
                vehicle.lights,
                0,
                0,
                0,
                0,
                0
            )

        if (self.get_state() == PLAYER_STATE_DRIVER) and (old_keys == 4):
            if not self.get_vehicle_id() in NoEngineVehicleIDs.ids:
                vehicle = Vehicle.get_from_registry(self.get_vehicle_id())
                if vehicle.lights == 1:
                    vehicle.lights = 0
                else:
                    vehicle.lights = 1

                self.update_speedometer_sensors(vehicle)
                return vehicle.set_params_ex(
                    vehicle.engine,
                    vehicle.lights,
                    0,
                    0,
                    0,
                    0,
                    0
                )

    def on_state_change_handle(self, new_state: int, old_state: int) -> None:
        if new_state == PLAYER_STATE_DRIVER:
            self.send_notification_message(f"Чтобы завести авто используйте {{{Colors.cmd_hex}}}LCTRL{{{Colors.white_hex}}}.")
            vehicle = Vehicle.get_from_registry(self.get_vehicle_id())
            self.send_debug_message(f"on_state_change_handle | Inst: {self} | Veh id: {vehicle.id} | In")
            if vehicle.get_model() not in NoEngineVehicleIDs.ids:
                self.vehicle.last_id = vehicle.id
                self.create_speedometer()
                self.show_speedometer()
                self.vehicle_speedometer[5] = set_timer(self.update_speedometer_velocity, 200, True, vehicle)
                if self.mode == ServerWorldIDs.freeroam_world:
                    self.create_drift_counter()

        if new_state == PLAYER_STATE_ONFOOT and old_state == PLAYER_STATE_DRIVER:
            vehicle = Vehicle.get_from_registry(self.vehicle.last_id)
            self.send_debug_message(f"on_state_change_handle | Inst: {self} | Veh id: {vehicle.id} | Out")
            if vehicle.get_model() not in NoEngineVehicleIDs.ids:
                kill_timer(self.vehicle_speedometer[5])
                self.hide_speedometer()
                if self.mode == ServerWorldIDs.freeroam_world:
                    self.destroy_drift_counter()

    def on_click_textdraw_handle(self, clicked: TextDraw) -> None:
        if clicked.id == TextDraws.class_selection_td[0].id: # Left
            if self._freeroam_selector == 0:
                self._freeroam_selector = len(FreeroamSkins.skins) - 1

            else:
                self._freeroam_selector -= 1

            self.set_skin_ex(FreeroamSkins.skins[self._freeroam_selector])

        if clicked.id == TextDraws.class_selection_td[1].id: # Right
            if self._freeroam_selector == len(FreeroamSkins.skins) - 1:
                self._freeroam_selector = 0

            else:
                self._freeroam_selector += 1

            self.set_skin_ex(FreeroamSkins.skins[self._freeroam_selector])

        if clicked.id == TextDraws.class_selection_td[2].id: # Done
            self.set_skin_ex(FreeroamSkins.skins[self._freeroam_selector])
            self.hide_class_selector_textdraws()
            self.toggle_controllable(True)
            del self._freeroam_selector
            self.is_data.selecting_skin = False
            self.set_mode(ServerWorldIDs.freeroam_world)
            return self.enable_freeroam_mode()

    def on_click_map_handle(self, x: float, y: float, z: float) -> None:
        if self.mode == ServerWorldIDs.freeroam_world and self.vip == 1:
            return self.set_pos(x, y, z)

    def on_start_drift_handle(self) -> None:
        if self.mode == ServerWorldIDs.freeroam_world:
            return self.show_drift_counter()

    def on_drift_update_handle(self, value: int, combo: int, flag_id: int, distance: float, speed: float) -> None:
        if self.mode == ServerWorldIDs.freeroam_world:
            if not self.time.afk >= 1:
                return self.update_drift_counter(value)

    def on_end_drift_handle(self,  value: int, combo: int, reason: int) -> None:
        if self.mode == ServerWorldIDs.freeroam_world:
            return self.hide_drift_counter()


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
        return Dialog.create(1, f"{ServerInfo.name_short} | Авторизация", f"{player.get_name()}, добро пожаловать!\nВведите пароль:", "Ок", "", on_response=cls.login_response).show(player)

    @classmethod
    def login_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return player.kick_if_not_logged()

        if player.tmp.login_attempts == 3:
            return player.kick_if_not_logged()

        if len(input_text) < 6 or len(input_text) > 32:
            player.tmp.login_attempts += 1
            player.send_error_message("Длина пароля должна быть от 6 и до 32 символов!")
            return cls.show_login_dialog(player)

        player_db = DataBase.get_player(player)
        if input_text != player_db.password:
            player.tmp.login_attempts += 1
            player.send_error_message(f"Вы указали неверный пароль ({player.tmp.login_attempts}/3)")
            return cls.show_login_dialog(player)

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
    def email_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            player.email = ""
            player.send_notification_message("Вы пропустили этот шаг.")

        else:
            if len(input_text) < 6 or len(input_text) > 32:
                player.send_error_message("Длина почты должна быть от 6 и до 32 символов!")
                return cls.show_email_dialog(player)

            player.email = input_text

        player.pin = ""
        player.is_data.logged = True
        player.registration_ip = player.get_ip()
        player.registration_data = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        DataBase.create_player(player)
        return cls.show_select_mode_dialog(player)

    @classmethod
    def show_gang_choice_dialog(cls, player: Player) -> int:
        player = Player.from_registry_native(player)
        return Dialog.create(2, f"{ServerInfo.name_short} | Банда", "Grove Street Families\nThe Ballas\nLos Santos Vagos\nVarrios Los Aztecas\nLos Santos Rifa", "Ок", "", on_response=cls.gang_choice_response).show(player)

    @classmethod
    def gang_choice_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            player.send_error_message("Необходимо выбрать группировку!")
            return cls.show_gang_choice_dialog(player)

        player.gang_id = list_item
        player.gang = gangs[player.gang_id]
        if player.get_state() == PLAYER_STATE_SPECTATING:
            player.toggle_spectating(False)
        else:
            player.spawn()

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
        player.set_mode(ServerWorldIDs.gangwar_world)
        return player.enable_gangwar_mode()

    @classmethod
    def show_stats_dialog(cls, player: Player, player_id: int = None) -> Dialog:
        player = Player.from_registry_native(player)
        if player_id is None:
            player_stats = player

        else:
            player_stats = Player.from_registry_native(player_id)

        key, value = player.get_gang_rang()
        ratio = player.kills / player.deaths if player.kills and player.deaths != 0 else 0.0
        level = int(sqrt(player.score) / 2)
        next_lvl_exp = int((2 * ((level + 1))) ** 2)
        return Dialog.create(
            0,
            f"Статистика игрока {player_stats.get_name()}",
            (
                f"Ник:\t\t\t\t{player_stats.get_name()}\n"
                f"Уровень:\t\t\t{{{Colors.cmd_hex}}}{level}{{{Colors.dialog_hex}}} ({player_stats.score}/{next_lvl_exp})\n"
                f"Счёт:\t\t\t\t{{{Colors.cmd_hex}}}{player_stats.score}{{{Colors.dialog_hex}}}\n"
                f"Вирт:\t\t\t\t{{{Colors.green_hex}}}{player_stats.money}${{{Colors.dialog_hex}}}\n"
                f"Донат:\t\t\t\t{{{Colors.cmd_hex}}}{player_stats.donate}{{{Colors.dialog_hex}}}\n"
                f"Ранг:\t\t\t\t{value} ({{{Colors.green_hex}}}{player_stats.kills}{{{Colors.dialog_hex}}}/{key})\n"
                f"Группировка:\t\t\t{{{player_stats.gang.color_hex}}}{player_stats.gang.gang_name}{{{Colors.dialog_hex}}}\n"
                f"Убийств:\t\t\t{{{Colors.green_hex}}}{player_stats.kills}{{{Colors.dialog_hex}}}\n"
                f"Смертей:\t\t\t{{{Colors.red_hex}}}{player_stats.deaths}{{{Colors.dialog_hex}}}\n"
                f"K/D:\t\t\t\t{{{Colors.cmd_hex}}}{round(ratio, 00)}{{{Colors.dialog_hex}}}\n"
                f"Аптечек:\t\t\t{{{Colors.cmd_hex}}}{player_stats.heals}{{{Colors.dialog_hex}}}\n"
                f"Масок:\t\t\t\t{{{Colors.cmd_hex}}}{player_stats.masks}{{{Colors.dialog_hex}}}\n"
                f"Есть VIP:\t\t\t{{{Colors.cmd_hex}}}{'Есть' if player_stats.vip.level != -1 else 'Нет'}{{{Colors.dialog_hex}}}\n"
                f"Выдан мут:\t\t\t{{{Colors.cmd_hex}}}{'Да' if player_stats.is_data.muted else 'Нет'}{{{Colors.dialog_hex}}}"
            ),
            "Закрыть",
            "").show(player)

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

        if player.get_virtual_world() == ServerWorldIDs.gangwar_world:
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
        player.tmp.capture_tuple = (player.get_name(), atk_id, def_id, gangzone_id, ZoneNames.names[zone_id]) # Инициатор, Атака, Оборона, ID
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
            return player.send_notification_message("Вы отменили захват территории.")

        player.gang.is_capturing = True
        player.gang.capture_id = player.tmp.capture_tuple[3]
        gangs[player.tmp.capture_tuple[2]].is_capturing = True
        gangs[player.tmp.capture_tuple[2]].capture_id = player.tmp.capture_tuple[3]
        for player_reg in Player._registry.values():
            if player_reg.gang_id == gangs[player_reg.tmp.capture_tuple[1]].gang_id or player_reg.gang_id == gangs[player_reg.tmp.capture_tuple[2]].gang_id:
                player_reg.send_capture_message(*player.tmp.capture_tuple)

        return player.start_capture(player.tmp.capture_tuple[1], player.tmp.capture_tuple[2], player.tmp.capture_tuple[3])

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
            return cls.show_stats_dialog(player)

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
            "1. Личные команды\n2. Общие команды\n3. GangWar команды\n4. Freeroam команды\n5. VIP команды",
            "Ок",
            "Назад",
            on_response=cls.commands_list_response
        ).show(player)

    @classmethod
    def commands_list_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_mn_dialog(player)

        if list_item == 0:
            return Dialog.create(
                1, "Личные настройки",
                (
                    f"{'Выключить' if player.is_data.disabled_fps_and_ping_td else 'Включить'} счётчик FPS & PING"
                ),
                "Ок",
                "Закрыть"
            ).show(player)

        if list_item == 1:
            return Dialog.create(
                0, "Общие команды",
                (
                    f"{{{Colors.cmd_hex}}}/sms\t\t{{{Colors.dialog_hex}}}Отправка SMS\n"
                    f"{{{Colors.cmd_hex}}}/pay\t\t{{{Colors.dialog_hex}}}Передача денег игроку\n"
                    f"{{{Colors.cmd_hex}}}/id\t\t{{{Colors.dialog_hex}}}Поиск игрока нику\n"
                    f"{{{Colors.cmd_hex}}}/o\t\t{{{Colors.dialog_hex}}}Общий чат\n"
                    f"{{{Colors.cmd_hex}}}/donate\t{{{Colors.dialog_hex}}}Донат\n"
                    f"{{{Colors.cmd_hex}}}/report\t\t{{{Colors.dialog_hex}}}Отправка жалобы/вопроса"
                ),
                "Закрыть",
                "").show(player)

        if list_item == 2:
            return Dialog.create(
                0, "GangWar команды",
                (
                    f"{{{Colors.cmd_hex}}}/healme\t{{{Colors.dialog_hex}}}Использование аптечки\n"
                    f"{{{Colors.cmd_hex}}}/mask\t\t{{{Colors.dialog_hex}}}Использование маски\n"
                    f"{{{Colors.cmd_hex}}}/maskoff\t{{{Colors.dialog_hex}}}Снятие маски\n"
                    f"{{{Colors.cmd_hex}}}/newgang\t{{{Colors.dialog_hex}}}Смена банды\n"
                    f"{{{Colors.cmd_hex}}}/randomskin\t{{{Colors.dialog_hex}}}Случайный скин\n"
                    f"{{{Colors.cmd_hex}}}/changeskin\t{{{Colors.dialog_hex}}}Новый скин\n"
                    f"{{{Colors.cmd_hex}}}/f\t\t{{{Colors.dialog_hex}}}Чат банды\n"
                    f"{{{Colors.cmd_hex}}}/members\t{{{Colors.dialog_hex}}}Онлайн в банде\n"
                    f"{{{Colors.cmd_hex}}}/gangzones\t{{{Colors.dialog_hex}}}Список территорий\n"
                    f"{{{Colors.cmd_hex}}}/capture\t{{{Colors.dialog_hex}}}Захват территории"
                ),
                "Закрыть",
                "").show(player)

        if list_item == 3:
            return Dialog.create(
                0, "Freeroam команды",
                (
                    f"{{{Colors.cmd_hex}}}/weapons\t{{{Colors.dialog_hex}}}Покупка оружия\n"
                    f"{{{Colors.cmd_hex}}}/vehicles\t{{{Colors.dialog_hex}}}Покупка транспорта\n"
                    f"{{{Colors.cmd_hex}}}/elegy\t{{{Colors.dialog_hex}}}Покупка Elegy\n"
                    f"{{{Colors.cmd_hex}}}/infernus\t{{{Colors.dialog_hex}}}Покупка Ifernus\n"
                    f"{{{Colors.cmd_hex}}}/bullet\t{{{Colors.dialog_hex}}}Покупка Bullet\n"
                    f"{{{Colors.cmd_hex}}}/sultan\t{{{Colors.dialog_hex}}}Покупка Sultan\n"
                ),
                "Закрыть",
                "").show(player)


        if list_item == 4:
            return Dialog.create(
                0, "VIP команды",
                (
                    f"{{{Colors.cmd_hex}}}/vipinfo\t\t{{{Colors.dialog_hex}}}Информация о VIP статусах\n"
                    f"{{{Colors.cmd_hex}}}/vc\t\t{{{Colors.dialog_hex}}}VIP чат\n"
                    f"{{{Colors.cmd_hex}}}/vbuy\t\t{{{Colors.dialog_hex}}}VIP транспорт\n"
                    f"{{{Colors.cmd_hex}}}/rclist\t\t{{{Colors.dialog_hex}}}Переливающийся цвет игрока"
                    f"{{{Colors.cmd_hex}}}/jp\t\t{{{Colors.dialog_hex}}}Покупка джетпака\n"
                ),
                "Закрыть",
                "").show(player)

    @classmethod
    def show_select_mode_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Выбрать режим",
            "GangWar\nDeathmatch (Indev)\nFreeroam\nMinigames (Indev)",
            "Ок",
            "",
            on_response=cls.select_mode_response
        ).show(player)

    @classmethod
    def select_mode_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            player.send_error_message("Необходимо выбрать режим!")
            return cls.show_select_mode_dialog(player)

        if list_item == 0:
            if player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world]):
                return player.send_error_message("Вы уже выбрали этот режим!")

            player.set_mode(ServerWorldIDs.gangwar_world)
            player.send_notification_message(f"Вы выбрали режим {{{Colors.cmd_hex}}}GangWar{{{Colors.white_hex}}}!")
            return cls.show_gang_choice_dialog(player)

        if list_item == 1:
            ...

        if list_item == 2:
            if player.check_player_mode([ServerWorldIDs.freeroam_world]):
                return player.send_error_message("Вы уже выбрали этот режим!")

            player.send_notification_message(f"Вы выбрали режим {{{Colors.cmd_hex}}}Freeroam{{{Colors.white_hex}}}!")
            if player.get_state() == PLAYER_STATE_SPECTATING:
                player.toggle_spectating(False)
            else:
                player.spawn()
            return player.enable_freeroam_selector()

    # @classmethod
    # def show_password_ask_dialog(cls, player) -> None:
    #     player = Player.from_registry_native(player)
    #     return Dialog.create(
    #         3,
    #         "Введите пароль",
    #         "Перед продолжением необходимо указать пароль:",
    #         "Ок",
    #         "Назад",
    #         on_response=cls.password_ask_response
    #     ).show(player)

    # @classmethod
    # def password_ask_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
    #     player = Player.from_registry_native(player)
    #     if not response:
    #         return cls.show_mn_dialog(player)

    #     if len(input_text) < 6 or len(input_text) > 32:
    #         return player.send_error_message("Длина пароля должна быть от 6 и до 32 символов!")

    #     player_db = DataBase.get_player(player)
    #     if input_text != player_db.password:
    #         return player.send_error_message("Вы указали неверный пароль!")

    #     return cls.show_privacy_settings_dialog(player)

    @classmethod
    def show_account_settings_dialog(cls, player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Настройки аккаунта",
            (
                f"1. Изменить e-mail\n"
                f"2. Изменить PIN код\n"
                f"3. {'Отключить' if player.settings.disabled_ping_td else 'Включить'} показание пинга\n"
                f"4. {'Отключить' if player.settings.disabled_global_chat_gw else 'Включить'} глобальный чат в режиме GangWar по умолчанию\n"

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

            return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}{'включили' if player.settings.disabled_ping_td else 'отключили'}{{{Colors.white_hex}}} показание пинга.")

        if list_item == 3:
            if player.settings.disabled_global_chat_gw:
                player.settings.disabled_global_chat_gw = False

            else:
                player.settings.disabled_global_chat_gw = True

            return player.send_notification_message(f"Вы {{{Colors.cmd_hex}}}{'включили' if player.settings.disabled_global_chat_gw else 'отключили'}{{{Colors.white_hex}}} глобальный чат по умолчанию в режиме {{{Colors.cmd_hex}}}GangWar{{{Colors.white_hex}}}.")

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
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}${{{Colors.dialog_hex}}}\n"

        if list_item == 1: # Offroad
            veh_type = VehicleTypes.OFFROAD
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.OFFROAD:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}${{{Colors.dialog_hex}}}\n"

        if list_item == 2: # Services
            veh_type = VehicleTypes.SERVICES
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.SERVICES:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}${{{Colors.dialog_hex}}}\n"

        if list_item == 3: # Sedan
            veh_type = VehicleTypes.SEDAN
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.SEDAN:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}${{{Colors.dialog_hex}}}\n"

        if list_item == 4: # Sport
            veh_type = VehicleTypes.SPORT
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.SPORT:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}${{{Colors.dialog_hex}}}\n"

        if list_item == 5: # Universal
            veh_type = VehicleTypes.UNIVERSAL
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.UNIVERSAL:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}${{{Colors.dialog_hex}}}\n"

        if list_item == 6: # Uniqe
            veh_type = VehicleTypes.UNIQE
            for id, veh in VehicleData.data.items():
                if veh[0] == VehicleTypes.UNIQE:
                    veh_str += f"{{{Colors.dialog_hex}}}{id}\t{{{Colors.cmd_hex}}}{veh[1]}\t{{{Colors.green_hex}}}{veh[2]}${{{Colors.dialog_hex}}}\n"

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

        player.remove_unused_vehicle()
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
        player.vehicle.id = player_veh.id
        player.put_in_vehicle(player.vehicle.id, 0)