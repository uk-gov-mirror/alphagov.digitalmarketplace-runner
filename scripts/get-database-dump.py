#!/usr/bin/env python3

from dmrunner.config import config

DATA_DUMP_URL = config["data-dump-url"]
SQL_DATA_PATH = Path(config["sql-data-path"])


def get_database_dump(clean=False):
    SQL_DATA_PATH.mkdir(parents=True, exist_ok=True)

    existing_files = (SQL_DATA_PATH.glob("*.sql") + SQL_DATA_PATH.glob("*.sql.gz"))

    if clean:
        for f in existing_files:
            f.unlink()
    elif existing_files:
        return True

    print("* No data is available"

    webbrowser.open(DATA_DUMP_URL)
