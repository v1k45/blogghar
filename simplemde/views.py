from django.views.generic import CreateView
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from blog.decorators import blogger_required
from .models import ImageUpload


class ImageUploadView(CreateView):
    model = ImageUpload
    fields = ['image']

    @method_decorator([login_required, require_POST, blogger_required])
    def dispatch(self, request, *args, **kwargs):
        return super(ImageUploadView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse({'success': False})

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.uploader = self.request.user
        form_data.save()
        return JsonResponse({'success': True, 'imgURL': form_data.image.url})
