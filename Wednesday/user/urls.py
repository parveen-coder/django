
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('home11/',views.user11),
    path('html/',views.htmlres),
    path('json/',views.jsonres),
    path('userdetail/',views.userdetails),
    path('user1/',views.user1),
    path('user8/<str:name>/<int:id>',views.user2,),
    path('user6/<slug:name>/',views.user6),
    path('user7/<uuid:name>/',views.user7),
    path('user9/<path:name>/',views.user97),

    re_path(r'^user23/(?P<id>[A-Za-z]{3})/(?P<name>[0-9]+)/$', views.user34),



    path('mylist/',views.userlist),
    path('mydict/',views.userdict),

    path('listdict/',views.listdict),






    re_path(r'^user3/(?P<id>[0-9]{3}/$)', views.user2),

    path('list/',views.mylist),
    path('set/',views.myset),
    path('tuple/',views.mytuple),
    path('dict/',views.mydict),



    path('listdisplay/',views.list1),
    path('setdisplay/',views.set1),
    path('tupledisplay/edwsdw/desdced/wewdff/',views.tuple1,name="tuple"),
    path('dictdisplay/',views.dict1),

    path('list2/hello/welcome/user',views.list2,name="first"),
    path('list3/',views.list3),
    path('dict123/', views.dictlist),
    path('user/',views.user1),
    re_path(r'^username/(?P<id>[0-9]+)/(?P<name>[A-Za-z]+)/$', views.user2),

    path('username1/<slug:id>/',views.user90),
    path('username2/<uuid:id>/',views.user91),
    path('username3/<path:id>/',views.user92),
    path('monday1/<int:id>',views.monday), 
    # [0-9]
    re_path(r'^monday5/(?P<id>[0-9]{2})/(?P<name>[A-Za-z]+)/$', views.monday),


#    re_path(r'^monday8/(?P<id>[]{})/$')

    path('monday2/<slug:id>',views.monday),
    # [0-9a-zA-z_-]
    path('monday3/<uuid:id>',views.monday),
    #  [0-9a-f] -> 8-4-4-4-12
    path('monday4/<path:id>', views.monday),
    # [0-9a-zA-Z-_s/.ext]
]
