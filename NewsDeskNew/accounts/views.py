from django.shortcuts import render
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.utils import IntegrityError
from desk.models import Post, Comment, User
from .utils import conf_code_generator, conf_code_verificator, confirmation_code_sender, postman
from desk.mixins import *


# Create your views here.


class PersonalCabinetView(CustomLoginRequiredMixin, ListView):
    model = Comment
    template_name = 'PersonalCabinet.html'
    context_object_name = 'comments'
    
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['user'] = self.request.user
        c['posts'] = Post.objects.filter(author=self.request.user).order_by('-datecreation')
        return c
    
    def post(self, request, *args, **kwargs):
        if request.method == 'Post':
            if request.POST.get('about_sub'):
                user_id = request.POST.get('about_sub')
                user = User.objects.get(pk=user_id)
                user.about_sub = True
                user.save()
            if request.POST.get('about_unsub'):
                user_id = request.POST.get('about_unsub')
                user = User.objects.get(pk=user_id)
                user.about_sub = False
                user.save()
            if request.POST.get('comment_notif_sub'):
                user_id = request.POST.get('comment_notif_sub')
                user = User.objects.get(pk=user_id)
                user.users_comments = True
                user.save()
            if request.POST.get('comment_notif_unsub'):
                user_id = request.POST.get('comment_notif_unsub')
                user = User.objects.get(pk=user_id)
                user.save()
            if request.POST.get('agree'):
                comment_id = request.POST.get('agree')
                comment = Comment.objects.get(pk=comment_id)
                comment.is_confirmed = True
                comment.save()
            if request.POST.get('decline'):
                comment_id = request.POST.get('decline')
                comment = Comment.objects.get(pk=comment_id)
                comment.is_confirmed = False
                comment.save()
        return redirect('PersonalCabinet')


def Logout(request):
    logout(request)
    return redirect('MainPage')


def SignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        try:
            about = request.POST['about_sub']
            about_sub = True
        except KeyError:
            about_sub = False
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1, about_sub=about_sub)
            except IntegrityError:
                msg = 'Такой пользователь уже есть'
                return render(request, 'registration/SignUp.html', {'msg': msg})
            conf_code_generator(user=user)
            confirmation_code_sender(user=user)
            
            return redirect('Verification', user_id=user.pk)
        
        else:
            msg = 'Проверьте правильность пароля'
            return render(request, 'registration/SignUp.html', {'msg': msg})
    
    return render(request, 'registration/SignUp.html')


def Verification(request, user_id=None):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        email_conf_code = request.POST['email_conf_code']
        if conf_code_verificator(code=email_conf_code, user=user):
            user.is_verified = True
            user.email_conf_code = None
            
            common_users = Group.objects.get(name='common_users')
            user.groups.add(common_users)
            user.save()
            login(request, user)
            return redirect('MainPage')
        else:
            msg = 'Проверьте правильность кода'
            return render(request, 'registration/Verification.html', {'error': msg, 'user': user})
    return render(request, 'registration/Verification.html', {'user': user})
