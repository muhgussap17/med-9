from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import date, timedelta, datetime

from .models import *
from .forms import * # type: ignore

def get_pasien_choices_context():
    return {
        'jenis_pasien_choices': JenisPasienChoices.choices,
        'agama_choices': AgamaChoices.choices,
        'pendidikan_choices': PendidikanChoices.choices,
        'pekerjaan_choices': PekerjaanChoices.choices,
        'status_pernikahan_choices': StatusPernikahanChoices.choices,
        'status_choices': StatusPasienChoices.choices,
        'jenis_kelamin_choices': JenisKelaminChoices.choices,
        'status_merokok_choices': StatusPerokokChoices.choices,
        'golongan_darah_choices': GolonganDarahChoices.choices,
    }

def get_rekam_medis_choices_context():
    return {
        'prognosis_choices': PrognosisChoices.choices,
        'status_kesadaran_choices': StatusKesadaranChoices.choices,
        'status_pulang_choices': StatusPulangChoices.choices,
    }

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
 
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    today = date.today()
    queryset = Registrasi.objects.select_related('pasien').order_by('-waktu')

    total_terdaftar = Registrasi.objects.filter(tanggal=today).count()
    belum_dilayani = Registrasi.objects.filter(
        status=StatusRegistrasiChoices.MENUNGGU,
        tanggal=today
    ).count()
    sudah_dilayani = Registrasi.objects.filter(
        status=StatusRegistrasiChoices.SELESAI,
        tanggal=today
    ).count()

    status_filter = request.GET.get('status')
    tanggal_filter = request.GET.get("tanggal")


    status_filter = StatusRegistrasiChoices.MENUNGGU

    tanggal_filter = today

    queryset = queryset.filter(status=status_filter)
    queryset = queryset.filter(tanggal=today)
    
    context = {
        'data_registrasi': queryset,
        'total_terdaftar': total_terdaftar,
        'belum_dilayani': belum_dilayani,
        'sudah_dilayani': sudah_dilayani,
        'status_filter': status_filter,
        'tanggal_filter': tanggal_filter,
        "page_title": "Dashboard",
        "breadcrumbs": [
            {"title": "Dashboard", "url": "/"},
        ]
    }

    return render(request, 'core/dashboard.html', context)

################################################################################################################################################################################
################################################################################# FITUR PASIEN #################################################################################
################################################################################################################################################################################
@login_required
def daftar_pasien(request): # UDAH FIX
    pasien_list = Pasien.objects.all().order_by('-created_at')
    status_filter = request.GET.get('status')

    if status_filter in StatusPasienChoices.values:
        pasien_list = Pasien.objects.filter(status=status_filter)
    else:
        pasien_list = Pasien.objects.all()

    breadcrumbs = [
        {'title': 'Pasien', 'url': '/pasien/'},
    ]

    context = {
        'pasien_list': pasien_list,
        'status_filter': status_filter,

        'page_title': 'Pasien',
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'core/pasien.html', context)

@login_required
def tambah_pasien(request): # UDAH FIX
    if request.method == 'POST':
        form = PasienForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pasien berhasil ditambahkan.')
            return redirect('daftar_pasien')
        else:
            messages.error(request, 'Terjadi kesalahan. Periksa kembali input Anda.')
    else:
        form = PasienForm()
    
    breadcrumbs = [
        {'title': 'Pasien', 'url': '/pasien/'},
        {'title': 'Tambah Pasien'},    
    ]

    context = {
        'form': form,
        'mode': 'tambah',

        'page_title': 'Tambah Pasien',
        'breadcrumbs': breadcrumbs,

        **get_pasien_choices_context(),
    }
    return render(request, 'core/pasien_form.html', context)

@login_required
def detail_pasien(request, pk): # UDAH FIX
    pasien = get_object_or_404(Pasien, pk=pk)

    breadcrumbs = [
        {'title': 'Pasien', 'url': '/pasien/'},
        {'title': pasien.nama_lengkap},
    ]

    context = {
        'pasien': pasien,

        'page_title': 'Detail Pasien',
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'core/pasien_detail.html', context)

@login_required
def edit_pasien(request, pk): # UDAH FIX
    pasien = get_object_or_404(Pasien, pk=pk)

    if request.method == 'POST':
        form = PasienForm(request.POST, instance=pasien)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data pasien berhasil diperbarui.')
            return redirect('daftar_pasien')
        else:
            messages.error(request, 'Terdapat kesalahan pada form.')
    else:
        form = PasienForm(instance=pasien)

    breadcrumbs = [
        {'title': 'Pasien', 'url': '/pasien/'},
        {'title': pasien.nama_lengkap, 'url': f"/pasien/{pasien.pk}/"},
        {'title': 'Edit'},
    ]

    context = {
        'form': form,
        'pasien': pasien,
        'mode': 'edit',

        'page_title': 'Edit Pasien',
        'breadcrumbs': breadcrumbs,
        
        **get_pasien_choices_context(),
    }
    return render(request, 'core/pasien_form.html', context)   

@login_required
def riwayat_rekam_medis_pasien(request, pasien_id): # UDAH FIX
    pasien = get_object_or_404(Pasien, id=pasien_id)

    # Mengambil semua rekam medis dari pasien ini via relasi ke Registrasi
    rekam_list = RekamMedis.objects.select_related('registrasi', 'kode_diagnosis') \
        .filter(registrasi__pasien=pasien) \
        .order_by('-created_at')

    breadcrumbs = [
        {'title': 'Pasien', 'url': '/pasien/'},
        {'title': pasien.nama_lengkap, 'url': f"/pasien/{pasien.pk}/"},
        {'title': 'Riwayat'},
    ]

    context = {
        'pasien': pasien,
        'rekam_list': rekam_list,

        'page_title': 'Riwayat Pasien',
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'core/pasien_riwayat_rm.html', context)

@login_required
def buat_registrasi_pasien_auto(request, pasien_id): # UDAH FIX 
    pasien = get_object_or_404(Pasien, id=pasien_id)
    today = timezone.localdate()

    if Registrasi.objects.filter(pasien=pasien, tanggal=today).exists():
        messages.warning(request, f"Pasien {pasien.nama_lengkap} sudah teregistrasi hari ini.")
        return redirect('daftar_pasien')
    
    registrasi = Registrasi.objects.create(pasien=pasien)
    registrasi.save()
    messages.success(request, f"Registrasi {pasien.nama_lengkap} berhasil dibuat.")
    return redirect('daftar_pasien')

@login_required
def nonaktifkan_pasien(request, pk): # UDAH FIX 
    pasien = get_object_or_404(Pasien, pk=pk)
    pasien.status = StatusPasienChoices.NONAKTIF
    pasien.save()
    messages.warning(request, "Pasien telah dinonaktifkan")
    return redirect('daftar_pasien')


####################################################################################################################################################################################
################################################################################# FITUR REGISTRASI #################################################################################
####################################################################################################################################################################################
@login_required
def daftar_registrasi(request): # UDAH FIX 
    batas_waktu = timezone.now() - timedelta(hours=24)
    Registrasi.objects.filter(
        status=StatusRegistrasiChoices.MENUNGGU,
        waktu__lt=batas_waktu
    ).update(status=StatusRegistrasiChoices.BATAL)

    status_filter = request.GET.get('status')
    tanggal_filter = request.GET.get('tanggal')

    queryset = Registrasi.objects.select_related('pasien').order_by('-waktu')

    if status_filter in StatusRegistrasiChoices.values:
        queryset = queryset.filter(status=status_filter)
    else:
        status_filter = None

    parsed_date = None
    if tanggal_filter:
        try:
            parsed_date = datetime.strptime(tanggal_filter, '%m/%d/%Y').date()
        except ValueError:
            parsed_date = None
    else:
        parsed_date = date.today()

    if parsed_date:
        queryset = queryset.filter(tanggal=parsed_date)
    else:
        tanggal_filter = None
    if status_filter in StatusRegistrasiChoices.values:
        queryset = queryset.filter(status=status_filter)
    else:
        status_filter = None

    breadcrumbs = [
        {'title': 'Registrasi', 'url': '/registrasi/'},
    ]
    context = {
        'registrasi_list': queryset,
        'status_filter': status_filter,
        'tanggal_filter': tanggal_filter,

        "page_title": "Registrasi",
        "breadcrumbs": breadcrumbs,
    }

    return render(request, 'core/registrasi.html', context)

@login_required
def batalkan_registrasi(request, pk): # UDAH FIX
    registrasi = get_object_or_404(Registrasi, pk=pk)
    registrasi.status = StatusRegistrasiChoices.BATAL
    registrasi.save()
    messages.warning(request, "Registrasi dibatalkan.")

    return redirect('daftar_registrasi')



#####################################################################################################################################################################################
################################################################################# FITUR REKAM MEDIS #################################################################################
#####################################################################################################################################################################################
@login_required
def daftar_rekam_medis(request):
    tanggal_filter = request.GET.get('tanggal')
    
    rekam_list = RekamMedis.objects.select_related(
        'registrasi', 'registrasi__pasien'
    )

    parsed_date = None
    if tanggal_filter:
        try:
            parsed_date = datetime.strptime(tanggal_filter, '%m/%d/%Y').date()
        except ValueError:
            parsed_date = None
    else:
        parsed_date = date.today()

    if parsed_date:
        rekam_list = rekam_list.filter(created_at__date=parsed_date)
    else:
        tanggal_filter = None

    rekam_list = rekam_list.order_by('-created_at')

    breadcrumbs = [
        {'title': 'Rekam Medis', 'url': '/rekam-medis/'},
    ]

    context = {
        'rekam_list': rekam_list,
        'tanggal_filter': tanggal_filter,
        
        'page_title': 'Rekam Medis',
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'core/rekam_medis.html', context)

@login_required
def buat_rekam_medis(request, registrasi_id):
    registrasi = get_object_or_404(Registrasi, id=registrasi_id)
    pasien = registrasi.pasien

    # Mengambil data terakhir rekam medis si pasien ini (riwayat)
    rekam_sebelumnya = RekamMedis.objects.filter(
        registrasi__pasien=pasien
    ).order_by('-created_at').first()

    # Mengambil semua rekam medis si pasien ini (riwayat juga tapi lebih detail)
    rekam_list = RekamMedis.objects.select_related('registrasi', 'kode_diagnosis') \
        .filter(registrasi__pasien=pasien) \
        .order_by('-created_at')
    
    # Mengambil semua kode diagnosis dalam tabel ICD10
    icd_list = ICD10.objects.all().order_by('kode')

    if request.method == 'POST':
        form = RekamMedisForm(request.POST)
        if form.is_valid():
            rekam_medis = form.save(commit=False)
            rekam_medis.registrasi = registrasi
            rekam_medis.created_by = request.user
            rekam_medis.updated_by = request.user
            rekam_medis.save()
            registrasi.status = StatusRegistrasiChoices.SELESAI
            registrasi.save()
            messages.success(request, "Rekam medis berhasil dibuat.")
            return redirect('daftar_registrasi')
        else:
            messages.error(request, "Gagal menambahkan rekam medis. Periksa kembali form Anda.")
    else:
        form = RekamMedisForm(initial={'registrasi': registrasi})

    breadcrumbs = [
        {'title': 'Registrasi', 'url': '/registrasi/'},
        {'title': 'Buat Rekam Medis'},
    ]
    
    context = {
        'form': form,
        'mode': 'buat',
        'registrasi': registrasi,
        'pasien': pasien,
        'rekam_sebelumnya': rekam_sebelumnya, # Untuk Tab Resume Medis bagian Objective
        'rekam_list': rekam_list, # Untuk Tab Riwayat Konsul
        'icd_list': icd_list,

        'page_title': "Buat Rekam Medis",
        'breadcrumbs': breadcrumbs,

        **get_rekam_medis_choices_context(),
    }
    return render(request, 'core/rekam_medis_form.html', context)

@login_required
def edit_rekam_medis(request, rekam_id):
    rekam = get_object_or_404(RekamMedis, id=rekam_id)
    pasien = rekam.registrasi.pasien

    rekam_sebelumnya =  RekamMedis.objects.filter(
        registrasi__pasien=pasien
    ).exclude(id=rekam_id).order_by('-created_at').first()

    rekam_list = RekamMedis.objects.select_related('registrasi', 'kode_diagnosis') \
        .filter(registrasi__pasien=pasien) \
        .order_by('-created_at')
    
    icd_list = ICD10.objects.all().order_by('kode')
    
    if request.method == 'POST':
        form = RekamMedisForm(request.POST, instance=rekam)
        if form.is_valid():
            rekam_edited = form.save(commit=False)
            rekam_edited.updated_by = request.user
            rekam_edited.save()
            messages.success(request, "Rekam medis telah diperbarui.")
            return redirect('daftar_rekam_medis')
        else:
            messages.error(request, "Terdapat kesalahan pada form.")
    else:
        form = RekamMedisForm(instance=rekam)

    breadcrumbs = [
        {'title': 'Rekam Medis', 'url': '/rekam-medis/'},
        {'title': f'{pasien.nama_lengkap} | {rekam.created_at.strftime("%d %B  %Y")}', 'url': f'/rekam-medis/{rekam.id}/detail'}, # type: ignore
        {'title': 'Edit Rekam Medis'},
    ]

    context = {
        'form': form,
        'mode': 'edit',
        'rekam': rekam,
        'pasien': pasien,
        'rekam_sebelumnya': rekam_sebelumnya,
        'rekam_list': rekam_list,
        'icd_list': icd_list,

        'page_title': 'Edit Rekam Medis',
        'breadcrumbs': breadcrumbs,

        **get_rekam_medis_choices_context(),
    }
    return render(request, 'core/rekam_medis_form.html', context)

@login_required
def detail_rekam_medis(request, rekam_id):
    rekam = get_object_or_404(RekamMedis, id=rekam_id)
    pasien = rekam.registrasi.pasien

    breadcrumbs = [
        {'title': 'Rekam Medis', 'url': '/rekam-medis/'},
        {'title': f'{pasien.nama_lengkap} | {rekam.created_at.strftime("%d %B  %Y")}', 'url': f'/pasien/{pasien.pk}/'},
    ]

    context = {
        'rekam': rekam,
        'pasien': pasien,

        'page_title': f'Detail Rekam Medis ',
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'core/rekam_medis_detail.html', context)

@login_required
def resume_medis_view(request, rekam_id):
    rekam = get_object_or_404(RekamMedis, id=rekam_id)
    pasien = rekam.registrasi.pasien

    context = {
        'rekam': rekam,
        'pasien': pasien,
    }

    return render(request, 'core/rekam_medis_cetak.html', context)