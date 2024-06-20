from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import EducationModule, Lesson, Subscription
from materials.serializers import MaterialSerializer, LessonSerializer, SubscriptionSerializer

# Create your views here.


class MaterialsListAPIView(ListAPIView):
    serializer_class = MaterialSerializer
    queryset = EducationModule.objects.all()


class MaterialsCreateAPIView(CreateAPIView):
    serializer_class = MaterialSerializer


class MaterialsUpdateAPIView(UpdateAPIView):
    serializer_class = MaterialSerializer
    queryset = EducationModule.objects.all()


class MaterialsDeleteAPIView(DestroyAPIView):
    queryset = EducationModule.objects.all()


class MaterialsRetrieveAPIView(RetrieveAPIView):
    serializer_class = MaterialSerializer
    queryset = EducationModule.objects.all()


class LessonsListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonsCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonsUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonsDeleteAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()


class LessonsRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(EducationModule, pk=course_id)
        subs_item = Subscription.objects.all().filter(user=user).filter(course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка отключена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка включена'
        return Response({"message": message})
