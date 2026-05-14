from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .forms import CreateBlogForm, CommentCreateForm
from .models import Blog, LikeSystem


        
class CreateBlogView(LoginRequiredMixin, View):
    template_name = 'blogs/create_blog.html'
    form_class = CreateBlogForm
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Your blog created successfully.', 'success')
            return redirect('accounts:profile')
        
        return render(request, self.template_name, {'form':form})
        

class CreateCommentView(View):
    template_name = 'comment_create.html'
    form_class = CommentCreateForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
        
        
        
class UpdateBlogView(LoginRequiredMixin, View):
    template_name = 'blogs/update_blog.html'
    form_class = CreateBlogForm
    
    def get(self, request, blog_slug):
        blog = get_object_or_404(Blog, author=request.user, slug=blog_slug)
        form = self.form_class(instance=blog)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, blog_slug):
        blog = get_object_or_404(Blog, author=request.user, slug=blog_slug)
        form = self.form_class(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your blog updated successfully.', 'success')
            return redirect('blogs:my-blogs')
            
        messages.error(request, "We couldn't update your blog.", 'danger')      
        return render(request, self.template_name, {'form':form})
        
        
class DeleteBlogView(LoginRequiredMixin, View):
    def post(self, request, blog_slug):
        blog = get_object_or_404(Blog, author=request.user, slug=blog_slug)
        blog.delete()
        messages.info(request, 'Your blog deleted successfully.', 'info')
        return redirect('blogs:my-blogs')
        

class UserBlogView(LoginRequiredMixin, ListView):
    template_name = 'blogs/user_blogs.html'
    context_object_name = 'user_blogs'
    paginate_by = 5
    ordering = ['-updated_at', '-created_at']
    
    def get_queryset(self):
        return  self.request.user.blogs.all().order_by('-updated_at', '-created_at')



class BlogDetailView(LoginRequiredMixin, View):
    template_name = 'blogs/blogs_detail.html'
    form_class = CommentCreateForm
    
    def setup(self, request, *args, **kwargs):
        self.blogs_instance = get_object_or_404(Blog, slug=kwargs['blog_slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwrags):
        comments = self.blogs_instance.pcomments.all()
        form = self.form_class
        can_like = False
        if self.blogs_instance.user_can_like(request.user):
            can_like = True
        return render(request, self.template_name, {'blog_detail':self.blogs_instance, 'comments':comments, 'form':form, 'can_like':can_like})
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.published_from = self.blogs_instance
            new_comment.save()
            messages.success(request, 'Your comment commited successfully.', 'success')
            return redirect('blogs:blogs-detail', self.blogs_instance.slug)
            
            
class BlogLikeView(LoginRequiredMixin, View):
    def post(self, request, blog_slug):
        blog = get_object_or_404(Blog, slug=blog_slug)
        like = LikeSystem.objects.filter(blog=blog, user=request.user)
        if like.exists():
            messages.error(request, 'You already liked this post...', 'danger')
        else:
            LikeSystem.objects.create(blog=blog, user=request.user)
            messages.success(request, f'You liked "{blog.title}".', 'success')
            
        return redirect("blogs:blogs-detail", blog.slug)
        
        
class BlogUnlikeView(LoginRequiredMixin, View):
    def post(self, request, blog_slug):
        blog = get_object_or_404(Blog, slug=blog_slug)
        like = LikeSystem.objects.filter(blog=blog, user=request.user)
        if like.exists():
            like.delete()
            messages.success(request, 'You unliked this blog...', 'success')
        else:
            messages.error(request, "You didn't liked this blog before...", 'danger')
            
        return redirect("blogs:blogs-detail", blog.slug)