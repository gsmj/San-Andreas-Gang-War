from pystreamer.dynamicobject import DynamicObject
from .utils import ServerWorldIDs


class Objects:
    @classmethod
    def load(cls) -> None:
        DynamicObject.create(18753, 5509.365234, 1245.812866, 6.623889, 0.000000, 0.000000, 0.000000, world_id=ServerWorldIDs.jail_world)
        DynamicObject.create(18759, 5512.342285, 1244.404418, 7.128617, 0.000000, 0.000000, 0.000000, world_id=ServerWorldIDs.jail_world)