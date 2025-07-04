# Generated by Django 5.2.1 on 2025-05-28 05:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_remove_pengguna_akses_admin_remove_pengguna_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ICD10',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.CharField(max_length=10, unique=True)),
                ('deskripsi', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pasien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_rm', models.CharField(max_length=20, unique=True)),
                ('nama_lengkap', models.CharField(max_length=100)),
                ('nik', models.CharField(blank=True, max_length=16, null=True, unique=True)),
                ('agama', models.CharField(choices=[('islam', 'Islam')], max_length=20)),
                ('pendidikan', models.CharField(choices=[('sma', 'SMA')], max_length=20)),
                ('pekerjaan', models.CharField(max_length=20)),
                ('status_pernikahan', models.CharField(choices=[('sudah nikah', 'Sudah Nikah')], max_length=20)),
                ('nomor_hp', models.CharField(blank=True, max_length=15, null=True)),
                ('alamat', models.TextField()),
                ('tanggal_lahir', models.DateField()),
                ('jenis_kelamin', models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Pasien',
            },
        ),
        migrations.CreateModel(
            name='TenagaKesehatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('profesi', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Tenaga Kesehatan',
            },
        ),
        migrations.CreateModel(
            name='Kunjungan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_kunjungan', models.DateTimeField(auto_now_add=True)),
                ('jenis_pelayanan', models.CharField(choices=[('P1', 'Pelayanan 1'), ('P2', 'Pelayanan 2'), ('P3', 'Pelayanan 3')], max_length=20)),
                ('anamnesis', models.TextField()),
                ('alergi_obat', models.CharField(choices=[('Y', 'Ya'), ('T', 'Tidak')], max_length=1)),
                ('jenis_alergi_obat', models.TextField()),
                ('tensi_darah', models.TextField()),
                ('tinggi_badan', models.TextField()),
                ('berat_badan', models.TextField()),
                ('suhu', models.TextField()),
                ('diagnosis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.icd10')),
                ('pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kunjungan', to='core.pasien')),
            ],
            options={
                'verbose_name_plural': 'Kunjungan',
            },
        ),
        migrations.CreateModel(
            name='RekamMedis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_dibuat', models.DateTimeField(auto_now_add=True)),
                ('kunjungan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rekam_medis', to='core.kunjungan')),
            ],
            options={
                'verbose_name_plural': 'Rekam Medis',
            },
        ),
        migrations.CreateModel(
            name='Diagnosa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_icd10', models.CharField(max_length=10)),
                ('deskripsi', models.TextField()),
                ('rekam_medis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnosa', to='core.rekammedis')),
            ],
            options={
                'verbose_name_plural': 'Diagnosa',
            },
        ),
        migrations.CreateModel(
            name='Rujukan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis_rujukan', models.CharField(choices=[('rawat_inap', 'Rawat Inap'), ('gawat_darurat', 'Gawat Darurat')], max_length=50)),
                ('faskes_tujuan', models.CharField(max_length=200)),
                ('alasan', models.TextField()),
                ('kunjungan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rujukan', to='core.kunjungan')),
            ],
            options={
                'verbose_name_plural': 'Rujukan',
            },
        ),
        migrations.CreateModel(
            name='LogAksesRekamMedis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_akses', models.DateTimeField(auto_now_add=True)),
                ('catatan', models.TextField(blank=True)),
                ('pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pasien')),
                ('tenaga_kesehatan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tenagakesehatan')),
            ],
            options={
                'verbose_name_plural': 'Log Akses Rekam Medis',
            },
        ),
        migrations.CreateModel(
            name='Tindakan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_icd9', models.CharField(blank=True, max_length=10)),
                ('nama_tindakan', models.TextField()),
                ('rekam_medis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tindakan', to='core.rekammedis')),
            ],
            options={
                'verbose_name_plural': 'Tindakan',
            },
        ),
    ]
