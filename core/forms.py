from django import forms
from .models import *

class PasienForm(forms.ModelForm):
    class Meta:
        model = Pasien
        fields = '__all__'

        # fields = [
        #     'jenis_pasien', 'no_asuransi', 'nama_lengkap', 'no_rm', 'nik',
        #     'tanggal_lahir', 'jenis_kelamin', 'status', 'nomor_hp', 'alamat',
        #     'agama', 'pendidikan', 'pekerjaan', 'status_pernikahan',
        #     'status_merokok', 'golongan_darah'
        # ]

class RekamMedisForm(forms.ModelForm):
    class Meta:
        model = RekamMedis
        fields = '__all__'
        exclude = ['registrasi']