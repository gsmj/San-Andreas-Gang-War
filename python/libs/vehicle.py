from pysamp import add_static_vehicle_ex
from pysamp.vehicle import Vehicle as BaseVehicle
from .utils import ServerWorldIDs
from functools import wraps


class Vehicle(BaseVehicle):
    _registry: dict = {}
    def __init__(self, vehicle_id: int, owner: str = "", engine: int = 0, lights: int = 0, doors: int = 0):
        super().__init__(vehicle_id)
        self.owner = owner
        self.engine = engine
        self.lights = lights
        self.doors = doors

    @classmethod
    def from_registry_native(cls, vehicle: BaseVehicle) -> "Vehicle":
        if isinstance(vehicle, int):
            vehicle_id = vehicle

        if isinstance(vehicle, BaseVehicle):
            vehicle_id = vehicle.id

        vehicle = cls._registry.get(vehicle_id)
        if not vehicle:
            cls._registry[vehicle_id] = vehicle = cls(vehicle_id)

        return vehicle

    @classmethod
    def using_registry(cls, func):
        @wraps(func)
        def from_registry(*args, **kwargs):
            args = list(args)
            args[0] = cls.from_registry_native(args[0])
            return func(*args, **kwargs)

        return from_registry

    def add_to_registry(self) -> "Vehicle":
        return self.from_registry_native(self)

    @classmethod
    def get_from_registry(cls, id: int) -> "Vehicle":
        return cls._registry[id]