from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, UserDeleteForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import CustomUser, FollowingSystem
from blogs.models import Blog 
from django.contrib.auth.views import PasswordChangeForm, PasswordChangeView, PasswordChangeDoneView




class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        user = request.user.username
        email = request.user.email
        bio = request.user.bio
        context = {'username':user, 'email':email, 'bio':bio}
        return render(request, self.template_name, context)

class UserProfileExploreView(View):
    template_name = 'accounts/profile_explore.html'
    
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        blogs = Blog.objects.filter(author=user)
        is_following = False
        relation = FollowingSystem.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        
        if user.username == request.user.username:
            return redirect('accounts:profile')
        
        return render(request, self.template_name, {"blogs":blogs, 'user':user, 'is_following':is_following})


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')
    form_class = PasswordChangeForm
    
class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class UserProfileUpdateView(LoginRequiredMixin, View):
    form_class = UserUpdateForm
    template_name = 'accounts/profile_edit.html'
    
    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {"form": form})
        
    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile updated successfully!', 'success')
            return redirect('accounts:profile')

        messages.error(request, "We couldn't update your profile...", 'danger')
        return render(request, self.template_name, {"form": form})
        

class UserRegistrationView(View):
    template_name = "accounts/register.html"
    form_class = UserRegistrationForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You can't register when you are login... :)", "warning")
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form":form})
    
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        
            user = form.save(commit=False)
            password = cd["password"]
            user.set_password(password)
            user.save()
            
            if user is not None:
                login(request, user)
                
            msg = 'Your account created successfully 🎉. Thank you for choosing us :)'
            messages.success(request, msg, 'success')
            return redirect('home:home')
        
        return render(request, self.template_name, {'form':form})    
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You can't login again... :)", "warning")
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
 

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(request, email=cd['email'], password=cd['password'])

            if user is not None:
                login(request, user)
                msg = f'You logged in successfully. Welcome back dear {user.username} :)'
                messages.success(request, msg, 'success')
                return redirect('home:home')
            messages.warning(request, 'Your email or password is wrong...', 'warning')
            return render(request, self.template_name, {'form':form})
            
        messages.error(request, 'There was an error... please try again few minutes later.', 'danger')
        return render(request, self.template_name, {'form':form})
        
        
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully. We hope you back soon ;)', 'success')
        return redirect('home:home')


@method_decorator(login_required, name='dispatch')
class UserDeleteView(View):
    form_class = UserDeleteForm

    def get(self, request, user_id):
        form = self.form_class(request.GET)
        if form.is_valid():
            
            user = CustomUser.objects.get(pk=user_id)
            user.delete()

            messages.success(request, 'Your account deleted successfully.', 'success')
            return redirect('home:home')
        
        messages.error(request, 'Please Enter a valid email.', 'danger')
        return redirect('accounts:delete')
        
        

class UserFollowView(LoginRequiredMixin, View):    
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        if request.user == user:
            messages.error(request, 'You can not follow yourself :)...', 'warning')
            return redirect('accounts:profile-explore', user.username)
        relation = FollowingSystem.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'You are already following this user...', 'danger')
        else:
            FollowingSystem.objects.create(from_user=request.user, to_user=user)
            messages.success(request, f'You are following {user.username} now.', 'success')
            
        return redirect('accounts:profile-explore', user.username)
    

class UserUnfollowView(LoginRequiredMixin, View):    
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        relation = FollowingSystem.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You unfollowed this user.', 'success')
        else:
            messages.error(request, "You weren't following this user.", 'danger')
        return redirect('accounts:profile-explore', user.username)