from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Models(models.Model):
    title = models.CharField(max_length=20)
    text = models.TextField(default='', null=True, blank=True)
    image1 = models.ImageField(upload_to = 'images/')
    image2 = models.ImageField(upload_to = 'images/', default='', null=True, blank=True)
    image3 = models.ImageField(upload_to = 'images/', default='', null=True, blank=True)
    image4 = models.ImageField(upload_to = 'images/', default='', null=True, blank=True)
    image5 = models.ImageField(upload_to = 'images/', default='', null=True, blank=True)
    thumbnail = ImageSpecField(source='image1', processors=[ResizeToFill(120,80)], format='JPEG')


    CATEGORY_CHOICES = (
        ('큐티', '큐티'),
        ('청량', '청량'),
        ('흑백사진', '흑백사진'),
        ('플러스모델', '플러스모델'),
    )

    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, null=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=20)
    text = models.TextField(default='', null=True, blank=True)
    image1 = models.ImageField(upload_to = 'images/')
    image2 = models.ImageField(upload_to = 'images/', default='', null=True, blank=True)
    image3 = models.ImageField(upload_to = 'images/', default='', null=True, blank=True)
    image4 = models.ImageField(upload_to = 'images/', default='', null=True, blank=True)
    image5 = models.ImageField(upload_to = 'images/', default='', null=True, blank=True)
    thumbnail = ImageSpecField(source='image1', processors=[ResizeToFill(120,80)], format='JPEG')

    CATEGORY_CHOICES = (
        ('큐티', '큐티'),
        ('청량', '청량'),
        ('흑백사진', '흑백사진'),
        ('플러스모델', '플러스모델'),
    )

    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, null=True)

    def __str__(self):
        return self.title

