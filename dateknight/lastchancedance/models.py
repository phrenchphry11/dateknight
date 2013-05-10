from django.db import models

class Student(models.Model):
    email = models.CharField(max_lengt=200)
    first = models.CharField(max_length=200)
    last = models.CharField(max_length=200)

class Crush(models.Model):
    crusher = models.ForeignKey(Student)
    crushee = models.ForeginKey(Student)