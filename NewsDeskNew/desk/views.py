from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from rest_framework.reverse import reverse_lazy
from django.db.utils import IntegrityError
from desk.models import Post, Comment, Image, Video, User
from .forms import ImageFormSet, VideoFormSet, PostForm
from .utils import conf_code_generator, conf_code_verificator, confirmation_code_sender, email_about_new_comment, postman


# Create your views here.


class PostListView(ListView):
    model = Post
    ordering = '-datecreation'
    template_name = '.html'
    context_object_name = 'main'
    paginate_by = 10
    
    def post_review(request, pk):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-datecreation')
        if request.user.is_authenticated:
            user_verification = request.user.is_verified or request.user.is_staff
        else:
            user_verification = False
        
        if request.method == 'POST':
            text = request.POST['text']
            Comment.objects.create(text=text, post=post, author=request.user)
            
            email_about_new_comment(author=post.author, post_pk=post.id)
            
            return redirect('PostDetail', pk=pk)
        
        return render(
            request,
            'post.html',
            {'post': post, 'comments': comments, 'user_verification': user_verification}
        )
    
    