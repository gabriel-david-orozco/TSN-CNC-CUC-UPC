from django.db import models

# Create your models here.

class User(models.Model):
    Model_Descriptor = models.JSONField()
    Model_Descriptor_vector = models.JSONField()
    unused_links = models.JSONField()
    Frames_Duration = models.JSONField()