from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),  # halaman utama setelah login

    path('ajax/icd-search/', views.icd_search, name='icd_search'),


    # URL Pasien
    path('pasien/', views.daftar_pasien, name='daftar_pasien'),
    path('pasien/tambah/', views.tambah_pasien, name='tambah_pasien'),
    path("pasien/<str:hash_id>/", views.detail_pasien, name="detail_pasien"),
    path('pasien/<str:hash_id>/edit/', views.edit_pasien, name='edit_pasien'),
    path('pasien/<str:hash_id>/riwayat-rm/', views.riwayat_rekam_medis_pasien, name='riwayat_rekam_medis_pasien'),
    path('pasien/buat-registrasi/<str:hash_id>/', views.buat_registrasi_pasien_auto, name='buat_registrasi_pasien'),
    path('pasien/<str:hash_id>/nonaktifkan/', views.nonaktifkan_pasien, name='nonaktifkan_pasien'),
    # Cetak Kartu
    # URL Pasien lainnya

    # URL Registrasi
    path('registrasi/', views.daftar_registrasi, name='daftar_registrasi'),
    path('registrasi/<str:hash_id>/batalkan/', views.batalkan_registrasi, name='batalkan_registrasi'),
    # URL Registrasi lainnya

    # URL Rekam Medis
    path('rekam-medis/', views.daftar_rekam_medis, name='daftar_rekam_medis'),
    path('rekam-medis/buat-rm/<str:hash_id>/', views.buat_rekam_medis, name='buat_rekam_medis'),
    path('rekam-medis/<str:hash_id>/edit/', views.edit_rekam_medis, name='edit_rekam_medis'),
    path('rekam-medis/<str:hash_id>/detail/', views.detail_rekam_medis, name='detail_rekam_medis'),
    path('rekam-medis/<str:hash_id>/resume/', views.resume_medis_view, name='resume_medis'),
]
