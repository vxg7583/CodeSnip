from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):


    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    headline = models.TextField(max_length = 200, blank=True)
    country = models.TextField(max_length = 200, blank=True)
    city = models.TextField(max_length = 200, blank=True)
    employed = models.CharField(max_length=10, choices=[['yes', 'yes'], ['no', 'no']])
    employer = models.TextField(max_length = 200, blank=True)
    education_level = models.CharField(max_length=10, choices=[['masters', 'masters'],\
                                                                ['bachelors','bachelors']])
    major = models.TextField(max_length = 200, blank=True)
    school = models.TextField(max_length = 200, blank=True)
    fav_coding_lang = models.TextField(max_length = 200, blank=True)


    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))
