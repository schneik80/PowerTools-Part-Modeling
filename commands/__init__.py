from .sketchfix import entry as sketchfix
from .sketchunderconstrained import entry as sketchunderconstrained
from .sketchcirclecenterpoint import entry as sketchcirclecenterpoint
from .timelinecompute import entry as timelinecompute
from .mirrorderive import entry as mirrorderive
from .hideobjects import entry as hideobjects

# Fusion will automatically call the start() and stop() functions.
commands = [
    sketchfix,
    sketchunderconstrained,
    sketchcirclecenterpoint,
    timelinecompute,
    mirrorderive,
    hideobjects,
]


def start():
    for command in commands:
        command.start()


def stop():
    for command in commands:
        command.stop()
