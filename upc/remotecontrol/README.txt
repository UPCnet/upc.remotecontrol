=================
upc.remotecontrol
=================

Connect to the Plone Instance:: 

>>> from xmlrpclib import ServerProxy
>>> client = ServerProxy('http://admin:admin@localhost:8080/')

List all Plone instances inside the Zope instance::

>>> client.listInstances()
['instance1', 'instance2', 'instance3']

Install a product in all instances::

>>> client.installProduct("collective.fancyzoomview")
'Successfully installed collective.fancyzoomview on all instances.'

Uninstall a product in all instances::

>>> client.uninstallProduct("collective.fancyzoomview")
'Successfully uninstalled collective.fancyzoomview on all instances.'

Reinstall a product in all instances::

>>> print client.reinstallProduct("collective.fancyzoomview")
'Successfully reinstalled collective.fancyzoomview on all instances.'

Apply specific Generic Setup import step::

>>> client.applyImportStep("collective.fancyzoomview", "catalog")
'Successfully applied import step catalog to profile collective.fancyzoomview.'
