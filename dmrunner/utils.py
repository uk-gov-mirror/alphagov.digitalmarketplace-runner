import os

PROCESS_NOEXIST = -1
PROCESS_TERMINATED = -2


def get_app_name(repo_name):
    return os.path.basename(repo_name).replace('digitalmarketplace-', '')
