from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import EducationModule, Lesson, Subscription
from materials.paginators import LessonPaginator, EducationModulePaginator
from materials.serializers import MaterialSerializer, LessonSerializer, SubscriptionSerializer

# Create your views here.


class MaterialsListAPIView(ListAPIView):
    serializer_class = MaterialSerializer
    queryset = EducationModule.objects.all()
    pagination_class = EducationModulePaginator


class MaterialsCreateAPIView(CreateAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [IsAdminUser]

class MaterialsUpdateAPIView(UpdateAPIView):
    serializer_class = MaterialSerializer
    queryset = EducationModule.objects.all()
    permission_classes = [IsAdminUser]


class MaterialsDeleteAPIView(DestroyAPIView):
    queryset = EducationModule.objects.all()
    permission_classes = [IsAdminUser]


class MaterialsRetrieveAPIView(RetrieveAPIView):
    serializer_class = MaterialSerializer
    queryset = EducationModule.objects.all()


class LessonsListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator


class LessonsCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser]


class LessonsUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser]


class LessonsDeleteAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser]


class LessonsRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    @swagger_auto_schema(request_body=SubscriptionSerializer)
    def post(self, *args, **kwargs):
        user = self.request.user
        module_id = self.request.data.get('module')
        module = get_object_or_404(EducationModule, pk=module_id)
        subs_item = Subscription.objects.all().filter(user=user).filter(module=module)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка отключена'
        else:
            Subscription.objects.create(user=user, module=module)
            message = 'Подписка включена'
        return Response({"message": message})
