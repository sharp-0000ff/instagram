# Generated by Django 3.0.6 on 2020-05-13 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=7)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='profile/user/%Y/%m/%d/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, height_field='height', upload_to='user/%Y/%m/%d/', width_field='width')),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=128)),
                ('publish', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_photo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('publish', models.DateField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('photography', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='instagram_profile.Photography')),
            ],
        ),
    ]
