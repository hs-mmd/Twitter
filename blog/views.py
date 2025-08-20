from django.urls import reverse_lazy
from .models import Post,Category,Comment,CategorySubscription
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from .forms import PostForm,CommentForm
from django.shortcuts import get_object_or_404,redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-date_posted']
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(is_archived=False).order_by('-date_posted')
                          
class PostDetailsView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailsView, self).get_context_data()
        user_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        
        liked = False
        if user_post.like.filter(id=self.request.user.id).exists():
            liked = True
            
        context['liked'] = liked
        context['total_likes'] = user_post.total_likes()
        return context
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_archived:
            raise Http404("This post is archived.")
        return obj

    
def like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    
    return redirect('post_detail', pk=pk)     

class CreatePostView(CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
                  
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = PostForm
    
class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')                      
                  
class CreatCategoryView(CreateView):
    model = Category
    template_name = 'create_category.html'    
    fields = '__all__'                 
    
class ListCategoryView(ListView):
    model = Category
    template_name = 'list_category.html'    
    context_object_name = 'list_category'   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscribed_ids = self.request.user.profile.category_subscriptions.values_list('category', flat=True)
        context['subscribed_ids'] = set(subscribed_ids)
        return context
    
def category_view(request, cat):
    category_posts = Post.objects.filter(category__name=cat.replace('-',''))
    context = {'cat':cat.replace('-',''), 'category_posts':category_posts}
    return render(request=request, template_name='category.html', context=context)

class CreateComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'create_comment.html'
    
    def form_valid(self, form):
        form.instance.post_id  = self.kwargs['pk']
        form.instance.name  = self.request.user.username
        return super().form_valid(form)


@login_required
def subscribe_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    CategorySubscription.objects.get_or_create(user=request.user.profile, category=category)
    return redirect('category_feed')

@login_required
def unsubscribe_category(request, pk):
    CategorySubscription.objects.filter(user=request.user.profile, category__pk=pk).delete()
    return redirect('category_feed')

class CategoryFeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'category_feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        cats = self.request.user.profile.category_subscriptions.values_list('category', flat=True)
        return Post.objects.filter(category__in=cats, is_archived=False).order_by('-date_posted')

@login_required
def archive_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.is_archived = True
    post.save()
    return redirect('home')

@login_required
def unarchive_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.is_archived = False
    post.save()
    return redirect('home')