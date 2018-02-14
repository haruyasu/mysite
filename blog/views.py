from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post, Comment, Category
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.db.models import Q, Count

# Create your views here.

class HomePage(TemplateView):
    template_name = 'index.html'

class SkillsView(TemplateView):
    template_name = 'skills.html'

class PortfolioView(TemplateView):
    template_name = 'portfolio.html'

class PhotosView(TemplateView):
    template_name = 'photos.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class BaseListView(ListView):
    paginate_by = 3

    def base_queryset(self):
        queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return queryset

class PostListView(BaseListView):
    model = Post

    def get_queryset(self):
        queryset = self.base_queryset()
        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['categories'] = Category.objects.all()
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        return context

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class CategoryView(BaseListView):
    model = Post

    def get_queryset(self):
        queryset = self.base_queryset()
        category_name = self.kwargs['category']
        self.category = Category.objects.get(name=category_name)
        queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['categories'] = Category.objects.all()
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        return context

#######

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
