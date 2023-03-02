from django.urls import path

from . import views
from .API.views import *


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('home', views.home, name='home'),
    path('post', views.add_post, name='post-form'),
    path('author/search', views.author_search, name='author-search'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
    path('<str:username>/following', views.following, name='following'),
    path('<str:username>/followers', views.followers, name='followers'),
    path('authors', views.authors, name='authors'),
    path('<str:username>', views.profile, name='profile'),
    path('<str:username>/true-friends', views.true_friends, name='true-friends'),
    path('<str:username>/received', views.received_requests, name='requests'),
    path('<str:username>/sent', views.sent_requests, name='sent_requests'),

    #API urls
    path('api/authors/', AuthorListAPIView.as_view(), name='api-author-list'),
    path('api/authors/<uuid:author_id>/', SingleAuthorAPIView.as_view(), name='api-single_author'),
    path('api/authors/<uuid:author_id>/followers/', AuthorFollowersAPIView.as_view(), name='api-author-followers'),
    path('api/authors/<uuid:author_id>/followers/<uuid:follower_author_id>/', FollowerAPIView.as_view(), name='api-followers'),
    path('api/authors/<uuid:author_id>/posts/<uuid:post_id>/', PostDetailView.as_view(), name ='api-post-detail'),
    path('api/authors/<uuid:author_id>/posts/', AuthorPostsView.as_view(), name ='api-author-post'),
    
]
