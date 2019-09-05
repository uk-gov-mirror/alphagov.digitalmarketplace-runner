
from pathlib import Path
from typing import List

from .config import config
from .logging import logger

def get_db_dump(prompt_delete_existing=False):
    logger(bold("Checking that you have data available to populate your Postgres database."))

    data_path = Path(config["sql-data-path"])
    data_path.mkdir(parents=True, exist_ok=True)

    def find_dumps() -> List[Path]:
        return data_path.glob("*.sql") + data_path.glob("*.sql.*")

    if prompt_delete_existing:
        prompt = "Do you need want to delete any existing Postgres data dumps in order to download a newer one?"
        if get_yes_no_input(logger, prompt, default="n") == "y":
            sql_files = find_dumps()
            for sql_file in sql_files:
                logger(f"Removing file `{sql_file}` ...")
                sql_file.unlink()

    while not find_dumps():
        logger(
            red("* No data is available.") + " When you press ENTER, a link will be opened for you. Please "
            "download the file to `{data_path}` then press ENTER "
            "again.".format(data_path=data_path),
            end="",
        )
        input(" ")
        webbrowser.open(config["data-dump-url"])
        logger("* ")
        logger(
            "* Press ENTER, after saving the file to `{data_path}`, to continue, or type anything to "
            "abort.".format(data_path=data_path),
            end="",
        )
        user_input = input(" ").strip()
        if user_input:
            raise KeyboardInterrupt

        gzip_sql_files = data_path.glob("*.sql.gz")
        for gzip_sql_file in gzip_sql_files:
            target_sql_file = gzip_sql_file.with_suffix("")  # Remove '.gz' suffix

            if not target_sql_file.is_file():
                logger("* Extracting {} ...".format(gzip_sql_file))

                try:
                    with open(target_sql_file, "wb") as outfile, gzip.open(gzip_sql_file, "rb") as infile:
                        before_read = -1
                        while before_read < infile.tell():
                            before_read = infile.tell()

                            # Read and write in chunks to avoid macs failing on writes > 2GB
                            outfile.write(infile.read(2 ** 30))
                            outfile.flush()

                except KeyboardInterrupt:
                    target_sql_file.unlink()
                    raise

                gzip_sql_file.unlink()
                logger("* Extracted.")

        logger(green("* You have data available to populate your Postgres database."))
