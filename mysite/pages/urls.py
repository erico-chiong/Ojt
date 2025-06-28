from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_update, name='item_update'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('search/', views.search, name='search'),
    path('to_form/', views.to_form, name='to_form'),
    path('so_form/', views.so_form, name='so_form'),
    path('cl_form/', views.cl_form, name='cl_form'),
    path('moau_form/', views.moau_form, name='moau_form'),
    path('item_form/', views.item_form, name='item_form'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reports/', views.reports, name='reports'),
    path('user-documents/', views.user_document_list, name='user_document_list'),
    path('user-notification/', views.user_notification, name='user_notification'),
]
