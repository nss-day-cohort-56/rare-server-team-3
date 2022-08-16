from django.db import models

class Post(models.Model):

    title = models.CharField(max_length=55)
    publication_date = models.DateField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="post_category")
    author = models.ForeignKey("Author", on_delete = models.CASCADE, related_name = "post_author")
    content = models.TextField(max_length=300)
    image_url = models.URLField(max_length=200)
    post_tags = models.ManyToManyField("Tag", through="PostTag", related_name="tags")

