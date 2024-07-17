from django.db import models

class URL(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    hit_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.short_url} short for {self.long_url}"

