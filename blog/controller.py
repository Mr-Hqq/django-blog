
from django.shortcuts import get_object_or_404
from ninja import Schema, UploadedFile, File

from blog.models import Post, Comment, Reply


class Item(Schema):
    title: str
    content: str
    image: UploadedFile = File()


def add_post(item: Item, image):
    post = Post()
    post.title = item.title
    post.content = item.content
    post.image = image

    post.save()


def update_post(item: Item, image, post_id):
    post = Post.objects.get(pk=post_id)
    post.title = item.title
    post.content = item.content
    post.image = image

    post.save()


def get_one_post(id):
    post = get_object_or_404(Post, pk=id)
    return post


def get_all_posts(request):
    posts = Post.objects.order_by('-createdat')
    return posts


def add_one_comment(content, email, post):
    comment = Comment.objects.create(content=content, post=post, email=email)
    return comment


def add_one_reply(content, email, comment):
    reply = Reply.objects.create(content=content, post=comment, email=email)
    return reply
