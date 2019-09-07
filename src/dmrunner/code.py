from invoke import task
from invoke.exceptions import UnexpectedExit

from pathlib import Path

from terminal import terminal as t
from utils import group_by_key


@task
def download_code(ctx):
    print(t.bold("Checking authentication with GitHub ..."))

    try:
        ctx.run("ssh -T git@github.com", hide=True)
    except UnexpectedExit:
        print(
            t.red(
                *"Authentication failed - check that your local SSH keys have been uploaded to GitHub."
            )
        )
        raise
    else:
        print(t.green("* Authentication to Github succeeded."))

    code_directory = Path(ctx["code"]["directory"])

    print(
        t.bold(
            f"Ensuring you have local copies of Digital Marketplace code in {code_directory} ..."
        )
    )

    code_directory.mkdir(parents=True, exists_ok=True)

    nested_repositories = group_by_key(
        c["repositories"], "run-order", include_missing=True
    )
    for repo_name in itertools.chain.from_iterable(nested_repositories):
        repo_path = code_directory / repo_name

        if repo_path.isdir():
            continue

        print(
            t.green("* Downloading")
            + " "
            + ctx["repositories"][repo_name].get("name", repo_name)
            + " "
        )
        ctx.run(f"git clone {ctx['base-git-url']/repo_name} {repo_path}", hide="out")

    print(t.green("* Your Digital Marketplace code is all present and accounted for."))
