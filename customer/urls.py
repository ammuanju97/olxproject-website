from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import (
    CreatePost, ProductDisplay, ProfileDisplay, EditProduct,
     ViewMore, DeleteProduct, Userhome
                )
urlpatterns = [
    path('userhome/', Userhome.as_view(), name='userhome'),
    path('password/', auth_views.PasswordChangeView.as_view
    (template_name = 'registration/change-password.html', success_url = '/userhome'),
    name='password'),
    path('edit-profile/', views.editprofile, name = 'edit_profile'),
    path('add-details/', views.adddetail,name='adddetails'),
    path('viewprofile/', ProfileDisplay.as_view(), name='viewprofile'),
    path('createpost/', CreatePost.as_view(),name='createpost'),
    path('viewpost/', ProductDisplay.as_view(), name='viewpost'),
    path('editpost/<int:pk>/', EditProduct.as_view(),name='editpost'),
    path('deletepost/<int:pk>/',DeleteProduct.as_view(),name='deletepost'),
    path('viewmore/<int:id>/', ViewMore.as_view(), name='viewmore'),
    
    ]
