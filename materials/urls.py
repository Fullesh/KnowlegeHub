from django.urls import path

from materials.apps import MaterialsConfig
from materials.views import MaterialsListAPIView, MaterialsCreateAPIView, MaterialsRetrieveAPIView, \
    MaterialsUpdateAPIView, MaterialsDeleteAPIView, LessonsListAPIView, LessonsCreateAPIView, LessonsUpdateAPIView, \
    LessonsRetrieveAPIView, LessonsDeleteAPIView, SubscriptionAPIView

app_name = MaterialsConfig.name
urlpatterns = [
    path('', MaterialsListAPIView.as_view(), name='home'),
    path('view/<int:pk>/', MaterialsRetrieveAPIView.as_view(), name='materials_detail'),
    path('create/', MaterialsCreateAPIView.as_view(), name='materials_create'),
    path('edit/<int:pk>/', MaterialsUpdateAPIView.as_view(), name='materials_update'),
    path('delete/<int:pk>/', MaterialsDeleteAPIView.as_view(), name='materials_delete'),
    path('subscribe/', SubscriptionAPIView.as_view(), name='materials_subscribe'),
    # CRUD для уроков
    path('lessons/', LessonsListAPIView.as_view(), name='lessons_list'),
    path('lessons/create/', LessonsCreateAPIView.as_view(), name='lessons_create'),
    path('lessions/<int:pk>/', LessonsRetrieveAPIView.as_view(), name='lessons_detail'),
    path('lessons/update/<int:pk>/', LessonsUpdateAPIView.as_view(), name='lessons_update'),
    path('lessons/delete/<int:pk>/', LessonsDeleteAPIView.as_view(), name='lessons_delete'),
]
