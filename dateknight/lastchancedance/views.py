# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return HttpResponse("Hello.  Let us help you find luv here.")

def confirm(request):
	return HttpResponseRedirect("/confirm/")