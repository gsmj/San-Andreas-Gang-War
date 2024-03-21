from pysamp.event import event
from pysamp import call_native_function

class Core:
    @event("OnGameModeInit")
    def on_init(cls) -> None:
        return ()

    # @event("OnGameModeExit")
    # def on_exit(cls) -> None:
    #     return ()
