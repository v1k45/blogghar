from django import forms
from django.template.loader import render_to_string


class SimpleMdeWidget(forms.Textarea):

    def render(self, name, value, attrs=None):
        # adding simplemde-editor class to the Textarea tag.
        if 'class' in attrs:
            attrs['class'] += ' simplemde-editor'
        else:
            attrs.update({'class': 'simplemde-editor'})

        widget = super(SimpleMdeWidget, self).render(name, value, attrs)

        widget_html = render_to_string('simplemde/widget.html', {
            'widget': widget
        })

        return widget_html

    class Media(object):

        css = {
            'all': ('//cdn.jsdelivr.net/simplemde/latest/simplemde.min.css', )
        }

        js = ('//cdn.jsdelivr.net/simplemde/latest/simplemde.min.js',
              'js/simplemde.init.js')
