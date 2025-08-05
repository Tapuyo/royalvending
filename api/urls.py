from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('categories', views.getCategories),
    path('signup', views.signup),
    path('login', views.login),
    path('validatetoken', views.test_token),
    path('addUserFav', views.addUserFav),
    path('getUserFav', views.getUserFav),
    path('deleteUserFav', views.deleteUserFav),
    path('updateUserFav', views.updateUserFav),
]