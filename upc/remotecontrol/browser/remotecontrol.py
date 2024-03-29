from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from OFS.interfaces import IFolder

import os
from Acquisition import *
from Globals import package_home

from Products.GenericSetup import profile_registry, EXTENSION
from Products.GenericSetup.upgrade import listUpgradeSteps
from Products.CMFCore.utils import getToolByName

import transaction
import logging
logger = logging.getLogger('upc.remotecontrol')


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

class InstallProductView(BrowserView):
    
    def __call__(self, product):
        context = aq_inner(self.context)
        success = []
        fail = []
        counter = 0
        for plonesite in listPloneSites(context):
            qi = getattr(plonesite, 'portal_quickinstaller', None)
            result = qi.installProducts(products=[product])
            if "%s:ok" % product in result:
                success.append(plonesite.id)
                counter = counter +1
                transaction.commit()
                logger.info("||||||||||||||| Successful installed in %s" % plonesite.id)
                logger.info("||||||||||||||| Plonesite number %s" % str(counter))
            else:
                fail.append(plonesite.id)
                logger.info("Failed to install in %s" % plonesite.id)
        if fail:
            return "Installing %s failed on instances (%s)" % (product, fail)
        else:
            return "Successfully installed %s on all instances." % (product)


class ReinstallProductView(BrowserView):
    
    def __call__(self, product):
        context = aq_inner(self.context)
        counter = 0
        for plonesite in listPloneSites(context):
            logger.info("Reinstalling product %s in site %s" % (product, plonesite))
            qi = getattr(plonesite, 'portal_quickinstaller', None)
            try:
                qi.reinstallProducts(products=[product])
            except:
                logger.info("XXXXXXXXXXXXX Failed reinstall in %s" % plonesite.id)
            counter = counter +1
            transaction.commit()
            logger.info("||||||||||||||| Successful installed in %s" % plonesite.id)
            logger.info("||||||||||||||| Plonesite number %s" % str(counter))
        return "Successfully reinstalled %s on all instances." % (product)
        
class UninstallProductView(BrowserView):
    
    def __call__(self, product):
        context = aq_inner(self.context)
        for plonesite in listPloneSites(context):
            qi = getattr(plonesite, 'portal_quickinstaller', None)
            qi.uninstallProducts(products=[product])
        return "Successfully uninstalled %s on all instances." % (product)


class ApplyImportStepView(BrowserView):
    """ Apply an import step given the product and the name of the step
    """
    def __call__(self, product, step_id):
        context = aq_inner(self.context)
        counter = 0
        for plonesite in listPloneSites(context):
            setup = getattr(plonesite, 'portal_setup', None)
            profile_id = 'profile-%s:default' % product
            setup.runImportStepFromProfile(profile_id, step_id,
                                           run_dependencies=True, purge_old=None)
            transaction.commit()
            logger.info("||||||||||||||| Successful applied in %s" % plonesite.id)
            logger.info("||||||||||||||| Plonesite number %s" % str(counter))
            counter = counter +1
        return "Successfully applied import step %s to profile %s." % (step_id, product)

class ApplyMigrationProfileView(BrowserView):
    """ Apply a migration profile given the product, the migration version (name of the profiles folder) and the step id
    """
    def __call__(self, product, migrationVersion, step_id):
        context = aq_inner(self.context)
        counter = 0     
        for plonesite in listPloneSites(context):
            setup = getattr(plonesite, 'portal_setup', None)                
            profile_id = 'profile-%s:%s' % (product, migrationVersion)
            setup.runImportStepFromProfile(profile_id, step_id,
                                           run_dependencies=True, purge_old=None)
            transaction.commit()
            logger.info("||||||||||||||| Successful applied in %s" % plonesite.id)
            logger.info("||||||||||||||| Plonesite number %s" % str(counter))
            counter = counter +1
        return "Successfully applied import step %s to profile %s from migration profile %s." % (step_id, product, migrationVersion)
    
class applyUpgradeView(BrowserView):
    """ Run upgrade steps available for a given version and for a given product.
        Usage: sourceversion must have the format ('1','2','1')
    """
    def __call__(self, product, sourceversion):
        context = aq_inner(self.context)
        request = self.request
        for plonesite in listPloneSites(context):
            setup = getattr(plonesite, 'portal_setup', None) 
            profile_id = '%s:default' % product
            request.form['profile_id'] = profile_id
            steps = listUpgradeSteps(setup, profile_id, tuple(sourceversion))
            #import pdb; pdb.set_trace()
            step_id = steps[0][0]['id']
            request.form['upgrades'] = [step_id]
            upgrade = setup.manage_doUpgrades()
        return upgrade

class reloadi18nCatalogView(BrowserView):
    """ Given the directory name of the product (without the i18n part), reload this catalog in PTS 
        (you must delete the catalog record for the given product first via ZMI)
    """
    def __call__(self, product):
        context = aq_inner(self.context)        
        cp_id = 'TranslationService'
        import ipdb;ipdb.set_trace()
        cp = context.Control_Panel
        if cp_id in cp.objectIds():
            cp_ts = getattr(cp, cp_id)
            prod_path = package_home({'__name__' : product})
            if os.path.isdir(os.path.join(prod_path, 'i18n')):
                cp_ts._load_i18n_dir(os.path.join(prod_path, 'i18n'))
        return 'Successfully reloaded i18n from product located at %s' % os.path.isdir(os.path.join(product, 'i18n'))
