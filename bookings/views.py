import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking, Activity
from .forms import BookingForm, ActivityForm, UserBookingForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from datetime import time
from payments.models import Payment
from promotions.models import Promotion
from users.models import Membership, Review
from users.forms import ReviewForm
from django.utils import timezone


#Homepage
def home(request):
    reviews = Review.objects.all()  # Retrieve all reviews from the database

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')  # Redirect to the same page to clear the form
    else:
        form = ReviewForm()

    return render(request, 'bookings/home.html', {'form': form, 'reviews': reviews})

class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now().date()
        upcoming_bookings = Booking.objects.filter(date__gte=now).order_by('date', 'time')
        previous_bookings = Booking.objects.filter(date__lt=now).order_by('-date', '-time')

        context['upcoming_bookings'] = upcoming_bookings
        context['previous_bookings'] = previous_bookings
        context['discounted_prices'] = self.get_discounted_prices(upcoming_bookings) | self.get_discounted_prices(previous_bookings)
        return context

    def get_discounted_prices(self, bookings):
        discounted_prices = {}
        for booking in bookings:
            try:
                payment = booking.payments.first()
                if payment:
                    discounted_prices[booking.id] = payment.amount
                else:
                    discounted_prices[booking.id] = booking.get_total_price()  # Original price if no payment
            except AttributeError:
                discounted_prices[booking.id] = booking.get_total_price()  # Original price if no payments attribute
        return discounted_prices

#Booking Create View (Admin)
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')  

    def form_valid(self, form):
        response = super().form_valid(form)
        amount = self.object.activity.price
        Payment.objects.create(booking=self.object, amount=amount)
        return response

#Booking (Update/Edit)  View 
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

def booking_events(request):
    bookings = Booking.objects.all()
    status_colors = {
        "pending": "#ffc107",  # Yellow
        "confirmed": "#28a745",  # Green
        "cancelled": "#dc3545",  # Red
    }

    events = [
        {
            "title": f"{booking.activity.name}",
            "start": f"{booking.date}T{booking.time}",
            "end": f"{booking.date}T{booking.time}",
            "color": status_colors.get(booking.status, "#007bff"),  # Default Blue
        }
        for booking in bookings
    ]
    return JsonResponse(events, safe=False)

def calendar_view(request):
    bookings = Booking.objects.all()
    
    # Format bookings as events for FullCalendar.js
    events = []
    for booking in bookings:
        # Combine date and time into a single ISO 8601 datetime string
        start_datetime = f"{booking.date}T{booking.time}"  # e.g., "2025-03-10T14:30:00"
        
        events.append({
            "id": booking.id,
            "title": f"{booking.user.username} - {booking.activity.name}",  # Customize title
            "start": start_datetime,  # FullCalendar expects a combined date and time
            "duration": booking.duration,  # Optional: include duration if needed
            "color": "#28a745" if booking.status == "confirmed" else "#ff0000" if booking.status == "cancelled" else "#ffc107",  # Customize color based on status
        })

   

    return render(request, "users/calendar.html", {"events": json.dumps(events)})

@login_required
def user_booking_create(request):
    activities = Activity.objects.filter(availability_status=True)
    if request.method == "POST":
        form = UserBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = 'pending'
            promotion_code = form.cleaned_data.get('promotion_code')

            try:
                if promotion_code:
                    promotion = Promotion.objects.get(code=promotion_code, is_active=True)
                    request.session['promotion_id'] = promotion.id
                else:
                    request.session.pop('promotion_id', None)
                booking.save()

                # Email sending code removed

                return redirect('payment_review', booking_id=booking.id)

            except Promotion.DoesNotExist:
                messages.error(request, "Invalid promotion code.")
                return render(request, 'bookings/users_booking_form.html', {"form": form, 'activities': activities})

            except Exception as e:
                messages.error(request, f"Booking failed: {e}")
    else:
        form = UserBookingForm()

    return render(request, 'bookings/users_booking_form.html', {"form": form, 'activities': activities})


def check_availability(request):
    date = request.GET.get("date")
    activity_id = request.GET.get("activity")

    if date and activity_id:
        booked_slots = Booking.objects.filter(date=date, activity_id=activity_id).values_list("time", flat=True)

        # Define time slots (e.g., 8 AM - 8 PM, every hour)
        available_slots = [
            "08:00", "09:00", "10:00", "11:00", "12:00",
            "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"
        ]

        # Remove booked slots
        available_slots = [slot for slot in available_slots if slot not in booked_slots]

        return JsonResponse({"available_slots": available_slots})

    return JsonResponse({"error": "Invalid data"}, status=400)


@login_required
def user_dashboard(request):
    now = timezone.now().date()
    upcoming_bookings = Booking.objects.filter(user=request.user, date__gte=now).order_by('date', 'time')
    previous_bookings = Booking.objects.filter(user=request.user, date__lt=now).order_by('-date', '-time')
    user_membership = Membership.objects.filter(user=request.user).first()

    context = {
        'upcoming_bookings': upcoming_bookings,
        'previous_bookings': previous_bookings,
        'user_membership': user_membership,
    }
    return render(request, 'users/user_dashboard.html', context)
@login_required
def payment_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    activity = booking.activity
    total_price = activity.price  # Initial price

    promotion_id = request.session.get('promotion_id')  # Get promotion from session
    if promotion_id:
        promotion = get_object_or_404(Promotion, id=promotion_id)
        discount = promotion.discount_percentage / 100
        total_price = total_price * (1 - discount)  # Apply discount

    context = {
        'booking': booking,
        'activity': activity,
        'total_price': total_price,
    }
    return render(request, 'bookings/user_payment_review.html', context)

@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    activity = booking.activity
    total_price = booking.get_total_price()  # Get total price including duration

    promotion_id = request.session.get('promotion_id')  # Get promotion from session
    promotion = None  # Initialize promotion to None

    print(f"Total price before discount: {total_price}")  # Add this line

    if promotion_id:
        promotion = get_object_or_404(Promotion, id=promotion_id)
        discount = promotion.discount_percentage / 100
        total_price = total_price * (1 - discount)  # Apply discount

    print(f"Total price after discount: {total_price}")  # Add this line

    if request.method == "POST":
        messages.success(request, "Payment successful!")

        # Create Payment object with discounted price and promotion
        payment = Payment.objects.create(booking=booking, amount=total_price, promotion=promotion)
        print(f"Payment created: {payment}") # Debugging line

        # Update booking status
        booking.status = 'confirmed'
        booking.save()

        # Clear the promotion from the session
        if 'promotion_id' in request.session:
            del request.session['promotion_id']

        return redirect('user_dashboard')
    else:
        messages.error(request, "Invalid request.")
        return redirect('payment_review', booking_id=booking.id)
    


def about(request):
    return render(request, "bookings/about.html")

def activity_list_user(request):
    activities = Activity.objects.all()
    return render(request, 'bookings/activities.html', {'activities': activities})