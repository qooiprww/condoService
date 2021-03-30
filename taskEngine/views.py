from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from taskEngine.tasks import taskQueue
from farm.models import Task
from farm.farmSerializer import TaskSerializer

import json

@api_view(['GET'])
def get_current_task(request):
    if request.method == 'GET':
        if taskQueue:
            task = Task.objects.get(id=taskQueue[0])
            # 'safe=False' for objects serialization
            task_serializer = TaskSerializer([task], many=True)
            return JsonResponse(task_serializer.data, safe=False)
        else:
            return JsonResponse("empty", safe=False)

@api_view(['GET'])
def get_next_task(request):
    if request.method == 'GET':
        if len(taskQueue) > 1:
            task = Task.objects.get(id=taskQueue[1])
            # 'safe=False' for objects serialization
            task_serializer = TaskSerializer([task], many=True)
            return JsonResponse(task_serializer.data, safe=False)
        else:
            return JsonResponse("empty", safe=False)

@api_view(['GET'])
def get_task_queue_length(request):
    # GET list of tasks, POST a new task, DELETE all tasks
    if request.method == 'GET':
        return JsonResponse(len(taskQueue), safe=False)
