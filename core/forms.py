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

class ResepObatForm(forms.ModelForm):
    class Meta:
        model = ResepObat
        fields = '__all__'

        # fields = [
        #     'nama_obat', 'jumlah', 'bentuk', 'bentuk_lainnya',
        #     'dosis_nilai', 'dosis_satuan', 'dosis_satuan_lainnya',
        #     'frekuensi', 'frekuensi_lainnya',
        #     'aturan_pakai', 'aturan_pakai_lainnya',
        # ]

def clean(self):
    cleaned_data = super().clean() # type: ignore

    bentuk = cleaned_data.get("bentuk")
    bentuk_lainnya = cleaned_data.get("bentuk_lainnya")
    dosis_satuan = cleaned_data.get("dosis_satuan")
    dosis_satuan_lainnya = cleaned_data.get("dosis_satuan_lainnya")
    frekuensi = cleaned_data.get("frekuensi")
    frekuensi_lainnya = cleaned_data.get("frekuensi_lainnya")
    aturan_pakai = cleaned_data.get("aturan_pakai")
    aturan_pakai_lainnya = cleaned_data.get("aturan_pakai_lainnya")

    if bentuk == "lainnya" and not bentuk_lainnya:
        self.add_error("bentuk_lainnya", "Harap isi bentuk obat lainnya.")

    if dosis_satuan == "lainnya" and not dosis_satuan_lainnya:
        self.add_error("dosis_satuan_lainnya", "Harap isi satuan dosis lainnya.")

    if frekuensi == "lainnya" and not frekuensi_lainnya:
        self.add_error("frekuensi_lainnya", "Harap isi frekuensi lainnya.")

    if aturan_pakai == "lainnya" and not aturan_pakai_lainnya:
        self.add_error("aturan_pakai_lainnya", "Harap isi aturan pakai lainnya.")