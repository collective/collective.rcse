from plone.app.testing import *
import collective.rcse


FIXTURE = PloneWithPackageLayer(
    zcml_filename="configure.zcml",
    zcml_package=collective.rcse,
    additional_z2_products=[],
    gs_profile_id='collective.rcse:default',
    name="collective.rcse:FIXTURE"
)

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,), name="collective.rcse:Integration"
)

FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,), name="collective.rcse:Functional"
)
