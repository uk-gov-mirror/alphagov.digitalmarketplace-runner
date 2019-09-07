from invoke import task

from pathlib import Path

from terminal import confirm
from terminal import terminal as t


@task
def get_db_dump(ctx, clean=False, yes=False):
    print(
        t.bold(
            "Checking that you have data available to populate your Postgres database."
        )
    )

    data_path = Path(ctx["db-dump-dir"])
    data_path.mkdir(parents=True, exist_ok=True)

    if clean and not yes:
        clean = confirm(
            "Do you want to delete any existing Postgres data dumps in order to download a newer one?"
        )

    if clean:
        for f in data_path.glob("*.sql*"):
            logger(f"Removing file `{f}` ...")
            f.unlink()

    while not data_path.glob("*.sql*"):
        print(
            t.red("* No data is available.")
            + " When you press ENTER, a link will be opened for you. Please "
            "download the file to `{data_path}` then press ENTER "
            "again.".format(data_path=data_path),
            end="",
        )
        input(" ")
        webbrowser.open(ctx["db-dump-url"])
        # abuse webbrowser to open a directory in Finder
        webbrowser.open(f"file://{data_path.resolve()}")
        print("* ")
        print(
            f"* Press ENTER, after saving the file to `{data_path}`, to continue ...",
            end="",
        )
        user_input = input(" ").strip()
        if user_input:
            raise KeyboardInterrupt

        logger(green("* You have data available to populate your Postgres database."))
