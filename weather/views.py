import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from django.views.generic.edit import DeleteView


def index(request):
    appid = 'f7acec38a465338815dfedfbd0ceee12'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid


    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if res.get('main'):
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"]
            }

            all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form
    }

    return render(request, 'weather/index.html', context)

def delete_city(request, city_name):
    City.objects.filter(name=city_name).delete()
    return redirect('home')
