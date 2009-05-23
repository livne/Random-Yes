from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
#from django.conf.global_settings import LANGUAGES
from country_names import country_names
from language_names import language_names
from django.forms import ModelForm
from django import forms
from operator import itemgetter

countries=sorted(country_names.items(), key=itemgetter(1))
langs=sorted(language_names.items(), key=itemgetter(1))
country_choices = tuple(countries)
language_choices = tuple(langs)

GENDER = (
    ('m', _('Male')),
    ('f', _('Female')),
)

class CustomUser(User):
    """User with custom settings."""
    country = models.CharField(_('Country'), default='xx', max_length=2)
    language = models.CharField(_('Language'), default='en', max_length=5, help_text=_("Interface language."))
    gender = models.CharField(_('Gender'), blank=True, max_length=1, choices=GENDER)
    age = models.IntegerField(_('Age'), null=True, blank=True)
    keywords = models.CharField(_('Keywords'), blank=True, max_length=120, help_text=_("Comma separated words"))
    recipients = models.ManyToManyField('self', related_name='senders', symmetrical=False, null=True, blank=True)
    recipients_amount = models.IntegerField(_('Recipients amount'), default=3, help_text=_("Number of recipients for each message."))
    suggest_message = models.BooleanField(_('Suggest message'), default=False, help_text=_("Always use automatic message composition."))
    karma = models.IntegerField(_('Karma'), default=0)
    first_ip = models.IPAddressField(_('First IP Address'), null=True, blank=True)
    first_client = models.CharField(_('First client'), null=True, blank=True, max_length=120)
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


    #username - Autogenerated, 30 Alphanumberic chars.
    #first_name - Optional. 30 characters or fewer.
    #last_name - Optional. 30 characters or fewer.
    #email - Optional. E-mail address.
    #password - IGNORE
    #is_staff - Boolean. Designates whether this user can access the admin site.
    #is_active - Boolean. Designates whether this user account should be considered active.
    #is_superuser - IGNORE
    #last_login - A datetime of the user's last login.
    #date_joined - A datetime designating when the account was created.

class PreferencesForm(ModelForm):
    country = forms.ChoiceField(required=True, label='Country', choices=country_choices)
    language = forms.ChoiceField(required=True, label='Language', choices=language_choices)

    class Meta:
        model = CustomUser
        exclude = ('username', 'password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', \
                   'user_permissions', 'recipients', 'karma', 'first_ip', 'first_client')

    def clean_age(self):
        data = self.cleaned_data['age']
        if data:
            if data < 1 or data > 120:
                raise forms.ValidationError(_("Age must be positive and not more than 120"))
        return data

    def clean_recipients_amount(self):
        data = self.cleaned_data['recipients_amount']
        if data < 1 or data > 5:
            raise forms.ValidationError(_("Recipients amount must be between 1 and 5"))
        return data


