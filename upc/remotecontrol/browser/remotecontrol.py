from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ListProductsView(BrowserView):
    
    def __call__(self):
        print "ListProductsView"
        return True
    
class InstallProductView(BrowserView):
    
    def __call__(self):
        print "InstallProductView"
        return True
    
class UninstallProductView(BrowserView):
    
    def __call__(self):
        print "UninstallProductView"
        return True