from django import forms

from allauth.account import forms as allauth_forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton


class CustomLoginForm(allauth_forms.LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.helper = FormHelper(self)
        self.helper.col_class = False
        self.helper.form_tag = False
        self.helper.form_show_labels = True

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = None
            del self.fields[field].widget.attrs['placeholder']

        self.helper.layout = Layout(
            'login', 'password', 'remember',
            StrictButton(
                'Sign In', type='submit', style='margin-top: 10px',
                css_class="waves-effect btn-large blue waves-light btn right"),
        )
