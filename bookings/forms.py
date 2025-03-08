from django import forms
from .models import Booking, Activity

#Booking form
class BookingForm(forms.ModelForm):
    activity = forms.ModelChoiceField(
        queryset=Activity.objects.filter(availability_status=True),  # Only available activities
        empty_label="Select an Activity",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Booking
        fields = ["user", "activity", "date", "time", "duration", "status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "duration": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

#Activity Form
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'availability_status']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),  # Prevent name editing
            'description': forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            'availability_status': forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }