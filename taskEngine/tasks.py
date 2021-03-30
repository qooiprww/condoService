from farm.models import Plant
from farm.models import Task
from farm.models import PlantData
from farm.models import PlantType
from farm.models import AmbientData
from django.conf import settings
from datetime import datetime
from collections import deque
from celery import shared_task
from celery import app
import paho.mqtt.client as mqtt
import json

taskQueue = deque()


@shared_task
def dataGatheringTask():
    allPlants = Plant.objects.filter(
        harvested='false', planted='true').order_by('degree', 'radius')
    task_serializer = PlantDataSerializer(
        data={'task_type': settings.TASK_AMBIENT_DATA_GATHERING,  'task_status': settings.TASK_STATUS_QUEUED})

    offerTask(task_serializer)
    for plant in allPlants:
        task_serializer = PlantDataSerializer(
            data={'plant_id': plant.id, 'task_type': settings.TASK_PLANT_DATA_GATHERING, 'task_status': settings.TASK_STATUS_QUEUED})
        offerTask(task_serializer)


@shared_task
def offerTask(task_serializer):
    task_serializer.save()
    print(taskQueue)
    if not taskQueue:
        taskQueue.append(task_serializer.data['id'])
        taskHandler()
    else:
        if task_serializer.data['task_type'] == settings.TASK_MANUAL_CONTROL:
            taskQueue.insert(1, task_serializer.data['id'])
        else:
            taskQueue.append(task_serializer.data['id'])


def taskHandler():

    task = Task.objects.get(id=taskQueue[0])
    task.task_status = settings.TASK_STATUS_EXECUTING
    task.save()

    if task.task_type == settings.TASK_WATERING:
        plant = Plant.objects.get(id=task.plant_id)
        plant_type = Plant.objects.get(plant_type=plant.plant_type_id)
        wateringTask(task, plant.degree, plant.radius, plant.level,
                     plant_type.desired_humidity)

    elif task.task_type == settings.TASK_SEEDING:
        plant = Plant.objects.get(id=task.plant_id)
        plant_type = Plant.objects.get(id=plant.plant_type_id)
        seed_container = Plant.objects.get(id=plant.seed_container_id)
        seedingTask(task, plant.degree, plant.radius, plant.level,
                    seed_container.degree, seed_container.radius, seed_container.level)

    elif task.task_type == settings.TASK_PLANT_DATA_GATHERING:
        plant = Plant.objects.get(id=task.plant_id)
        plantDataGatheringTask(
            task, plant.degree, plant.radius, plant.level)

    elif task.task_type == settings.TASK_AMBIENT_DATA_GATHERING:
        ambientDataGatheringTask(task)

    elif task.task_type == settings.TASK_MANUAL_CONTROL:
        plant = Plant.objects.get(id=task.plant_id)
        manualControlTask(
            task, plant.degree, plant.radius, plant.level)

    elif task.task_type == settings.TASK_LIGHTING_CONTROL:
        plant = Plant.objects.get(id=task.plant_id)
        plant_type = PlantType.objects.get(id=plant.plant_type_id)
        lightingControlTask(
            task, plant_type.desired_light_red, plant_type.desired_light_green, plant_type.desired_light_blue)

    else:
        task.task_status = settings.TASK_STATUS_FAILED
        task.save()


def wateringTask(task, degree, radius, level, desired_humidity):

    client.publish('request', json.dumps({'task_id': task.id,
                                          'task_type': task.task_type,
                                          'degree': degree,
                                          'radius': radius,
                                          'level': level,
                                          'target_humidity': desired_humidity}))



def seedingTask(task, degree, radius, level, seed_container_degree, seed_container_radius, seed_container_level):

    client.publish('request', json.dumps({'task_id': task.id,
                                          'task_type': task.task_type,
                                          'degree': degree,
                                          'radius': radius,
                                          'level': level,
                                          'seed_container_degree': seed_container_degree,
                                          'seed_container_radius': seed_container_radius,
                                          'seed_container_level': seed_container_level}))



def plantDataGatheringTask(task, degree, radius, level):

    client.publish('request', json.dumps({'task_id': task.id,
                                          'task_type': task.task_type,
                                          'degree': degree,
                                          'radius': radius,
                                          'level': level}))



def ambientDataGatheringTask(task):

    client.publish('request', json.dumps({'task_id': task.id,
                                          'task_type': task.task_type}))

def manualControlTask(task, degree, radius, level):

    client.publish('request', json.dumps({'task_id': task.id,
                                          'task_type': task.task_type,
                                          'degree': degree,
                                          'radius': radius,
                                          'level': level}))



def lightingControlTask(task, desired_light_red, desired_light_green, desired_light_blue):

    client.publish('request', json.dumps({'task_id': task.id,
                                          'task_type': task.task_type,
                                          'desired_light_red': desired_light_red,
                                          'desired_light_green': desired_light_green,
                                          'desired_light_blue': desired_light_blue}))


# The callback for when a PUBLISH message is received from the server.


def handleResponse(client, userdata, msg):
    print("Received message: " + msg.topic +
          " -> " + msg.payload.decode('utf-8'))

    task_id = taskQueue[0]
    task = Task.objects.get(id=task_id)
    data = json.loads(msg.payload.decode('utf-8'))

    if task.task_type == settings.TASK_WATERING:
        if data['task_id'] == task_id and data['succeeded'] == True:
            task.task_status = settings.TASK_STATUS_FINISHED
            task.save()
        else:
            task.task_status = settings.TASK_STATUS_FAILED
            task.save()

    elif task.task_type == settings.TASK_SEEDING:
        if data['task_id'] == task_id and data['succeeded'] == True:
            task.task_status = settings.TASK_STATUS_FINISHED
            task.save()
            plant = Plant.objects.get(id=task.plant_id)
            plant.planted = True
            plant.save()
        else:
            task.task_status = settings.TASK_STATUS_FAILED
            task.save()

    elif task.task_type == settings.TASK_PLANT_DATA_GATHERING:
        if data['task_id'] == task_id and data['succeeded'] == True:
            task.task_status = settings.TASK_STATUS_FINISHED
            task.save()
            PlantData.objects.create(
                plant=task.plant_id, humidity=data['humidity'])
            plant = Plant.objects.get(id=task.plant_id)
            plant_type = Plant.objects.get(id=plant.plant_type_id)
            if data['humidity'] + settings.WATERING_TASK_THRESHOLD < plant_type.desired_humidity:
                task_serializer = PlantDataSerializer(
                    data={'plant_id': plant.id, 'task_type': settings.TASK_WATERING, 'task_status': settings.TASK_STATUS_QUEUED})
                offerTask(task_serializer)
        else:
            task.task_status = settings.TASK_STATUS_FAILED
            task.save()

    elif task.task_type == settings.TASK_AMBIENT_DATA_GATHERING:
        if data['task_id'] == task_id and data['succeeded'] == True:
            task.task_status = settings.TASK_STATUS_FINISHED
            task.save()
            AmbientData.objects.create(ambient_humidity=data['ambient_humidity'],
                                       ambient_light_intensity=data['ambient_light_intensity'], ambient_temperature=data['ambient_temperature'])
            print("created data")
        else:
            task.task_status = settings.TASK_STATUS_FAILED
            task.save()

    elif task.task_type == settings.TASK_MANUAL_CONTROL:
        if data['task_id'] == task_id and data['succeeded'] == True:
            task.task_status = settings.TASK_STATUS_FINISHED
            task.save()
        else:
            task.task_status = settings.TASK_STATUS_FAILED
            task.save()

    elif task.task_type == settings.TASK_LIGHTING_CONTROL:
        if data['task_id'] == task_id and data['succeeded'] == True:
            task.task_status = settings.TASK_STATUS_FINISHED
            task.save()
        else:
            task.task_status = settings.TASK_STATUS_FAILED
            task.save()

    taskQueue.popleft()
    if taskQueue:
        taskHandler()


# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = handleResponse

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set(settings.HIVEMQ_USERNAME, settings.HIVEMQ_PASSWORD)

# connect to HiveMQ Cloud on port 8883

client.connect("84da454f982d4061a3e9339908532687.s1.eu.hivemq.cloud", 8883)
client.subscribe('response')

client.loop_start()