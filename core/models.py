from django.db import models
from django.utils import timezone
from datetime import date

########## Model TextChoice ##########
class AgamaChoices(models.TextChoices):
    ISLAM = 'islam', 'Islam'
    KRISTEN_PROTESTAN = 'kristen_protestan', 'Kristen Protestan'
    KATOLIK = 'katolik', 'Katolik'
    HINDU = 'hindu', 'Hindu'
    BUDDHA = 'buddha', 'Buddha'
    KONGHUCU = 'konghucu', 'Konghucu'
    KEPERCAYAAN_LAIN = 'kepercayaan_lain', 'Kepercayaan Lain'
    TIDAK_DIISI = '', '-'

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
    TIDAK_DIISI = '', '-'

class PekerjaanChoices(models.TextChoices):
    BELUM_KERJA = 'belum_kerja', 'Belum Bekerja'
    PELAJAR_MAHASISWA = 'pelajar_mahasiswa', 'Pelajar/Mahasiswa'
    IBU_RUMAH_TANGGA = 'ibu_rumah_tangga', 'Mengurus Rumah Tangga'
    PENSIUNAN = 'pensiunan', 'Pensiunan'
    PNS = 'pns', 'PNS'
    TNI_POLRI = 'tni_polri', 'TNI/Polri'
    KARYAWAN_SWASTA = 'karyawan_swasta', 'Karyawan Swasta'
    KARYAWAN_BUMN = 'karyawan_bumn', 'Karyawan BUMN/BUMD'
    PENGUSAHA = 'pengusaha', 'Pengusaha'
    LAINNYA = 'lainnya', 'Lainnya'
    TIDAK_DIISI = '', '-'

class StatusPernikahanChoices(models.TextChoices):
    BELUM_NIKAH = 'belum_nikah', 'Belum Nikah'
    NIKAH = 'nikah', 'Nikah'
    CERAI_HIDUP = 'cerai_hidup', 'Cerai Hidup'
    CERAI_MATI = 'cerai_mati', 'Cerai Mati'
    LAINNYA = 'lainnya', 'Lainnya'
    TIDAK_DIISI = '', '-'

class JenisKelaminChoices(models.TextChoices):
    LAKI_LAKI = 'L', 'Laki-laki'
    PEREMPUAN = 'P', 'Perempuan'
    TIDAK_DIISI = '', '-'

class StatusPerokokChoices(models.TextChoices):
    MEROKOK = 'merokok', 'Merokok'
    TIDAK_MEROKOK = 'tidak_merokok', 'Tidak Merokok'
    TIDAK_DIISI = '', '-'

class GolonganDarahChoices(models.TextChoices):
    O = 'o', 'O'
    A = 'a', 'A'
    B = 'b', 'B'
    AB = 'ab', 'AB'
    TIDAK_DIISI = '', '-'

class StatusPasienChoices(models.TextChoices):
    AKTIF = 'aktif', 'Aktif'
    NONAKTIF = 'nonaktif', 'Tidak Aktif'

class StatusRegistrasiChoices(models.TextChoices):
    MENUNGGU = 'menunggu', 'Menunggu Konsultasi'
    # DIPERIKSA = 'diperiksa', 'Diperiksa'
    SELESAI = 'selesai', 'Selesai Konsultasi'
    BATAL = 'batal', 'Dibatalkan'

class StatusKesadaranChoices(models.TextChoices):
    COMPOS_MENTIS = 'CM', 'Compos Mentis'
    APATIS = 'AP', 'Apatis'
    SOMNOLEN = 'SL', 'Somnolen'
    SOPOR = 'SP', 'Sopor'
    COMA = 'C', 'Coma'

########## Model Master Data Wajib ##########
class ICD10(models.Model): # Kode Diagnosa
    kode = models.CharField(max_length=10, unique=True)
    deskripsi = models.CharField(max_length=255)
    bab = models.CharField(max_length=100, blank=True, null=True)  # Contoh: "Penyakit Infeksi dan Parasit"

    def __str__(self):
        return f"{self.kode} - {self.deskripsi[:50]}"

    class Meta:
        verbose_name_plural = 'Master Data ICD-10'
        unique_together = ('bab', 'kode', 'deskripsi')

class Penyakit(models.Model): # Jenis Penyakit untuk Riwayat Penyakit
    jenis = models.CharField()
    deskripsi = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.jenis} - {self.deskripsi[:50]}"

    class Meta:
        verbose_name_plural = 'Master Data Jenis Penyakit'

class Alergi(models.Model): # Jenis Alergi untuk Riwayat Alergi
    jenis = models.CharField()
    deskripsi = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.jenis} - {self.deskripsi[:50]}"

    class Meta:
        verbose_name_plural = 'Master Data Jenis Alergi'


########## Model Master Data Tambahaan ##########
class Obat(models.Model):
    class JenisObat(models.TextChoices):
        TABLET = 'tablet', 'Tablet'
        KAPSUL = 'kapsul', 'Kapsul'
        SIRUP = 'sirup', 'Sirup'
        SALEP = 'salep', 'Salep'
        INJEKSI = 'injeksi', 'Injeksi'
        TETES = 'tetes', 'Tetes'
        SUPPOSITORIA = 'suppositoria', 'Suppositoria'
        LAINNYA = 'lainnya', 'Lainnya'

    class SatuanDosis(models.TextChoices):
        G = 'g', 'Gram'
        MG = 'mg', 'Miligram'
        ML = 'ml', 'Mililiter'
        IU = 'IU', 'IU'
        TABLET = 'tablet', 'Tablet'
        KAPSUL = 'kapsul', 'Kapsul'
        UNIT = 'unit', 'Unit'
        CC = 'cc', 'cc'
        AMPUL = 'ampul', 'Ampul'
        TETES = 'tetes', 'Tetes'

    nama = models.CharField(max_length=255)
    bentuk = models.CharField(max_length=50, choices=JenisObat.choices, default=JenisObat.TABLET)
    dosis_nilai = models.PositiveIntegerField(default=1, help_text="Contoh: 500, 5, dll")
    dosis_satuan = models.CharField(max_length=20, choices=SatuanDosis.choices)
    keterangan = models.TextField(blank=True, null=True, help_text="Contoh: Aturan pakai, efek samping, dll")
    # harga = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.nama} ({self.dosis_nilai} {self.dosis_satuan})"

    class Meta:
        verbose_name_plural = 'Master Data Obat'
        ordering = ['nama']

class Vaksin(models.Model):
    nama = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Master Data Vaksin'

class Tindakan(models.Model):
    kode = models.CharField(max_length=20, blank=True, null=True)
    kategori = models.CharField(max_length=100, blank=True, null=True)
    nama = models.CharField(max_length=255)
    # harga = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Master Data Tindakan'

########## Model Utama ##########
# === PASIEN ===
class Pasien(models.Model): # Diisi oleh Admisi/Resepsionis, Digunakan hanya untuk menambahkan pasien baru dan membuat registrasi pemeriksaan.
    # --- Data Identitas Wajib (Sesuai PMK) ---
    no_rm = models.CharField(max_length=20, unique=True) # Wajib diisi dan unik (Manual/Auto Generate nanti ditentukan)
    nama_lengkap = models.CharField(max_length=100) # Wajib diisi
    nik = models.CharField(max_length=16, unique=True) # Wajib diisi dan unik
    # --- Data Sosial Wajib tapi Opsional (Sesuai PMK) ---
    agama = models.CharField(max_length=30, choices=AgamaChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    pendidikan = models.CharField(max_length=30, choices=PendidikanChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    pekerjaan = models.CharField(max_length=30, choices=PekerjaanChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    status_pernikahan = models.CharField(max_length=30, choices=StatusPernikahanChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    # --- Tambahan Data Identitas --- 
    nomor_hp = models.CharField(max_length=14, blank=True, null=True) # Tidak Wajib diisi
    alamat = models.CharField(max_length=255, blank=True, null=True) # Tidak Wajib diisi
    tanggal_lahir = models.DateField() # Wajib diisi (Untuk Generate Umur juga)
    jenis_kelamin = models.CharField(max_length=10, choices=JenisKelaminChoices.choices) # Wajib diisi
    status = models.CharField(max_length=10, choices=StatusPasienChoices.choices, default=StatusPasienChoices.AKTIF) # Wajib diisi
    # --- Tambahan Data Kesehatan --- 
    status_merokok = models.CharField(max_length=20 , choices=StatusPerokokChoices.choices, blank=True, null=True) # Tidak Wajib diisi
    golongan_darah = models.CharField(max_length=10, choices=GolonganDarahChoices.choices, blank=True, null=True) # Tidak Wajib diisi

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_lengkap}"
    
    @property
    def umur(self):
        today = date.today()
        born = self.tanggal_lahir

        tahun = today.year - born.year
        bulan = today.month - born.month
        hari = today.day - born.day

        if hari < 0:
            bulan -= 1
            hari += (date(today.year, today.month, 1) - date(today.year, today.month - 1, 1)).days

        if bulan < 0:
            tahun -= 1
            bulan += 12

        return f"{tahun} tahun, {bulan} bulan, {hari} hari"
    
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

    # --- Data Umum --- 
    # pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='kunjungan')

    # --- Subjective / Anamnesis ---
    keluhan_utama = models.CharField(max_length=255)  # Wajib diisi
    riwayat_penyakit = models.ForeignKey(Penyakit, on_delete=models.SET_NULL, null=True, blank=True) # Tidak Wajib diisi
    catatan_riwayat_penyakit = models.CharField(max_length=255, blank=True) # Tidak Wajib diisi
    riwayat_alergi = models.ForeignKey(Alergi, on_delete=models.SET_NULL, null=True, blank=True) # Tidak Wajib diisi
    catatan_riwayat_alergi = models.CharField(max_length=255, blank=True) # Tidak Wajib diisi
    
    # --- Objective ---
    # -- Status Kesadaran -- 
    status_kesadaran = models.CharField(max_length=20, choices=StatusKesadaranChoices.choices, default=StatusKesadaranChoices.COMPOS_MENTIS) # Wajib diisi
    # -- Tanda-tanda Vital -- (dalam view ditambahkan tanda-tanda vital pada kunjungan sebelumnya)
    suhu_tubuh = models.PositiveIntegerField(blank=True, null=True)           # Format: °C
    sistole = models.PositiveIntegerField(blank=True, null=True)              # Format: mmHg
    diastole = models.PositiveIntegerField(blank=True, null=True)             # Format: mmHg
    nadi = models.PositiveIntegerField(blank=True, null=True)                 # Format: x/menit
    frekuensi_pernafasan = models.PositiveIntegerField(blank=True, null=True) # Format: x/menit
    tinggi_badan = models.PositiveIntegerField(blank=True, null=True)         # Format: cm
    berat_badan = models.PositiveIntegerField(blank=True, null=True)          # Format: kg

    # --- Assesment ---
    kode_diagnosis = models.ForeignKey(ICD10, on_delete=models.CASCADE, blank=False, null=False) # Wajib diisi
    catatan_diagnosis = models.CharField(max_length=255) # Wajib diisi

    # --- Plan --- (Jika dibutuhkan aja)
    # Obat, Layanan, TIndakan, dan Vaksin dikelola lewat RekamMedisObat, RekamMedisLayanan, RekamMedisTindakan, dan RekamMedisVaksin

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registrasi.pasien.nama_lengkap} - {self.created_at.date()}"

    class Meta:
        verbose_name_plural = 'Rekam Medis'
        ordering = ['-created_at']

# === RELASI MANY TO MANY REKAM MEDIS ===
class RekamMedisObat(models.Model):
    rekam_medis = models.ForeignKey(
        'RekamMedis',
        on_delete=models.CASCADE,
        related_name='obat_diberikan'
    )
    obat = models.ForeignKey(
        'Obat',
        on_delete=models.PROTECT,
        help_text="Obat yang diberikan kepada pasien"
    )
    jumlah = models.PositiveIntegerField(
        default=1,
        help_text="Jumlah unit yang diberikan (tidak boleh nol)"
    )
    catatan = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Catatan tambahan seperti cara minum, waktu, dll"
    )

    def __str__(self):
        return f"{self.obat.nama} x {self.jumlah} untuk {self.rekam_medis.registrasi.pasien.nama_lengkap}"

    class Meta:
        verbose_name = 'Obat dalam Rekam Medis'
        verbose_name_plural = 'Tambahkan Obat'
        ordering = ['rekam_medis', 'obat']

class RekamMedisTindakan(models.Model):
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE, related_name='tindakan_diberikan')
    tindakan = models.ForeignKey(Tindakan, on_delete=models.PROTECT)
    catatan = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tindakan.nama} untuk {self.rekam_medis.registrasi.pasien.nama_lengkap}"
    
    class Meta:
        verbose_name = 'Tindakan dalam Rekam Medis'
        verbose_name_plural = 'Tambahkan Tindakan'

class RekamMedisVaksin(models.Model):
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE, related_name='vaksin_diberikan')
    vaksin = models.ForeignKey(Vaksin, on_delete=models.PROTECT)
    catatan = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.vaksin.nama} untuk {self.rekam_medis.registrasi.pasien.nama_lengkap}"

    class Meta:
        verbose_name = 'Vaksin dalam Rekam Medis'
        verbose_name_plural = 'Tambahkan Vaksin'