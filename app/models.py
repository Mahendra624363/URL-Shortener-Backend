from django.db import models

class UrlData(models.Model):
    id = models.AutoField(primary_key=True)
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)