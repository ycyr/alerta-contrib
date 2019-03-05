EasyVista Plugin
============

Use EasyVista plugin to open ticket in Easyvista.



Installation
------------

Clone the GitHub repo and run:

    $ python setup.py install

Or, to install remotely from GitHub run:

    $ pip install git+https://github.com/ycyr/alerta-contrib.git#subdirectory=plugins/easyvista

Note: If Alerta is installed in a python virtual environment then plugins
need to be installed into the same environment for Alerta to dynamically
discover them.

Configuration
-------------

Add `easyvista` to the list of enabled `PLUGINS` in `alertad.conf` server
configuration file and set plugin-specific variables either in the
server configuration file or as environment variables.

```python
PLUGINS = ['easyvista']
TBC
```


Troubleshooting
---------------

Restart Alerta API and confirm that the plugin has been loaded and enabled.

Set `DEBUG=True` in the `alertad.conf` configuration file and look for log
entries similar to below:

```
2016-11-20 21:54:48,627 - alerta.plugins.geoip[5416]: DEBUG - GeoIP lookup for IP: 86.128.7.160 [in build/bdist.macosx-10.12-x86_64/egg/alerta_geoip.py:19]
```


License
-------

Copyright (c) 2019 Yanick Cyr. Available under the MIT License.

