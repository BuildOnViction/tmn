import sys
from clint import resources
import validators
from tmn import display
# from tmn import compose

resources.init('tomochain', 'tmn')
name = None


def init(new_name=None):
    # name
    global name
    conf_name = resources.user.read('name')
    if conf_name:
        if new_name:
            display.warning_ignoring_name()
        name = conf_name
    else:
        if _validate_name(new_name):
            resources.user.write('name', new_name)
            name = new_name
        elif not new_name:
            display.error_start_not_initialized()
            sys.exit()
        else:
            # TODO display error validation
            pass
            sys.exit()


def _validate_name(name):
    if (
        name
        and validators.slug(name)
        and validators.length(name, min=4, max=10)
    ):
        return True
    else:
        return False
