from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class EeafacetednavigationtaxonomiccheckboxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import eea.facetednavigationtaxonomiccheckbox
        xmlconfig.file(
            'configure.zcml',
            eea.facetednavigationtaxonomiccheckbox,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        z2.installProduct(app, 'eea.facetednavigationtaxonomiccheckbox')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'eea.facetednavigationtaxonomiccheckbox')


EEA_FACETEDNAVIGATIONTAXONOMICCHECKBOX_FIXTURE = EeafacetednavigationtaxonomiccheckboxLayer()
EEA_FACETEDNAVIGATIONTAXONOMICCHECKBOX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_FACETEDNAVIGATIONTAXONOMICCHECKBOX_FIXTURE,),
    name="Eeafacetednavigationtaxonomiccheckbox:Integration"
)
EEA_FACETEDNAVIGATIONTAXONOMICCHECKBOX_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEA_FACETEDNAVIGATIONTAXONOMICCHECKBOX_FIXTURE, z2.ZSERVER_FIXTURE),
    name="Eeafacetednavigationtaxonomiccheckbox:Functional"
)
