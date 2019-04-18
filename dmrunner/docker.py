from os import getenv
from pathlib import Path
from subprocess import CalledProcessError, run
import sys
from typing import Dict, Iterable, List, Sequence

import docker
from docker.models.containers import Container

from dmrunner.service import Service, Status


def is_compose_container(container: Container, compose_project_name: str) -> bool:
    return container.labels.get("com.docker.compose.project") == compose_project_name


def compose_container_service(container: Container) -> str:
    try:
        return container.labels["com.docker.compose.service"]
    except KeyError:
        raise ValueError(f"container {container} is not managed by docker-compose")


class DockerService(Service):
    def __init__(self, provides, container: Container):
        super().__init__(provides)
        self.container = container
        self._state = Status.RUNNING if self.container.status == "running" else Status.STOPPED

    def status(self):
        try:
            self.container.reload()  # update self.container.attrs
        except docker.errors.NotFound:
            self._status = Status.STOPPED
            return self._status

        healthcheck = self.container.attrs["State"]["Health"]["Status"]
        status = self.container.status

        if self._status == Status.RUNNING:
            if status == "exited":
                self._status = Status.STOPPED

        elif self._status == Status.STARTING:
            if healthcheck == "healthy":
                self._status = Status.RUNNING

        elif self._status == Status.STOPPING:
            if status == "exited":
                self._status = Status.STOPPED

        elif self._status == Status.STOPPED:
            if healthcheck == "starting":
                self._status = Status.STARTING

        return self._status

    def start(self):
        self.container.start()

    def stop(self):
        self.container.stop()


def _docker_compose(
    self, docker_compose: Path, command: List[str], *, project_name: str = None, compose_files: List[Path] = None
):
    env: Dict[str, str] = {
        "PATH": str(docker_compose.parent),
        "COMPOSE_PROJECT_NAME": self.project_name,
        "COMPOSE_FILE": ":".join(str(f) for f in self.compose_files),
    }
    exe = str(docker_compose)
    args: List[str] = [str(exe)] + command
    p = run(args, env=env)
    try:
        p.check_returncode()  # if returncode is non-zero, raise a CalledProcessError
    except CalledProcessError:
        run([exe, "stop"], env=env)
    return p


class DockerCompose:
    def __init__(self, compose_files: Iterable[Path] = [], project_name: str = None):
        self.compose_files = [f.resolve(strict=True) for f in compose_files]
        self.project_name = project_name

        self.docker_client = docker.from_env()
        self.docker_compose_exe = Path(sys.prefix) / "bin" / "docker-compose"

        self.docker_compose_exe.resolve(strict=True)

        self.services: Dict[str, DockerService] = self._get_services()

    def _docker_compose(self, command: List[str]):
        return _docker_compose(
            self._docker_compose_exe, command, project_name=self.project_name, compose_files=self.compose_files
        )

    def _get_services(self) -> Dict[str, DockerService]:
        return {
            compose_container_service(c): DockerService(provides=compose_container_service(c), container=c)
            for c in self.docker_client.containers.list()
            if is_compose_container(c, self.project_name)
        }

    def status(self):
        return {name: service.status() for name, service in self.services.items()}

    def start(self):
        self._docker_compose("up -d")
        self.services.update(self._get_services())

    def stop(self):
        self._docker_compose("stop")
