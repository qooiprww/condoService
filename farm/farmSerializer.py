from rest_framework import serializers
from farm.models import SeedContainer
from farm.models import PlantType
from farm.models import Plant
from farm.models import AmbientData
from farm.models import PlantData
from farm.models import Task


class SeedContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedContainer
        fields = ('id',
        'seed_container_name',
                  'seed_container_degree',
                  'seed_container_radius',
                  'seed_container_level')


class PlantTypeSerializer(serializers.ModelSerializer):
    # seed_container = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = PlantType
        fields = ('id',
                  'plant_type_name',
                  'growing_radius',
                  'seed_container',
                  'desired_humidity',
                  'desired_light_red',
                  'desired_light_green',
                  'desired_light_blue',
                  'desired_temperature')


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id',
                  'plant_type',
                  'plant_name',
                  'degree',
                  'radius',
                  'level',
                  'harvested',
                  'planted')


class AmbientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbientData
        fields = ('id',
                  'ambient_data_date_time',
                  'ambient_humidity',
                  'ambient_light_intensity',
                  'ambient_temperature')


class PlantDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantData
        fields = ('id',
                  'plant_data_date_time',
                  'humidity')


class TaskSerializer(serializers.ModelSerializer):
    # plant = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Task
        fields = ('id',
                  'plant',
                  'task_type',
                  'task_date_time',
                  'task_status')
