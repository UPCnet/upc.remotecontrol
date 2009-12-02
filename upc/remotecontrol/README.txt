
Connect to the Plone Instance:: 

>>> from xmlrpclib import ServerProxy
>>> client = ServerProxy('http://admin:admin@localhost:8080/instance1')

List all installed products::

>>> client.listProducts()
True

>>> client.installProduct()
True

>>> client.uninstallProduct()
True

