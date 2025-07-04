# Generated by Django 5.2.1 on 2025-05-31 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_obat_options_alter_rekammedislayanan_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rekammedis',
            name='berat_badan',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rekammedis',
            name='diastole',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rekammedis',
            name='frekuensi_pernafasan',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rekammedis',
            name='nadi',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rekammedis',
            name='sistole',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rekammedis',
            name='suhu_tubuh',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rekammedis',
            name='tinggi_badan',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
