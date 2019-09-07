from invoke import task
from invoke.exceptions import Exit, Failure

import docker
from requests.exceptions import ConnectionError

from distutils.version import LooseVersion

from terminal import terminal as t
from utils import ExitCode


MINIMUM_DOCKER_VERSION = LooseVersion("18.00")
# SPECIFIC_NODE_VERSION = LooseVersion(Path(".nvmrc").read_text().strip())
SPECIFIC_NODE_VERSION = LooseVersion("v10.16.3")


@task
def check_git(ctx):
    print(t.bold("Verifying Git is available ..."))

    try:
        ctx.run("git --version", hide=True)
        print(t.green("* Git is available. Obviously."))
    except Failure:
        raise Exit(
            t.red(
                "* You do not appear to have Git installed and/or in your path. Please install it."
            ),
            ExitCode.GIT_NOT_AVAILABLE,
        )


@task
def check_docker(ctx):
    print(t.bold("Verifying Docker is available ..."))

    try:
        docker_client = docker.from_env()

    except ConnectionError:
        raise Exit(
            t.red(
                "* You do not appear to have Docker installed and/or running. Please install Docker and "
                "ensure it is running in the background."
            ),
            ExitCode.DOCKER_NOT_AVAILABLE,
        )

    except docker.errors.APIError as e:
        raise Exit(
            t.red(
                "* An error occurred connecting to the Docker API:\n"
                f"{e}\n"
                "Please make sure it has finished starting up and "
                "is running properly."
            ),
            ExitCode.DOCKER_NOT_AVAILABLE,
        )

    except Exception as e:
        raise Exit(
            t.red(
                "* Unknown error connecting to Docker:\n"
                f"{e}\n"
                "Please make sure it has finished starting up and is running "
                "properly."
            ),
            ExitCode.DOCKER_NOT_AVAILABLE,
        )

    try:
        docker_version = LooseVersion(docker_client.version()["Version"])
        assert docker_version >= MINIMUM_DOCKER_VERSION

    except AssertionError:
        print(
            t.yellow(
                "* WARNING - You are running Docker version {}. If you are on macOS, you need "
                "Docker for Mac version {} or higher.".format(
                    docker_version, MINIMUM_DOCKER_VERSION
                )
            )
        )

    else:
        print(
            t.green(
                "* Docker is available and a suitable version appears to be installed ({}).".format(
                    docker_version
                )
            )
        )


@task
def check_node(ctx):
    print(t.bold("Checking Node version ..."))

    try:
        node_version = LooseVersion(ctx.run("node -v", hide=True).stdout.strip())

    except Failure:
        raise Exit(
            t.red(
                "* Unable to verify Node version. Please check that you have Node installed and in your path."
            ),
            ExitCode.NODE_NOT_IN_PATH,
        )

    else:
        try:
            assert node_version == SPECIFIC_NODE_VERSION
            print(
                t.green(
                    "* You are using a suitable version of Node ({}).".format(
                        node_version
                    )
                )
            )

        except AssertionError:
            raise Exit(
                t.red(
                    "* You have Node {} installed; you should use {}".format(
                        node_version, SPECIFIC_NODE_VERSION
                    )
                ),
                ExitCode.NODE_VERSION_NOT_SUITABLE,
            )

@task(check_git, check_docker, check_node, default=True)
def check(ctx):
    pass
