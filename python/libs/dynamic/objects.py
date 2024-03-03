from pystreamer.dynamicobject import DynamicObject
from pysamp.player import Player
from ..utils.data import ServerMode


def create_objects() -> None:
    DynamicObject.create(18753, 5509.365234, 1245.812866, 6.623889, 0.000000, 0.000000, 0.000000, world_id=ServerMode.jail_world)
    DynamicObject.create(18759, 5512.342285, 1244.404418, 7.128617, 0.000000, 0.000000, 0.000000, world_id=ServerMode.jail_world)
    DynamicObject.create(984, -281.00650, 1522.13379, 75.11287, 0.00000, 0.00000, 132.18022, world_id=ServerMode.freeroam_world)
    DynamicObject.create(984, -271.49213, 1530.88208, 75.09000, 0.18000, -0.12000, 133.14018, world_id=ServerMode.freeroam_world)
    DynamicObject.create(3666, -289.20465, 1535.84424, 75.04942, 0.00000, 0.00000, 0.00000, world_id=ServerMode.freeroam_world)
    DynamicObject.create(16090, -302.80548, 1508.22253, 74.49982, 0.00000, 0.00000, -89.04012, world_id=ServerMode.freeroam_world)
    DynamicObject.create(984, -290.51578, 1513.45850, 75.10626, 0.00000, 0.00000, 132.59991, world_id=ServerMode.freeroam_world)
    DynamicObject.create(3582, -317.25836, 1538.90295, 76.70833, 0.00000, 0.00000, 179.33858, world_id=ServerMode.freeroam_world)
    DynamicObject.create(984, -262.14206, 1539.59937, 75.06228, 0.18000, -0.12000, 133.08031, world_id=ServerMode.freeroam_world)
    DynamicObject.create(984, -316.78406, 1508.72314, 75.12973, 0.00000, 0.00000, 90.59978, world_id=ServerMode.freeroam_world)
    DynamicObject.create(984, -329.60269, 1508.59534, 75.14970, 0.00000, 0.00000, 90.53979, world_id=ServerMode.freeroam_world)
    DynamicObject.create(984, -342.43365, 1508.49890, 75.12973, 0.00000, 0.00000, 90.17971, world_id=ServerMode.freeroam_world)
    DynamicObject.create(984, -354.32220, 1511.85852, 75.12973, 0.00000, 0.00000, 58.25982, world_id=ServerMode.freeroam_world)
    DynamicObject.create(3171, -342.24429, 1539.77649, 74.53220, 0.00000, 0.00000, 123.18008, world_id=ServerMode.freeroam_world)
    DynamicObject.create(3175, -328.45837, 1539.88318, 74.54250, 0.00000, 0.00000, 53.70004, world_id=ServerMode.freeroam_world)
    DynamicObject.create(979, -1203.57446, 1836.23730, 41.48737, 0.00000, 0.00000, 198.35902, world_id=ServerMode.freeroam_world)
    DynamicObject.create(979, -1222.53735, 1816.24988, 41.28181, 0.00000, 0.00000, -94.91979, world_id=ServerMode.freeroam_world)
    DynamicObject.create(979, -1216.06067, 1795.73022, 41.14235, 0.00000, 0.00000, -9.53974, world_id=ServerMode.freeroam_world)
    DynamicObject.create(979, -1206.80664, 1794.25061, 41.13261, 0.00000, 0.00000, -8.75974, world_id=ServerMode.freeroam_world)
    DynamicObject.create(979, -1197.57715, 1793.15674, 41.14050, 0.00000, 0.00000, -4.73973, world_id=ServerMode.freeroam_world)
    return print(f"Created: Objects (server)")

def remove_objects_for_player(player: Player) -> None:
    player.remove_building(16616, -326.6953, 1541.3906, 74.5547, 0.25)
    player.remove_building(16138, -326.6953, 1541.3906, 74.5547, 0.25)