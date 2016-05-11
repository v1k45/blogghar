from django.db.models import TextField

from .widgets import SimpleMdeWidget


class SimpleMdeField(TextField):

    def __init__(self, *args, **kwargs):
        super(SimpleMdeField, self).__init__(*args, **kwargs)
        # using SimpleMdeWidget for TextField
        self.widget = SimpleMdeWidget()

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(SimpleMdeField, self).formfield(**defaults)
