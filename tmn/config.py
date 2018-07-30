import pathlib
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
        p = pathlib.Path(self.path).expanduser()
        if not p.is_file():
            try:
                p.touch()
            except pathlib.PermissionError:
                return False
        return True
