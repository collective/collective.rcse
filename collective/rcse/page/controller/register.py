from plone.autoform import directives
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from z3c.form import button
from z3c.form import interfaces
from z3c.form.browser.password import PasswordFieldWidget
from zope import component
from zope import interface
from zope import schema

from collective.rcse.i18n import _
from collective.rcse.page.controller import register_information


class RegisterFormSchema(register_information.RegisterInformationFormSchema):
    """Form used by user to register."""
    directives.order_after(
        login='email',
        password='login',
        password_confirm='password',
        )
    login = schema.ASCIILine(
        title=_(u'Login')
        )
    directives.widget('password', PasswordFieldWidget)
    password = schema.TextLine(
        title=_(u'Password')
        )
    directives.widget('password_confirm', PasswordFieldWidget)
    password_confirm = schema.TextLine(
        title=_(u'Confirm the password')
        )


class RegisterFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(RegisterFormSchema)

    def __init__(self, context):
        self.context = context
        self.login = ''
        self.password = ''
        self.password_confirm = ''


class RegisterForm(register_information.RegisterInformationForm):
    schema = RegisterFormSchema
    enableCSRFProtection = True
    label = _('Register')

    @button.buttonAndHandler(_(u"Register"), name="register")
    def handleRegister(self, action):
        data, errors = self.extractData()
        self._checkForm(data)
        if errors:
            return
        if data['password'] != data['password_confirm']:
            raise interfaces.WidgetActionExecutionError(
                'password',
                interface.Invalid(_(u'Passwords do not match.'))
                )
        self._registerUser(data)
        self._updateDataCompany(data, data['login'])
        self._updateUser(data['login'], data)
        self._renameUserContent()
        self._sendMailToUser()
        self._sendNotificationToAdmin()
        portal_url = getToolByName(self.context, "portal_url")
        self.request.response.redirect(
            '%s/login' % portal_url()
            )

    def _registerUser(self, data):
        regtool = getToolByName(self.context, 'portal_registration')
        try:
            regtool.addMember(data['login'], data['password'])
            self.portal_url = getToolByName(self.context, "portal_url")
            self.status = _(u"Your can now log in.")
            self.request.response.redirect('%s/login' % self.portal_url())
        except ValueError, e:
            raise interfaces.ActionExecutionError(
                interface.Invalid(unicode(e))
                )


class RegisterFormWrapper(FormWrapper):
    form = RegisterForm
    label = _(u'Register')

    def update(self):
        super(RegisterFormWrapper, self).update()
        mtool = getToolByName(self.context, 'portal_membership')
        if not mtool.isAnonymousUser():
            portal_url = getToolByName(self.context, "portal_url")
            self.request.response.redirect(
                '%s/@@personal-information' % portal_url()
                )
