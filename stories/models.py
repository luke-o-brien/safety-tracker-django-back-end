from django.db import models

# Create your models here.
class Story(models.Model):
    """Per Pylint, it recommends I do a class docstring: Story represents a story with a title, author, content, and owner - these are shared stories of how people survived and got out."""
    def __str__(self):
        return f'{self.title} - {self.author}'

    # models.CharField is the data type and means "string"
    title = models.CharField(max_length=80, unique=True)
    author = models.ForeignKey(
        "authors.Author",
        related_name = "stories",
        on_delete = models.CASCADE
    )
    content = models.TextField()
    owner = models.ForeignKey(
        "authentication.User",
        related_name = "stories",
        on_delete = models.CASCADE
    )
    