from django.contrib import admin
from .models import Town, Temperature


#отображение в админ панели модели для города
@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ("t_name", "t_user",)
    search_fields = ("t_name", "t_user",)
    save_on_top = True
    save_as = True


#отображение в админ панели модели для температуры
@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    list_display = ("tmp_town", "tmp_date", "tmp_value")
    search_fields = ("tmp_town", "tmp_date",)
    save_on_top = True
    save_as = True 


