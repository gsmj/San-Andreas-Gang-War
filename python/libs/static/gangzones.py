from pysamp.gangzone import Gangzone
from ..utils.data import ServerMode
deathmatch: dict[int, "Gangzone"] = {}
freeroam: dict[int, "Gangzone"] = {}

def create_gangzones() -> None:
    deathmatch[ServerMode.deathmatch_world_shotgun] = Gangzone.create(-468.61114501953125, 2178.4027709960938, -337.61114501953125, 2279.4027709960938)
    deathmatch[ServerMode.deathmatch_world_oc_deagle] = Gangzone.create(-468.61114501953125, 2178.4027709960938, -337.61114501953125, 2279.4027709960938)
    deathmatch[ServerMode.deathmatch_world_old_country] = Gangzone.create(-468.61114501953125, 2178.4027709960938, -337.61114501953125, 2279.4027709960938)
    deathmatch[ServerMode.deathmatch_world_farm] = Gangzone.create(997.388916015625, -387.0556640625, 1132.388916015625, -277.0556640625)
    deathmatch[ServerMode.deathmatch_world_abandoned_country] = Gangzone.create(-1343.3888549804688, 2468.0555572509766, -1245.3888549804688, 2562.0555572509766)
    deathmatch[ServerMode.deathmatch_world_kass] = Gangzone.create(2537.72216796875, 2793.5, 2717.72216796875, 2852.5)
    return print(f"Created: GangZones (deathmatch) (server)")
