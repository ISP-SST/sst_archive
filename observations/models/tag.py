from django.db import models


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=30, blank=False, null=False)

    def __str__(self):
        return self.name
