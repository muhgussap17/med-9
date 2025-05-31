from django.contrib import admin
from .models import (
    Pasien, StatusPasienChoices, Registrasi, StatusRegistrasiChoices, RekamMedis,
    ICD10, Penyakit, Alergi,
    Layanan, Obat, Vaksin, Tindakan,
    RekamMedisObat, RekamMedisLayanan, RekamMedisTindakan, RekamMedisVaksin,
)

# Inline untuk data terkait Rekam Medis
class RekamMedisObatInline(admin.TabularInline):
    model = RekamMedisObat
    extra = 1
    autocomplete_fields = ['obat']

class RekamMedisLayananInline(admin.TabularInline):
    model = RekamMedisLayanan
    extra = 1

class RekamMedisVaksinInline(admin.TabularInline):
    model = RekamMedisVaksin
    extra = 1

class RekamMedisTindakanInline(admin.TabularInline):
    model = RekamMedisTindakan
    extra = 1

# Admin untuk Rekam Medis dengan inlines
@admin.register(RekamMedis)
class RekamMedisAdmin(admin.ModelAdmin):
    list_display = ('registrasi', 'created_at')
    # list_display = ('registrasi_link', 'pasien_nama', 'created_at', 'ringkasan_rekam_medis')
    inlines = [RekamMedisObatInline, RekamMedisLayananInline, RekamMedisVaksinInline, RekamMedisTindakanInline]
    autocomplete_fields = ['riwayat_penyakit', 'riwayat_alergi', 'kode_diagnosis']
    list_filter = ('created_at',)
    search_fields = (
        'registrasi__pasien__nama_lengkap',
        'registrasi__pasien__nik',
        'kode_diagnosis__kode',
        'kode_diagnosis__deskripsi',
    )
    ordering = ('-created_at',)
    readonly_fields = [
        'registrasi', 'created_at', 'keluhan_utama', 'catatan',
        'riwayat_penyakit', 'riwayat_alergi', 'kode_diagnosis',
        'ringkasan_rekam_medis'
    ]

    @admin.display(description="Detail Rekam Medis")
    def detail_link(self, obj):
        from django.utils.html import format_html
        url = f"/admin/core/rekammedis/{obj.id}/change/"
        return format_html(f'<a class="button" href="{url}">Lihat</a>')
    
    # @admin.display(description="Ringkasan Rekam Medis")
    # def ringkasan_rekam_medis(self, obj):
    #     from django.utils.html import format_html
    #     return format_html(
    #         "<strong>Keluhan:</strong> {}<br><strong>Diagnosis:</strong> {}<br><strong>Terapi:</strong> {}",
    #         obj.keluhan_utama or "-",
    #         obj.kode_diagnosis.deskripsi if obj.kode_diagnosis else "-",
    #         ", ".join([str(o.obat) for o in obj.obat_diberikan.all()]) or "-"
    #     )

    @admin.display(description="Registrasi")
    def registrasi_link(self, obj):
        from django.utils.html import format_html
        url = f"/admin/core/registrasi/{obj.registrasi.id}/change/"
        return format_html(f'<a href="{url}">#{obj.registrasi.id}</a>')

    @admin.display(description="Pasien")
    def pasien_nama(self, obj):
        return obj.registrasi.pasien.nama_lengkap

# Admin untuk Registrasi
@admin.register(Registrasi)
class RegistrasiAdmin(admin.ModelAdmin):
    list_display = (
        'no_antrian', 'pasien_link', 'tanggal', 'waktu', 'status', 'lihat_rekam_medis'
    )
    list_filter = ('tanggal', 'status')
    search_fields = ('pasien__nama_lengkap', 'pasien__nik', 'no_antrian', 'tanggal')
    autocomplete_fields = ['pasien']
    actions = ['tandai_menunggu', 'tandai_selesai', 'tandai_dibatalkan']
    ordering = ('-tanggal', '-waktu')

    @admin.display(description="Pasien", ordering="pasien__nama_lengkap")
    def pasien_link(self, obj):
        from django.utils.html import format_html
        url = f"/admin/core/pasien/{obj.pasien.id}/change/"
        return format_html(f'<a href="{url}">{obj.pasien.nama_lengkap}</a>')

    @admin.display(description="Lihat Rekam Medis")
    def lihat_rekam_medis(self, obj):
        from django.utils.html import format_html
        url = f"/admin/core/rekammedis/?registrasi__id__exact={obj.id}"
        return format_html(f'<a href="{url}">Rekam Medis</a>')

    @admin.action(description="Tandai sebagai Menunggu Konsultasi")
    def tandai_menunggu(self, request, queryset):
        updated = queryset.update(status=StatusRegistrasiChoices.MENUNGGU)
        self.message_user(request, f"{updated} registrasi ditandai sebagai 'Menunggu Konsultasi'.")

    @admin.action(description="Tandai sebagai Selesai Konsultasi")
    def tandai_selesai(self, request, queryset):
        updated = queryset.update(status=StatusRegistrasiChoices.SELESAI)
        self.message_user(request, f"{updated} registrasi berhasil ditandai sebagai 'Selesai Konsultasi'.")

    @admin.action(description="Tandai sebagai Dibatalkan")
    def tandai_dibatalkan(self, request, queryset):
        updated = queryset.update(status=StatusRegistrasiChoices.BATAL)
        self.message_user(request, f"{updated} registrasi berhasil dibatalkan.")

# Admin untuk Pasien
@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    list_display = (
        'no_rm', 'nama_lengkap', 'nik', 'jenis_kelamin', 
        'tanggal_lahir', 'umur', 'status', 'lihat_registrasi'
    )
    list_filter = ('status', 'jenis_kelamin', 'agama', 'pendidikan')
    search_fields = ('nama_lengkap', 'nik', 'no_rm')
    actions = ['nonaktifkan_pasien', 'aktifkan_pasien']
    readonly_fields = ('umur',)

    @admin.display(description="Lihat Registrasi")
    def lihat_registrasi(self, obj):
        from django.utils.html import format_html
        url = f"/admin/core/registrasi/?pasien__id__exact={obj.id}"
        return format_html(f'<a href="{url}">Lihat</a>')

    @admin.action(description="Nonaktifkan Pasien Terpilih")
    def nonaktifkan_pasien(self, request, queryset):
        updated = queryset.update(status=StatusPasienChoices.NONAKTIF)
        self.message_user(request, f"{updated} pasien berhasil dinonaktifkan.")

    @admin.action(description="Aktifkan Pasien Terpilih")
    def aktifkan_pasien(self, request, queryset):
        updated = queryset.update(status=StatusPasienChoices.AKTIF)
        self.message_user(request, f"{updated} pasien berhasil diaktifkan.")

# Admin untuk Master Data
@admin.register(ICD10)
class ICD10Admin(admin.ModelAdmin):
    list_display = ('kode', 'deskripsi')
    search_fields = ['kode', 'deskripsi']  # <-- Wajib untuk autocomplete
    
@admin.register(Penyakit)
class PenyakitAdmin(admin.ModelAdmin):
    list_display = ('jenis', 'deskripsi')
    search_fields = ['jenis', 'deskripsi']

@admin.register(Alergi)
class AlergiAdmin(admin.ModelAdmin):
    list_display = ('jenis', 'deskripsi')
    search_fields = ['jenis', 'deskripsi']
    
@admin.register(Layanan)
class LayananAdmin(admin.ModelAdmin):
    list_display = ('nama', 'harga')
    search_fields = ['nama']

@admin.register(Obat)
class ObatAdmin(admin.ModelAdmin):
    list_display = ('nama', 'bentuk', 'dosis_nilai', 'dosis_satuan', 'keterangan')
    search_fields = ['nama']

@admin.register(Vaksin)
class VaksinAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ['nama']

@admin.register(Tindakan)
class TindakanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'harga')
    search_fields = ['nama']
