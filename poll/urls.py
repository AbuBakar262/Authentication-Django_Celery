from django.urls import path
from poll.views import CreatePollView


urlpatterns = [
    path('create_poll/', CreatePollView.as_view({"post": "create_poll"}), name='create_poll'),
]