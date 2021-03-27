from django.contrib import admin
from .models import SeedContainer, PlantType, AmbientData, PlantData, Plant, Task

admin.site.register(SeedContainer)
admin.site.register(PlantType)
admin.site.register(AmbientData)
admin.site.register(PlantData)
admin.site.register(Plant)
admin.site.register(Task)

# Register your models here.
