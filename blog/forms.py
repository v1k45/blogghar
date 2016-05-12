from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import StrictButton
from dal import autocomplete

from .models import Blog, Post, Tag


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


class TagCreateField(autocomplete.CreateModelMultipleField):
    def create_value(self, value):
        return Tag.objects.create(name=value).pk


class PostForm(forms.ModelForm):
    tags = TagCreateField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='blog:tag_autocomplete'),
        required=False,
        )

    class Meta(object):
        model = Post
        fields = ['title', 'slug', 'cover', 'content', 'summary', 'tags']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['slug'].label = 'Slug (leave blank to auto-generate)'
        self.fields['cover'].label = 'Post cover (optional)'
        self.fields['content'].label = ''
        # making forms crispy
        self.helper = FormHelper(self)
        self.helper.include_media = False
        self.helper.add_input(Submit(
            'draft', 'draft',
            css_class='btn orange btn-large right waves-effect waves-light'))
        self.helper.add_input(Submit(
            'publish', 'publish',
            css_class='btn blue btn-large right waves-effect waves-light'))

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        if 'publish' in self.data:
            cleaned_data['status'] = 'p'
        else:
            cleaned_data['status'] = 'd'
        return cleaned_data

    def save(self, commit=True):
        save_data = super(PostForm, self).save(commit=False)
        save_data.author = self.user
        save_data.blog = self.user.blog
        save_data.status = self.cleaned_data['status']
        save_data.save()
        return save_data
