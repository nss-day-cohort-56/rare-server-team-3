from xml.dom.minidom import CharacterData
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField


class Author(models.Model):

    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.URLField(max_length = 200)