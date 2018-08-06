# masternode

| Branch  | Status | Coverage |
| --- | --- | --- |
| Master | [![Build Status](https://travis-ci.org/tomochain/masternode.svg?branch=master)](https://travis-ci.org/tomochain/masternode?branch=master) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/masternode/badge.svg?branch=master)](https://coveralls.io/github/tomochain/masternode?branch=master) |
| Develop | [![Build Status](https://travis-ci.org/tomochain/masternode.svg?branch=develop)](https://travis-ci.org/tomochain/masternode?branch=develop) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/masternode/badge.svg?branch=develop)](https://coveralls.io/github/tomochain/masternode?branch=develop) |

All you need to run your own masternode

## Requirements

- Python >= 3.5
- Docker

## Installation

```
pip3 install --user tmn
```

## Usage

```
Usage: tmn [OPTIONS] COMMAND [ARGS]...

  Tomo MasterNode (tmn) is a cli tool to help you run a Tomochain masternode

Options:
  --config PATH    Path to the config file
  --dockerurl URL  Url to the docker server
  --version        Show the version and exit.
  --help           Show this message and exit.

Commands:
  docs   Display Tomochain documentation link
  start  Start your Tomochain masternode
  stop   Stop your Tomochain masternode
```
