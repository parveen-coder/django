from django.urls import path, re_path
from . import views

urlpatterns = [
    
    path('home/<name>/<id>', views.home),
    path('json/',views.json1),
    path('user/',views.user1),
    path('username/',views.user2),
    path('home1/',views.user3),
    path('user4/<int:id>/<str:name>',views.user4),
    path('user4/<slug:name>',views.user7), 
    path('studentlist/',views.studentlist, name="student"),
    path('studentlist1/',views.studentlist1, name="student1"),
    path('linkuse/',views.linkuse),
    path('studentindex/<int:id>', views.studentindex),
    re_path(r'^students/(?P<id>[0-9]{4})/$', views.regexp),
    # path('html1/<str:name>', views.html1),
    re_path(r'^html1/(?P<name>[A-Za-z]{9})/$', views.html1),
    path('listdata/',views.listdata),
    path('studdict/',views.userdict)
,

  
  
   
]