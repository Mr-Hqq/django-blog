from django.views.generic import CreateView
from django.core.paginator import Paginator
from .models import Comment, Post, Reply
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.dispatch import receiver
from blog.tasks import image_resize_task
from django.db.models.signals import post_save


# Create your views here.

def postview(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'blog/post.html',
                  {'title': 'my title', 'post': post, 'comments': post.commentpost.all().order_by('-createdat')})


class comment(CreateView):
    model = Comment
    fields = ('content', 'email')
    template_name = 'blog/addcomment.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['id'])
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(comment, self).get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        return reverse('post', kwargs={'id': self.kwargs['id']})


class reply(CreateView):
    model = Reply
    fields = ('content', 'email')
    template_name = 'blog/addcomment.html'

    def form_valid(self, form):
        print(form.instance)
        form.instance.comment = get_object_or_404(Comment, pk=self.kwargs['id'])
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(reply, self).get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        return reverse('post', kwargs={'id': self.object.comment.post.pk})


def home(request):
    posts = Post.objects.order_by('-createdat')
    paginator = Paginator(posts, 1)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/home.html', context={"posts": posts, 'page_obj': page_obj})


@receiver(post_save, sender=Post)
def image_resizer(sender, instance, **kwargs):
    if instance.image and instance.image.width > 500 and instance.image.height > 500:
        image_resize_task.delay(instance.id)
