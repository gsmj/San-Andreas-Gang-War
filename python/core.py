from pysamp.event import event

class Core:
    @event("OnGameModeInit")
    def on_init(cls) -> None:
        return ()

    @event("OnGameModeExit")
    def on_exit(cls) -> None:
        return ()
