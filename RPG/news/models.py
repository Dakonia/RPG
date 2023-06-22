from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торогвцы'),
        ('gildemaster','Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tittle = models.CharField(max_length=64)
    text = RichTextUploadingField(blank=True, null=True)
    dateCreation = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=12, choices=TYPE, default='tank')
    # upload = models.FileField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return f'{self.tittle}: {self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Response(models.Model):
    post = models.ForeignKey(Post, related_name='responses', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)