# from pathlib import Path
# import toml


class ConfigManager:
    """
    Manage the tmn configuration

    :param path: path to the config file
    :type path: string
    """

    def __init__(self, path='~/.config/.tmn'):
        self.path = path

    def init(self):
        return True
