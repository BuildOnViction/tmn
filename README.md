# tmn <a href="https://gitter.im/tomochain/tmn"><img align="right" src="https://badges.gitter.im/gitterHQ/gitter.png"></a>

| Branch  | Status | Coverage |
| --- | --- | --- |
| Master | [![Build Status](https://travis-ci.org/tomochain/tmn.svg?branch=master)](https://travis-ci.org/tomochain/tmn) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/tmn/badge.svg?branch=master)](https://coveralls.io/github/tomochain/tmn?branch=master) |
| Develop | [![Build Status](https://travis-ci.org/tomochain/tmn.svg?branch=develop)](https://travis-ci.org/tomochain/tmn) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/tmn/badge.svg?branch=develop)](https://coveralls.io/github/tomochain/tmn?branch=develop) |

Tomo MasterNode (tmn) is a cli tool to help you run a TomoChain masternode

## Running and applying a masternode

If you are consulting this repo, it's probably because you want to run a masternode.
For complete guidelines on running a full node and applying it as a masternode, please refer to the [documentation](https://docs.tomochain.com/get-started/run-node/).

## Requirements

- Python >= 3.5
- Docker

## Installation

```
pip3 install --user tmn
```

If you are using macOS, make sure that the user python3 path is in your `$PATH`.

They are in `~/Library/Python/[python version number]/bin`.

For example, with python `3.6` and `bash`, add `PATH=$PATH:$HOME/Library/Python/3.6/bin` to your `$HOME/.bashrc`.

## Update

To update `tmn, use pip3 directly.

```
pip3 install -U tmn
```

If you want to update the version of the TomoChain masternode run by tmn, directly use `tmn update`.
We communicate about updates on our [Gitter channel](https://gitter.im/tomochain/tmn).

## Usage

```
Usage: tmn [OPTIONS] COMMAND [ARGS]...

  Tomo MasterNode (tmn) is a cli tool to help you run a TomoChain masternode

Options:
  --debug       Enable debug mode
  --docker URL  Url to the docker server
  --version     Show the version and exit.
  --help        Show this message and exit.

Commands:
  docs     Display TomoChain documentation link
  inspect  Show details about your TomoChain masternode
  remove   Remove your TomoChain masternode
  start    Start your TomoChain masternode
  status   Show the status of your TomoChain masternode
  stop     Stop your TomoChain masternode
  update   Update your masternode
```

### First start

On the first run you will need to provide some options to the start command.
It will let you configure your node.

```
name = tomochain-orion  # A name that represents you.
                        # It will be the public name available on tomomaster
                        # and on the network stat page.

net = testnet           # The network you want to connect to.
                        # Should be testnet or mainnet.

pkey = a25...5f5        # The private key of the account you want your
                        # masternode to use.
                        # It will be used to receive transactions fees
                        # Please use a separate new account for security reasons

tmn start --name $name --net $net --pkey $pkey
```

### After the first start

Once your node has been configured, you can use the start, stop and
status command to interact with your node without any options.

```
tmn stop

tmn start

tmn status

tmn inspect

tmn update
```

### Removing

If you want to completely remove your node, you can use the `remove` command.
Be aware that it will delete all data and lose your unique identity.

```
tmn remove
```

## Applying your node

With a running node, you can now apply it as a masternode on TomoMaster.
You can get the details of your node required to apply directly from `tmn`.

```
tmn inspect
```
