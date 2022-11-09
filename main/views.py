from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.recommend_sys import main
from .models import Preference, PreferenceForm
from .models import Trip
from amadeus import Client, ResponseError


# Create your views here.

def index(request):

    context = {}

    return render(request, 'main/index.html', context)

@login_required(login_url='/accounts/signin/')
def update_preference(request):
    try:
        traveler = request.user.traveler.preference
    except:
        traveler = request.user.traveler

    form = PreferenceForm(request.POST or None, instance=traveler)

    context = {'form': form}

    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            try:
                f = form.save(commit=False)
                f.traveler = request.user.traveler
                f.save()

            except:
                traveler = Preference.objects.get(traveler_id=request.user.traveler.id)
                traveler.depart_date=form.cleaned_data['depart_date']
                traveler.return_date=form.cleaned_data['return_date']
                traveler.budget=form.cleaned_data['budget']
                traveler.point_of_interest=form.cleaned_data['point_of_interest']
                traveler.on_season=form.cleaned_data['on_season']
                traveler.save()
        #     except:
        #         Preference.objects.create(
        #         traveler_id=traveler.id,
        #         depart_date=form.cleaned_data['depart_date'],
        #         return_date=form.cleaned_data['return_date'],
        #         budget=form.cleaned_data['budget'],
        #         point_of_interest=form.cleaned_data['point_of_interest'],
        #         on_season=form.cleaned_data['on_season'])


            return redirect('index')
        return render(request, 'main/update_preference.html', {'form': form})
    return render(request, 'main/update_preference.html', context)

@login_required(login_url='/accounts/signin/')
def hotels(request, c_code):
    amadeus = Client(
        client_id='kXwip4ajLF3GZ1LYwNyE5LADVLprotR6',
        client_secret='S6v7ukGgHGOfR6Zf'
    )

    try:
        '''
        Get list of hotels by city code
        '''
        trip = Trip.objects.get(city_code=c_code)
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=trip.city_code)
        context = {'response':response, 'trip':trip}

    except ResponseError as error:
        print(error)
        context = {}
        
        @property
        def link(self):
            return self.name.replace("", "-")

    return render(request, 'main/hotels.html', context)

@login_required(login_url='/accounts/signin/')
def recommender(request):
    try:
        traveler_p = request.user.traveler.preference
        context = {'traveler':traveler_p}
    except:
        new = True
        context = {'new':new}
    
    
    trip = Trip.objects.get(city_code='Test')
    if request.POST.get('Next') == 'Next':
        trip.info = traveler_p.point_of_interest
        trip.save()
        recommend_trip, graphic = main()
        recommend_trips = []
        for i in recommend_trip['Countries']:
            trip = Trip.objects.get(name=i)
            recommend_trips.append(trip)
        print(recommend_trips)
        context = {'traveler':traveler_p, 'recommend':recommend_trips, 'graphic':graphic}
        return render(request, 'main/recommend.html', context)
    
    return render(request, 'main/recommend.html', context)