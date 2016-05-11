from django.views.generic import CreateView, View
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from blog.decorators import blogger_required
from .models import ImageUpload
from .utils import md2html


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


class MarkdownToHTML(View):

    @method_decorator([login_required, require_POST, blogger_required])
    def dispatch(self, request, *args, **kwargs):
        return super(MarkdownToHTML, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        if content:
            response = md2html(content)
        else:
            response = b""
        return HttpResponse(response)
