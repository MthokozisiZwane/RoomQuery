from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'user_type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email','user_type')

class PropertySearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
    property_type = forms.ChoiceField(choices=[('all', 'All'), ('house', 'House'), ('room','Room'),('garage','Garage'), ('apartment', 'Apartment')], required=False)
    min_bedrooms = forms.IntegerField(label='Min Bedrooms', required=False)
    max_bedrooms = forms.IntegerField(label='Max Bedrooms', required=False)
    min_price = forms.DecimalField(label='Min Price', max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(label='Max Price', max_digits=10, decimal_places=2, required=False)
