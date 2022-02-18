from django.urls import path, re_path

from .views import (
    post_detail,
    post_list,
    post_create,
    post_edit,
    subscriber_view,
    sub_conf,
)

app_name = 'blog'

urlpatterns = [
    path('subscribe/', subscriber_view, name='subscribe'),
    path('edit/<slug:slug>/', post_edit, name='post_edit'),
    path('create/', post_create, name='post_create'),
    path('<slug:slug>/', post_detail, name='post_detail'),
    path('', post_list, name='post_list'),
    re_path(r'^sub_conf/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        sub_conf, name='sub_conf'),
]