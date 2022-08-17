from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule, SolarSchedule, ClockedSchedule
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            message = 'Email Already Exists'
            raise serializers.ValidationError(_(message))
        return attrs

    def create(self, validated_data):
        obj = User.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
        )
        obj.set_password(validated_data.get('password'))
        obj.save()
        return obj


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['email'] = self.user.email
        data['password'] = self.user.password

        return data


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_customer', 'is_superuser']


class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'


class CrontabScheduleSerializer(serializers.ModelSerializer):
    timezone = serializers.SerializerMethodField('get_timezone')

    class Meta:
        model = CrontabSchedule
        fields = '__all__'


class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class SolarScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarSchedule
        fields = '__all__'


class ClockedScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockedSchedule
        fields = '__all__'


class UpdateDeleteUserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id']
