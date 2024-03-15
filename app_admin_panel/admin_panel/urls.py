from django.urls import path
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='admin'), name='redirect_to_admin'),
]
