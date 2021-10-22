from django.db import models


class Tag(models.Model):
    class Type(models.IntegerChoices):
        FEATURE = 1
        EVENT = 2

    name = models.CharField(primary_key=True, max_length=30, blank=False, null=False)
    type = models.IntegerField(choices=Type.choices)

    def __str__(self):
        return self.name
