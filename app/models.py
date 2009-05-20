from django.db import models
from django.contrib.auth.models import User, UserManager
import uuid
from django.utils.translation import ugettext_lazy as _

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('de', 'German'),
    ('il', 'Hebrew'),
)

class UUIDField(models.CharField) :
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)



class CustomUser(User):
    """User with custom settings."""
    uuid = UUIDField(primary_key=False, editable=False, default=str(uuid.uuid4()))
    language = models.CharField(_('Language'), default="en", max_length=2, choices=LANGUAGE_CHOICES)
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    #username
    #Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores).

    #first_name
    #Optional. 30 characters or fewer.

    #last_name
    #Optional. 30 characters or fewer.

    #email
    #Optional. E-mail address.

    #password
    # IGNORE

    #is_staff
    #Boolean. Designates whether this user can access the admin site.

    #is_active
    #Boolean. Designates whether this user account should be considered active. Set this flag to False instead of deleting accounts.

    #is_superuser
    # IGNORE

    #last_login
    #A datetime of the user's last login. Is set to the current date/time by default.

    #date_joined
    #A datetime designating when the account was created. Is set to the current date/time by default when the account is created.
