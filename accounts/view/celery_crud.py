import pytz
from celery.schedules import solar
from django_celery_beat.models import (
    PeriodicTask, CrontabSchedule,
    IntervalSchedule, SolarSchedule,
    ClockedSchedule,
)
from rest_framework import viewsets, permissions, status, pagination
from rest_framework.response import Response
from celery import current_app
from accounts.serializers import (
    PeriodicTaskSerializer, CrontabScheduleSerializer,
    IntervalScheduleSerializer, SolarScheduleSerializer,
    ClockedScheduleSerializer
)


class DynamicPagination(pagination.PageNumberPagination):
    page_size = 10


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PeriodicTaskSerializer
    queryset = PeriodicTask.objects.all().order_by('-id')
    pagination_class = DynamicPagination

    def list(self, request, *args, **kwargs):
        try:
            res = super(PeriodicTaskViewSet, self).list(request).data
            return Response(
                {
                    "success": True,
                    "message": "Periodic Tasks Listed Successfully",
                    "data": res,
                 }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            res = super(PeriodicTaskViewSet, self).create(request, *args, **kwargs).data
            return Response(
                {
                    "success": True,
                    "message": "Periodic Task Created Successfully",
                    "data": res,
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            if PeriodicTask.objects.filter(id=object.id).exists():
                PeriodicTask.objects.get(id=object.id).delete()
                return Response(
                    {
                        "success": True,
                        "message": "Periodic Task Data Deleted Successfully",
                        "data": "",
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Periodic Task Data Not Found",
                        "data": "",
                    }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            res = super(PeriodicTaskViewSet, self).update(request, *args, **kwargs).data
            return Response({
                "success": True,
                "message": "Periodic Task Data Updated Successfully",
                "data": res,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)


class GetTimeZoneList(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        try:
            timezone_list = pytz.common_timezones
            return Response(
                {
                    "success": True,
                    "message": "Timezone List",
                    "data": timezone_list,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)


class CrontabTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CrontabScheduleSerializer
    queryset = CrontabSchedule.objects.all().order_by('-id')
    pagination_class = DynamicPagination

    def list(self, request, *args, **kwargs):
        try:
            res = super(CrontabTaskViewSet, self).list(request, *args, **kwargs)
            return Response(
                {
                    "success": True,
                    "message": "Crontab Task Listed Successfully",
                    "data": res.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            res = super(CrontabTaskViewSet, self).create(request, *args, **kwargs)
            return Response(
                {
                    "success": True,
                    "message": "Crontab Schedule Created Successfully",
                    "data": res.data,
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            if CrontabSchedule.objects.filter(id=object.id).exists():
                CrontabSchedule.objects.get(id=object.id).delete()
                return Response(
                    {
                        "success": True,
                        "message": "Crontab Schedule Data Deleted Successfully",
                        "data": "",
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Crontab Task Data Not Found",
                        "data": "",
                    }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            res = super(CrontabTaskViewSet, self).update(request, *args, **kwargs).data
            return Response(
                {
                    "success": True,
                    "message": "Crontab Schedule Data Updated Successfully",
                    "data": res,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)


class IntervalPeriod(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        try:
            period = []
            for i in IntervalSchedule.PERIOD_CHOICES:
                period.append(i[0])
            return Response(
                {
                    "success": True,
                    "message": "Interval Periods Listed Successfully",
                    "data": period,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)


class IntervalTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = IntervalScheduleSerializer
    queryset = IntervalSchedule.objects.all().order_by('-id')
    pagination_class = DynamicPagination

    def list(self, request, *args, **kwargs):
        try:
            res = super(IntervalTaskViewSet, self).list(request).data
            return Response(
                {
                    "success": True,
                    "message": "Interval Schedule Data listed successfully",
                    'data': res,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            res = super(IntervalTaskViewSet, self).create(request, *args, **kwargs).data
            return Response(
                {
                    "success": True,
                    "message": "Interval Task created Successfully",
                    'data': res,
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            if IntervalSchedule.objects.filter(id=object.id).exists():
                IntervalSchedule.objects.filter(id=object.id).delete()
                return Response(
                    {
                        "success": True,
                        "message": "Interval Schedule Deleted Successfully",
                        "data": "",
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Interval Schedule Does Not Exist",
                        "data": "",
                    }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            res = super(IntervalTaskViewSet, self).update(request, *args, **kwargs).data
            return Response(
                {
                    "success": True,
                    "message": "Interval Schedule Updated Successfully",
                    "data": res,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)


class SolarEvent(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny, ]

    def list(self, request):
        try:
            events = solar._all_events
            return Response(
                {
                    "success": True,
                    "message": "Solar Schedule Events",
                    "data": events,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)


class SolarTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = SolarScheduleSerializer
    queryset = SolarSchedule.objects.all().order_by('-id')
    pagination_class = DynamicPagination

    def list(self, request, *args, **kwargs):
        try:
            res = super(SolarTaskViewSet, self).list(request, *args, **kwargs)
            return Response(
                {
                    "success": True,
                    "message": "Solar Schedule Data Listed Successfully",
                    "data": res.data,
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            res = super(SolarTaskViewSet, self).create(request, *args, **kwargs)
            return Response(
                {
                    "success": True,
                    "message": "Solar Schedule Created Successfully",
                    'data': res.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": [],
                }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            if SolarSchedule.objects.filter(id=object.id).exists():
                SolarSchedule.objects.filter(id=object.id).delete()
                return Response(
                    {
                        "success": True,
                        "message": "Solar Schedule Deleted Successfully",
                        "data": "",
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Solar Schedule Does Not exist",
                        "data": "",
                    }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            res = super(SolarTaskViewSet, self).update(request, *args, **kwargs).data
            return Response(
                {
                    "success": True,
                    "message": "Solar Schedule Updated Successfully",
                    "data": res,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)


class ClockedTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ClockedScheduleSerializer
    queryset = ClockedSchedule.objects.all().order_by('-id')
    pagination_class = DynamicPagination

    def create(self, request, *args, **kwargs):
        try:
            res = super(ClockedTaskViewSet, self).create(request, *args, **kwargs)
            return Response(
                {
                    "success": True,
                    "message": "Clocked Schedule Created Successfully",
                    'data': res.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            res = super(ClockedTaskViewSet, self).list(request, *args, **kwargs)
            return Response(
                {
                    "success": True,
                    "message": "Clocked Schedule Listed Successfully.",
                    "data": res.data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            if ClockedSchedule.objects.filter(id=object.id).exists():
                ClockedSchedule.objects.filter(id=object.id).delete()
                return Response(
                    {
                        "success": True,
                        "message": "Clocked Schedule Deleted Successfully",
                        "data": "",
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Clocked Schedule Does Not exist",
                        "data": "",
                    }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            res = super(ClockedTaskViewSet, self).update(request, *args, **kwargs).data
            return Response(
                {
                    "success": True,
                    "message": "Clocked Schedule Updated Successfully",
                    "data": res,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)


class GetRegisteredTaskViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        try:
            current_app.loader.import_default_modules()
            tasks = list(sorted(name for name in current_app.tasks if not name.startswith('celery.')))
            return Response(
                {
                    "success": True,
                    "message": "Registered Tasks Fetched Successfully",
                    "data": tasks,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": e.args[0],
                    "data": "",
                }, status=status.HTTP_400_BAD_REQUEST)
