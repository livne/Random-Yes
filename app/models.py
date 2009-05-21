from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
#from django.conf.global_settings import LANGUAGES
from country_names import country_names
from language_names import language_names

COUNTRIES = tuple(country_names.items())
LANGUAGES = tuple(language_names.items())

class CustomUser(User):
    """User with custom settings."""
    country = models.CharField(_('Country'), default='xx', max_length=2, choices=COUNTRIES)
    language = models.CharField(_('Language'), default='en', max_length=5, choices=LANGUAGES)
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

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
