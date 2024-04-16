from typing import Optional

from django.http import HttpResponse, JsonResponse
from ninja import NinjaAPI, File, Schema
from ninja.files import UploadedFile

from blog import serializers
from blog.controller import add_post, get_all_posts, get_one_post, add_one_comment, add_one_reply, update_post
from json import JSONEncoder

apis = NinjaAPI()


class Item(Schema):
    title: str
    content: str


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


@apis.post("/post/add")
def add_posts(request, item: Item, image: UploadedFile = File()):
    add_post(item, image)
    return {"message": "Post Added"}

#
# @apis.patch("/post/{post_id}")
# def updates_post(request, item: Item, post_id, image: UploadedFile = File()):
#     update_post(item, image, post_id)
#     return {"message": "Post Updated"}


@apis.get("/post/{post_id}")
def get_post(request, post_id):
    post = get_one_post(post_id)
    data = serializers.PostSerializer(post, many=False)
    return JsonResponse(data.data, safe=False)


@apis.get("/post")
def get_all_post(request):
    post = get_all_posts(request)
    data = serializers.PostSerializer(post, many=True)
    return JsonResponse(data.data, safe=False)


@apis.get("/comment/add/{post_id}")
def add_comment(request, content, email, post_id):
    add_one_comment(content, email, post_id)
    return JsonResponse({"message": "Comment Added"}, safe=False)


@apis.get("/reply/add/{comment_id}")
def add_reply(request, content, email, comment_id):
    add_one_reply(content, email, comment_id)
    return JsonResponse({"message": "Reply Added"}, safe=False)
