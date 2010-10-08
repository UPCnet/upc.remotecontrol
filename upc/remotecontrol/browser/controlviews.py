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
        out = []
        for plonesite in listPloneSites(context):
            if getattr(plonesite, "portal_cache_settings", None):
                cachetool = plonesite.portal_cache_settings
                SquidUrls = cachetool.getSquidURLs()
                domains = cachetool.getDomains()
                policy = cachetool.getPolicy()
                rules = cachetool.getRules()
                out.append(plonesite.id +"::: SquidURLS:"+ str(SquidUrls) +", Domains:"+ str(domains) +", Policy:"+ str(policy.id) +", Rules:"+ str(rules.items()) +"\n")
            else:
                notinstalled ="Cache setup not installed in %s" % plonesite.id 
                out.append(notinstalled)
        return out