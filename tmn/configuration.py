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
            display.warning_ignoring_start_options(conf_name)
        name = conf_name
    else:
        if _validate_name(new_name):
            name = new_name
            create = True
        elif not new_name:
            display.error_start_not_initialized()
            sys.exit()
        else:
            display.error_validation_option('--name',
                                            '4 to 10 characters slug')
            sys.exit()
    if create:
        if not net:
            display.error_start_option_required('--net')
            sys.exit()
        elif not pkey:
            display.error_start_option_required('--pkey')
            sys.exit()
        if not _validate_pkey(pkey):
            display.error_validation_option('--pkey',
                                            '64 characters hex string')
            sys.exit()
        else:
            if net == 'devnet':
                compose.environment = networks.devnet
            if net == 'testnet':
                compose.environment = networks.testnet
            compose.environment['PRIVATE_KEY'] = pkey
        resources.user.write('name', name)


def _validate_name(name):
    if (
        name
        and validators.slug(name)
        and validators.length(name, min=4, max=10)
    ):
        return True
    else:
        return False


def _validate_pkey(pkey):
    if (
        pkey
        and validators.length(pkey, min=64, max=64)
    ):
        try:
            int(pkey, 16)
            return True
        except ValueError:
            return False
    else:
        return False
