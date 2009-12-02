from zope import schema

from zope.interface import Interface

class IRemoteControlUtility(Interface):
    """ Utility to manage a Plone instance.
    """

    def listInstalledProducts(self):
        """List all currently installed products.
        """
        
    def installProduct(self, id):
        """Install a product.
        """

    def removeProduct(self, id):
        """Remove a product.
        """