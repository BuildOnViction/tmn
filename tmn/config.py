# from pathlib import Path
# import toml


class ConfigManager:
    """
    Manage the tmn configuration
    :param path: Path to the config file
    """

    def __init__(self, path):
        self.path = path
