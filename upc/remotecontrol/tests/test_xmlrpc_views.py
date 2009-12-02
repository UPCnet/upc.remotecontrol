from upc.remotecontrol.tests.base import TestCase

from Products.CMFCore.utils import getToolByName

class TestXMLRPCViews(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))
        
    def testListProductsView(self):
        view = self.portal.restrictedTraverse('@@listProducts')
        self.failUnless(view)
        self.failUnless(view(), True)
            
    def testInstallProductView(self):
        view = self.portal.restrictedTraverse('@@installProduct')
        self.failUnless(view)
        self.failUnless(view(), True)

    def testUninstallProductView(self):
        view = self.portal.restrictedTraverse('@@uninstallProduct')
        self.failUnless(view)
        self.failUnless(view(), True)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestXMLRPCViews))
    return suite