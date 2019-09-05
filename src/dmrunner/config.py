from pathlib import Path
import yaml

config = yaml.safe_loads(Path("config/settings.yml").read_text())
user_config = yaml.safe_loads(Path("config/config.yml").read_text())
