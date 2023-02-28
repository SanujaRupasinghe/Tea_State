from django.urls import path
from . import views

urlpatterns = [
    path('Data/', views.data, name='data'),
    path('progress/', views.progress, name='progress'),
    path('analysis/', views.analysis, name='analysis'),
    path('map/', views.maps, name='map'),
    path('calender/', views.calender, name='calender'),
    path('reminder/', views.reminder, name='reminder'),
    path('Employees/', views.emps, name='emps'),
    path('Works/', views.works, name='works'),
    path('works_Details/<int:work_id>', views.works_details, name='works_details'),
]
