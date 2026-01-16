from django import forms
from .models import Purchase

class PurchaseForm(forms.ModelForm):
    """Checkout form for a single game purchase."""
    class Meta:
        model = Purchase
        fields = ("full_name", "email")
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
