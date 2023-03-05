from django.forms import ModelForm
from .models import Feeding
from datetime import date

class FeedingForm(ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']

