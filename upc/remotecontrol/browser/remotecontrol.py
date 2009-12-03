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
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                result = qi.installProducts(products=[product], forceProfile=True, omitSnapshots=True)
                print "%s: installProduct(%s)" % (plonesite.id, product)
                #print result
                # XXX: Todo: What if the installation fails?
        return True


class ReinstallProductView(BrowserView):
    
    def __call__(self, product):
        context = aq_inner(self.context)
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                qi.reinstallProducts(products=[product])
                print "%s: reinstallProduct(%s)" % (plonesite.id, product)
        return True        

class UninstallProductView(BrowserView):
    
    def __call__(self, product):
        context = aq_inner(self.context)
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                qi.uninstallProducts(products=[product])
                print "%s: uninstallProduct(%s)" % (plonesite.id, product)
        return True
