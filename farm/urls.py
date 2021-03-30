from django.conf.urls import url 
from farm import views 
 
urlpatterns = [ 
    url(r'^api/farm/task$', views.task_list),
    url(r'^api/farm/task/(?P<pk>[0-9]+)$', views.task_detail),
    #url(r'^api/farm/task/published$', views.task_list_published),

    url(r'^api/farm/seed_container$', views.seed_container_list),
    url(r'^api/farm/seed_container/(?P<pk>[0-9]+)$', views.seed_container_detail),
    url(r'^api/farm/seed_container/name$', views.seed_container_list_name),
    #url(r'^api/farm/seed_container/published$', views.seed_container_list_published),

    url(r'^api/farm/plant_data$', views.plant_data_list),
    url(r'^api/farm/plant_data/(?P<pk>[0-9]+)$', views.plant_data_detail),
    #url(r'^api/farm/plant_data/(?P<pk>[0-9]+)/latest$', views.plant_data_latest),

    url(r'^api/farm/ambient_data$', views.ambient_data_list),
    url(r'^api/farm/ambient_data/(?P<pk>[0-9]+)$', views.ambient_data_detail),
    url(r'^api/farm/ambient_data/latest$', views.ambient_data_latest),

    url(r'^api/farm/plant_type$', views.plant_type_list),
    url(r'^api/farm/plant_type/(?P<pk>[0-9]+)$', views.plant_type_detail),
    #url(r'^api/farm/plant_type/published$', views.plant_type_list_published),

    url(r'^api/farm/plant$', views.plant_list),
    url(r'^api/farm/plant/(?P<pk>[0-9]+)$', views.plant_detail),
    #url(r'^api/farm/plant/published$', views.plant_list_published),
]