from django.urls import path
from .views import first_task

urlpatterns = [
    path('', first_task, name='first_task')
]
