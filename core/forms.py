from django.forms import ModelForm

from .models import Profile, Theme

class ProfileForm(ModelForm):
    class Meta:
        model = Profile

        fields = ['first_name', 'last_name', 'email']


class ThemeForm(ModelForm):
    class Meta:
        model = Theme

        fields = ['theme_choice']