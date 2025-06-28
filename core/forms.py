from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import *


class PasienForm(forms.ModelForm):
    class Meta:
        model = Pasien
        fields = '__all__'

class RekamMedisForm(forms.ModelForm):
    class Meta:
        model = RekamMedis
        fields = '__all__'
        exclude = ['registrasi']