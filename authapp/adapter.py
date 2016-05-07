import re

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model

from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter

USERNAME_REGEX = re.compile(r'^[\w-]+$', re.UNICODE)


class CustomAccountAdapter(DefaultAccountAdapter):
    def clean_username(self, username, shallow=False):
        """
        Validates usernames.
        """
        # Instead of Overriding Django's User model, I thought doing this
        # would be more appropriate because even if I overrided django's
        # User model just for username regex, I would have to still do this.
        # This method just uses different regex, other than that it is pretty
        # much a replica of allauth's implementation.

        if not USERNAME_REGEX.match(username):
            raise forms.ValidationError(_("Usernames can only contain "
                                          "letters, digits, hyphens "
                                          "and underscores"))

        username_blacklist_lower = [ub.lower()
                                    for ub in app_settings.USERNAME_BLACKLIST]
        if username.lower() in username_blacklist_lower:
            raise forms.ValidationError(_("Username can not be used. "
                                          "Please use other username."))
        # Skipping database lookups when shallow is True, needed for unique
        # username generation.
        if not shallow:
            username_field = app_settings.USER_MODEL_USERNAME_FIELD
            assert username_field
            user_model = get_user_model()
            try:
                query = {username_field + '__iexact': username}
                user_model.objects.get(**query)
            except user_model.DoesNotExist:
                return username
            raise forms.ValidationError(
                _("This username is already taken. Please choose another."))
        return username
