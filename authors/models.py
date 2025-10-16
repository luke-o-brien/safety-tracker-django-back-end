from django.db import models

# Model created here for author
class Author(models.Model):
    def __str__(self):
        return f'{self.name}'

    name = models.CharField(max_length=80, unique=True)


