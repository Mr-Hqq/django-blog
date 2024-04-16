from django.urls import path
from .views import postview, comment, reply, home

urlpatterns = [
    path('<int:id>', postview, name='post'),
    path('addcomment/<int:id>', comment.as_view(), name='addcomment'),
    path('addreply/<int:id>', reply.as_view(), name='addreply'),
    path('home', home, name='homepage'),
]
