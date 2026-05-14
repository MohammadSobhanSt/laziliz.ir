from django.views.generic import ListView
from blogs.models import Blog


class HomeView(ListView):
    model = Blog
    template_name = 'home/home.html'
    context_object_name = 'blogs'
    paginate_by = 5
    ordering = ['-updated_at', '-created_at']
