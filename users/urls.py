from django.urls import path
from . import views
from bookings.views import home
from .views import register, user_login, user_logout, admin_dashboard, export_users_csv, export_bookings_csv, export_payments_csv, export_users_excel, user_list, edit_user, add_user, view_user, delete_user

urlpatterns = [
    path('', home, name='home'),  
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/add', views.add_user, name='add_user'),
    path('users/<int:user_id>/', views.view_user, name='view_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('export/users/csv/', views.export_users_csv, name='export_users_csv'),
    path('export/bookings/csv/', views.export_bookings_csv, name='export_bookings_csv'),
    path('export/payments/csv/', views.export_payments_csv, name='export_payments_csv'),
    path('export/users/excel/',views.export_users_excel, name='export_users_excel'),
    
    
]
