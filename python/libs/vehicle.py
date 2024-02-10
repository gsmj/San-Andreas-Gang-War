from pysamp.vehicle import Vehicle as BaseVehicle
from .utils import ServerWorldIDs
from functools import wraps
from dataclasses import dataclass
from .consts import NO_VEHICLE_OWNER

@dataclass
class VehicleTypes:
    LOWRIDER = "Лоурайдеры"
    OFFROAD = "Внедорожники"
    SERVICES = "Гос. службы"
    SEDAN = "Седаны"
    SPORT = "Спортивные"
    UNIVERSAL = "Универсалы"
    UNIQE = "Уникальные"


# @dataclass
# class VehicleData:
#     """
#     Key: id
#     Values: (type, name, price)
#     """
#     data = {
#         412: (VehicleTypes.LOWRIDER, "Voodoo", 1000),
#         534: (VehicleTypes.LOWRIDER, "Remington", 1000),
#         535: (VehicleTypes.LOWRIDER, "Slamvan", 1000),
#         536: (VehicleTypes.LOWRIDER, "Blade", 1000),
#         566: (VehicleTypes.LOWRIDER, "Tahoma", 1000),
#         567: (VehicleTypes.LOWRIDER, "Savanna", 1000),
#         575: (VehicleTypes.LOWRIDER, "Broadway", 1000),
#         576: (VehicleTypes.LOWRIDER, "Tornado", 1000),

#         400: (VehicleTypes.OFFROAD, "Landstalker", 5000),
#         424: (VehicleTypes.OFFROAD, "BF Injection", 5000),
#         444: (VehicleTypes.OFFROAD, "Monster", 5000),
#         470: (VehicleTypes.OFFROAD, "Patriot", 5000),
#         489: (VehicleTypes.OFFROAD, "Rancher", 5000),
#         495: (VehicleTypes.OFFROAD, "Sandking", 5000),
#         500: (VehicleTypes.OFFROAD, "Mesa", 5000),
#         556: (VehicleTypes.OFFROAD, "Monster A", 5000),
#         557: (VehicleTypes.OFFROAD, "Monster B", 5000),
#         568: (VehicleTypes.OFFROAD, "Bandito", 5000),
#         573: (VehicleTypes.OFFROAD, "Dune", 5000),
#         579: (VehicleTypes.OFFROAD, "Huntley", 5000),

#         407: (VehicleTypes.SERVICES, "Firetruck", 5000),
#         416: (VehicleTypes.SERVICES, "Ambulance", 5000),
#         420: (VehicleTypes.SERVICES, "Taxi", 5000),
#         427: (VehicleTypes.SERVICES, "Enforcer", 5000),
#         431: (VehicleTypes.SERVICES, "Bus", 5000),
#         433: (VehicleTypes.SERVICES, "Barracks", 5000),
#         437: (VehicleTypes.SERVICES, "Coach", 5000),
#         438: (VehicleTypes.SERVICES, "Cabbie", 5000),
#         490: (VehicleTypes.SERVICES, "FBI Rancher", 5000),
#         523: (VehicleTypes.SERVICES, "HPV1000", 5000),
#         528: (VehicleTypes.SERVICES, "FBI Truck", 5000),
#         544: (VehicleTypes.SERVICES, "Firetruck LA", 5000),
#         596: (VehicleTypes.SERVICES, "Police Car (LSPD)", 5000),
#         597: (VehicleTypes.SERVICES, "Police Car (SFPD)", 5000),
#         598: (VehicleTypes.SERVICES, "Police Car (LVPD)", 5000),
#         599: (VehicleTypes.SERVICES, "Police Ranger", 5000),

#         401: (VehicleTypes.SEDAN, "Bravura", 5000),
#         405: (VehicleTypes.SEDAN, "Sentinel", 5000),
#         410: (VehicleTypes.SEDAN, "Manana", 5000),
#         419: (VehicleTypes.SEDAN, "Esperanto", 5000),
#         421: (VehicleTypes.SEDAN, "Washington", 5000),
#         426: (VehicleTypes.SEDAN, "Premier", 5000),
#         436: (VehicleTypes.SEDAN, "Previon", 5000),
#         445: (VehicleTypes.SEDAN, "Admiral", 5000),
#         466: (VehicleTypes.SEDAN, "Glendale", 5000),
#         467: (VehicleTypes.SEDAN, "Oceanic", 5000),
#         474: (VehicleTypes.SEDAN, "Hermes", 5000),
#         491: (VehicleTypes.SEDAN, "Virgo", 5000),
#         492: (VehicleTypes.SEDAN, "Greenwood", 5000),
#         504: (VehicleTypes.SEDAN, "Bloodring Banger", 5000),
#         507: (VehicleTypes.SEDAN, "Elegant", 5000),
#         516: (VehicleTypes.SEDAN, "Nebula", 5000),
#         517: (VehicleTypes.SEDAN, "Majestic", 5000),
#         518: (VehicleTypes.SEDAN, "Buccaneer", 5000),
#         526: (VehicleTypes.SEDAN, "Fortune", 5000),
#         527: (VehicleTypes.SEDAN, "Cadrona", 5000),
#         529: (VehicleTypes.SEDAN, "Willard", 5000),
#         540: (VehicleTypes.SEDAN, "Vincent", 5000),
#         542: (VehicleTypes.SEDAN, "Clover", 5000),
#         546: (VehicleTypes.SEDAN, "Intruder", 5000),
#         547: (VehicleTypes.SEDAN, "Primo", 5000),
#         549: (VehicleTypes.SEDAN, "Tampa", 5000),
#         550: (VehicleTypes.SEDAN, "Sunrise", 5000),
#         551: (VehicleTypes.SEDAN, "Merit", 5000),
#         560: (VehicleTypes.SEDAN, "Sultan", 5000),
#         562: (VehicleTypes.SEDAN, "Elegy", 5000),
#         580: (VehicleTypes.SEDAN, "Stafford", 5000),
#         585: (VehicleTypes.SEDAN, "Emperor", 5000),

#         402: (VehicleTypes.SPORT, "Buffalo", 5000),
#         411: (VehicleTypes.SPORT, "Infernus", 5000),
#         415: (VehicleTypes.SPORT, "Cheetah", 5000),
#         429: (VehicleTypes.SPORT, "Banshee", 5000),
#         451: (VehicleTypes.SPORT, "Turismo", 5000),
#         475: (VehicleTypes.SPORT, "Sabre", 5000),
#         477: (VehicleTypes.SPORT, "ZR-350", 5000),
#         494: (VehicleTypes.SPORT, "Hotring Racer", 5000),
#         496: (VehicleTypes.SPORT, "Blista Compact", 5000),
#         502: (VehicleTypes.SPORT, "Hotring Racer", 5000),
#         503: (VehicleTypes.SPORT, "Hotring Racer", 5000),
#         506: (VehicleTypes.SPORT, "Super GT", 5000),
#         541: (VehicleTypes.SPORT, "Bullet", 5000),
#         558: (VehicleTypes.SPORT, "Uranus", 5000),
#         559: (VehicleTypes.SPORT, "Jester", 5000),
#         565: (VehicleTypes.SPORT, "Flash", 5000),
#         587: (VehicleTypes.SPORT, "Euros", 5000),
#         589: (VehicleTypes.SPORT, "Club", 5000),
#         602: (VehicleTypes.SPORT, "Alpha", 5000),
#         603: (VehicleTypes.SPORT, "Phoenix", 5000),

#         404: (VehicleTypes.UNIVERSAL, "Perenniel", 5000),
#         418: (VehicleTypes.UNIVERSAL, "Moonbeam", 5000),
#         458: (VehicleTypes.UNIVERSAL, "Solair", 5000),
#         479: (VehicleTypes.UNIVERSAL, "Regina", 5000),
#         561: (VehicleTypes.UNIVERSAL, "Stratum", 5000),

#         406: (VehicleTypes.UNIQE, "Dumper", 5000),
#         409: (VehicleTypes.UNIQE, "Stretch", 5000),
#         423: (VehicleTypes.UNIQE, "Mr. Whoopee", 5000),
#         428: (VehicleTypes.UNIQE, "Securicar", 5000),
#         434: (VehicleTypes.UNIQE, "Hotknife", 5000),
#         442: (VehicleTypes.UNIQE, "Romero", 5000),
#         457: (VehicleTypes.UNIQE, "Caddy", 5000),
#         483: (VehicleTypes.UNIQE, "Camper", 5000),
#         485: (VehicleTypes.UNIQE, "Baggage", 5000),
#         486: (VehicleTypes.UNIQE, "Dozer", 5000),
#         508: (VehicleTypes.UNIQE, "Journey", 5000),
#         525: (VehicleTypes.UNIQE, "Towtruck", 5000),
#         530: (VehicleTypes.UNIQE, "Forklift", 5000),
#         532: (VehicleTypes.UNIQE, "Combine Harvester", 5000),
#         539: (VehicleTypes.UNIQE, "Vortex", 5000),
#         545: (VehicleTypes.UNIQE, "Hustler", 5000),
#         571: (VehicleTypes.UNIQE, "Kart", 5000),
#         572: (VehicleTypes.UNIQE, "Mower", 5000),
#         574: (VehicleTypes.UNIQE, "Sweeper", 5000),
#         583: (VehicleTypes.UNIQE, "Tug", 5000),
#         588: (VehicleTypes.UNIQE, "Hotdog", 5000),
#     }

@dataclass
class VehicleData:
    """
    Key: id
    Values: (type, name, price)
    """
    data = {
        412: (VehicleTypes.LOWRIDER, "Voodoo", 1000),
        534: (VehicleTypes.LOWRIDER, "Remington", 1000),
        535: (VehicleTypes.LOWRIDER, "Slamvan", 1000),
        536: (VehicleTypes.LOWRIDER, "Blade", 1000),
        566: (VehicleTypes.LOWRIDER, "Tahoma", 1000),
        567: (VehicleTypes.LOWRIDER, "Savanna", 1000),
        575: (VehicleTypes.LOWRIDER, "Broadway", 1000),
        576: (VehicleTypes.LOWRIDER, "Tornado", 1000),

        400: (VehicleTypes.OFFROAD, "Landstalker", 5000),
        424: (VehicleTypes.OFFROAD, "BF Injection", 5000),
        444: (VehicleTypes.OFFROAD, "Monster", 5000),
        470: (VehicleTypes.OFFROAD, "Patriot", 5000),
        489: (VehicleTypes.OFFROAD, "Rancher", 5000),
        495: (VehicleTypes.OFFROAD, "Sandking", 5000),
        500: (VehicleTypes.OFFROAD, "Mesa", 5000),
        556: (VehicleTypes.OFFROAD, "Monster A", 5000),
        557: (VehicleTypes.OFFROAD, "Monster B", 5000),
        568: (VehicleTypes.OFFROAD, "Bandito", 5000),
        573: (VehicleTypes.OFFROAD, "Dune", 5000),
        579: (VehicleTypes.OFFROAD, "Huntley", 5000),

        407: (VehicleTypes.SERVICES, "Firetruck", 5000),
        416: (VehicleTypes.SERVICES, "Ambulance", 5000),
        420: (VehicleTypes.SERVICES, "Taxi", 5000),
        427: (VehicleTypes.SERVICES, "Enforcer", 5000),
        431: (VehicleTypes.SERVICES, "Bus", 5000),
        433: (VehicleTypes.SERVICES, "Barracks", 5000),
        437: (VehicleTypes.SERVICES, "Coach", 5000),
        438: (VehicleTypes.SERVICES, "Cabbie", 5000),
        490: (VehicleTypes.SERVICES, "FBI Rancher", 5000),
        523: (VehicleTypes.SERVICES, "HPV1000", 5000),
        528: (VehicleTypes.SERVICES, "FBI Truck", 5000),
        544: (VehicleTypes.SERVICES, "Firetruck LA", 5000),
        596: (VehicleTypes.SERVICES, "Police Car (LSPD)", 5000),
        597: (VehicleTypes.SERVICES, "Police Car (SFPD)", 5000),
        598: (VehicleTypes.SERVICES, "Police Car (LVPD)", 5000),
        599: (VehicleTypes.SERVICES, "Police Ranger", 5000),

        445: (VehicleTypes.SEDAN, "Admiral", 5000),
        504: (VehicleTypes.SEDAN, "Bloodring", 5000),
        401: (VehicleTypes.SEDAN, "Bravura", 5000),
        518: (VehicleTypes.SEDAN, "Buccaneer", 5000),
        527: (VehicleTypes.SEDAN, "Cadrona", 5000),
        542: (VehicleTypes.SEDAN, "Clover", 5000),
        507: (VehicleTypes.SEDAN, "Elegant", 5000),
        585: (VehicleTypes.SEDAN, "Emperor", 5000),
        419: (VehicleTypes.SEDAN, "Esperanto", 5000),
        526: (VehicleTypes.SEDAN, "Fortune", 5000),
        466: (VehicleTypes.SEDAN, "Glendale", 5000),
        492: (VehicleTypes.SEDAN, "Greenwood", 5000),
        474: (VehicleTypes.SEDAN, "Hermes", 5000),
        517: (VehicleTypes.SEDAN, "Majestic", 5000),
        410: (VehicleTypes.SEDAN, "Manana", 5000),
        551: (VehicleTypes.SEDAN, "Merit", 5000),
        516: (VehicleTypes.SEDAN, "Nebula", 5000),
        467: (VehicleTypes.SEDAN, "Oceanic", 5000),
        426: (VehicleTypes.SEDAN, "Premier", 5000),
        540: (VehicleTypes.SEDAN, "Previon", 5000),
        436: (VehicleTypes.SEDAN, "Primo", 5000),
        405: (VehicleTypes.SEDAN, "Sentinel", 5000),
        580: (VehicleTypes.SEDAN, "Stafford", 5000),
        550: (VehicleTypes.SEDAN, "Sunrise", 5000),
        549: (VehicleTypes.SEDAN, "Tampa", 5000),
        540: (VehicleTypes.SEDAN, "Vincent", 5000),
        491: (VehicleTypes.SEDAN, "Virgo", 5000),
        421: (VehicleTypes.SEDAN, "Washington", 5000),
        529: (VehicleTypes.SEDAN, "Willard", 5000),

        602: (VehicleTypes.SPORT, "Alpha", 5000),
        402: (VehicleTypes.SPORT, "Buffalo", 5000),
        429: (VehicleTypes.SPORT, "Banshee", 5000),
        541: (VehicleTypes.SPORT, "Bullet", 5000),
        496: (VehicleTypes.SPORT, "Blista Compact", 5000),
        415: (VehicleTypes.SPORT, "Cheetah", 5000),
        589: (VehicleTypes.SPORT, "Club", 5000),
        587: (VehicleTypes.SPORT, "Euros", 5000),
        562: (VehicleTypes.SPORT, "Elegy", 5000),
        565: (VehicleTypes.SPORT, "Flash", 5000),
        451: (VehicleTypes.SPORT, "Turismo", 5000),
        494: (VehicleTypes.SPORT, "Hotring Racer", 5000),
        502: (VehicleTypes.SPORT, "Hotring Racer", 5000),
        503: (VehicleTypes.SPORT, "Hotring Racer", 5000),
        411: (VehicleTypes.SPORT, "Infernus", 5000),
        559: (VehicleTypes.SPORT, "Jester", 5000),
        603: (VehicleTypes.SPORT, "Phoenix", 5000),
        475: (VehicleTypes.SPORT, "Sabre", 5000),
        506: (VehicleTypes.SPORT, "Super GT", 5000),
        560: (VehicleTypes.SPORT, "Sultan", 5000),
        558: (VehicleTypes.SPORT, "Uranus", 5000),
        477: (VehicleTypes.SPORT, "ZR-350", 5000),

        404: (VehicleTypes.UNIVERSAL, "Perenniel", 5000),
        418: (VehicleTypes.UNIVERSAL, "Moonbeam", 5000),
        458: (VehicleTypes.UNIVERSAL, "Solair", 5000),
        479: (VehicleTypes.UNIVERSAL, "Regina", 5000),
        561: (VehicleTypes.UNIVERSAL, "Stratum", 5000),

        406: (VehicleTypes.UNIQE, "Dumper", 5000),
        409: (VehicleTypes.UNIQE, "Stretch", 5000),
        423: (VehicleTypes.UNIQE, "Mr. Whoopee", 5000),
        428: (VehicleTypes.UNIQE, "Securicar", 5000),
        434: (VehicleTypes.UNIQE, "Hotknife", 5000),
        442: (VehicleTypes.UNIQE, "Romero", 5000),
        457: (VehicleTypes.UNIQE, "Caddy", 5000),
        483: (VehicleTypes.UNIQE, "Camper", 5000),
        485: (VehicleTypes.UNIQE, "Baggage", 5000),
        486: (VehicleTypes.UNIQE, "Dozer", 5000),
        508: (VehicleTypes.UNIQE, "Journey", 5000),
        525: (VehicleTypes.UNIQE, "Towtruck", 5000),
        530: (VehicleTypes.UNIQE, "Forklift", 5000),
        532: (VehicleTypes.UNIQE, "Combine Harvester", 5000),
        539: (VehicleTypes.UNIQE, "Vortex", 5000),
        545: (VehicleTypes.UNIQE, "Hustler", 5000),
        571: (VehicleTypes.UNIQE, "Kart", 5000),
        572: (VehicleTypes.UNIQE, "Mower", 5000),
        574: (VehicleTypes.UNIQE, "Sweeper", 5000),
        583: (VehicleTypes.UNIQE, "Tug", 5000),
        588: (VehicleTypes.UNIQE, "Hotdog", 5000),
    }

class Vehicle(BaseVehicle):
    _registry: dict = {}
    def __init__(self, vehicle_id: int):
        super().__init__(vehicle_id)
        self.owner = NO_VEHICLE_OWNER
        self.engine = 0
        self.lights = 0
        self.doors = 0

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

    @classmethod
    def get_from_registry(cls, id: int) -> "Vehicle":
        return cls._registry[id]

    @classmethod
    def delete_registry(cls, vehicle: BaseVehicle) -> None:
        del cls._registry[vehicle.id]

    @classmethod
    def create(
        cls,
        model: int,
        x: float,
        y: float,
        z: float,
        rotation: float,
        color1: int,
        color2: int,
        respawn_delay: int,
        mode: int,
        add_siren: bool = False,
    ) -> "Vehicle":
        veh = super().create(model, x, y, z, rotation, color1, color2, respawn_delay, add_siren=add_siren)
        veh.set_virtual_world(mode)
        return cls.from_registry_native(veh)

    def set_info(self, owner: str = "", engine: int = 0, lights: int = 0, doors: int = 0) -> "Vehicle":
        self.owner = owner,
        self.engine = engine
        self.lights = lights
        self.doors = doors

    def set_owner(self, owner: str):
        self.owner = owner

    @classmethod
    def remove_unused_player_vehicle(cls, vehicle: "Vehicle") -> None:
        if vehicle.is_valid():
            vehicle.destroy()

        cls.delete_registry(vehicle)

    def on_death_handle(self, killer) -> None:
        if self.owner != NO_VEHICLE_OWNER:
            self.delete_registry(self)