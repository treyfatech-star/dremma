from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('meet-dr-musa/', views.meet_candidate, name='meet_candidate'),

    path('accomplishments/', views.accomplishments, name='accomplishments'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('signup/', views.signup, name='signup'),
]
