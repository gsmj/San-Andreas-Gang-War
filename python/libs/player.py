from pysamp.player import Player as BasePlayer
from pysamp.dialog import Dialog
from pystreamer.dynamicpickup import DynamicPickup
from pystreamer.dynamiccp import DynamicCheckpoint
from pysamp.timer import set_timer
from pysamp import (
    send_death_message,
    send_client_message,
    create_player_3d_text_label,
    delete_player_3d_text_label,
    gang_zone_show_for_player,
    gang_zone_hide_for_player,
    text_draw_show_for_player
)
from .utils import *
from functools import wraps
from datetime import datetime
from zoneinfo import ZoneInfo
from .gang import gangs, CaptureGangData, Capture
from .textdraws import TextDraws
from .version import __version__
from .database import DataBase
import random
import time
from samp import INVALID_PLAYER_ID # type: ignore


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
        self.kills: int = 0
        self.deaths: int = 0
        self.heals: int = 0
        self.masks: int = 0
        self.gang_id: int = -1 # No gang
        self.is_muted: bool = False
        self.is_jailed: bool = False
        self.is_logged: bool = False
        self.is_banned: bool = False
        self.is_wearing_mask: bool = False
        self._cooldown_time: float = None


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


    def send_error_message(self, message: str) -> None:
        return self.send_client_message(Colors.red, f"[ОШИБКА] {message}")


    def send_notification_message(self, message: str) -> None:
        return self.send_client_message(Colors.white, f"{message}")


    def get_gang_rang(self):
        for key, value in gangs[self.gang_id].rangs.items():
            if self.kills <= key:
                return key, value


    def show_server_logotype(self):
        for key, value in TextDraws.logo.items():
            text_draw_show_for_player(self.id, key)


    def check_cooldown(self, unix_seconds: float) -> bool:
        if self._cooldown_time is not None:
            if (time.time() - self._cooldown_time) < unix_seconds:
                return False

        self._cooldown_time = time.time()
        return True


    def update_player_cooldown_time(self) -> float:
        self._cooldown_time = time.time()
        return self._cooldown_time


    def kick_if_not_logged(self) -> None:
        encode()
        if not self.is_logged:
            Dialog.create(0, "[ОШИБКА]", "Для игры на сервере необходимо пройти регистрацию/авторизацию.", "Закрыть", "").show(self)
            self.send_error_message("Введите /q (/quit) чтобы выйти!")
            return set_timer(self.kick, 1000, False)


    def kick_teamkill(self) -> None:
        encode()
        Dialog.create(0, "[ОШИБКА]", "Вы были кикнуты. Убийство союзников - запрещено!.", "Закрыть", "").show(self)
        self.send_error_message("Введите /q (/quit) чтобы выйти!")
        return set_timer(self.kick, 1000, False)


    def ban_from_server(self) -> None:
        encode()
        if self.is_banned:
            Dialog.create(0, "[ОШИБКА]", "Вы забанены на этом сервере!.", "Закрыть", "").show(self)
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


    def is_in_area(self, min_x: float, min_y: float, max_x: float, max_y: float) -> bool:
        x, y, z = self.get_pos()
        if ((x <= max_x and x >= min_x) and (y <= max_y and y >= min_y)): # I don't fucking know how it works
            return True

        return False


    def set_gang_spawn(self):
        self.set_pos(gangs[self.gang_id].spawn_pos[0], gangs[self.gang_id].spawn_pos[1], gangs[self.gang_id].spawn_pos[2])
        self.set_camera_behind()
        self.set_virtual_world(2)
        self.set_skin(random.choice(gangs[self.gang_id].skins))
        self.set_color(gangs[self.gang_id].color)
        self.set_interior(gangs[self.gang_id].interior_id)
        self.set_score(self.kills)
        self.show_gangzones_for_player()
        return self.game_text(f"Welcome~n~{gangs[self.gang_id].game_text_color}{self.get_name()}", 2000, 1)


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


    def show_warehouse_dialog(self) -> int:
        return Dialog.create(2, f"Склад банды {gangs[self.gang_id].gang_name}.", "1. Аптечка\n2. Маска\n3. Оружие", "Ок", "Закрыть", on_response=self.warehouse_response).show(self)


    def warehouse_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        if not response:
            return

        if list_item == 0: # Heals
            if self.heals < 3:
                self.heals = 3
                return self.send_notification_message(f"Вы взяли 3 аптечки. Используйте {{FFCD00}}/healme{{FFFFFF}} для применения аптечки.")

            else:
                return self.send_error_message("У Вас уже есть аптечки!")

        if list_item == 1: # Masks
            if self.masks < 3:
                self.masks = 3
                return self.send_notification_message(f"Вы взяли 3 маски. Используйте {{FFCD00}}/mask{{FFFFFF}} для применения маски.")

            else:
                return self.send_error_message("У Вас уже есть маски!")

        if list_item == 2: # Guns
            return Dialog.create(2, "Выбор оружия", "1. Desert Eagle\n2. Shotgun\n3. AK-47\n4. M4\n5. Rifle\n6. Бита", "Ок", "Закрыть", on_response=self.warehouse_gun_response).show(self)


    def warehouse_gun_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        if not response:
            return self.show_warehouse_dialog()

        if list_item == 0:
            self.give_weapon(24, 100)
            self.send_notification_message("Вы взяли Desert Eagle.")
            return self.show_warehouse_dialog()

        if list_item == 1:
            self.give_weapon(25, 100)
            self.send_notification_message("Вы взяли Shotgun.")
            return self.show_warehouse_dialog()

        if list_item == 2:
            self.give_weapon(30, 100)
            self.send_notification_message("Вы взяли AK-47.")
            return self.show_warehouse_dialog()

        if list_item == 3:
            self.give_weapon(31, 100)
            self.send_notification_message("Вы взяли M4.")
            return self.show_warehouse_dialog()

        if list_item == 4:
            self.give_weapon(33, 100)
            self.send_notification_message("Вы взяли Rifle.")
            return self.show_warehouse_dialog()

        if list_item == 5:
            self.give_weapon(5, 1)
            self.send_notification_message("Вы взяли биту.")
            return self.show_warehouse_dialog()


    def show_login_dialog(self) -> int:
        return Dialog.create(1, f"{ServerInfo.name_short} | Авторизация", f"{self.get_name()}, добро пожаловать!\nВведите пароль:", "Ок", "", on_response=self.login_response).show(self)


    def login_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        player_db = DataBase.get_player(self)
        if not response:
            return self.kick_if_not_logged()

        if self.login_attempt == 3:
            return self.kick_if_not_logged()

        if len(input_text) < 6 or len(input_text) > 32:
            self.login_attempt += 1
            self.send_error_message("Длина пароля должна быть от 6 и до 32 символов!")
            return self.show_login_dialog()

        if input_text != player_db.password:
            self.login_attempt += 1
            self.send_error_message(f"Вы указали неверный пароль ({self.login_attempt}/3)")
            return self.show_login_dialog()

        del self.login_attempt
        self.password = player_db.password
        self.email = player_db.email
        self.pin = player_db.pin
        self.registration_ip = player_db.registration_ip
        self.registration_data = player_db.registration_data
        self.kills = player_db.kills
        self.deaths = player_db.deaths
        self.heals = player_db.heals
        self.masks = player_db.masks
        self.gang_id = player_db.gang_id
        self.is_muted = player_db.is_muted
        self.is_jailed = player_db.is_jailed
        self.is_logged= True
        self.is_banned = False
        self.toggle_spectating(False)
        self.set_max_gun_skill()
        self.spawn()


    def show_registration_dialog(self) -> int:
        return Dialog.create(1, f"{ServerInfo.name_short} | Регистрация", f"{self.get_name()}, добро пожаловать на проект {ServerInfo.name_short}\nДля игры необходимо пройти регистрацию.\nПридумайте пароль:", "Ок", "", on_response=self.registration_response).show(self)


    def registration_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        if not response:
            return self.kick_if_not_logged()

        if len(input_text) < 6 or len(input_text) > 32:
            self.send_error_message("Длина пароля должна быть от 6 и до 32 символов!")
            return self.show_registration_dialog()

        self.password = input_text
        return self.show_email_dialog()


    def show_email_dialog(self) -> int:
        return Dialog.create(1, f"{ServerInfo.name_short} | E-mail", f"Вы можете указать Ваш e-mail.\nВ случае потери доступа к аккаунту, Вы сможете получить код восстановления.\nВведите почту:", "Ок", "Позже",on_response=self.email_response).show(self)


    def email_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        if not response:
            self.email = ""
            self.send_notification_message("Вы пропустили этот шаг.")
            return self.show_gang_choice_dialog()

        if len(input_text) < 6 or len(input_text) > 32:
            self.send_error_message("Длина почты должна быть от 6 и до 32 символов!")
            return self.show_email_dialog()

        self.email = input_text
        return self.show_gang_choice_dialog()


    def show_gang_choice_dialog(self) -> int:
        return Dialog.create(2, f"{ServerInfo.name_short} | Фракция", "Grove Street Families\nThe Ballas\nLos Santos Vagos\nVarrios Los Aztecas\nLos Santos Rifa", "Ок", "", on_response=self.gang_choice_response).show(self)


    def gang_choice_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        if not response:
            self.send_error_message("Необходимо выбрать группировку!")
            return self.show_gang_choice_dialog()

        self.gang_id = list_item
        self.is_logged = True
        self.registration_ip = self.get_ip()
        self.registration_data = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        DataBase.create_player(self)
        self.toggle_spectating(False)
        self.set_max_gun_skill()
        self.spawn()


    def show_command_gang_choice_dialog(self) -> int:
        return Dialog.create(2, f"{ServerInfo.name_short} | Фракция", "Grove Street Families\nThe Ballas\nLos Santos Vagos\nVarrios Los Aztecas\nLos Santos Rifa", "Ок", "", on_response=self.command_gang_choice_response).show(self)


    def command_gang_choice_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        if not response:
            return

        self.gang_id = list_item
        self.set_gang_spawn()


    def show_stats_dialog(self) -> Dialog:
        key, value = self.get_gang_rang()
        ratio = self.kills / self.deaths if self.kills and self.deaths != 0 else 0.0
        return Dialog.create(
            0,
            f"Статистика игрока {self.get_name()}",
            f"Имя:\t\t\t\t{self.get_name()}\nРанг:\t\t\t\t{value} ({self.kills}/{key})\nГруппировка:\t\t\t{gangs[self.gang_id].gang_name}\nУбийств:\t\t\t{self.kills}\nСмертей:\t\t\t{self.deaths}\nУбийств / Смертей:\t\t{self.kills / self.deaths}\nK/D:\t\t\t\t{ratio}\nАптечек:\t\t\t{self.heals}\nМасок:\t\t\t\t{self.masks}\n",
            "Закрыть",
            "").show(self)


    def show_commands_list_dialog(self) -> Dialog:
        return Dialog.create(
            2,
            "Список команд",
            "1. Личные команды\n2. Основные команды\n3. Команды банд",
            "Ок",
            "Назад",
            on_response=self.commands_list_response
        ).show(self)


    def commands_list_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        if not response:
            return self.show_mn_dialog()

        if list_item == 0:
            ...

        if list_item == 1:
            pass

        if list_item == 2:
            pass
            # TODO. Доделать команды


    def show_mn_dialog(self) -> Dialog:
        return Dialog.create(
            2,
            "Меню игрока",
            "1. Статистика\n2. Список команд\n3. Личные настройки\n4. Настройки безопасности\n5. Связь с администрацией\n6. VIP\n7. О проекте",
            "Ок",
            "Закрыть",
            on_response=self.mn_response).show(self)


    def mn_response(self, player: "Player", response: int, list_item: int, input_text: str) -> None:
        if not response:
            return

        if list_item == 0:
            return self.show_stats_dialog()

        if list_item == 2:
            return self.show_commands_list_dialog()




    # Handle block. Only callbacks handlers should be below..


    def on_connect_handle(self) -> None:
        encode()
        if self.is_connected():
            self.send_client_message(Colors.blue, f"Добро пожаловать на сервер {ServerInfo.name_short}!")
            self.send_client_message(Colors.blue, f"Последняя версия: {__version__}!")
            self.show_server_logotype()
            self.toggle_spectating(True)
            player_db = DataBase.get_player(self)
            if not player_db:
                return self.show_registration_dialog()

            if not player_db.is_banned:
                self.login_attempt = 0
                return self.show_login_dialog()

            return self.ban_from_server()


    def on_disconnect_handle(self) -> None:
        if self.is_logged:
            DataBase.save_player(
                self,
                password=self.password,
                email=self.email,
                pin=self.pin,
                last_ip=self.last_ip,
                kills=self.kills,
                deaths=self.deaths,
                heals=self.heals,
                masks=self.masks,
                gang_id=self.gang_id,
                is_muted=self.is_muted,
                is_jailed=self.is_jailed,
                is_banned=self.is_banned
                )

        return self.delete_registry(self)


    def on_spawn_handle(self) -> None:
        self.kick_if_not_logged()
        self.toggle_controllable(True)
        return self.set_gang_spawn()


    def on_death_handle(self, killer: "Player", reason: int) -> None:
        if killer.id != INVALID_PLAYER_ID:
            if killer.gang_id != self.gang_id:
                send_death_message(killer.id, self.id, reason)
                killer.kills += 1
                killer.set_score(killer.kills)

            else:
                return killer.kick_teamkill()

        self.deaths += 1
        self.masks = 0
        self.heals = 0
        return self.spawn()


    def on_text_handle(self, text: str) -> False:
        encode()
        if self.is_muted:
            self.set_chat_bubble("Пытается что-то сказать..", Colors.red, 20.0, 10000)
            return self.send_error_message("Доступ в чат заблокирован!")

        self.set_chat_bubble(text, -1, 20.0, 10000)
        self.prox_detector(20.0, -1, text)
        return False


    def on_pick_up_pickup_handle(self, pickup: DynamicPickup) -> None:
        encode()
        if pickup.id == gangs[0].enter_exit[0].id: # Grove enter
            if not self.gang_id == gangs[0].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(2466.2649, -1698.4724, 1013.5078)
            self.set_facing_angle(90.0)
            self.set_camera_behind()
            self.set_virtual_world(2)
            self.set_interior(2)

        if pickup.id == gangs[0].enter_exit[1].id: # Grove exit
            if not self.gang_id == gangs[0].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2495.3022, -1688.5438, 13.8722)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(0)
            self.set_interior(0)

        if pickup.id == gangs[1].enter_exit[0].id: # Ballas enter
            if not self.gang_id == gangs[1].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(-42.6860, 1408.4878, 1084.4297)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(2)
            self.set_interior(8)

        if pickup.id == gangs[1].enter_exit[1].id: # Ballas exit
            if not self.gang_id == gangs[1].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2022.9169, -1122.7472, 26.2329)
            self.set_camera_behind()
            self.set_virtual_world(0)
            self.set_interior(0)

        if pickup.id == gangs[2].enter_exit[0].id: # Vagos enter
            if not self.gang_id == gangs[2].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(318.564971, 1118.209960, 1083.882812)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(2)
            self.set_interior(5)

        if pickup.id == gangs[2].enter_exit[1].id: # Vagos exit
            if not self.gang_id == gangs[2].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2756.1492, -1180.2386, 69.3978)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(0)
            self.set_interior(0)

        if pickup.id == gangs[3].enter_exit[0].id: # Aztecas enter
            if not self.gang_id == gangs[3].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(223.0174, 1240.1416, 1082.1406)
            self.set_facing_angle(270.0)
            self.set_camera_behind()
            self.set_virtual_world(2)
            self.set_interior(2)

        if pickup.id == gangs[3].enter_exit[1].id: # Aztecas exit
            if not self.gang_id == gangs[3].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2185.6555, -1812.5112, 13.5650)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(0)
            self.set_interior(0)

        if pickup.id == gangs[4].enter_exit[0].id: # Rifa enter
            if not self.gang_id == gangs[4].gang_id:
                return self.send_error_message("У Вас нет доступа к входу!")

            self.set_pos(-68.9146, 1353.8420, 1080.2109)
            self.set_facing_angle(0.0)
            self.set_camera_behind()
            self.set_virtual_world(2)
            self.set_interior(6)

        if pickup.id == gangs[4].enter_exit[1].id: # Rifa exit
            if not self.gang_id == gangs[4].gang_id:
                return self.send_error_message("У Вас нет доступа к выходу!")

            self.set_pos(2784.5544, -1926.1563, 13.5469)
            self.set_facing_angle(90.0)
            self.set_camera_behind()
            self.set_virtual_world(0)
            self.set_interior(0)


    def on_enter_checkpoint_handle(self, checkpoint: DynamicCheckpoint) -> None:
        if checkpoint.id == gangs[0].warehouse.id: # Grove
            return self.show_warehouse_dialog()

        if checkpoint.id == gangs[1].warehouse.id: # Ballas
            return self.show_warehouse_dialog()

        if checkpoint.id == gangs[2].warehouse.id: # Vagos
            return self.show_warehouse_dialog()

        if checkpoint.id == gangs[3].warehouse.id: # Aztecas
            return self.show_warehouse_dialog()

        if checkpoint.id == gangs[4].warehouse.id: # Rifa
            return self.show_warehouse_dialog()


    def on_update_handle(self) -> None:
        pass


    def on_damage_handler(self, issuer: "Player", amount: float, weapon_id: int, body_part) -> None:
        self.play_sound(17802, 0.0, 0.0, 0.0)
        x, y, z, to_x, to_y, to_z = self.get_last_shot_vectors()
        damage_informer = create_player_3d_text_label(self.id, f"{int(amount)}", Colors.white, to_x, to_y, to_z, 150)
        return set_timer(delete_player_3d_text_label, 1000, False, self.id, damage_informer)

