from rest_framework import serializers

from materials.models import EducationModule, Lesson, Subscription
from materials.validator import URLValidator


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationModule
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [URLValidator(url='URL')]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
