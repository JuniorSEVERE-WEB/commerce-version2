from django import forms 
from .models import Listing
from django.core.validators import URLValidator

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]


        def clean_image_url(self):
            url = self.cleaned_data.get('image_url')
            if url and not url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError("Please enter a valid image URL (PNG, JPG, GIF)")
            return url