from datetime import datetime
from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', 'date_birth', 'location', 'bio', 'photo')
        photo = forms.ImageField()
        widgets = {
            'bio': forms.Textarea(
                attrs={'cols': 50}
            ),
            'date_birth': forms.SelectDateWidget(
                years=[year for year in range(1920, datetime.now().year + 1)]
            ),
        }
