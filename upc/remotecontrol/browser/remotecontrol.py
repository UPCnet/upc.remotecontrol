from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from Acquisition import *

class ListInstancesView(BrowserView):
    
    def __call__(self):
        context = aq_inner(self.context)
        out = []
        for item in context.values():
            if IPloneSiteRoot.providedBy(item):
                out.append(item.id)
        return out
   

class InstallProductView(BrowserView):
    
    def __call__(self, product):
        context = aq_inner(self.context)
        success = []
        fail = []
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                result = qi.installProducts(products=[product], forceProfile=True, omitSnapshots=True)
                if "%s:ok" % product in result:
                    success.append(plonesite.id)
                else:
                    fail.append(plonesite.id)
        if fail:
            return "Installing %s failed on instances (%s)" % (product, fail)
        else:
            return "Successfully installed %s on all instances." % (product)


class ReinstallProductView(BrowserView):
    
    def __call__(self, product):
        context = aq_inner(self.context)
        success = []
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                qi.reinstallProducts(products=[product])
        return "Successfully reinstalled %s on all instances." % (product)
        
class UninstallProductView(BrowserView):
    
    def __call__(self, product):
        context = aq_inner(self.context)
        success = []
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                qi.uninstallProducts(products=[product])
        return "Successfully uninstalled %s on all instances." % (product)
