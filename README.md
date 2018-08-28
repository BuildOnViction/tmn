# masternode

| Branch  | Status | Coverage |
| --- | --- | --- |
| Master | [![Build Status](https://travis-ci.org/tomochain/masternode.svg?branch=master)](https://travis-ci.org/tomochain/masternode?branch=master) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/masternode/badge.svg?branch=master)](https://coveralls.io/github/tomochain/masternode?branch=master) |
| Develop | [![Build Status](https://travis-ci.org/tomochain/masternode.svg?branch=develop)](https://travis-ci.org/tomochain/masternode?branch=develop) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/masternode/badge.svg?branch=develop)](https://coveralls.io/github/tomochain/masternode?branch=develop) |

All you need to run your own masternode

## Requirements

- Python >= 3.6
- Docker

## Installation

```
pip3 install --user tmn
```

## Update

```
pip3 install -U tmn
```

## Usage

```
Usage: tmn [OPTIONS] COMMAND [ARGS]...

  Tomo MasterNode (tmn) is a cli tool to help you run a Tomochain masternode

Options:
  --dockerurl URL  Url to the docker server
  --version        Show the version and exit.
  --help           Show this message and exit.

Commands:
  docs    Display Tomochain documentation link
  remove  Remove your Tomochain masternode
  start   Start your Tomochain masternode
  status  Status of your Tomochain masternode
  stop    Stop your Tomochain masternode
```

### First start

On the first run you will need to provide some options to the start command.
It will let you configure your Masternode.

```
name = tomochain-orion  # A name that represents you.
                        # It will be the public name available on tomomaster
                        # and on the network stat page.

net = testnet           # The network you want to connect to.
                        # Should be testnet or mainnet.

pkey = a25...5f5        # The private key of the account you want your
                        # masternode to use.
                        # It will be used to receive rewards.

tmn start --name $name --net $net --pkey $pkey
```

### After first start

Once your masternode has been configured one, you can use the start, stop and
status command to interact with your masternode without any options.

```
tmn stop

tmn start

tmn status
```

### Removing

If you want to completely remove your masternode, you can use the `remove` command.
Be aware that it will delete all data and lose your unique identity.

```
tmn remove
```
