from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),  # halaman utama setelah login

    # URL Pasien
    path('pasien/', views.daftar_pasien, name='daftar_pasien'),
    path('pasien/tambah/', views.tambah_pasien, name='tambah_pasien'),
    path("pasien/<int:pk>/", views.detail_pasien, name="detail_pasien"),
    path('pasien/<int:pk>/edit/', views.edit_pasien, name='edit_pasien'),
    path('pasien/<int:pk>/nonaktifkan/', views.nonaktifkan_pasien, name='nonaktifkan_pasien'),
    path('pasien/<int:pasien_id>/riwayat/', views.riwayat_rekam_medis_pasien, name='riwayat_rekam_medis'),
    # URL Pasien lainnya

    # URL Registrasi
    path('registrasi/', views.daftar_registrasi, name='daftar_registrasi'),
    # path('registrasi/tambah/', views.tambah_registrasi, name='tambah_registrasi'),
    path('registrasi/tambah/<int:pasien_id>/', views.tambah_registrasi_auto, name='tambah_registrasi'),
    path('registrasi/<int:pk>/batalkan/', views.batalkan_registrasi, name='batalkan_registrasi'),
    path('registrasi/<int:pk>/selesaikan/', views.selesaikan_registrasi, name='selesaikan_registrasi'),
    # URL Registrasi lainnya

    # URL Rekam Medis
    path('rekam-medis/', views.daftar_rekam_medis, name='daftar_rekam_medis'),
    path('rekam-medis/buat/<int:registrasi_id>/', views.tambah_rekam_medis, name='tambah_rekam_medis'),
    # URL Rekam Medis lainnya
]
