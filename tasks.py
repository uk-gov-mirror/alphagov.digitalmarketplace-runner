from pathlib import Path
import os

import yaml
from colored import fore, style
from invoke import task
from invoke.exceptions import UnexpectedExit

from dmdevtools.invoke_tasks import library_tasks


os.environ["COMPOSE_FILE"] = f"config/docker-compose.yml:config/docker-compose.{os.uname().sysname}.yml"
os.environ["COMPOSE_PROJECT_NAME"] = "dmrunner"


@task
def brew(c):
    """Install system dependencies using Homebrew"""
    c.run("brew bundle")
    c.run("pyenv install --skip-existing && pyenv version")
    c.run(". Brewfile.env ; nvm install")

    pwd_pretty = str(Path().resolve()).replace(os.environ["HOME"], "$(HOME)")

    print(
        f"""{style.BOLD}
😸 Prerequisites have been installed! 😸
😺 The following steps are recommended for a seamless experience 😺
1️⃣  Add the following lines to your shell profile (usually ~/.bash_profile): 1️⃣
{style.RESET}
[ -s "{pwd_pretty}/Brewfile.env" ] && \\
	. {pwd_pretty}/Brewfile.env
{style.BOLD}
2️⃣  Source the file now so you can continue with the next step: 2️⃣
{style.RESET}
$ source Brewfile.env
{style.BOLD}
3️⃣  Increase the memory limit of Docker for Mac to 4 GiB 3️⃣
{style.RESET}"""
    )


@task(library_tasks["requirements_dev"], aliases=["requirements-dev"])
def install(c):
    """Install Python dependencies to venv"""
    pass


@task(install)
def config(c):
    """Configure preferences"""
    c.run("python main.py config", pty=True)


@task(install)
def setup(c):
    """Setup apps"""
    c.run("python main.py setup", pty=True)


@task(install)
def data(c):
    """Rebuild database"""
    c.run("python main.py data", pty=True)


@task(library_tasks["virtualenv"])
def run(c):
    """Run the Digital Marketplace"""
    c.run("python main.py run", pty=True)


@task(library_tasks["virtualenv"])
def rebuild(c):
    c.run("python main.py --rebuild run", pty=True)


@task
def docker_compose_env(c):
    print(f"export COMPOSE_FILE='{os.environ['COMPOSE_FILE']}'")
    print(f"export COMPOSE_PROJECT_NAME='{os.environ['COMPOSE_PROJECT_NAME']}'")


@task(install)
def black(c):
    """Format code using black"""
    c.run("black config/ dmrunner/ main.py setup.py tasks.py")


@task(install)
def test_black(c):
    """Check formatting of code"""
    c.run("black --check config/ dmrunner/ main.py setup.py tasks.py")


@task(install)
def test_pyflakes(c):
    """Check for code errors"""
    c.run("pyflakes config/ dmrunner/ main.py setup.py tasks.py")


@task(install)
def test_mypy(c):
    """Check for static type errors"""
    c.run("mypy dmrunner/ main.py setup.py")


@task(test_black, test_mypy, test_pyflakes)
def test(c):
    pass


def git_get_default_branch_from_remote(c, repo: Path, remote="origin"):
    if repo.samefile(c.cwd):
        result = c.run(f"git remote set-head -a {remote}", hide=True)
    else:
        with c.cd(repo):
            result = c.run(f"git remote set-head -a {remote}", hide=True)

    stdout = result.stdout.strip()
    # expecting message to be like 'origin/HEAD set to main'
    prefix = f"{remote}/HEAD set to "
    if stdout.startswith(prefix):
        branch_name = stdout[len(prefix) :]
    else:
        raise UnexpectedExit(result, f"unable to parse output from `git remote set-head -a {remote}`")

    return branch_name


def git_get_default_branch(c, repo: Path, remote="origin"):
    # When checking out a git repo with a new enough version of git you should
    # get a symbolic ref <remote>/HEAD that points to the default branch on the
    # remote. However this is not updated automatically, so it is possible for
    # it to get out of sync. If it is out of sync we fallback to
    # `git_default_branch_from_remote`.

    # look at the remote ref if it exists
    remote_head_path = repo / ".git" / "refs" / "remotes" / remote / "HEAD"
    if not remote_head_path.is_file():
        return git_get_default_branch_from_remote(c, repo, remote)
    remote_head_ref = remote_head_path.read_text().strip()

    # check that it is a symbolic ref
    if not remote_head_ref.startswith("ref: "):
        return git_get_default_branch_from_remote(c, repo, remote)

    # parse ref
    default_branch = remote_head_ref[len("ref: ") :].split("/")[-1]

    # check that branch exists locally
    if not (repo / ".git" / "refs" / "heads" / default_branch):
        return git_get_default_branch_from_remote(c, repo, remote)

    return default_branch


def git_checkout_and_pull(c, repo: Path, branch=None, remote="origin"):
    """Get the latest upstream version of a branch for a git repo

    Equivalent to (but not the same as) `git checkout <branch> && git pull`.

    If `branch` is None we get the default default branch.
    """

    git = "git -c color.ui=always"  # force output to be colo(u)rful

    with c.cd(repo):
        # We do things in a slightly different order to give us more control

        # if this fails it probably means the internet connection is bad
        fetch = c.run(f"{git} fetch {remote}", hide=True)

        if not branch:
            branch = git_get_default_branch(c, repo, remote)

        # if this fails it probably means that there are files that would be overwritten by checkout
        checkout = c.run(f"{git} checkout {branch}", hide=True)

        # if this fails the branch has diverged from the remote and user intervention is desired
        # --ff-only stops merge trying to fix it itself
        merge = c.run(f"{git} merge --ff-only FETCH_HEAD", hide=True)

    # TODO make this a more structured response
    return {
        "remote": remote,
        "branch": branch,
        "fetch": fetch,
        "checkout": checkout,
        "merge": merge,
    }


@task
def update_code(c):
    """Checkout latest version of all code"""
    config = yaml.safe_load(Path("config", "config.yml").read_text())
    code_dir = Path(config["code"]["directory"])
    for subdir in code_dir.iterdir():
        if not (subdir / ".git").is_dir():
            continue

        print(f"{fore.BLUE}Fetching latest code in default branch in {subdir.name}...{style.RESET}", end="")

        with c.cd(subdir):
            try:
                result = git_checkout_and_pull(c, subdir)
                print(f"{fore.GREEN}DONE{style.RESET}")
                if result["merge"].stdout:
                    print(result["merge"].stdout.strip())
            except UnexpectedExit as error:
                result = error.args[0]
                if result.exited < 0:
                    # We want to stop everything if the user hits ctrl-C.
                    # Invoke forwards keyboard interrupts to processes so we
                    # can't catch KeyboardInterrupt here, but in POSIX exit
                    # codes >128 are due to signals so if we get a return code
                    # less than 0 we just assume the user did a keyboard
                    # interrupt and stop everything.
                    print()
                    print("cancelled by keyboard interrupt")
                    break
                print(f"{fore.RED}ERROR{style.RESET}")
                print(result.stderr.strip())
