from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('groupItems', views.getDataGroup),
    path('categories', views.getCategories),
    path('signup', views.signup),
    path('login', views.login),
    path('validatetoken', views.test_token),
    path('addUserFav', views.addUserFav),
    path('getUserFav', views.getUserFav),
    path('deleteUserFav', views.deleteUserFav),
    path('updateUserFav', views.updateUserFav),
    path("products/add/", views.addProduct, name="add_product"),
    path("products/update/<int:pk>/", views.updateProduct, name="update_product"),
    path("products/delete/<int:pk>/", views.deleteProduct, name="delete_product"),
]