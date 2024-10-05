from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from rest_framework.reverse import reverse_lazy
from desk.models import Post, Comment, Image, Video, User
from .forms import ImageFormSet, VideoFormSet, PostForm
from .utils import email_about_new_comment
from django.db.utils import IntegrityError
from .mixins import *


# Create your views here.


class PostListView(ListView):
    model = Post
    ordering = '-datecreation'
    template_name = 'MainPage.html'
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
        
        return redirect('PostReview', pk=pk)
    
    return render(
        request,
        'PostReview.html',
        {'post': post, 'comments': comments, 'user_verification': user_verification}
    )


class PostIfc():
    form_class = PostForm
    model = Post
    template_name = 'Create.html'
    
    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((n.is_valid() for n in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('MainPage')
    
    def formset_video_valid(self, formset):
        video = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for v in video:
            v.post = self.object
            v.save()
    
    def formset_images_valid(self, formset):
        images = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for i in images:
            i.post = self.object
            i.save()


class PostCreateView(IsVerifipdMixin, PostIfc, CreateView):
    def get_context_data(self, **kwargs):
        c = super(PostCreateView, self).get_context_data(**kwargs)
        c['named_formsets'] = self.get_named_formsets()
        return c
    
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'video': VideoFormSet(prefix='video'),
                'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'video': VideoFormSet(self.request.POST or None, self.request.FILES or None, prefix='video'),
                'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }


class PostUpdateView(AuthorRequiredMixin, PostIfc, UpdateView):
    
    def get_context_data(self, **kwargs):
        c = super(PostUpdateView, self).get_context_data(**kwargs)
        c['named_formsets'] = self.get_named_formsets()
        return c
    
    def get_named_formsets(self):
        return {
            'video': VideoFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix='videos'
            ),
            
            'images': ImageFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix='images'
            ),
        }


class PostDeleteView(AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'Delete.html'
    success_url = reverse_lazy('MainPage', )


def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        messages.success(
            request, 'Такого изображения не существует'
        )
        return redirect('Update', pk=image.post.id)
    
    image.delete()
    messages.success(
        request, 'Изображение удалено'
    )
    return redirect('Update', pk=image.post.id)


def delete_video(request, pk):
    try:
        video = Video.objects.get(id=pk)
    except Video.DoesNotExist:
        messages.success(
            request, 'Видео не существует'
        )
        return redirect('Update', pk=video.post.id)
    
    video.delete()
    messages.success(
        request, 'Видео удалено'
    )
    return redirect('Update', pk=video.post.id)
