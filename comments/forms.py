from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton


from .models import Comment
from blog.models import Post


class CommentForm(forms.ModelForm):
    post_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta(object):
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['class'] = 'materialize-textarea'
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('comments:post')
        self.helper.form_id = 'postcomment'
        self.helper.layout = Layout(
            'post_id',
            'comment',
            StrictButton(
                'Post a comment', type='submit',
                css_class='btn blue btn-large right waves-effect waves-light')
            )

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        post_id = cleaned_data['post_id']
        if not post_id:
            raise forms.ValidationError("Invalid post")
        else:
            post_exists = Post.objects.published().filter(id=post_id).exists()
            if not post_exists:
                raise forms.ValidationError("Post not found.")

        return cleaned_data

    def save(self, commit=True):
        save_data = super(CommentForm, self).save(commit=False)
        save_data.author = self.user
        save_data.post_id = self.cleaned_data['post_id']
        save_data.save()
        return save_data
