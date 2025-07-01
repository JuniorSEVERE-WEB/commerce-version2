from django import forms 
from .models import Listing, Bid
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
        
# kod s abel anpil
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid 
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={
                "step": "0.01",
                "min": "0.01",
                "class": "form-control"
            })
        }
