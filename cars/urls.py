from django.urls import path
from cars.views  import CarView


urlpatterns = [
    path('', CarView.as_view()),
    path('/tire', CarView.as_view()),
]