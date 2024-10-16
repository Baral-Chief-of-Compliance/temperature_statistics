from django.urls import path
from django.contrib.auth.decorators import login_required
from temperature_statistics_app.views import TownListView, TownFormView, AuthenticationFormView, TownDeleteView, TownUpdateView, TownDetailView
from temperature_statistics_app.views import TemperatueFormView, TemperatureDeleteView, TemperatureUpdateView, DayTemperatureFormView, DayTemperatureDetailView
from django.contrib.auth.views import LogoutView

app_name = 'tmp_stat_app'

urlpatterns = [
    path('', TownListView.as_view(), name='index'),
    path('towns/', TownFormView.as_view(), name='add_town'),
    path('login/', AuthenticationFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('towns/<int:pk>/delete/',TownDeleteView.as_view(), name='delete_town'),
    path('towns/<int:pk>/update/', TownUpdateView.as_view(), name='update_town'),
    path('towns/<int:pk>/', TownDetailView.as_view(), name='detail_town'),
    path('towns/<int:pk>/add-temperature/', TemperatueFormView.as_view(), name='add_temperature'),
    path('towns/<int:pk>/delete-tmp/<int:tmp_id>/', TemperatureDeleteView.as_view(), name='delete_temperature'),
    path('towns/<int:pk>/update-tmp/<int:tmp_id>/', TemperatureUpdateView.as_view(), name='update_temperature'),
    path('towns/<int:pk>/tmp-stat/', DayTemperatureFormView.as_view(), name='set_tmp_date'),
    path('towns/<int:pk>/tmp-stat/<int:day>-<int:month>-<int:year>/', DayTemperatureDetailView.as_view(), name='day_tmp_chart')
]