import sys
from clint import resources
import validators
from tmn import display
from tmn import networks
from tmn import compose

resources.init('tomochain', 'tmn')
name = None


def init(new_name=None, net=None, pkey=None):
    # name
    global name
    create = False
    conf_name = resources.user.read('name')
    if conf_name:
        if new_name:
            display.warning_ignoring_name()
        name = conf_name
    else:
        if _validate_name(new_name):
            resources.user.write('name', new_name)
            name = new_name
            create = True
        elif not new_name:
            display.error_start_not_initialized()
            sys.exit()
        else:
            # TODO display error validation
            pass
            sys.exit()
    if create:
        # TODO validate net and pkey
        if not net or not pkey:
            sys.exit()
            # TODO display error required
        else:
            if net == 'devnet':
                compose.environment = networks.devnet
            if net == 'testnet':
                compose.environment = networks.testnet
            elif net == 'mainnet':
                compose.environment = networks.mainnet
            compose.environment['PRIVATE_KEY'] = pkey


def _validate_name(name):
    if (
        name
        and validators.slug(name)
        and validators.length(name, min=4, max=10)
    ):
        return True
    else:
        return False
