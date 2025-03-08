from django.urls import path
from .views import BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView, activity_list, add_activity,edit_activity, delete_activity

urlpatterns = [
    path('', BookingListView.as_view(), name='booking_list'), 
    path('create/', BookingCreateView.as_view(), name='create_booking'),
    path('<int:pk>/edit/', BookingUpdateView.as_view(), name='edit_booking'),
    path('<int:pk>/delete/', BookingDeleteView.as_view(), name='delete_booking'),
    path('activities/', activity_list, name='activity_list'),
    path('activities/add/', add_activity, name='add_activity'),
    path('activities/<int:activity_id>/edit/', edit_activity, name='edit_activity'),
    path('activities/<int:activity_id>/delete/', delete_activity, name='delete_activity'),
]
