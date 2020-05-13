from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    gender = models.CharField(max_length=7)
    birthday = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile/user/%Y/%m/%d/', blank=True)


class Photography(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user_photo')
    photo = models.ImageField(upload_to='user/%Y/%m/%d/',
                              blank=True,)
    description = models.TextField(max_length=128)
    publish = models.DateField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('instagram_profile:detail_photography',
                       args=[self.pk])

    def save(self):
        super().save()
        img = Image.open(self.photo.path)
        if img.height > 1000 or img.wight > 1000:
            output_size = (1000, 1000)
            img.thumbnail(output_size, Image.ANTIALIAS)
            img.save(self.photo.path)
        else:
            print('image cant resize')


class Comment(models.Model):
    photography = models.ForeignKey(Photography,
                                    on_delete=models.CASCADE,
                                    related_name='comment')
    name = models.CharField(max_length=50)
    body = models.TextField()
    publish = models.DateField(auto_now_add=True)
    email = models.EmailField()
