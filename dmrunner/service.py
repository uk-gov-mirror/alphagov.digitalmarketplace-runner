from enum import Enum
from subprocess import run

import docker


class Status(Enum):
    STOPPED = object()
    RUNNING = object()
    STARTING = object()
    STOPPING = object()

    def __bool__(self):
        return self == Status.RUNNING


class Service:
    def __init__(self, provides: str):
        self.provides = provides

    def status(self) -> Status:
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
