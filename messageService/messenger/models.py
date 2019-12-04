from django.db import models

class Date(models.Model):
    date = models.DateField(unique=True, blank=False, null=False, verbose_name="Dia programado")

    def __str__(self):
        return str(self.date)

class WeekDay(models.Model):
    day = models.IntegerField(verbose_name="Dia de la semana")

    def __str__(self):
        days = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado' ]
        return str(days[self.day])

class Message(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name="Nombre del fichero")
    date = models.ManyToManyField(Date, blank=True, null=True)
    week_day = models.ManyToManyField(WeekDay, blank=True, null=True)

    def __str__(self):
        return self.name


