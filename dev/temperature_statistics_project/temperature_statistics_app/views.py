from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import ListView, FormView, DeleteView, UpdateView, DetailView
from temperature_statistics_app.models import Town, Temperature
from temperature_statistics_app.forms import TownForm, AuthenticationForm, TemperatureForm, DayTemperatureForm 
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  HttpResponseRedirect


#список городов
class TownListView(LoginRequiredMixin, ListView):
    login_url = 'tmp_stat_app:login'
    model=Town
    template_name='town_list.html'
    context_object_name='town_list'

    def get_queryset(self):
        town = Town.objects.filter(t_user=self.request.user)
        return town
    

#добавление города пользователем в бд
class TownFormView(LoginRequiredMixin, FormView):
    login_url = 'tmp_stat_app:login'

    template_name = 'town_form.html'
    form_class = TownForm
    success_url = reverse_lazy('tmp_stat_app:index')

    def form_valid(self, form):
        Town.objects.create(
            t_name=form.cleaned_data['t_name'], 
            t_user=self.request.user
        )
        return super().form_valid(form)
    

#удаление города из бд
class TownDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'tmp_stat_app:login'

    model = Town
    template_name = 'delete_town.html'
    context_object_name = 'town'
    success_url = reverse_lazy('tmp_stat_app:index')

    def get_queryset(self):
        town = Town.objects.filter(t_user=self.request.user)
        return town
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj


#редактирование города 
class TownUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'tmp_stat_app:login'

    model = Town
    form_class = TownForm
    template_name = 'update_town.html'
    context_object_name = 'town'
    success_url = reverse_lazy('tmp_stat_app:index')

    def get_queryset(self):
        town = Town.objects.filter(t_user=self.request.user)
        return town
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj


#получить температуру в городе
class TownDetailView(LoginRequiredMixin, DetailView):
    login_url = 'tmp_stat_app:login'

    model = Town
    template_name = 'detail_town.html'
    context_object_name = 'town'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            temperatures = Temperature.objects.filter(
                tmp_town__id=self.kwargs['pk'],
                tmp_town__t_user=self.request.user
                )
            context['temperatures'] = temperatures
            context['temperatures_for_chart'] = temperatures.order_by('tmp_date')
            
        except Temperature.DoesNotExist:
            pass
        return context
    

#добавление температуры конкретного города
class TemperatueFormView(LoginRequiredMixin, FormView):
    login_url = 'tmp_stat_app:login'

    template_name = 'add_temperature.html'
    form_class = TemperatureForm

    def get_queryset(self):
        towns = Town.objects.filter(t_user=self.request.user)
        return towns
    
    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        context = super().get_context_data(**kwargs)
        town = get_object_or_404(queryset, pk=self.kwargs['pk'])
        context['town'] = town
        return context

    def form_valid(self, form):
        Temperature.objects.create(
            tmp_town=Town.objects.get(pk=self.kwargs['pk']),
            tmp_date=form.cleaned_data['tmp_date'], 
            tmp_value=form.cleaned_data['tmp_value']
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('tmp_stat_app:detail_town', kwargs={'pk': self.kwargs['pk']})
    

#удаление одного показателя температуры города 
class TemperatureDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'tmp_stat_app:login'

    model = Temperature
    template_name = 'delete_temperature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        town = get_object_or_404(
            Town, 
            pk=self.kwargs['pk'],
            t_user=self.request.user
            )
        context['town'] = town
        return context
    
    def get_queryset(self):
        temperatures = Temperature.objects.filter(
            tmp_town__id=self.kwargs['pk'],
            tmp_town__t_user=self.request.user
            )
        return temperatures
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['tmp_id'])
        return obj
    
    def get_success_url(self) -> str:
        return reverse_lazy('tmp_stat_app:detail_town', kwargs={'pk': self.kwargs['pk']})
    

#редактирование температуры города
class TemperatureUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'tmp_stat_app:login'

    model = Temperature
    form_class = TemperatureForm
    template_name = 'update_temperature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        town = get_object_or_404(
            Town, 
            pk=self.kwargs['pk'],
            t_user=self.request.user
            )
        context['town'] = town
        return context
    
    def get_queryset(self):
        temperatures = Temperature.objects.filter(
            tmp_town__id=self.kwargs['pk'],
            tmp_town__t_user=self.request.user
            )
        return temperatures

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['tmp_id'])
        return obj
    
    def get_success_url(self) -> str:
        return reverse_lazy('tmp_stat_app:detail_town', kwargs={'pk': self.kwargs['pk']})
    

#форма для получения графика температуры за конкретную дату
class DayTemperatureFormView(LoginRequiredMixin, FormView):
    login_url = 'tmp_stat_app:login'

    template_name = 'town_day_temperature_form.html'
    form_class = DayTemperatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        town = get_object_or_404(
            Town, 
            pk=self.kwargs['pk'],
            t_user=self.request.user
            )
        context['town'] = town
        return context

    def form_valid(self, form):
        self.form = form
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self) -> str:
        day = self.form.cleaned_data['tmp_date'].day
        month = self.form.cleaned_data['tmp_date'].month
        year = self.form.cleaned_data['tmp_date'].year
        return reverse_lazy(
            'tmp_stat_app:day_tmp_chart', 
            kwargs={
                'pk': self.kwargs['pk'],
                'day': day,
                'month': month,
                'year': year
            }
            )
    

#отображение графика с температурами за конкретную дату
class DayTemperatureDetailView(LoginRequiredMixin, DetailView):
    login_url = 'tmp_stat_app:login'
    template_name = 'town_day_temperature.html'
    model = Town

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        town = get_object_or_404(
            Town, 
            pk=self.kwargs['pk'],
            t_user=self.request.user
            )
        context['town'] = town
        context['date'] = f"{self.kwargs['day']}.{self.kwargs['month']}.{self.kwargs['year']}"
        context['temperatures'] = Temperature.objects.filter(
            tmp_town__id=self.kwargs['pk'],
            tmp_town__t_user=self.request.user,
            tmp_date__day=self.kwargs['day'],
            tmp_date__month=self.kwargs['month'],
            tmp_date__year=self.kwargs['year']
        ).order_by('tmp_date')
        return context


#авторизации
class AuthenticationFormView(LoginView):
    template_name = 'authentication_page.html'
    authentication_form = AuthenticationForm
    next_page = 'tmp_stat_app:index'