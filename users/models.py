from django.db import models

class User(models.Model):
    id       = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=150)

    class Meta:
        db_table = "users"