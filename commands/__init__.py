from .sketchfix import entry as sketchfix
from .sketchunderconstrained import entry as sketchunderconstrained
from .timelinecompute import entry as timelinecompute

# Fusion will automatically call the start() and stop() functions.
commands = [
    sketchfix,
    sketchunderconstrained,
    timelinecompute,
]

def start():
    for command in commands:
        command.start()

def stop():
    for command in commands:
        command.stop()