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
    send_death_message,
    send_client_message,
    create_player_3d_text_label,
    delete_player_3d_text_label,
    gang_zone_show_for_player,
    gang_zone_hide_for_player,
    text_draw_show_for_player,
    text_draw_hide_for_player,
    gang_zone_flash_for_player,
    gang_zone_stop_flash_for_player,
    call_remote_function,
    select_text_draw,
    cancel_select_text_draw

)
from .utils import *
from functools import wraps
from datetime import datetime
from zoneinfo import ZoneInfo
from .gang import gangs, GangZoneData
from .textdraws import TextDraws
from .version import __version__
from .database import DataBase
from .vehicle import Vehicle
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
        self.donate: int = 0
        self.kills: int = 0
        self.deaths: int = 0
        self.heals: int = 0
        self.masks: int = 0
        self.skin: int = 0
        self.gang_id: int = -1 # No gang
        self.gang: list = gangs[self.gang_id]
        self.mode: int = 0
        self.vip: int = 1
        self.is_muted: bool = False
        self.is_jailed: bool = False
        self.is_logged: bool = False
        self.is_banned: bool = False
        self.is_wearing_mask: bool = False
        self.cooldown_time: float = None
        self.vehicle_speedometer: dict = {}

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
        self.vehicle_speedometer[2] = PlayerTextDraw.create(self, 442.399963, 386.026580, "SPEED: 0")
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
        self.vehicle_speedometer[0].hide()
        self.vehicle_speedometer[1].hide()
        self.vehicle_speedometer[2].hide()
        self.vehicle_speedometer[3].hide()
        self.vehicle_speedometer[4].hide()

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
        return self.vehicle_speedometer[2].set_string(f"SPEED: {self.get_speed_in_vehicle(vehicle)}")

    def get_speed_in_vehicle(self, vehicle: Vehicle):
        x, y, z = vehicle.get_velocity()
        x_res = abs(x)**2.0
        y_res = abs(y)**2.0
        z_res = abs(z)**2.0

        res = sqrt(x_res + y_res + z_res) * 100.3
        return int(res)

    def send_error_message(self, message: str) -> None:
        return self.send_client_message(Colors.red, f"[ОШИБКА] {message}")

    def send_notification_message(self, message: str) -> None:
        return self.send_client_message(Colors.white, f"{message}")

    def send_capture_message(self, initiator: str, atk_id: int, def_id: int, gangzone_id: int, zone_name: str) -> None:
        self.send_client_message(Colors.white, f"{{{gangs[atk_id].color_hex}}}{initiator}{{{Colors.white_hex}}} инициировал захват территории {{{Colors.cmd_hex}}}{zone_name}{{{Colors.white_hex}}}!")
        return self.send_client_message(Colors.white, f"Началась война между {{{gangs[atk_id].color_hex}}}{gangs[atk_id].gang_name}{{{Colors.white_hex}}} и {{{gangs[def_id].color_hex}}}{gangs[def_id].gang_name}{{{Colors.white_hex}}}!")

    def get_gang_rang(self):
        for key, value in self.gang.rangs.items():
            if self.kills <= key:
                return key, value

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
        for key in TextDraws.logo.keys():
            text_draw_show_for_player(self.id, key)

    def check_cooldown(self, unix_seconds: float) -> bool:
        if self.cooldown_time is not None:
            if (time.time() - self.cooldown_time) < unix_seconds:
                return False

        self.cooldown_time = time.time()
        return True

    def update_player_cooldown_time(self) -> float:
        self.cooldown_time = time.time()
        return self.cooldown_time

    def kick_if_not_logged(self) -> None:
        encode()
        if not self.is_logged:
            Dialogs.show_kick_dialog(self)
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.kick, 1000, False)

    def kick_teamkill(self) -> None:
        encode()
        Dialogs.show_kick_teamkill(self)
        self.send_error_message("Введите /q (/quit) чтобы выйти!")
        return set_timer(self.kick, 1000, False)

    def ban_from_server(self) -> None:
        encode()
        if self.is_banned:
            Dialogs.show_banned_dialog(self)
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.ban, 1000, False)

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
        if ((x <= max_x and x >= min_x) and (y <= max_y and y >= min_y)): # I don't fucking know how it works
            return True

        return False

    def enable_gangwar_mode(self, first_show: bool = True):
        self.set_pos(self.gang.spawn_pos[0], self.gang.spawn_pos[1], self.gang.spawn_pos[2])
        self.set_camera_behind()
        self.set_virtual_world(ServerWorldIDs.gangwar_world_interior)
        self.mode = self.get_virtual_world()
        self.set_interior(self.gang.interior_id)
        if first_show: # Если показывается первый раз
            self.set_skin(random.choice(self.gang.skins))
            self.skin = self.get_skin()
            self.set_color(self.gang.color)
            self.set_score(self.kills)
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
        self.toggle_controllable(False)
        self.set_skin(FreeroamSkins.skins[0])
        self.skin = self.get_skin()
        self.set_pos(204.6633, -6.5563, 1001.2109)
        self.set_facing_angle(299.4084)
        self.set_camera_position(208.7765, -3.9595, 1001.2178)
        self.set_camera_look_at(204.6633, -6.5563, 1001.2109)
        self.set_interior(5)
        self._freeroam_selector = 0
        return self.show_class_selector_textdraws()

    def _set_freeroam_spawn_info(self):
        self.set_spawn_info(
            255,
            self.skin,
            RandomSpawns.spawns[0][0],
            RandomSpawns.spawns[0][1],
            RandomSpawns.spawns[0][2],
            0.0, 0, 0, 0, 0, 0, 0)

    def enable_freeroam_mode(self):
        self.set_camera_behind()
        self.set_virtual_world(ServerWorldIDs.freeroam_world)
        self.set_interior(0)
        self.set_score(0)
        self.set_color(randint(0, 16777215))
        self.disable_gangzones_for_player()
        self.mode = self.get_virtual_world()
        self.set_pos(RandomSpawns.spawns[0][0], RandomSpawns.spawns[0][1], RandomSpawns.spawns[0][2])
        self._set_freeroam_spawn_info()
        return self.game_text(f"Welcome~n~{self.get_name()}", 2000, 1)

    def prox_detector(self, max_range: float, color: int, message: str, max_ratio: float = 1.6) -> None:
        if not self.get_pos():
            return

        color_r = float(color >> 24 & 0xFF)
        color_g = float(color >> 16 & 0xFF)
        color_b = float(color >> 8 & 0xFF)
        range_with_ratio = max_range * max_ratio
        print(self._registry)
        for player in self._registry:
            player = self.from_registry_native(player)
            if self.id == player.id:
                continue

            if not self.is_streamed_in(player):
                continue

            range = player.distance_from_point(*self.get_pos())
            if range > max_range:
                continue

            range_ratio = (range_with_ratio - range) / range_with_ratio
            clr_r = int(range_ratio * color_r)
            clr_g = int(range_ratio * color_g)
            clr_b = int(range_ratio * color_b)
            send_client_message(player.id, (color & 0xFF) | (clr_b << 8) | (clr_g << 16) | (clr_r << 24), f"{self.get_name()}: {message}")

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
        self.password = player_db.password
        self.email = player_db.email
        self.pin = player_db.pin
        self.registration_ip = player_db.registration_ip
        self.registration_data = player_db.registration_data
        self.donate = player_db.donate
        self.kills = player_db.kills
        self.deaths = player_db.deaths
        self.heals = player_db.heals
        self.masks = player_db.masks
        self.gang_id = player_db.gang_id
        self.gang = gangs[self.gang_id]
        self.vip = player_db.vip
        self.is_muted = player_db.is_muted
        self.is_jailed = player_db.is_jailed
        self.is_logged = True
        self.is_banned = False
        self.set_virtual_world(ServerWorldIDs.default_world)
        self.mode = self.get_virtual_world()
        self.set_max_gun_skill()
        return Dialogs.show_select_mode_dialog(self)

    def show_credits_dialog(self):
        return Dialogs.show_credits_dialog(self)

    def show_class_selector_textdraws(self):
        select_text_draw(self.id, Colors.textdraw)
        text_draw_show_for_player(self.id, 6)
        text_draw_show_for_player(self.id, 7)
        text_draw_show_for_player(self.id, 8)

    def hide_class_selector_textdraws(self):
        cancel_select_text_draw(self.id)
        text_draw_hide_for_player(self.id, 6)
        text_draw_hide_for_player(self.id, 7)
        text_draw_hide_for_player(self.id, 8)

    def show_capture_textdraws(self, player_id: int = None):
        if not player_id:
            player_id = self.id
        text_draw_show_for_player(player_id, 3)
        text_draw_show_for_player(player_id, 4)
        text_draw_show_for_player(player_id, 5)

    def hide_capture_textdraws(self, player_id: int = None):
        if not player_id:
            player_id = self.id

        text_draw_hide_for_player(player_id, 3)
        text_draw_hide_for_player(player_id, 4)
        text_draw_hide_for_player(player_id, 5)

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
        for player in self._registry: # Общий показ текстдрава капта для двух банд
            player = self.from_registry_native(player)
            if (player.gang_id == atk_id) or (player.gang_id == def_id):
                player.set_team(player.gang_id)
                player.send_notification_message("Во время войны урон по своим был отключён!")
                gang_zone_flash_for_player(player.id, gz.gangzone_id, gangs[gz.gang_atk_id].color)
                player.show_capture_textdraws(player.id)

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
                player.remove_map_icon(player.gang_id)

        destroy_dynamic_map_icon(0)
        gangzone.gang_atk_id = -1
        gangzone.gang_def_id = -1
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
        self.send_notification_message("ON CONNECT")
        encode()
        if self.is_connected():
            for i in range(25):
                self.send_notification_message(" ")
            self.send_notification_message(f"Добро пожаловать на сервер {{{Colors.cmd_hex}}}{ServerInfo.name_short}{{{Colors.white_hex}}}!")
            self.send_notification_message(f"Последняя версия: {{{Colors.cmd_hex}}}{__version__}{{{Colors.white_hex}}}!")
            self.show_server_logotype()
            self.toggle_spectating(True)
            player_db = DataBase.get_player(self)
            if not player_db:
                return Dialogs.show_registration_dialog(self)

            if not player_db.is_banned:
                return Dialogs.show_login_dialog(self)

            return self.ban_from_server()

    def on_disconnect_handle(self) -> None:
        if self.is_logged:
            DataBase.save_player(
                self,
                password=self.password,
                email=self.email,
                pin=self.pin,
                last_ip=self.last_ip,
                donate=self.donate,
                kills=self.kills,
                deaths=self.deaths,
                heals=self.heals,
                masks=self.masks,
                gang_id=self.gang_id,
                vip=self.vip,
                is_muted=self.is_muted,
                is_jailed=self.is_jailed,
                is_banned=self.is_banned)

        return self.delete_registry(self)

    def on_request_class_handle(self, class_id: int) -> None:
        self.send_notification_message("ON REQUEST HANDLE")
        self.kick_if_not_logged()
        self.spawn()
        return True

    def on_spawn_handle(self) -> None:
        self.send_notification_message(f"ON SPAWN HANDLE | WORLD_ID: {self.get_virtual_world()} | INTERIOR: {self.get_interior()}")
        if self.mode == ServerWorldIDs.gangwar_world or self.mode == ServerWorldIDs.gangwar_world_interior:
            return self.enable_gangwar_mode()

        if self.mode == ServerWorldIDs.freeroam_world_interior: # Если игрок выбирает скин во freeroam, то включить селектор. Так как игрок уже заспавнен
            return self.enable_freeroam_selector()

        if self.mode == ServerWorldIDs.freeroam_world: # Если игрок в обычном фрироме и выбрал скин, то просто ставить позицию т.д
            return self.enable_freeroam_mode()

    def on_death_handle(self, killer: "Player", reason: int) -> None:
        self.send_notification_message("ON DEATH HANDLE")
        self.kick_if_not_logged()
        self.deaths += 1
        self.masks = 0
        self.heals = 0
        if killer.id == INVALID_PLAYER_ID:
            killer.delete_registry(killer)

        if not killer.gang_id != self.gang_id:
            killer.kick_teamkill()

        killer.kills += 1
        killer.set_score(killer.kills)
        if killer.gang.is_capturing:
            if killer.gang.capture_id == self.gang.capture_id:
                gz = GangZoneData.get_from_registry(killer.gang.capture_id)
                gz.gang_atk_score += 1
                send_death_message(killer.id, self.id, reason)

        if self.mode == ServerWorldIDs.gangwar_world or self.mode == ServerWorldIDs.gangwar_world_interior:
            return self.set_spawn_info(
                255,
                self.skin,
                self.gang.spawn_pos[0],
                self.gang.spawn_pos[1],
                self.gang.spawn_pos[2],
                0.0, 0, 0, 0, 0, 0, 0)

        if self.mode == ServerWorldIDs.freeroam_world or self.mode == ServerWorldIDs.freeroam_world_interior:
            return self._set_freeroam_spawn_info()


    def on_text_handle(self, text: str) -> False:
        self.kick_if_not_logged()
        encode()
        if self.is_muted:
            self.set_chat_bubble("Пытается что-то сказать..", Colors.red, 20.0, 10000)
            return self.send_error_message("Доступ в чат заблокирован!")

        self.set_chat_bubble(text, -1, 20.0, 10000)
        self.prox_detector(20.0, -1, text)
        return False

    def on_pick_up_pickup_handle(self, pickup: DynamicPickup) -> None:
        self.kick_if_not_logged()
        encode()
        if pickup.id == gangs[0].enter_exit[0].id: # Grove enter
            if not self.gang_id == gangs[0].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(2466.2649, -1698.4724, 1013.5078)
            self.set_facing_angle(90.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world_interior)
            self.set_interior(2)

        if pickup.id == gangs[0].enter_exit[1].id: # Grove exit
            if not self.gang_id == gangs[0].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2495.3022, -1688.5438, 13.8722)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world)
            self.set_interior(0)

        if pickup.id == gangs[1].enter_exit[0].id: # Ballas enter
            if not self.gang_id == gangs[1].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(-42.6860, 1408.4878, 1084.4297)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world_interior)
            self.set_interior(8)

        if pickup.id == gangs[1].enter_exit[1].id: # Ballas exit
            if not self.gang_id == gangs[1].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2022.9169, -1122.7472, 26.2329)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world)
            self.set_interior(0)

        if pickup.id == gangs[2].enter_exit[0].id: # Vagos enter
            if not self.gang_id == gangs[2].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(318.564971, 1118.209960, 1083.882812)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world_interior)
            self.set_interior(5)

        if pickup.id == gangs[2].enter_exit[1].id: # Vagos exit
            if not self.gang_id == gangs[2].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2756.1492, -1180.2386, 69.3978)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world)
            self.set_interior(0)

        if pickup.id == gangs[3].enter_exit[0].id: # Aztecas enter
            if not self.gang_id == gangs[3].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(223.0174, 1240.1416, 1082.1406)
            self.set_facing_angle(270.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world_interior)
            self.set_interior(2)

        if pickup.id == gangs[3].enter_exit[1].id: # Aztecas exit
            if not self.gang_id == gangs[3].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2185.6555, -1812.5112, 13.5650)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world)
            self.set_interior(0)

        if pickup.id == gangs[4].enter_exit[0].id: # Rifa enter
            if not self.gang_id == gangs[4].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(-68.9146, 1353.8420, 1080.2109)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world_interior)
            self.set_interior(6)

        if pickup.id == gangs[4].enter_exit[1].id: # Rifa exit
            if not self.gang_id == gangs[4].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2784.5544, -1926.1563, 13.5469)
            self.set_facing_angle(90.0)
            self.set_camera_behind()
            self.set_virtual_world(ServerWorldIDs.gangwar_world)
            self.set_interior(0)

        self.mode = self.get_virtual_world()

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
        pass

    def on_damage_handler(self, issuer: "Player", amount: float, weapon_id: int, body_part) -> None:
        self.play_sound(17802, 0.0, 0.0, 0.0)
        x, y, z, to_x, to_y, to_z = self.get_last_shot_vectors()
        damage_informer = create_player_3d_text_label(self.id, f"{int(amount)}", Colors.white, to_x, to_y, to_z, 150)
        return set_timer(delete_player_3d_text_label, 1000, False, self.id, damage_informer)

    def on_key_state_change_handle(self, new_keys: int, old_keys: int) -> None:
        self.kick_if_not_logged()
        if (old_keys == 65536) and (new_keys == 0):
            return Dialogs.show_mn_dialog(self)

        if (self.get_state() == PLAYER_STATE_DRIVER) and (old_keys == 1):
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
            self.create_speedometer()
            self.show_speedometer()
            vehicle = Vehicle.get_from_registry(self.get_vehicle_id())
            self.vehicle_speedometer[5] = set_timer(self.update_speedometer_velocity, 200, True, vehicle)

        if new_state == PLAYER_STATE_ONFOOT and old_state == PLAYER_STATE_DRIVER:
            kill_timer(self.vehicle_speedometer[5])
            return self.hide_speedometer()

    def on_click_textdraw_handle(self, clicked: TextDraw) -> None:
        if clicked.id == TextDraws.class_selection_td[0].id: # Left
            if self._freeroam_selector == 0:
                self._freeroam_selector = len(FreeroamSkins.skins) - 1

            else:
                self._freeroam_selector -= 1

            self.send_notification_message(f"LEFT: {self._freeroam_selector}/{len(FreeroamSkins.skins)}")
            self.set_skin(FreeroamSkins.skins[self._freeroam_selector])

        if clicked.id == TextDraws.class_selection_td[1].id: # Right
            if self._freeroam_selector == len(FreeroamSkins.skins) - 1:
                self._freeroam_selector = 0

            else:
                self._freeroam_selector += 1

            self.send_notification_message(f"RIGHT: {self._freeroam_selector}/{len(FreeroamSkins.skins)}")
            self.set_skin(FreeroamSkins.skins[self._freeroam_selector])

        if clicked.id == TextDraws.class_selection_td[2].id: # Done
            self.set_skin(FreeroamSkins.skins[self._freeroam_selector])
            self.hide_class_selector_textdraws()
            self.toggle_controllable(True)
            del self._freeroam_selector
            return self.enable_freeroam_mode()


class Dialogs:
    login_attempt: dict = {}
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
        return Dialog.create(0, "[ОШИБКА]", "Вы забанены на этом сервере!.", "Закрыть", "").show(player)

    @classmethod
    def show_credits_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(
            0,
            "О проекте",
            f"San Andreas {{{Colors.error_hex}}}Gang War\n\n{{{Colors.dialog_hex}}}Разработчик:\t{{{Colors.vagos_hex}}}Ykpauneu\n{{{Colors.dialog_hex}}}Тестировщик:\t{{{Colors.rifa_hex}}}Rein.{{{Colors.dialog_hex}}}\n\nВерсия:\t{{{Colors.cmd_hex}}}{__version__}",
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
                player.send_notification_message(f"Вы взяли 3 аптечки. Используйте {{{Colors.cmd_hex}}}/healme{{{Colors.white_hex}}} для применения аптечки.")
                return cls.show_warehouse_dialog(player)

            else:
                return player.send_error_message("У Вас уже есть аптечки!")

        if list_item == 1: # Masks
            if player.masks < 3:
                player.masks = 3
                player.send_notification_message(f"Вы взяли 3 маски. Используйте {{{Colors.cmd_hex}}}/mask{{{Colors.white_hex}}} для применения маски.")
                return cls.show_warehouse_dialog(player)

            else:
                return player.send_error_message("У Вас уже есть маски!")

        if list_item == 2: # Guns
            return Dialog.create(2, "Выбор оружия", "1. Desert Eagle\n2. Shotgun\n3. AK-47\n4. M4\n5. Rifle\n6. Бита", "Ок", "Закрыть", on_response=cls.warehouse_gun_response).show(player)

    @classmethod
    def warehouse_gun_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_warehouse_dialog(player)

        if list_item == 0:
            player.give_weapon(24, 100)
            player.send_notification_message("Вы взяли Desert Eagle.")
            return cls.show_warehouse_dialog(player)

        if list_item == 1:
            player.give_weapon(25, 100)
            player.send_notification_message("Вы взяли Shotgun.")
            return cls.show_warehouse_dialog(player)

        if list_item == 2:
            player.give_weapon(30, 100)
            player.send_notification_message("Вы взяли AK-47.")
            return cls.show_warehouse_dialog(player)

        if list_item == 3:
            player.give_weapon(31, 100)
            player.send_notification_message("Вы взяли M4.")
            return cls.show_warehouse_dialog(player)

        if list_item == 4:
            player.give_weapon(33, 100)
            player.send_notification_message("Вы взяли Rifle.")
            return cls.show_warehouse_dialog(player)

        if list_item == 5:
            player.give_weapon(5, 1)
            player.send_notification_message("Вы взяли биту.")
            return cls.show_warehouse_dialog(player)

    @classmethod
    def show_login_dialog(cls, player: Player) -> int:
        player = Player.from_registry_native(player)
        return Dialog.create(1, f"{ServerInfo.name_short} | Авторизация", f"{player.get_name()}, добро пожаловать!\nВведите пароль:", "Ок", "", on_response=cls.login_response).show(player)

    @classmethod
    def login_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            del cls.login_attempt[player.id]
            return player.kick_if_not_logged()

        cls.login_attempt[player.id] = 1
        if cls.login_attempt[player.id] == 3:
            return player.kick_if_not_logged()

        if len(input_text) < 6 or len(input_text) > 32:
            cls.login_attempt[player.id] += 1
            player.send_error_message("Длина пароля должна быть от 6 и до 32 символов!")
            return cls.show_login_dialog(player)

        player_db = DataBase.get_player(player)
        if input_text != player_db.password:
            cls.login_attempt[player.id] += 1
            player.send_error_message(f"Вы указали неверный пароль ({cls.login_attempt[player.id]}/3)")
            return cls.show_login_dialog(player)

        del cls.login_attempt[player.id]
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
            return cls.show_select_mode_dialog(player)

        if len(input_text) < 6 or len(input_text) > 32:
            player.send_error_message("Длина почты должна быть от 6 и до 32 символов!")
            return cls.show_email_dialog(player)

        player.email = input_text
        player.pin = ""
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

        if not player.is_logged:
            player.is_logged = True
            player.registration_ip = player.get_ip()
            player.registration_data = datetime.now(tz=ZoneInfo("Europe/Moscow"))
            DataBase.create_player(player)

        player.gang_id = list_item
        player.gang = gangs[player.gang_id]
        player.set_max_gun_skill()
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
        return player.enable_gangwar_mode()

    @classmethod
    def show_stats_dialog(cls, player: Player) -> Dialog:
        player = Player.from_registry_native(player)
        key, value = player.get_gang_rang()
        ratio = player.kills / player.deaths if player.kills and player.deaths != 0 else 0.0
        return Dialog.create(
            0,
            f"Статистика игрока {player.get_name()}",
            f"Имя:\t\t\t\t{player.get_name()}\n\t\t[GANGWAR]\nРанг:\t\t\t\t{value} ({{{Colors.green_hex}}}{player.kills}{{{Colors.dialog_hex}}}/{key})\nГруппировка:\t\t\t{{{player.gang.color_hex}}}{player.gang.gang_name}{{{Colors.dialog_hex}}}\nУбийств:\t\t\t{{{Colors.green_hex}}}{player.kills}{{{Colors.dialog_hex}}}\nСмертей:\t\t\t{{{Colors.error_hex}}}{player.deaths}{{{Colors.dialog_hex}}}\nK/D:\t\t\t\t{{{Colors.cmd_hex}}}{round(ratio, 00)}{{{Colors.dialog_hex}}}\nАптечек:\t\t\t{{{Colors.cmd_hex}}}{player.heals}{{{Colors.dialog_hex}}}\nМасок:\t\t\t\t{{{Colors.cmd_hex}}}{player.masks}\n",
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

        if player.get_virtual_world() == ServerWorldIDs.gangwar_world_interior:
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
        player._tmp_capture_tuple = (player.get_name(), atk_id, def_id, gangzone_id, ZoneNames.names[zone_id]) # Инициатор, Атака, Оборона, ID
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
            del player._tmp_capture_tuple
            return player.send_notification_message("Вы отменили захват территории.")

        player.gang.is_capturing = True
        player.gang.capture_id = player._tmp_capture_tuple[3]
        gangs[player._tmp_capture_tuple[2]].is_capturing = True
        gangs[player._tmp_capture_tuple[2]].capture_id = player._tmp_capture_tuple[3]
        for player_reg in Player._registry:
            player_reg = Player.from_registry_native(player_reg)
            if player_reg.gang_id == gangs[player_reg._tmp_capture_tuple[1]].gang_id: # atk
                player_reg.send_capture_message(*player._tmp_capture_tuple)

            if player_reg.gang_id == gangs[player_reg._tmp_capture_tuple[2]].gang_id: # def
                player_reg.send_capture_message(*player._tmp_capture_tuple)

        player.start_capture(player._tmp_capture_tuple[1], player._tmp_capture_tuple[2], player._tmp_capture_tuple[3])
        del player._tmp_capture_tuple

    @classmethod
    def show_mn_dialog(cls, player) -> Dialog:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Меню игрока",
            f"1. Статистика\n2. Список команд\n3. Выбрать режим\n4. Настройки безопасности\n5. Связь с администрацией\n6. Донат\n7. О проекте",
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
            return cls.show_password_ask_dialog(player)

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
            "1. Личные команды\n2. Общие команды\n3. GangWar команды",
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
            ...

        if list_item == 1:
            return Dialog.create(
                0, "Общие команды",
                (
                    f"{{{Colors.cmd_hex}}}/sms\t{{{Colors.dialog_hex}}}Отправка SMS\n"
                    f"{{{Colors.cmd_hex}}}/id\t{{{Colors.dialog_hex}}}Поиск игрока нику\n"
                    f"{{{Colors.cmd_hex}}}/o\t{{{Colors.dialog_hex}}}Общий чат\n"
                    f"{{{Colors.cmd_hex}}}/donate\t{{{Colors.dialog_hex}}}Донат\n"
                    f"{{{Colors.cmd_hex}}}/report\t{{{Colors.dialog_hex}}}Отправка жалобы/вопроса\n"
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
                    f"{{{Colors.cmd_hex}}}/changeskin\t{{{Colors.dialog_hex}}}Смена скина\n"
                    f"{{{Colors.cmd_hex}}}/f\t\t{{{Colors.dialog_hex}}}Чат банды\n"
                    f"{{{Colors.cmd_hex}}}/members\t{{{Colors.dialog_hex}}}Онлайн в банде\n"
                    f"{{{Colors.cmd_hex}}}/gangzones\t{{{Colors.dialog_hex}}}Список территорий\n"
                    f"{{{Colors.cmd_hex}}}/capture\t{{{Colors.dialog_hex}}}Захват территории"
                ),
                "Закрыть",
                "").show(player)

    @classmethod
    def show_select_mode_dialog(cls, player: Player):
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Выбрать режим",
            "GangWar\nDeathmatch (Indev)\nFreeroam\nDrift (Indev)\nRace (Indev)\nMinigames (Indev)",
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
            if player.check_player_mode([ServerWorldIDs.gangwar_world, ServerWorldIDs.gangwar_world_interior]):
                return player.send_error_message("Вы уже выбрали этот режим!")

            player.set_virtual_world(ServerWorldIDs.gangwar_world)
            player.mode = player.get_virtual_world()
            player.send_notification_message(f"Вы выбрали режим {{{Colors.cmd_hex}}}GangWar{{{Colors.white_hex}}}!")
            return cls.show_gang_choice_dialog(player)

        if list_item == 1:
            ...

        if list_item == 2:
            if player.check_player_mode([ServerWorldIDs.freeroam_world, ServerWorldIDs.freeroam_world_interior]):
                return player.send_error_message("Вы уже выбрали этот режим!")

            player.set_virtual_world(ServerWorldIDs.freeroam_world_interior)
            player.mode = player.get_virtual_world()
            player.send_notification_message(f"Вы выбрали режим {{{Colors.cmd_hex}}}Freeroam{{{Colors.white_hex}}}!")
            player.set_max_gun_skill()
            if player.get_state() == PLAYER_STATE_SPECTATING:
                player.toggle_spectating(False)
            else:
                player.spawn()
            return player.enable_freeroam_selector()

    @classmethod
    def show_password_ask_dialog(cls, player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            3,
            "Введите пароль",
            "Перед продолжением необходимо указать пароль:",
            "Ок",
            "Назад",
            on_response=cls.password_ask_response
        ).show(player)

    @classmethod
    def password_ask_response(cls, player: Player, response: int, list_item: int, input_text: str) -> None:
        player = Player.from_registry_native(player)
        if not response:
            return cls.show_mn_dialog(player)

        if len(input_text) < 6 or len(input_text) > 32:
            return player.send_error_message("Длина пароля должна быть от 6 и до 32 символов!")

        player_db = DataBase.get_player(player)
        if input_text != player_db.password:
            return player.send_error_message("Вы указали неверный пароль!")

        return cls.show_privacy_settings_dialog(player)

    @classmethod
    def show_privacy_settings_dialog(cls, player) -> None:
        player = Player.from_registry_native(player)
        return Dialog.create(
            2,
            "Настройки безопасности",
            "1. Изменить e-mail\n2. Изменить PIN код",
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

        return player.send_notification_message("Ваше сообщение было отправлено!")
        # TODO: Доделать админ систему

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
                return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{50 - player.donate}{{{Colors.error_hex}}} донат очков!")

            if player.vip != -1 and player.vip >= 0:
                return player.send_error_message("У Вас уже есть VIP-статус!")

            player.donate -= 50
            player.vip = 0
            return player.send_notification_message(f"Вы купили {{{VIPData.colors[player.vip]}}}BRONZE VIP{{{Colors.white_hex}}}!")

        if list_item == 2:
            if player.donate < 100:
                return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{100 - player.donate}{{{Colors.error_hex}}} донат очков!")

            if player.vip != -1 and player.vip >= 1:
                return player.send_error_message("У Вас уже есть VIP-статус!")

            player.donate -= 100
            player.vip = 1
            return player.send_notification_message(f"Вы купили {{{VIPData.colors[player.vip]}}}SILVER VIP{{{Colors.white_hex}}}!")

        if list_item == 3:
            if player.donate < 200:
                return player.send_error_message(f"Вам не хватает {{{Colors.cmd_hex}}}{200 - player.donate}{{{Colors.error_hex}}} донат очков!")

            if player.vip != -1 and player.vip >= 2:
                return player.send_error_message("У Вас уже есть VIP-статус!")

            player.donate -= 200
            player.vip = 2
            return player.send_notification_message(f"Вы купили {{{VIPData.colors[player.vip]}}}GOLD VIP{{{Colors.white_hex}}}!")
