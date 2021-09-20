from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ALL_FIELDS
from .models import Member

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('username','password1','password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user