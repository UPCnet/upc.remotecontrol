from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from OFS.interfaces import IFolder
from Acquisition import *

def listPloneSites(context):
    out = []
    for item in context.values():
        if IPloneSiteRoot.providedBy(item):
            out.append(item)
        if IFolder.providedBy(item):
            for site in item.values():
                if IPloneSiteRoot.providedBy(site):
                    out.append(site)
    return out

class ListInstancesView(BrowserView):
    """ List all the Plone instances in a Zope instance
    """
    def __call__(self):
        context = aq_inner(self.context)
        out = []
        sites = listPloneSites(context)
        for site in sites:
            out.append(site.id)
        return out

class showCacheInfo(BrowserView):
    
    def cacheValues(self):
        context = aq_inner(self.context)
        #import ipdb; ipdb.set_trace()
        for plonesite in listPloneSites(context):
            if getattr(plonesite, "portal_cache_settings", None):
                cachetool = plonesite.portal_cache_settings
                SquidUrls = cachetool.getSquidURLs()
                domains = cachetool.getDomains()
                policy = cachetool.getPolicy()
                rules = cachetool.getRules()
                yield dict(installed=True, plonesite=plonesite.id, SquidUrls=str(SquidUrls), domains=str(domains), policy=str(policy.id), rules=str(rules.items()))
            else:
                notinstalled ="Cache setup not installed in %s" % plonesite.id 
                yield dict(installed=False, notinstalled=notinstalled, plonesite=plonesite.id)
