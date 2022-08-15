from datetime import datetime
from django.db import models


class Comment(models.Model):
    post = models.ForeignKey(   
        "Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(   
        "Author", on_delete=models.CASCADE, related_name="comments_authored")
    subject = models.CharField(max_length=30)
    content = models.CharField(max_length=140)
    datetime = models.DateTimeField()