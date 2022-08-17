from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from poll.serializers import PollSerializer
from poll.models import Poll


class CreatePollView(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PollSerializer

    def create_poll(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "Poll Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            res = super(CreatePollView, self).list(request, args, kwargs).data
            return Response({
                "success": True,
                "message": 'All Poll Listed Successfully',
                "data": res
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
