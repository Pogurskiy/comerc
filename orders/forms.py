from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash on Delivery'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'postal_code', 'payment_method', 'notes',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
