volumes = ['chaindata']

networks = ['tmn_default']

environment = {
    'NETSTATS_HOST': 'Test'
}

containers = {
    'metrics': {
        'image': 'tomochain/infra-telegraf:devnet',
        'hostname': None,
        'name': 'metrics',
        'environment': None,
        'network': 'tmn_default',
        'volumes': None,
        'detach': True
    },
    'tomochain': {
        'image': 'tomochain/infra-tomochain:devnet',
        'name': 'tomochain',
        'environment': {
            'NETSTATS_HOST': None
        },
        'network': 'tmn_default',
        'volumes': {
            'chaindata': {'bind': '/tomochain/data', 'mode': 'rw'}
        },
        'detach': True
    }
}


def process(name):
    """
    Compose the containers with their volumes, networks, environment variables
    """
    for container in list(containers):
        # add environment variables
        try:
            for variable in list(containers[container]['environment']):
                try:
                    containers[container]['environment'][variable] = (
                        environment[variable])
                except KeyError:
                    # TODO add logging
                    pass
        except TypeError:
            pass
        # rename containers
        containers[container]['name'] = '{}_{}'.format(name, container)
