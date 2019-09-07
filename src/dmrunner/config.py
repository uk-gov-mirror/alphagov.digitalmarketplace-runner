from invoke import Collection, task

from pathlib import Path

from terminal import confirm, prompt
from terminal import terminal as t

def save_config(*args):
    pass

@task(default=True)
def config(ctx):
    new_config = ctx.config.clone()
    initial_code_directory = Path(ctx["code"]["directory"]).resolve()

    print(
        "If you are an existing developer, enter the directory where your current Digital Marketplace code is "
        "checked out."
    )
    print(
        "If you do not have code currently checked out, enter the directory you would like "
        "code to be downloaded to."
    )
    user_input = prompt("", default=initial_code_directory)
    requested_code_directory = Path(user_input).resolve()
    requested_code_directory.mkdir(parents=True, exist_ok=True)

    print(f"Code directory set to {t.yellow}{requested_code_directory}{t.normal}")
    new_config["code"]["directory"] = requested_code_directory

    current_decryption = ctx["credentials"]["sops"]
    print()
    print(
        "Do you want to decrypt credentials automatically (requires security clearance)?"
    )
    decrypt_credentials = confirm("", default=current_decryption)

    print(
        "Credentials "
        + (t.green("will") if decrypt_credentials else t.red("will not"))
        + " be decrypted automatically."
    )
    new_config["credentials"]["sops"] = decrypt_credentials

    save_config(new_config, "dmrunner.yaml")

    # Patch the runner config with our new/modified configuration.
    ctx.config.update(new_config)


ns = Collection(config)
ns.configure({"code": {"directory": "code"}, "credentials": {"sops": False}})
