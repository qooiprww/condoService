from django.db import models

# Create your models here.
from djongo import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def validate_light(value):
    if value > 255 or value < 0:
        raise ValidationError(
            _('%(value)s should be a value between 0~255'),
            params={'value': value},
        )


def validate_humidity(value):
    if value > 100.0 or value < 0.0:
        raise ValidationError(
            _('%(value)s should be a value between 0.0~100.0'),
            params={'value': value},
        )


def validate_temperature(value):
    if value > 70.0 or value < -50.0:
        raise ValidationError(
            _('%(value)s should be a value between -50.0~70.0'),
            params={'value': value},
        )


def validate_degree(value):
    if value > 360.0 or value < 0.0:
        raise ValidationError(
            _('%(value)s should be a value between 0.0~360.0'),
            params={'value': value},
        )


def validate_radius(value):
    if value < 0.0 or value > settings.MAX_RADIUS:
        raise ValidationError(
            _('%(value)s should be a value between 0.0~%(radius)s'),
            params={'value': value, 'radius': settings.MAX_RADIUS},
        )


def validate_level(value):
    if value < 0 or value > settings.MAX_LEVEL:
        raise ValidationError(
            _('%(value)s should be a value between 0~%(level)s'),
            params={'value': value, 'level': settings.MAX_LEVEL},
        )


class SeedContainer(models.Model):
    seed_container_name = models.CharField(blank=False, max_length=255, default="Seed Container")
    seed_container_degree = models.FloatField(
        blank=False, validators=[validate_degree])
    seed_container_radius = models.FloatField(
        blank=False, validators=[validate_radius])
    seed_container_level = models.IntegerField(
        blank=False, default=settings.LEVEL_1, choices=settings.LEVEL_CHOICES, validators=[validate_level])


class PlantType(models.Model):
    plant_type_name = models.CharField(blank=False, max_length=255)
    growing_radius = models.FloatField(
        blank=False, default=2.0, validators=[validate_radius])
    seed_container = models.ForeignKey(SeedContainer, on_delete=models.CASCADE)
    desired_humidity = models.FloatField(
        blank=False, default=30.0, validators=[validate_humidity])
    desired_light_red = models.IntegerField(
        blank=False, default=150, validators=[validate_light])
    desired_light_green = models.IntegerField(
        blank=False, default=150, validators=[validate_light])
    desired_light_blue = models.IntegerField(
        blank=False, default=150, validators=[validate_light])
    desired_temperature = models.FloatField(
        blank=False, default=25.0, validators=[validate_temperature])

    def __str__(self):
        return self.plant_type_name


class AmbientData(models.Model):
    ambient_data_date_time = models.DateTimeField(auto_now_add=True)
    ambient_humidity = models.FloatField(
        blank=False, validators=[validate_humidity])
    ambient_light_intensity = models.FloatField(blank=False)
    ambient_temperature = models.FloatField(
        blank=False, validators=[validate_temperature])

    def __str__(self):
        return self.ambient_data_date


class Plant(models.Model):
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    plant_name = models.CharField(blank=True, max_length=255, default='plant')
    degree = models.FloatField(blank=False, validators=[validate_degree])
    radius = models.FloatField(blank=False, validators=[validate_radius])
    level = models.IntegerField(blank=False, default=settings.LEVEL_1,
                                choices=settings.LEVEL_CHOICES, validators=[validate_level])
    harvested = models.BooleanField(default=False)
    planted = models.BooleanField(default=False)


class PlantData(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, default=0)
    plant_data_date_time = models.DateTimeField(auto_now_add=True)
    humidity = models.FloatField(blank=False, validators=[validate_humidity])


class Task(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, blank=True)
    task_type = models.CharField(
        blank=False, max_length=2, choices=settings.TASK_CHOICES)
    task_date_time = models.DateTimeField(auto_now_add=True)
    task_status = models.CharField(blank=False, max_length=3, default=settings.TASK_STATUS_QUEUED,
                                   choices=settings.TASK_STATUS_CHOICES)
