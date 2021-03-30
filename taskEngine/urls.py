from django.conf.urls import url 
from taskEngine import views 
 
urlpatterns = [ 
    url(r'^api/taskEngine/current$', views.get_current_task),
    url(r'^api/taskEngine/next$', views.get_next_task),
    url(r'^api/taskEngine/all$', views.get_task_queue_length),
]