from django.shortcuts import render , redirect, get_object_or_404
from django.views import generic , View
from django.urls import reverse_lazy
from .forms import RegistrationForm , LoginForm , EditeRegisterForm,ChangePasswordForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView,UpdateView,ListView
from .models import Profile,FollowRequest, Follow
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



class UserRegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login_page')
    
class UserLoginView(View):
    def get(self, request):
        Login_form = LoginForm()
        return render(request=request, template_name='login.html', context={'form' : Login_form})        
    
    def post(self, request):
        Login_form = LoginForm(request.POST)
        if Login_form.is_valid():
            username = Login_form.cleaned_data.get('username')
            password = Login_form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()
            if user is not None:
                corroct_password = user.check_password(password)
                
                if corroct_password:
                    if hasattr(user, 'profile') and user.profile.is_archived:
                        Login_form.add_error(None, 'Your account is archived. Contact support to reactivate.')
                    else:
                        login(request, user)
                        return redirect('home')
                else:
                    Login_form.add_error(field='password' , error='password is wrong')
            else:
                Login_form.add_error(field='username' , error='the user not found')
                
        return render(request=request, template_name='login.html', context={'form' : Login_form})        

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class UserEditeRegisterView(generic.UpdateView):
    form_class = EditeRegisterForm
    template_name = 'edit_register.html'
    success_url = reverse_lazy('home')
    
    def get_object(self):
        return self.request.user
    
class UserChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('home')
    
    
class UserProfilePageView(DetailView):
    model = Profile
    template_name = "profile_page.html"
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if not user.is_authenticated or user.profile == self.object:
            context['is_pending']  = False
            context['is_following'] = False
            return context

        sender   = user.profile
        receiver = self.object

        context['is_pending'] = FollowRequest.objects.filter(
            sender=sender,
            receiver=receiver,
            accepted__isnull=True
        ).exists()

        context['is_following'] = Follow.objects.filter(
            follower=sender,
            following=receiver
        ).exists()

        return context

class UserEditProfilePageView(UpdateView):
    model = Profile
    template_name = "edit_profile_page.html"
    fields = ['bio', 'picture']
    success_url = reverse_lazy('home')
    
class UsersListView(ListView):
    model = User
    template_name = 'userslist.html'    
    context_object_name = 'userslist'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(username__icontains=q)
        return qs.order_by('username')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx

@login_required
def send_follow_request(request, pk):
    receiver = get_object_or_404(Profile,pk=pk)
    sender = request.user.profile
    if sender == receiver:
        return redirect('profile_page', pk=pk)

    FollowRequest.objects.get_or_create(sender=sender, receiver=receiver)
    return redirect('profile_page', pk=pk)


class IncomingFollowRequestsView(LoginRequiredMixin, ListView):
    model = FollowRequest
    template_name = 'incoming_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return FollowRequest.objects.filter(
            receiver=self.request.user.profile,
            accepted__isnull=True
        )

@login_required
def respond_follow_request(request, request_id, action): 
    fr = get_object_or_404(FollowRequest, id=request_id, receiver=request.user.profile)
    accept = (action == 'accept')
    if accept:
        Follow.objects.get_or_create(
            follower=fr.sender,
            following=fr.receiver
        )
        fr.accepted = True
        fr.save()
    else:
        fr.delete()

    return redirect('incoming_requests')

@login_required
def unfollow_user(request, pk):
    target = get_object_or_404(Profile, pk=pk)
    follower = request.user.profile

    Follow.objects.filter(follower=follower, following=target).delete()
    FollowRequest.objects.filter(sender=follower, receiver=target).delete()
    return redirect('profile_page', pk=pk)


@login_required
def archive_account(request):
    profile = request.user.profile
    profile.is_archived = True
    profile.save()
    logout(request)
    return redirect('home')

@login_required
def unarchive_account(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile.is_archived = False
    profile.save()
    return redirect('profile_page', pk=pk)
