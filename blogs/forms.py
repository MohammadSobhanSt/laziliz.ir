from django import forms
from .models import Blog, Comment


class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter blog title'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Write your blog content here...', 'rows': 10})
        
        
class CommentCreateForm(forms.ModelForm):    
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'user_comment': 'Comment',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Write your comment here...', 'rows': 3})