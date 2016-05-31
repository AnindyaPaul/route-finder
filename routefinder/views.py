from django.shortcuts import render
from routefinder.utilities import init,find_districts
# Create your views here.
def index(request):
    cities = find_districts()
    return render(request, "index.html", {'cities':cities})

def route(request):
    print request.GET['src']
    print request.GET['des']
    print request.GET['param']
    paths = init(request.GET['src'],request.GET['des'],request.GET['param'])
    return render(request, "route.html", paths)