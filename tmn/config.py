import pathlib
# import toml


class ConfigManager:
    """
    Manage the tmn configuration

    :param path: path to the config file
    :type path: string
    """

    def __init__(self, path='~/.config/tmn'):
        self.path = pathlib.Path(path).expanduser()
        try:
            self.path.touch(exist_ok=True)
            self.valid = True
        except (PermissionError, FileNotFoundError):
            self.valid = False
