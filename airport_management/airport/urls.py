from django.urls import path
from airport.views import AirportView, AirportDetailedView

urlpatterns = [
    path('airport/', AirportView.as_view()),
    path('airport/<int:pk>/', AirportDetailedView.as_view()),
    # path('aeroplane/', AeroplaneView.as_view()),
    # path('runway/', RunwayView.as_view()),
    # path('flight/', FlightView.as_view()),
]