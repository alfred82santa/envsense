========
EnvSense
========

Environment Sense on Intel Edison

Motivation
==========

The goal of this project is to create a device for sensing the environment around a person,
to understand the environmental conditions that the person is experiencing in order to
alarm in case of danger or to warn about risk situations.

Members
=======

* Marta Tolós (github user: @martatolos)
* Javier Lago (github user: @xlake)
* Alfred Santacatalina (github user: @alfred82santa)

Installation
============

Adding repositories and installing required software

.. code-block:: bash

    $ echo "src/gz all http://repo.opkg.net/edison/repo/all" >> /etc/opkg/base-feeds.conf  && echo "src/gz edison http://repo.opkg.net/edison/repo/edison" >> /etc/opkg/base-feeds.conf  && echo "src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32" >> /etc/opkg/base-feeds.conf && opkg update

Updating mraa and upm

.. code-block:: bash

    $ opkg upgrade libmraa0 && opkg upgrade upm

Installing Python 3 and libs

.. code-block:: bash

    $ opkg install mraa-python3 upm-python3 python3-misc python3-importlib