import logging
import sys

from clint import resources
from eth_keys import keys
from slugify import slugify
import docker

from tmn import display
from tmn.elements.network import Network
from tmn.elements.service import Service
from tmn.elements.volume import Volume
from tmn.environments import environments

logger = logging.getLogger('tmn')
resources.init('tomochain', 'tmn')


class Configuration:
    """docstring for Configuration."""

    def __init__(self, name: str = None, net: str = None,
                 pkey: str = None, start: bool = False,
                 docker_url: str = None, api: bool = False) -> None:
        self.networks = {}
        self.services = {}
        self.volumes = {}
        self.name = name
        self.net = net
        self.pkey = pkey or ''
        self.id = None
        self.force_recreate = False
        if not docker_url:
            self.client = docker.from_env()
        else:
            self.client = docker.DockerClient(base_url=docker_url)
        self.api = 'True' if api else 'False'
        try:
            self.client.ping()
        except Exception as e:
            logger.error(e)
            display.error_docker()
            sys.exit('\n')
        if resources.user.read('name'):
            self._load()
        elif start:
            self._write()
        else:
            display.error_start_not_initialized()
            sys.exit('\n')
        self._compose()

    def _get_address(self) -> str:
        pk = keys.PrivateKey(bytes.fromhex(self.pkey))
        return pk.public_key.to_address()[2:]

    def _load(self) -> None:
        if self.name or self.net or self.pkey:
            display.warning_ignoring_start_options(resources.user.read('name'))
        self.id = resources.user.read('id')
        self.name = resources.user.read('name')
        self.net = resources.user.read('net')
        self.api = resources.user.read('api')
        #######################################################################
        # this is a dirty fix for retro compatiblity                          #
        # can be removed in some future version                               #
        # old `tmn` don't write the `id` or `net` option to disk              #
        # screw with `tmn update`                                             #
        # will ask to recreate as this is a breaking change                   #
        #######################################################################
        if not self.id or not self.net:
            self.force_recreate = True
            self.net = 'devnet'
        #######################################################################

    def _write(self) -> None:
        if not self.name:
            display.error_start_option_required('--name')
            sys.exit('\n')
        elif not self.net:
            display.error_start_option_required('--net')
            sys.exit('\n')
        elif not self.pkey:
            display.error_start_option_required('--pkey')
            sys.exit('\n')
        self._validate()
        self.id = self._get_address()
        resources.user.write('id', self.id)
        resources.user.write('name', self.name)
        resources.user.write('net', self.net)
        resources.user.write('api', self.api)

    def _compose(self) -> None:
        self.networks['tmn'] = Network(
            name='{}_tmn'.format(self.name),
            client=self.client
        )
        self.volumes['chaindata'] = Volume(
            name='{}_chaindata'.format(self.name),
            client=self.client
        )
        if self.net == 'mainnet':
            tag = 'stable'
        elif self.net == 'testnet':
            tag = 'testnet'
        else:
            tag = 'latest'
        if self.api == 'True':  # this is dirty, should be refactored
            tomochain_ports = {'30303/udp': 30303, '30303/tcp': 30303,
                               8545: 8545, 8546: 8546}
        else:
            tomochain_ports = {'30303/udp': 30303, '30303/tcp': 30303}
        self.services['metrics'] = Service(
            name='{}_metrics'.format(self.name),
            hostname='{}'.format(self.id),
            image='tomochain/telegraf:{}'.format(tag),
            network=self.networks['tmn'].name,
            volumes={
                '/var/run/docker.sock': {
                    'bind': '/var/run/docker.sock', 'mode': 'ro'
                },
                '/sys': {'bind': '/rootfs/sys', 'mode': 'ro'},
                '/proc': {'bind': '/rootfs/proc', 'mode': 'ro'},
                '/etc': {'bind': '/rootfs/etc', 'mode': 'ro'}
            },
            client=self.client
        )
        self.services['tomochain'] = Service(
            name='{}_tomochain'.format(self.name),
            image='tomochain/node:{}'.format(
                'devnet' if tag == 'latest' else tag
            ),
            network=self.networks['tmn'].name,
            environment={
                'IDENTITY': '{}'.format(self.name),
                'PRIVATE_KEY': '{}'.format(self.pkey)
            },
            volumes={
                self.volumes['chaindata'].name: {
                    'bind': '/tomochain', 'mode': 'rw'
                }
            },
            ports=tomochain_ports,
            client=self.client
        )
        for container, variables in environments[self.net].items():
            for variable, value in variables.items():
                self.services[container].add_environment(
                    name=variable,
                    value=value
                )

    def _validate(self) -> None:
        self.name = slugify(self.name)
        if len(self.name) < 5 or len(self.name) > 30:
            display.error_validation_option('--name', '5 to 30 characters '
                                            'slug')
            sys.exit('\n')
        if len(self.pkey) != 64:
            display.error_validation_option('--pkey', '64 characters hex '
                                            'string')
            sys.exit('\n')
        try:
            bytes.fromhex(self.pkey)
        except ValueError:
            display.error_validation_option('--pkey', '64 characters hex '
                                            'string')
            sys.exit('\n')

    def remove(self) -> None:
        resources.user.delete('id')
        resources.user.delete('name')
        resources.user.delete('net')
