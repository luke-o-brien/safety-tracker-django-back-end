from django.db import models

# Create your models here - Creating my Check_In Model
class Check_In(models.Model):
  def __str__(self):
    return f'{self.title} - {self.category}'
  title = models.CharField(max_length=80, unique=True)
  description = models.CharField(max_length=5000)
  category = models.CharField(max_length=80)
  reaction_level = models.FloatField()
  coping_action = models.CharField(max_length=5000)
  effectiveness = models.FloatField()
  owner = models.ForeignKey(
    "authentication.User",
    related_name="check_ins",
    on_delete=models.CASCADE
)
  
