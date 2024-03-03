from pystreamer.dynamicpickup import DynamicPickup
from pystreamer.dynamicmapicon import DynamicMapIcon
from pystreamer.dynamictextlabel import DynamicTextLabel
from ..database.database import DataBase
from ..utils.data import ServerMode, Colors
from ..utils.consts import NO_HOUSE_OWNER
from dataclasses import dataclass
houses: dict[int, tuple["House", "DynamicPickup"]] = {}
"""
Key: House uid
Values: (House dataclass, DynamicPickup)
"""
houses_by_pickup: dict[int, "House"] = {}
"""
Key: Pickup id
Values: House dataclass
"""
houses_by_owner: dict[str, "House"] = {}
"""
Key: Owner name
Values: House dataclass
"""

interiors: dict[int, tuple[float, float, float]] = {
    1: (245.23, 304.76, 999.14), # Низкий класс 1
    10: (2262.83, -1137.71, 1050.63), # Низкий класс 2
    6: (2333.033, -1073.96, 1049.1), # Низкий класс 3
    11: (2282.97, -1140.28, 1050.89), # Средний класс 1
    12: (446.32, 509.96, 1001.41), # Средний класс 2
    8: (2365.10, -1133.07, 1050.87), # Средний класс 3
    4: (-262.17, 1456.61, 1084.36), # Богатый класс 1
    5: (140.36, 1367.88, 1083.86), # Богатый класс 2
    9: (2319.12, -1023.95, 1050.21), # Богатый класс 3
    2: (1.18, -3.23, 999.42) # Трейлер
}
"""
Key: Interior id
Values (x, y, z)
"""
for interior, values in interiors.items():
    DynamicTextLabel.create(
        "PRESS ALT",
        Colors.blue,
        values[0],
        values[1],
        values[2],
        draw_distance=15.0,
        interior_id=interior
    )


@dataclass(repr=False)
class House:
    uid: int
    owner: str
    interior_id: int
    price: int
    pos_x: float
    pos_y: float
    pos_z: float
    is_locked: bool
    label: DynamicTextLabel = None
    map_icon: DynamicMapIcon = None
    pickup: DynamicPickup = None


    def __post_init__(self) -> None:
        if self.owner == NO_HOUSE_OWNER:
            model_id = 1273
            icon = 31
        else:
            houses_by_owner[self.owner] = self
            model_id = 19522
            icon = 32

        self.label = DynamicTextLabel.create(
            f"ID: {self.uid}\nOwner: {self.owner}",
            Colors.blue,
            self.pos_x,
            self.pos_y,
            self.pos_z,
            5.0,
            world_id=ServerMode.freeroam_world,
            interior_id=0,
        )
        self.map_icon = DynamicMapIcon.create(
            self.pos_x,
            self.pos_y,
            self.pos_z,
            icon,
            0,
            world_id=ServerMode.freeroam_world,
            interior_id=0
        )
        self.pickup = DynamicPickup.create(
            model_id,
            23,
            self.pos_x,
            self.pos_y,
            self.pos_z,
            ServerMode.freeroam_world,
            interior_id=0
        )

        houses[self.uid] = (
            self,
            self.pickup
        )
        houses_by_pickup[self.pickup.id] = self

    def set_owner(self, owner: str) -> None:
        self.owner = owner
        houses_by_owner[self.owner] = self
        self.label.destroy()
        self.map_icon.destroy()
        self.pickup.destroy()
        self.label = DynamicTextLabel.create(
            f"ID: {self.uid}\nOwner: {self.owner}",
            Colors.blue,
            self.pos_x,
            self.pos_y,
            self.pos_z,
            5.0,
            world_id=ServerMode.freeroam_world,
            interior_id=0,
        )
        self.map_icon = DynamicMapIcon.create(
            self.pos_x,
            self.pos_y,
            self.pos_z,
            32,
            0,
            world_id=ServerMode.freeroam_world,
            interior_id=0
        )
        self.pickup = DynamicPickup.create(
            19522,
            23,
            self.pos_x,
            self.pos_y,
            self.pos_z,
            ServerMode.freeroam_world,
            interior_id=0
        )
        DataBase.save_house(
            self.uid,
            owner=owner
        )

    def remove_owner(self) -> None:
        del houses_by_owner[self.owner]
        self.owner = NO_HOUSE_OWNER
        self.is_locked = False
        self.label.destroy()
        self.map_icon.destroy()
        self.pickup.destroy()
        self.label = DynamicTextLabel.create(
            f"ID: {self.uid}\nOwner: {self.owner}",
            Colors.blue,
            self.pos_x,
            self.pos_y,
            self.pos_z,
            5.0,
            world_id=ServerMode.freeroam_world,
            interior_id=0,
        )
        self.map_icon = DynamicMapIcon.create(
            self.pos_x,
            self.pos_y,
            self.pos_z,
            31,
            0,
            world_id=ServerMode.freeroam_world,
            interior_id=0
        )
        self.pickup = DynamicPickup.create(
            1273,
            23,
            self.pos_x,
            self.pos_y,
            self.pos_z,
            ServerMode.freeroam_world,
            interior_id=0
        )
        DataBase.save_house(
            self.uid,
            owner=NO_HOUSE_OWNER,
            is_locked=False
        )

    def change_door_status(self, lock: bool) -> None:
        self.is_locked = lock
        DataBase.save_house(
            self.uid,
            is_locked=self.is_locked
        )
