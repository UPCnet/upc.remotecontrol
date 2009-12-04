Introduction
============

upc.remotecontrol is a tool for managing a set of Plone instances through XML-RPC calls.

Buildout Installation
=====================

To install upc.remotecontrol, add the following code to your buildout.cfg::

    [instance]
    ...
    eggs =
        ...
        upc.remotecontrol


Usage
=====

Connect to a Plone Instance:: 

	>>> from xmlrpclib import ServerProxy
	>>> client = ServerProxy('http://admin:admin@localhost:8080/')

List all Plone instances::

	>>> client.listInstances()
	['instance1', 'instance2', 'instance3']

Install a product for all instances::

	>>> client.installProduct("collective.fancyzoomview")
	'Successfully installed collective.fancyzoomview on all instances.'

Uninstall a product for all instances::

	>>> client.uninstallProduct("collective.fancyzoomview")
	'Successfully uninstalled collective.fancyzoomview on all instances.'

Reinstall a product for all instances::

	>>> print client.reinstallProduct("collective.fancyzoomview")
	'Successfully reinstalled collective.fancyzoomview on all instances.'

Apply a specific Generic Setup import step for all instances::

	>>> client.applyImportStep("collective.fancyzoomview", "catalog")
	'Successfully applied import step catalog to profile collective.fancyzoomview.'
