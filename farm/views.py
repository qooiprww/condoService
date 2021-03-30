from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from taskEngine.tasks import offerTask

# add all views
from farm.models import Task
from farm.farmSerializer import TaskSerializer

from farm.models import SeedContainer
from farm.farmSerializer import SeedContainerSerializer

from farm.models import PlantData
from farm.farmSerializer import PlantDataSerializer

from farm.models import AmbientData
from farm.farmSerializer import AmbientDataSerializer

from farm.models import PlantType
from farm.farmSerializer import PlantTypeSerializer

from farm.models import Plant
from farm.farmSerializer import PlantSerializer


#
# task
#


@api_view(['GET', 'POST', 'DELETE'])
def task_list(request):
    # GET list of tasks, POST a new task, DELETE all tasks
    if request.method == 'GET':
        task = Task.objects.all()

        task_id = request.GET.get('id', None)
        if task_id is not None:
            task = task.filter(task__icontains=task_id)

        task_serializer = TaskSerializer(task, many=True)
        return JsonResponse(task_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        task_data = JSONParser().parse(request)
        task_serializer = TaskSerializer(data=task_data)
        if task_serializer.is_valid():
            offerTask(task_serializer)
            return JsonResponse(task_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Task.objects.all().delete()
        return JsonResponse({'message': '{} Tasks were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    # find task by pk (id)
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return JsonResponse({'message': 'The task does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE task
    if request.method == 'GET':
        task_serializer = TaskSerializer(task)
        return JsonResponse(task_serializer.data)

    elif request.method == 'PUT':
        task_data = JSONParser().parse(request)
        task_serializer = TaskSerializer(task, data=task_data)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse(task_serializer.data)
        return JsonResponse(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'task was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def task_list_published(request):
    # GET all published seed containers
    task = Task.objects.filter(published=True)

    if request.method == 'GET':
        task_serializer = TaskSerializer(task, many=True)
        return JsonResponse(task_serializer.data, safe=False)

#
# seed_container
#


@api_view(['GET', 'POST', 'DELETE'])
def seed_container_list(request):
    # GET list of seed_containers, POST a new seed_container, DELETE all seed_containers
    if request.method == 'GET':
        seed_container = SeedContainer.objects.all()

        seed_container_id = request.GET.get('id', None)
        if seed_container_id is not None:
            seed_container = seed_container.filter(
                seed_container__icontains=seed_container_id)

        seed_container_serializer = SeedContainerSerializer(
            seed_container, many=True)
        return JsonResponse(seed_container_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        seed_container_data = JSONParser().parse(request)
        seed_container_serializer = SeedContainerSerializer(
            data=seed_container_data)
        if seed_container_serializer.is_valid():
            seed_container_serializer.save()
            return JsonResponse(seed_container_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(seed_container_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = SeedContainer.objects.all().delete()
        return JsonResponse({'message': '{} SeedContainers were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def seed_container_detail(request, pk):
    # find seed_container by pk (id)
    try:
        seed_container = SeedContainer.objects.get(pk=pk)
    except SeedContainer.DoesNotExist:
        return JsonResponse({'message': 'The seed_container does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE seed_container
    if request.method == 'GET':
        seed_container_serializer = SeedContainerSerializer(seed_container)
        return JsonResponse(seed_container_serializer.data)

    elif request.method == 'PUT':
        seed_container_data = JSONParser().parse(request)
        seed_container_serializer = SeedContainerSerializer(
            seed_container, data=seed_container_data)
        if seed_container_serializer.is_valid():
            seed_container_serializer.save()
            return JsonResponse(seed_container_serializer.data)
        return JsonResponse(seed_container_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        seed_container.delete()
        return JsonResponse({'message': 'seed_container was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def seed_container_list_name(request):
    # GET all published seed_containers    
    seed_container = SeedContainer.objects.filter(seed_container_name__icontains=JSONParser().parse(request)['seed_container_name'])
    if request.method == 'POST':
        seed_container_serializer = SeedContainerSerializer(
            seed_container, many=True)
        return JsonResponse(seed_container_serializer.data, safe=False)
#
# plant_data
#


@api_view(['GET', 'POST', 'DELETE'])
def plant_data_list(request):
    # GET list of plant_datas, POST a new plant_data, DELETE all plant_datas
    if request.method == 'GET':
        plant_data = PlantData.objects.all()

        plant_data_id = request.GET.get('id', None)
        if plant_data_id is not None:
            plant_data = plant_data.filter(plant_data__icontains=plant_data_id)

        plant_data_serializer = PlantDataSerializer(plant_data, many=True)
        return JsonResponse(plant_data_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        plant_data_data = JSONParser().parse(request)
        plant_data_serializer = PlantDataSerializer(data=plant_data_data)
        if plant_data_serializer.is_valid():
            plant_data_serializer.save()
            return JsonResponse(plant_data_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(plant_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = PlantData.objects.all().delete()
        return JsonResponse({'message': '{} PlantDatas were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def plant_data_detail(request, pk):
    # find plant_data by pk (id)
    try:
        plant_data = PlantData.objects.get(pk=pk)
    except PlantData.DoesNotExist:
        return JsonResponse({'message': 'The plant_data does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE plant_data
    if request.method == 'GET':
        plant_data_serializer = PlantDataSerializer(plant_data)
        return JsonResponse(plant_data_serializer.data)

    elif request.method == 'PUT':
        plant_data_data = JSONParser().parse(request)
        plant_data_serializer = PlantDataSerializer(
            plant_data, data=plant_data_data)
        if plant_data_serializer.is_valid():
            plant_data_serializer.save()
            return JsonResponse(plant_data_serializer.data)
        return JsonResponse(plant_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plant_data.delete()
        return JsonResponse({'message': 'plant_data was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def plant_data_list_published(request):
    # GET all published plant_datas
    plant_data = PlantData.objects.filter(published=True)

    if request.method == 'GET':
        plant_data_serializer = PlantDataSerializer(plant_data, many=True)
        return JsonResponse(plant_data_serializer.data, safe=False)

#
# ambient_data
#


@api_view(['GET', 'POST', 'DELETE'])
def ambient_data_list(request):
    # GET list of ambient_datas, POST a new ambient_data, DELETE all ambient_datas
    if request.method == 'GET':
        ambient_data = AmbientData.objects.all()

        ambient_data_id = request.GET.get('id', None)
        if ambient_data_id is not None:
            ambient_data = ambient_data.filter(
                ambient_data__icontains=ambient_data_id)

        ambient_data_serializer = AmbientDataSerializer(
            ambient_data, many=True)
        return JsonResponse(ambient_data_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        ambient_data_data = JSONParser().parse(request)
        ambient_data_serializer = AmbientDataSerializer(data=ambient_data_data)
        if ambient_data_serializer.is_valid():
            ambient_data_serializer.save()
            return JsonResponse(ambient_data_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(ambient_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = AmbientData.objects.all().delete()
        return JsonResponse({'message': '{} AmbientDatas were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def ambient_data_detail(request, pk):
    # find ambient_data by pk (id)
    try:
        ambient_data = AmbientData.objects.get(pk=pk)
    except AmbientData.DoesNotExist:
        return JsonResponse({'message': 'The ambient_data does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE ambient_data
    if request.method == 'GET':
        ambient_data_serializer = AmbientDataSerializer(ambient_data)
        return JsonResponse(ambient_data_serializer.data)

    elif request.method == 'PUT':
        ambient_data_data = JSONParser().parse(request)
        ambient_data_serializer = AmbientDataSerializer(
            ambient_data, data=ambient_data_data)
        if ambient_data_serializer.is_valid():
            ambient_data_serializer.save()
            return JsonResponse(ambient_data_serializer.data)
        return JsonResponse(ambient_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ambient_data.delete()
        return JsonResponse({'message': 'ambient_data was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ambient_data_latest(request):
    # GET all published ambient_datas
    ambient_data = AmbientData.objects.latest('ambient_data_date_time')

    if request.method == 'GET':
        ambient_data_serializer = AmbientDataSerializer(
            [ambient_data], many=True)
        return JsonResponse(ambient_data_serializer.data, safe=False)

#
# plant_type
#


@api_view(['GET', 'POST', 'DELETE'])
def plant_type_list(request):
    # GET list of plant_types, POST a new plant_type, DELETE all plant_types
    if request.method == 'GET':
        plant_type = AmbientData.objects.all()

        plant_type_id = request.GET.get('id', None)
        if plant_type_id is not None:
            plant_type = plant_type.filter(plant_type__icontains=plant_type_id)

        plant_type_serializer = PlantTypeSerializer(plant_type, many=True)
        return JsonResponse(plant_type_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        plant_type_data = JSONParser().parse(request)
        plant_type_serializer = PlantTypeSerializer(data=plant_type_data)
        if plant_type_serializer.is_valid():
            plant_type_serializer.save()
            return JsonResponse(plant_type_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(plant_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = PlantType.objects.all().delete()
        return JsonResponse({'message': '{} PlantTypes were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def plant_type_detail(request, pk):
    # find plant_type by pk (id)
    try:
        plant_type = PlantType.objects.get(pk=pk)
    except PlantType.DoesNotExist:
        return JsonResponse({'message': 'The plant_type does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE plant_type
    if request.method == 'GET':
        plant_type_serializer = PlantTypeSerializer(plant_type)
        return JsonResponse(plant_type_serializer.data)

    elif request.method == 'PUT':
        plant_type_data = JSONParser().parse(request)
        plant_type_serializer = PlantTypeSerializer(
            plant_type, data=plant_type_data)
        if plant_type_serializer.is_valid():
            plant_type_serializer.save()
            return JsonResponse(plant_type_serializer.data)
        return JsonResponse(plant_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plant_type.delete()
        return JsonResponse({'message': 'plant_type was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def plant_type_list_published(request):
    # GET all published plant_types
    plant_type = PlantType.objects.filter(published=True)

    if request.method == 'GET':
        plant_type_serializer = PlantTypeSerializer(plant_type, many=True)
        return JsonResponse(plant_type_serializer.data, safe=False)

#
# plant
#


@api_view(['GET', 'POST', 'DELETE'])
def plant_list(request):
    # GET list of plants, POST a new plant, DELETE all plants
    if request.method == 'GET':
        plant = AmbientData.objects.all()

        plant_id = request.GET.get('id', None)
        if plant_id is not None:
            plant = plant.filter(plant__icontains=plant_id)

        plant_serializer = PlantSerializer(plant, many=True)
        return JsonResponse(plant_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        plant_data = JSONParser().parse(request)
        plant_serializer = PlantSerializer(data=plant_data)
        if plant_serializer.is_valid():
            plant_serializer.save()
            return JsonResponse(plant_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(plant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Plant.objects.all().delete()
        return JsonResponse({'message': '{} Plants were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def plant_detail(request, pk):
    # find plant by pk (id)
    try:
        plant = Plant.objects.get(pk=pk)
    except Plant.DoesNotExist:
        return JsonResponse({'message': 'The plant does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE plant
    if request.method == 'GET':
        plant_serializer = PlantSerializer(plant)
        return JsonResponse(plant_serializer.data)

    elif request.method == 'PUT':
        plant_data = JSONParser().parse(request)
        plant_serializer = PlantSerializer(plant, data=plant_data)
        if plant_serializer.is_valid():
            plant_serializer.save()
            return JsonResponse(plant_serializer.data)
        return JsonResponse(plant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plant.delete()
        return JsonResponse({'message': 'plant was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def plant_list_published(request):
    # GET all published plants
    plant = Plant.objects.filter(published=True)

    if request.method == 'GET':
        plant_serializer = PlantSerializer(plant, many=True)
        return JsonResponse(plant_serializer.data, safe=False)
