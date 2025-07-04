import logging
import logging.config
import os
from pathlib import Path

import yaml


def setup_logging():
    """Настройка логирования из YAML файла."""
    current_file = Path(__file__).resolve()
    base_dir = current_file.parent.parent
    config_path = base_dir / "logger" / "logging_config.yaml"

    if os.path.exists(config_path):
        with open(config_path, "rt") as f:
            config = yaml.safe_load(f)

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)
