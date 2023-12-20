from django.urls import path,include
from .views import homepage,signup,loginpage,logoutpage,join,room
urlpatterns=[
    path('',homepage,name='home'),
    path('signup/',signup,name='signup'),
    path('login/',loginpage,name='signin'),
    path('logout/',logoutpage,name='logout'),
    path('join/',join,name='join'),
    path('room/<str:pk>',room,name='room')
    
]