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

# Alternate Check_In Model I could use as per researching (for future when I want to make it more accurate; however, maybe not use blank=True):
# Create my Check_In Model
# class Check_In(models.Model):
#   def __str__(self):
#     return f'{self.description} - {self.category}'
#   description = models.CharField(max_length=5000)
#   category = models.CharField(max_length=60, choices=[
#       ('fear', 'Fear/Stress'),
#       ('emotional', 'Emotional Abuse'),
#       ('physical', 'Physical Abuse'),
#       ('normal', 'Normal/Safe Day')
#   ])
#   date = models.DateField(auto_now_add=True)
#   trigger_event = models.CharField(max_length=200, blank=True)
#   reactionlevel = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], blank=True)
#   copingaction = models.CharField(max_length=60, blank=True)
#   effectiveness = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], blank=True)
