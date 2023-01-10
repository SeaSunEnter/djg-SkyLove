from django.urls import path
from . import views

app_name = 'action'

urlpatterns = [

  # Treatment Routes
  path('treatment/overview', views.treatment_overview, name='treatment_overview'),
  path('treatment/new/', views.TreatmentNew.as_view(), name='treatment_new'),
  path('treatment/<int:pk>/view/', views.TreatmentView.as_view(), name='treatment_view'),
  path('treatment/<int:pk>/update/', views.TreatmentUpdate.as_view(), name='treatment_update'),
  path('treatment/<int:pk>/append/', views.TreatmentAppend.as_view(), name='treatment_append'),
  # path('treatment/<int:pk>/delete/', views.TreatmentTag_Delete.as_view(), name='treatment_delete'),

  path('treatmentpro/<int:pk>/update/', views.TreatmentProcessUpdate.as_view(), name='treatmentpro_update'),
  path('treat_img_delete/<int:pk>/<int:img_tag>',
       views.treatment_process_update_delete,
       name='treatmentpro_update_delete'),

  # Consulting Routes
  path('consultant/overview', views.consulting_overview, name='consultant_overview'),
  path('consultant/new/', views.ConsultingNew.as_view(), name='consultant_new'),
  path('consultant/<int:pk>/view/', views.ConsultingView.as_view(), name='consultant_view'),
  path('consultant/<int:pk>/update/', views.ConsultingUpdate.as_view(), name='consultant_update'),

]
