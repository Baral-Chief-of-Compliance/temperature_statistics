from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


#модель для города
class Town(models.Model):
    t_name = models.CharField(
        verbose_name='Название города', 
        max_length=128
    )

    t_user = models.ForeignKey(
        verbose_name='Пользователь, который добавил', 
        to=User, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.t_name
    
    class Meta:
        ordering = ['t_name']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


#модель для температуры
class Temperature(models.Model):
    tmp_town = models.ForeignKey(
        verbose_name='Город', to=Town, 
        on_delete=models.CASCADE
    )

    tmp_date = models.DateTimeField(
        verbose_name='Дата', 
        default=datetime.today
    )

    tmp_value = models.IntegerField(
        verbose_name='Значение по Цельсия',
        default=0
    )

    def __str__(self):
        return f'температура в городе {self.tmp_town.t_name} за {self.tmp_date}'
    
    class Meta:
        ordering = ['-tmp_date']
        verbose_name = 'Температура'
        verbose_name_plural = 'Температуры'

