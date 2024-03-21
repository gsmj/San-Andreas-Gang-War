import random
from datetime import datetime as dt
from zoneinfo import ZoneInfo

from samp import (PLAYER_STATE_SPECTATING,  # type: ignore
                  SPECIAL_ACTION_USEJETPACK)

from pysamp import send_client_message_to_all, set_world_time
from pysamp.commands import cmd
from pysamp.dialog import Dialog
from pysamp.timer import kill_timer, set_timer

from ...player import Dialogs, Player
from ...vehicle import Vehicle
from ..modes.modes import GangWar
from ..database.database import DataBase
from ..gang.gang import gangs, gangzone_pool
from ..squad.squad import Squad, squad_pool_id, squad_gangzone_pool
from ..utils.consts import NO_HOUSE_OWNER, TIMER_ID_NONE
from ..utils.data import (Colors, MonthsConverter, ServerInfo, ServerMode,
                          VIPData, WeatherIDs, convert_seconds)
from .cmd_ex import CommandType, cmd_ex