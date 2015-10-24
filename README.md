# py_pushover
Object Oriented Python bindings to the [Push Over API](https://pushover.net/api).  Supports both python 2.7.x and 3.x.  See the [Wiki](https://github.com/KronosKoderS/py_pushover/wiki) for more detailed information regarding usage.  

# Instatllation
## PyPi

execute `pip install py-pushover`

## Manual Installation

1. Download the source code from Github
2. navigate to the downloaded folder
3. execute `python setup.py install`


# Usage
    
Basic Usage:
-----------
    import py_pushover as py_po
    pm = py_po.PushManager('<Token>', '<Group_Key>')
    pm.push_notification('Message Body', title="Title")
