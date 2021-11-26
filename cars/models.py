from django.db import models

class UserCar(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    car  = models.ForeignKey('Car', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_cars'


class Car(models.Model):
    name       = models.CharField(max_length=30)
    front_tire = models.ForeignKey('Tire', on_delete=models.CASCADE, related_name='front_tire')
    rear_tire  = models.ForeignKey('Tire', on_delete=models.CASCADE, related_name='rear_tire')


class TirePosition(models.Model):
    class Type(models.IntegerChoices):
        FRONT = 1
        REAR  = 2

    name = models.CharField(max_length=15)
    
    class Meta:
        db_table = 'tire_positions'


class Tire(models.Model):
    tire_position = models.ForeignKey('TirePosition', on_delete=models.PROTECT)
    width        = models.PositiveSmallIntegerField()
    aspect_ratio = models.PositiveSmallIntegerField()
    wheel_size   = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'tires'

