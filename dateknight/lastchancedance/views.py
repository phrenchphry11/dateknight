# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello.  Let us help you find luv here.")