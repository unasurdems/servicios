# Generated by Django 2.2.1 on 2019-05-02 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alcaldia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_creacion', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario_modificacion', models.IntegerField(blank=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(blank=True, null=True)),
                ('usuario_eliminacion', models.IntegerField(blank=True, null=True)),
                ('fecha_eliminacion', models.DateTimeField(blank=True, null=True)),
                ('alcaldia', models.CharField(max_length=100, unique=True, verbose_name='Nombre de la Alcaldia')),
                ('sigla', models.CharField(blank=True, max_length=15, null=True, verbose_name='Sigla de la Alcaldia')),
                ('dpa', models.CharField(blank=True, max_length=50, null=True, verbose_name='DPA de la Alcaldia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_creacion', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario_modificacion', models.IntegerField(blank=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(blank=True, null=True)),
                ('usuario_eliminacion', models.IntegerField(blank=True, null=True)),
                ('fecha_eliminacion', models.DateTimeField(blank=True, null=True)),
                ('departamento', models.CharField(max_length=15, unique=True, verbose_name='Nombre del departamento')),
                ('departamento_descripcion', models.CharField(blank=True, max_length=50, null=True, verbose_name='Descripcion del departamento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_creacion', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario_modificacion', models.IntegerField(blank=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(blank=True, null=True)),
                ('usuario_eliminacion', models.IntegerField(blank=True, null=True)),
                ('fecha_eliminacion', models.DateTimeField(blank=True, null=True)),
                ('provincia', models.CharField(max_length=50, unique=True, verbose_name='Nombre de la provincia')),
                ('provincia_descripcion', models.CharField(blank=True, max_length=80, null=True, verbose_name='Descripcion de la provincia')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='departamento_provincia', to='direccion.Departamento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_creacion', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario_modificacion', models.IntegerField(blank=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(blank=True, null=True)),
                ('usuario_eliminacion', models.IntegerField(blank=True, null=True)),
                ('fecha_eliminacion', models.DateTimeField(blank=True, null=True)),
                ('municipio', models.CharField(max_length=100, unique=True, verbose_name='Nombre del municipio')),
                ('municipio_descripcion', models.CharField(blank=True, max_length=150, null=True, verbose_name='Descripcion del municipio')),
                ('alcaldia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alcaldia_municipio', to='direccion.Alcaldia')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='provincia_municipio', to='direccion.Provincia')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]