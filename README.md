# San-Andreas Gang War

## This code needs a serious refactor. Please keep your complaints to yourself, however, you can certainly use it.

## About gamemode
The gamemode has:

- Math game
- GangWar system
- House system
- DM zones
- Drift system
- Squad system (player-created gangs)


## Installation

- Download latest [open.mp](https://github.com/openmultiplayer/open.mp/releases) server version
- Download [PySAMP](https://github.com/pysamp/PySAMP) ([plugin](https://github.com/pysamp/PySAMP/releases))
- Download [PySAMP-streamer](https://github.com/pysamp/PySAMP-streamer/releases) ([plugin](https://github.com/samp-incognito/samp-streamer-plugin/releases))
- Download [PySAMP-DriftCounter](https://github.com/gsmj/PySAMP-DriftCounter)

After installation, your server directory should look like this:
```
server /
    components/*
    gamemodes/
        empty.amx
        empty.pwn
    plugins/
        streamer
        PySAMP
        DriftPointsCounter
    driftcounter/*
    pysamp/*
    pystreamer/*
    python/*
```

If you failed to install plugins and server, you can always install [v.0.7.1-beta](https://github.com/gsmj/San-Andreas-Gang-War/tree/0.7.1-beta). This release contains a pre-installed server and plugins.