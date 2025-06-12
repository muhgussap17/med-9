from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date
from myproject.middleware.current_user import get_current_user

User = get_user_model()

########## Model TextChoice ##########
# === Untuk Identitas Pasien ===
class JenisPasienChoices(models.TextChoices):
    UMUM = 'umum', 'Umum',
    BPJS = 'bpjs', 'BPJS',
    ASURANSI_LAIN = 'asuransi_lain', 'Asuransi Lain'

class JenisKelaminChoices(models.TextChoices):
    LAKI_LAKI = 'l', 'Laki-laki'
    PEREMPUAN = 'p', 'Perempuan'

class AgamaChoices(models.TextChoices):
    ISLAM = 'islam', 'Islam'
    KRISTEN_PROTESTAN = 'kristen_protestan', 'Kristen Protestan'
    KATOLIK = 'katolik', 'Katolik'
    HINDU = 'hindu', 'Hindu'
    BUDDHA = 'buddha', 'Buddha'
    KONGHUCU = 'konghucu', 'Konghucu'
    KEPERCAYAAN_LAIN = 'kepercayaan_lain', 'Kepercayaan Lain'

class PendidikanChoices(models.TextChoices):
    BELUM_SEKOLAH = 'belum_sekolah', 'Belum Sekolah'
    SD = 'sd', 'SD/Sederajat'
    SMP = 'smp', 'SMP/Sederajat'
    SMA = 'sma', 'SMA/Sederajat'
    D3 = 'd3', 'Diploma 3 (D3)'
    S1 = 's1', 'Sarjana (S1)'
    S2 = 's2', 'Magister (S2)'
    S3 = 's3', 'Doktor (S3)'
    LAINNYA = 'lainnya', 'Lainnya'

class PekerjaanChoices(models.TextChoices):
    BELUM_KERJA = 'belum_kerja', 'Belum Bekerja'
    PELAJAR_MAHASISWA = 'pelajar_mahasiswa', 'Pelajar/Mahasiswa'
    IBU_RUMAH_TANGGA = 'ibu_rumah_tangga', 'Mengurus Rumah Tangga'
    GURU = 'guru', 'Guru'
    PENSIUNAN = 'pensiunan', 'Pensiunan'
    PNS = 'pns', 'PNS'
    TNI_POLRI = 'tni_polri', 'TNI/Polri'
    KARYAWAN_SWASTA = 'karyawan_swasta', 'Karyawan Swasta'
    KARYAWAN_BUMN = 'karyawan_bumn', 'Karyawan BUMN/BUMD'
    PENGUSAHA = 'pengusaha', 'Pengusaha'
    LAINNYA = 'lainnya', 'Lainnya'

class StatusPernikahanChoices(models.TextChoices):
    BELUM_NIKAH = 'belum_nikah', 'Belum Nikah'
    NIKAH = 'nikah', 'Nikah'
    CERAI_HIDUP = 'cerai_hidup', 'Cerai Hidup'
    CERAI_MATI = 'cerai_mati', 'Cerai Mati'

class GolonganDarahChoices(models.TextChoices):
    O = 'o', 'O'
    A = 'a', 'A'
    B = 'b', 'B'
    AB = 'ab', 'AB'

class StatusPerokokChoices(models.TextChoices):
    MEROKOK = 'merokok', 'Merokok'
    TIDAK_MEROKOK = 'tidak_merokok', 'Tidak Merokok'

class StatusPasienChoices(models.TextChoices):
    AKTIF = 'aktif', 'Aktif'
    NONAKTIF = 'nonaktif', 'Tidak Aktif'

# ==== Untuk Registrasi ===
class StatusRegistrasiChoices(models.TextChoices):
    MENUNGGU = 'menunggu', 'Menunggu Konsultasi'
    # DIPERIKSA = 'diperiksa', 'Diperiksa'
    SELESAI = 'selesai', 'Selesai Konsultasi'
    BATAL = 'batal', 'Dibatalkan'

# === Untuk Rekam Medis ===
class StatusKesadaranChoices(models.TextChoices):
    COMPOS_MENTIS = 'cm', 'Compos Mentis'
    APATIS = 'ap', 'Apatis'
    SOMNOLEN = 'sl', 'Somnolen'
    SOPOR = 'sp', 'Sopor'
    COMA = 'c', 'Coma'

class PrognosisChoices(models.TextChoices):
    SANAM = 'sanam', 'Sanam',
    BONAM = 'bonam', 'Bonam',
    MALAM = 'malam', 'Malam',
    DUBIA = 'dubia', 'Dubia'

class StatusPulangChoices(models.TextChoices):
    BEROBAT_JALAN = 'berobat_jalan', 'Berobat Jalan',
    SEHAT = 'sehat', 'Sehat',
    RUJUK = 'rujuk', 'Rujuk',

########## Model Master Data ##########
class ICD10(models.Model): # Kode Diagnosa
    kode = models.CharField(max_length=10, unique=True)
    deskripsi = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.kode} - {self.deskripsi[:50]}"

    class Meta:
        verbose_name_plural = 'Master Data ICD-10'
        unique_together = ('kode', 'deskripsi')


########## Model Utama ##########
# === PASIEN ===
def generate_no_rm():
    last_rm = Pasien.objects.order_by('-no_rm').first()
    if last_rm and last_rm.no_rm:
        last_number = int(last_rm.no_rm.replace('RM', ''))
        return f'RM{last_number + 1:06d}'
    return 'RM000001'

class Pasien(models.Model): # Diisi oleh Admisi/Resepsionis, Digunakan hanya untuk menambahkan pasien baru dan membuat registrasi pemeriksaan.
    # --- Data Jenis Pasien ---
    jenis_pasien = models.CharField(max_length=30, choices=JenisPasienChoices.choices, default=JenisPasienChoices.UMUM, blank=True, null=True) # Tidak Wajib diisi
    no_asuransi = models.CharField(max_length=30, unique=True, blank=True, null=True) # Tidak Wajib diisi dan unik jika Umum
    # --- Data Identitas Wajib (Sesuai PMK) ---
    no_rm = models.CharField(max_length=20, unique=True, blank=True, null=True) # Wajib diisi* dan unik (Manual/Auto Generate nanti ditentukan)
    nama_lengkap = models.CharField(max_length=100, blank=True, null=True) # Wajib diisi*
    nik = models.CharField(max_length=16, unique=True, blank=True, null=True) # Wajib diisi* dan unik
    # --- Data Sosial Wajib tapi Opsional (Sesuai PMK) ---
    agama = models.CharField(max_length=30, choices=AgamaChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    pendidikan = models.CharField(max_length=30, choices=PendidikanChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    pekerjaan = models.CharField(max_length=30, choices=PekerjaanChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    status_pernikahan = models.CharField(max_length=30, choices=StatusPernikahanChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    # --- Tambahan Data Identitas --- 
    status = models.CharField(max_length=10, choices=StatusPasienChoices.choices, default=StatusPasienChoices.AKTIF, blank=True, null=True) # Wajib diisi*
    tanggal_lahir = models.DateField(blank=True, null=True) # Wajib diisi* (Untuk Generate Umur juga)
    jenis_kelamin = models.CharField(max_length=10, choices=JenisKelaminChoices.choices, blank=True, null=True) # Wajib diisi*
    nomor_hp = models.CharField(max_length=14, blank=True, null=True) # Tidak Wajib diisi
    alamat = models.CharField(max_length=255, blank=True, null=True) # Tidak Wajib diisi
    # --- Tambahan Data Keseha  
    status_merokok = models.CharField(max_length=20 , choices=StatusPerokokChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    golongan_darah = models.CharField(max_length=10, choices=GolonganDarahChoices.choices, blank=True, null=True) # Tidak Wajib diisi

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.no_rm:
            self.no_rm = generate_no_rm()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nama_lengkap}"
    
    @property # Fungsi generate Umur
    def umur(self):
        today = date.today()
        born = self.tanggal_lahir

        tahun = today.year - born.year # type: ignore
        bulan = today.month - born.month # type: ignore
        hari = today.day - born.day # type: ignore

        if hari < 0:
            bulan -= 1
            hari += (date(today.year, today.month, 1) - date(today.year, today.month - 1, 1)).days

        if bulan < 0:
            tahun -= 1
            bulan += 12

        return f"{tahun} tahun, {bulan} bulan, {hari} hari"
    
    @property
    def umur_tahun(self):
        today = date.today()
        born = self.tanggal_lahir
        tahun = today.year - born.year # type: ignore

        # Koreksi umur jika ulang tahun belum lewat tahun ini
        if (today.month, today.day) < (born.month, born.day): # type: ignore
            tahun -= 1

        return f"{tahun} tahun"
    
    class Meta:
        verbose_name_plural = 'Pasien'

# === REGISTRASI ===
class Registrasi(models.Model): # Digunakan oleh Admisi/Resepsionis untuk menambahkan registrasi pemeriksaan
    # --- Data Umum ---
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='registrasi')
    tanggal = models.DateField(auto_now_add=True)
    waktu = models.TimeField(auto_now_add=True)
    no_antrian = models.PositiveIntegerField(blank=True)  # tidak wajib diisi manual
    status = models.CharField(max_length=20, choices=StatusRegistrasiChoices.choices, default=StatusRegistrasiChoices.MENUNGGU)
    # di View tambahkan form Tanggal Lahir, No. RM, Jenis Kelamin, NIK dengan form kosong. Tapi ketika Pasien sudah ada dan dipilih form otomatis terisi. 

    def save(self, *args, **kwargs):
        if not self.no_antrian:
            # Ambil jumlah registrasi untuk hari ini
            today = timezone.localdate()
            jumlah_hari_ini = Registrasi.objects.filter(tanggal=today).count()
            self.no_antrian = jumlah_hari_ini + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.no_antrian} | {self.status} | {self.pasien.nama_lengkap} "
    
    class Meta:
        verbose_name_plural = 'Registrasi'
        ordering = ['-tanggal', 'no_antrian']

# === REKAM MEDIS ===
class RekamMedis(models.Model):
    # --- Relasi ke Register
    registrasi = models.ForeignKey(Registrasi, on_delete=models.CASCADE, related_name='rekam_medis')

    # --- Subjective / Anamnesis ---
    keluhan_utama = models.CharField(max_length=255, blank=True, null=True)  # Wajib diisi
    riwayat_penyakit = models.CharField(max_length=255, blank=True, null=True) # Tidak Wajib diisi
    riwayat_alergi = models.CharField(max_length=255, blank=True, null=True) # Tidak Wajib diisi
    
    # --- Objective ---
    # -- Status Kesadaran -- 
    status_kesadaran = models.CharField(max_length=20, choices=StatusKesadaranChoices.choices, default=StatusKesadaranChoices.COMPOS_MENTIS, blank=True, null=True) # Wajib diisi
    # -- Tanda-tanda Vital -- (dalam view ditambahkan tanda-tanda vital pada kunjungan sebelumnya)
    suhu_tubuh = models.PositiveIntegerField(blank=True, null=True)           # Format: °C
    sistole = models.PositiveIntegerField(blank=True, null=True)              # Format: mmHg
    diastole = models.PositiveIntegerField(blank=True, null=True)             # Format: mmHg
    nadi = models.PositiveIntegerField(blank=True, null=True)                 # Format: x/menit
    frekuensi_pernafasan = models.PositiveIntegerField(blank=True, null=True) # Format: x/menit
    tinggi_badan = models.PositiveIntegerField(blank=True, null=True)         # Format: cm
    berat_badan = models.PositiveIntegerField(blank=True, null=True)          # Format: kg

    # --- Assesment ---
    kode_diagnosis = models.ForeignKey(ICD10, on_delete=models.CASCADE, blank=True, null=True) # Wajib diisi
    diagnosis = models.CharField(max_length=255, blank=True, null=True) # Wajib diisi
    prognosis = models.CharField(max_length=10, choices=PrognosisChoices.choices, blank=True, null=True) # Wajib diisi

    # --- Plan --- (Jika dibutuhkan aja)
    medikamentosa = models.TextField(max_length=255, blank=True, null=True) # Tidak Wajib diisi
    non_medikamentosa = models.TextField(max_length=255, blank=True, null=True) # Tidak Wajib diisi
    status_pulang = models.CharField(max_length=20, choices=StatusPulangChoices.choices, blank=True, null=True) # Tidak Wajib diisi

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rekam_dibuat')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rekam_diubah')

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not self.pk:  # baru dibuat
            self.created_by = user
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.registrasi.pasien.nama_lengkap} - {self.created_at.date()}"

    class Meta:
        verbose_name_plural = 'Rekam Medis'
        ordering = ['-created_at']
