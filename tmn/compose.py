import uuid
from tmn import configuration

volumes = ['chaindata']

networks = ['tmn_default']

environment = {
}

containers = {
    'metrics': {
        'image': 'tomochain/infra-telegraf:devnet',
        'hostname': None,
        'name': 'metrics',
        'environment': {
            'METRICS_ENDPOINT': None
        },
        'network': 'tmn_default',
        'volumes': {
          '/var/run/docker.sock': {'bind': '/var/run/docker.sock',
                                   'mode': 'ro'},
          '/sys': {'bind': '/rootfs/sys', 'mode': 'ro'},
          '/proc': {'bind': '/rootfs/proc', 'mode': 'ro'},
          '/etc': {'bind': '/rootfs/etc', 'mode': 'ro'}
        },
        'detach': True
    },
    'tomochain': {
        'image': 'tomochain/infra-tomochain:devnet',
        'name': 'tomochain',
        'environment': {
            'IDENTITY': None,
            'PRIVATE_KEY': None,
            'BOOTNODES': None,
            'NETSTATS_HOST': None,
            'NETSTATS_PORT': None,
            'WS_SECRET': None
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
    Compose the containers with their variables
    """
    # custom
    if configuration.read_conf('identity'):
        identity = configuration.read_conf('identity')
    else:
        identity = '{}_{}'.format(name, uuid.uuid4().hex[:6])
        configuration.write_conf('identity', identity)
    containers['metrics']['hostname'] = identity
    containers['tomochain']['environment']['IDENTITY'] = identity
    for container in list(containers):
        # add environment variables
        for variable in list(containers[container]['environment']):
            try:
                containers[container]['environment'][variable] = (
                    environment[variable])
            except KeyError:
                # TODO add logging
                pass
        # rename containers
        containers[container]['name'] = '{}_{}'.format(name, container)
