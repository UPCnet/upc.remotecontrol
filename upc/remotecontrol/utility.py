# -*- encoding: utf-8 -*-

from zope.interface import implements

from persistent import Persistent

from upc.remotecontrol.interfaces import IRemoteControlUtility

class RemoteControlUtility(Persistent):
    """Remote Control Utility
    """
    implements(IRemoteControlUtility)
    
    def __init__(self):
        pass
    
    def listProducts(self):
        print "listProducts()"
        return True
    
    def installProduct(self, id):
        print "installProduct()"
        return True

    def uninstallProduct(self, id):
        print "uninstallProduct()"
        return True