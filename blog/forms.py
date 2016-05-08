from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

from .models import Blog


class BlogForm(forms.ModelForm):

    class Meta(object):
        model = Blog
        fields = ['title', 'tag_line', 'short_description', 'is_public']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BlogForm, self).__init__(*args, **kwargs)

        # a little housekeeping
        self.fields['is_public'].label = 'Publicly visible'
        self.fields['short_description'].widget.attrs['class'] = 'materialize-textarea'  # noqa

        # making forms crispy
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'title', 'tag_line', 'short_description', 'is_public',
            StrictButton(
                'Create a Blog', type='submit',
                css_class='btn blue btn-large right waves-effect waves-light'
            )
        )

    def save(self, commit=True):
        save_data = super(BlogForm, self).save(commit=False)
        save_data.author = self.user
        save_data.save()
        return save_data
