from django.urls import path
from accounts.view.customer import (
    SignUpCustomer, LoginUser,
    ListUser, UpdateDeleteUser
)

urlpatterns = [
    path('signup/', SignUpCustomer.as_view(), name='signup'),
    path('login/', LoginUser.as_view(), name='login'),
    path("list/", ListUser.as_view(), name="list"),
    path('delete/', UpdateDeleteUser.as_view(), name='delete'),
    path('update/', UpdateDeleteUser.as_view(), name='update'),
]
