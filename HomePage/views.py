from django.views.generic import TemplateView
from Content.models import Video

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all().order_by('-created_at')[:10]
        return context