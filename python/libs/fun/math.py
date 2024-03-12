import random
from dataclasses import dataclass

from pysamp import send_client_message_to_all
from pysamp.timer import kill_timer, set_timer

from ..utils.consts import ID_NONE, TIMER_ID_NONE
from ..utils.data import Colors


@dataclass
class MathExpressions:
    exprs = ("+", "-", "*")


@dataclass
class MathTest:
    correct_answer: int = ID_NONE
    expr: str = ""
    math_timer: int = TIMER_ID_NONE

    @classmethod
    def send_math_test(cls) -> None:
        cls.expr = f"{random.randint(1, 1000)} {random.choice(MathExpressions.exprs)} {random.randint(1, 1000)}"
        cls.correct_answer = eval(cls.expr)
        cls.math_timer = set_timer(cls.no_winner_message, 30000, False)
        return send_client_message_to_all(Colors.dark_green, f"Решите пример: {{{Colors.cmd_hex}}}{cls.expr}")

    @classmethod
    def send_winner_message(cls, player) -> None:
        send_client_message_to_all(
            Colors.dark_green,
            f"{{{Colors.cmd_hex}}}{player.name}[{player.id}]{{{Colors.dark_green_hex}}} написал правильный ответ: {{{Colors.cmd_hex}}}{cls.correct_answer}{{{Colors.dark_green_hex}}}!"
        )
        player.set_money_ex(100000)
        cls.correct_answer = ID_NONE
        cls.expr = ""
        kill_timer(cls.math_timer)
        cls.math_timer = ID_NONE


    @classmethod
    def no_winner_message(cls) -> None:
        send_client_message_to_all(
            Colors.dark_green,
            f"Никто не написал правильный ответ! Ответ: {{{Colors.cmd_hex}}}{cls.correct_answer}{{{Colors.dark_green_hex}}}!"
        )
        cls.correct_answer = ID_NONE
        cls.expr = ""
        cls.math_timer = ID_NONE
