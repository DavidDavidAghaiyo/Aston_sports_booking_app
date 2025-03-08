from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking, Activity
from .forms import BookingForm, ActivityForm

#Homepage
def home(request):
  return render(request, 'bookings/home.html')

#Booking List View
class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

#Booking Create View
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

#Booking Create View (Update/Edit)
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

#Booking Confirm Delete View
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')


# View Activity List
@login_required
def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'users/activity_list.html', {'activities': activities})

# Add Activity View
@login_required
def add_activity(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity added successfully!")
            return redirect('activity_list')
    else:
        form = ActivityForm()
    
    return render(request, 'users/add_activity.html', {'form': form})

#Edit Activity View
@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated successfully!")
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity)

    return render(request, 'users/edit_activity.html', {'form': form, 'activity': activity})

# Delete Activity View
@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if request.method == "POST":
        activity.delete()
        messages.success(request, "Activity deleted successfully!")
        return redirect('activity_list')

    return render(request, 'users/delete_activity.html', {'activity': activity})