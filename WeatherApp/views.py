from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
import requests
from django.contrib import messages

# Create your views here.
def home(request):
    '''URL for accessing the OpenWeatherMap API to get weather information based on a city'''
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},&appid=b45d5fa6f08c270e3d043efa18bd610e&units=metric'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            NewCity = form.cleaned_data['name']
            CreateCity = City.objects.filter(name=NewCity).count()
            if CreateCity == 0:
                res = requests.get(url.format(NewCity)).json()
                if res['cod'] == 200:
                    form.save()
                    messages.success(request," "+ NewCity +" Added Successfully...")
                else:
                    messages.error(request,"City Does Not Exist...")
            else:
                messages.error(request,"City Already Exits...")
                
    form = CityForm()
    cities = City.objects.all()
    data = []
    for city in cities:
        res = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city,
            'temperature' : res['main']['temp'],
            'description' : res['weather'][0]['description'],
            'country' : res['sys']['country'],
            'icon' : res['weather'][0]['icon'] 
        }
        data.append(city_weather)
    context = {'data':data,'form':form}
    return render(request,"home.html",context)

def delete_city(request,CityName):
    City.objects.get(name=CityName).delete()
    messages.success(request," "+CityName+" Removed Successfully...!!!")
    return redirect('Home')