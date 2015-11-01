[![Build Status](https://travis-ci.org/KronosKoderS/py_pushover.svg?branch=master)](https://travis-ci.org/KronosKoderS/py_pushover)
[![Coverage Status](https://coveralls.io/repos/KronosKoderS/py_pushover/badge.svg?branch=master&service=github)](https://coveralls.io/github/KronosKoderS/py_pushover?branch=master)

# py_pushover
Object Oriented Python bindings to the [Push Over API](https://pushover.net/api).  Supports both python 2.7.x and 3.x.  See the [Wiki](https://github.com/KronosKoderS/py_pushover/wiki) for more detailed information regarding usage.  

# Instatllation

## Manual Installation

1. Download the source code from Github
2. navigate to the downloaded folder
3. execute `python setup.py install`


# Usage
    
Basic Usage:
-----------
    import py_pushover as py_po
    py_po.message.push_message('<app token>', '<user key>', 'Hello World!')
