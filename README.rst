Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ble_broadcastnet/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/ble_broadcastnet/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_BLE_BroadcastNet/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_BLE_BroadcastNet/actions
    :alt: Build Status

Basic IOT over BLE advertisements.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
.. note:: Only the bridge examples work on Raspberry Pi because Blinka `_bleio` doesn't support
    advertising, only scanning.

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ble_broadcastnet/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-ble-broadcastnet

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-ble-broadcastnet

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-ble-broadcastnet

Usage Example
=============

Add a secrets.py file and then run ``ble_broadcastnet_blinka_bridge.py``.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_BLE_BroadcastNet/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
