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
    re_path(r'^html1/(?P<name>[A-Za-z ]{9})/$', views.html1),
    path('listdata/',views.listdata),
    path('studdict/',views.userdict),
    path('listdict/', views.listdic),
    path('newdict/', views.newdict),
    path("student/<int:rollno>/", views.student_details),
    path('studentdetail/', views.studentdict),
    path('studentdisplay/<int:roll>/',views.studentdict2),
    # path('usertemplate/', views.usertemplate),


    path("homenew/123/dgfdtgdhg/fgghfg", views.homenew, name="home"),
    path("studentsnew/", views.student_listnew, name="students"),
    path("aboutnew/", views.aboutnew, name="about"),
   

    path('studentroll/<int:roll>/', views.studentdict),
    path('userdetails/<int:roll>/',views.userdetails),

    path("divide/", views.divide),
    path("multiple/", views.calculate),
 
    path('newstudent/', views.studentnew),
    path('studenttwo/', views.studenttwo),


    path('home3/', views.home3),

    path('wednesday/', views.wednesday),
    path('adminpage/', views.adminpage),
    path('wednes/', views.wednes),

    path('formnew/',views.student_form),

    path('form23/', views.form23),

    path('addstudent/', views.studentadd),

    path('djangoform/', views.djangoform),

    path('register/', views.registration),

    path('studentform/', views.studentform),

    path('examform/', views.examform),

    path('examreg/', views.examreg),


    path('newform/', views.newform),

    path('cars/', views.car_list, name='car_list'),

    path('cars/add/', views.car_create, name='car_create'),

    path('cars/details/<int:id>/', views.car_detail, name='car_detail'),

    path('cars/edit/<int:id>/', views.car_update, name='car_update'),

    path('cars/delete/<int:id>/', views.car_delete, name='car_delete'),

    path('studs/', views.stud_list, name='stud_list'),
    path('studs/add/', views.stud_create, name='stud_create'),
    path('studs/details/<int:id>/', views.stud_detail, name='stud_detail'),
    path('studs/edit/<int:id>/', views.stud_update, name='stud_update'),
    path('studs/delete/<int:id>/', views.stud_delete, name='stud_delete'),

    path('cloths/', views.cloth_list, name='cloth_list'),
    path('cloths/add/', views.cloth_add, name="cloth_add"),
    path('cloths/details/<int:id>/', views.cloth_view, name="cloth_details"),
    path('cloths/update/<int:id>/', views.cloth_update, name="cloth_update"),
    path('cloths/delete/<int:id>/', views.cloth_delete, name="cloth_delete"),





    path('clothes/', views.clothes_list, name="clothes_list"),
    path('clothes/add/', views.clothes_add, name="clothes_add"),
    path('clothes/detail/<int:id>/', views.clothes_details, name="clothes_details"),
    path('clothes/update/<int:id>/', views.clothes_update, name="clothes_update"),
    path('clothes/deleye/<int:id>/', views.clothes_delete, name="clothes_delete"),


    path('setcookie/', views.setcookie, name='setcookie'),
    path('getcookie/', views.getcookie, name='getcookie'),
    path('deletecookie/', views.deletecookie, name='deletecookie'),

    path('setsession/', views.setsession, name='setsession'),
    path('getsession/', views.getsession, name='getsession'),
    path('deletesession/', views.deletesession, name='deletesession'),
    path('clearsession/', views.clearsession, name='clearsession'),

    path('createuser/',views.createuser, name='createuser' ),
    path('alluser/',views.showusers, name='alluser' ), 
    path('updateuser/',views.updateuser, name='updateuser' ),
    path('deleteuser/',views.deleteuser, name='deleteuser' ),

   

    path('dashboard/', views.dashboard, name='dashboard'),


]
   
