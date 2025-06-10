from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin import RelatedOnlyFieldListFilter
from .models import *
from django.urls import reverse

########## Admin untuk Rekam Medis dengan inlines ##########
@admin.register(RekamMedis)
class RekamMedisAdmin(admin.ModelAdmin):
    list_display = (
        'get_pasien', 'get_tanggal_registrasi',
        'keluhan_utama', 'kode_diagnosis', 'status_kesadaran', 'created_at',
    )
    list_filter = ['created_at']
    search_fields = ('registrasi__pasien__nama_lengkap', 'keluhan_utama', 'diagnosis')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('registrasi', 'kode_diagnosis')
    allowed_filters = ["registrasi__pasien__id__exact"]

    fieldsets = (
        ('📌 Informasi Umum', {
            'fields': ('registrasi',),
        }),
        ('🩺 Subjective / Anamnesis', {
            'fields': (
                'keluhan_utama', 'riwayat_penyakit',
                'riwayat_alergi',
            ),
        }),
        ('📊 Objective', {
            'fields': (
                'status_kesadaran', 'suhu_tubuh', 'sistole', 'diastole',
                'nadi', 'frekuensi_pernafasan', 'tinggi_badan', 'berat_badan',
            ),
        }),
        ('📋 Assessment', {
            'fields': ('kode_diagnosis', 'diagnosis'),
        }),
        ('🕓 Waktu', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_pasien(self, obj):
        return obj.registrasi.pasien.nama_lengkap
    get_pasien.short_description = 'Pasien' # type: ignore

    def get_tanggal_registrasi(self, obj):
        return obj.registrasi.tanggal
    get_tanggal_registrasi.short_description = 'Tgl Registrasi' # type: ignore

    # Logika untuk update status registrasi
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.registrasi.status != 'selesai':
            obj.registrasi.status = 'selesai'
            obj.registrasi.save()

# Admin untuk Registrasi
@admin.register(Registrasi)
class RegistrasiAdmin(admin.ModelAdmin):
    list_display = (
        'no_antrian', 'pasien_link', 'get_nik', 'get_jenis_kelamin',
        'tanggal', 'waktu', 'status_colored'
    )
    list_filter = ('tanggal', 'status')
    search_fields = ('pasien__nama_lengkap', 'pasien__nik', 'no_antrian', 'tanggal')
    autocomplete_fields = ['pasien']
    actions = ['tandai_menunggu', 'tandai_selesai', 'tandai_dibatalkan']
    ordering = ('-tanggal', '-waktu')
    readonly_fields = ('tanggal', 'waktu', 'no_antrian')

    fieldsets = (
        ('📋 Informasi Registrasi', {
            'fields': ['pasien'],
        }),
    )

    @admin.display(description="Pasien", ordering="pasien__nama_lengkap")
    def pasien_link(self, obj):
        url = f"/admin/core/pasien/{obj.pasien.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.pasien.nama_lengkap)

    @admin.display(description="NIK", ordering="pasien__nik")
    def get_nik(self, obj):
        return obj.pasien.nik

    @admin.display(description="Jenis Kelamin", ordering="pasien__jenis_kelamin")
    def get_jenis_kelamin(self, obj):
        return obj.pasien.get_jenis_kelamin_display()

    @admin.display(description="Status", ordering="status")
    def status_colored(self, obj):
        warna = {
            StatusRegistrasiChoices.MENUNGGU: 'orange',
            StatusRegistrasiChoices.SELESAI: 'green',
            StatusRegistrasiChoices.BATAL: 'red',
        }.get(obj.status, 'gray')
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            warna, obj.get_status_display()
        )

    @admin.action(description="Tandai sebagai Menunggu Konsultasi")
    def tandai_menunggu(self, request, queryset):
        updated = queryset.update(status=StatusRegistrasiChoices.MENUNGGU)
        self.message_user(request, f"{updated} registrasi ditandai sebagai 'Menunggu Konsultasi'.")

    @admin.action(description="Tandai sebagai Selesai Konsultasi")
    def tandai_selesai(self, request, queryset):
        updated = queryset.update(status=StatusRegistrasiChoices.SELESAI)
        self.message_user(request, f"{updated} registrasi ditandai sebagai 'Selesai Konsultasi'.")

    @admin.action(description="Tandai sebagai Dibatalkan")
    def tandai_dibatalkan(self, request, queryset):
        updated = queryset.update(status=StatusRegistrasiChoices.BATAL)
        self.message_user(request, f"{updated} registrasi berhasil dibatalkan.")

# Admin untuk Pasien
@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    list_display = (
        'no_rm', 'nama_lengkap', 'nik', 'jenis_kelamin',
        'tanggal_lahir', 'umur', 'status'
    )
    list_filter = ('status', 'jenis_kelamin', 'agama', 'pendidikan')
    search_fields = ('nama_lengkap', 'nik', 'no_rm')
    actions = ['nonaktifkan_pasien', 'aktifkan_pasien']
    readonly_fields = ('umur',)
    fieldsets = (
        ('Data Identitas Wajib', {
            'fields': ('no_rm', 'nama_lengkap', 'nik', 'tanggal_lahir', 'umur', 'jenis_kelamin', 'status')
        }),
        ('Data Sosial (Opsional)', {
            'fields': ('agama', 'pendidikan', 'pekerjaan', 'status_pernikahan')
        }),
        ('Kontak dan Alamat', {
            'fields': ('nomor_hp', 'alamat')
        }),
        ('Data Kesehatan (Opsional)', {
            'fields': ('status_merokok', 'golongan_darah')
        }),
    )
    ordering = ('-created_at',)

    @admin.action(description="Nonaktifkan Pasien Terpilih")
    def nonaktifkan_pasien(self, request, queryset):
        updated = queryset.update(status=StatusPasienChoices.NONAKTIF)
        self.message_user(request, f"{updated} pasien berhasil dinonaktifkan.")

    @admin.action(description="Aktifkan Pasien Terpilih")
    def aktifkan_pasien(self, request, queryset):
        updated = queryset.update(status=StatusPasienChoices.AKTIF)
        self.message_user(request, f"{updated} pasien berhasil diaktifkan.")

########## Admin untuk Master Data ##########
@admin.register(ICD10)
class ICD10Admin(admin.ModelAdmin):
    list_display = ('kode', 'deskripsi')
    search_fields = ['kode', 'deskripsi']  # <-- Wajib untuk autocomplete
