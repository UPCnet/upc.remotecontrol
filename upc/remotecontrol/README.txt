
Connect to the Plone Instance:: 

>>> from xmlrpclib import ServerProxy
>>> client = ServerProxy('http://admin:admin@localhost:8080/')

List all Plone instances inside the Zope instance::

>>> client.listInstances()
['instance1', 'instance2', 'instance3']

Install a product in all instances::

>>> print client.installProduct()
True

>>> print client.uninstallProduct()
True

>>> print client.reinstallProduct()
True

