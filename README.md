[![PyPI version](https://badge.fury.io/py/pypushover.svg)](https://badge.fury.io/py/pypushover)

# pypushover
Object Oriented Python bindings to the [Pushover API](https://pushover.net/api).  Supports both python 2.7.x and 3.x.  See the [Wiki](https://github.com/KronosKoderS/py_pushover/wiki) for more detailed information regarding usage.  

# Installation

## Requirements

* [requests](http://docs.python-requests.org/en/latest/)
* [websocket-client](https://github.com/liris/websocket-client)

## PyPi

Just run the following:

    pip install pypushover

## Manual Installation

1. Download the source code from Github
2. navigate to the downloaded folder
3. execute `python setup.py install`


# Usage
    
Basic Usage:
-----------
    import pypushover as pypo
    pypo.message.push_message('<app token>', '<user key>', 'Hello World!')
