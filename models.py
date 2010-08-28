
from django.db import models

class JSVersion(models.Model):
    version = models.IntegerField(default=1)
