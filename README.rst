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

    $ opkg install mraa-python3 upm-python3 python3-misc python3-modules

Install dependencies
====================

* AsyncIO

.. code-block:: bash

    $ wget https://pypi.python.org/packages/source/a/asyncio/asyncio-3.4.3.tar.gz
    $ tar -xvzf asyncio-3.4.3.tar.gz
    $ cd asyncio-3.4.3
    $ python3 setup.py
    $ python3 setup.py install

* PyYaml

.. code-block:: bash

    $ wget https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.11.tar.gz
    $ tar -xvzf PyYAML-3.11.tar.gz
    $ cd PyYAML-3.11
    $ python3 setup.py install

* Enum34

.. code-block:: bash

    $ wget https://pypi.python.org/packages/source/e/enum34/enum34-1.0.4.tar.gz
    $ tar -xvzf enum34-1.0.4.tar.gz
    $ cd enum34-1.0.4
    $ python3 setup.py install

* Setuptools

.. code-block:: bash

    $ wget https://pypi.python.org/packages/source/s/setuptools/setuptools-18.4.zip
    $ unzip setuptools-18.4.zip
    $ cd setuptools-18.4
    $ python3 setup.py install
    $ vi setuptools/dist.py ; Comment lines with windows_support string
    $ python3 setup.py install

* Chardet

.. code-block:: bash

    $ wget https://pypi.python.org/packages/source/c/chardet/chardet-2.3.0.tar.gz
    $ tar -xvzf chardet-2.3.0.tar.gz
    $ cd chardet-2.3.0
    $ python3 setup.py install

* Aiohttp

.. code-block:: bash

    $ wget https://pypi.python.org/packages/source/a/aiohttp/aiohttp-0.17.4.tar.gz
    $ tar -xvzf aiohttp-0.17.4.tar.gz
    $ cd aiohttp-0.17.4
    $ python3 setup.py install