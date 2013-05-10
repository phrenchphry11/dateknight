from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from models import Student


@transaction.commit_manually()
def index(request):
    if request.user.is_authenticated():
        transaction.commit()
        return redirect("/dashboard/")

    if request.method == "GET":
        transaction.commit()
        return render_to_response("index.html", None, RequestContext(request))

    if request.POST["username"] and request.POST["password"]:
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            transaction.commit()
            return redirect("/dashboard/")

        else:
            try:
                carl = Student.objects.get(carlnetid=request.POST['username'])
            except Student.DoesNotExist:
                transaction.rollback()
                return render_to_response("index.html", {'worked': 'false', 'error': 'invalid_carl'}, RequestContext(request))

            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                email=request.POST['username']+'@carleton.edu',
                                                password=request.POST['password'])
                user.save()
                carl.user = user
                carl.save()
                transaction.commit()
            except Exception:
                transaction.rollback()
                return render_to_response("index.html", {'worked': 'false', 'error': 'invalid_login'}, RequestContext(request))

            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user)
                transaction.commit()
                return redirect('dashboard/')
            else:
                transaction.rollback()
                return render_to_response("index.html", {'worked': 'false', 'error': 'invalid_login'}, RequestContext(request))

    if request["worked"] == "false":
        transaction.rollback()
        return render_to_response("index.html", {'worked': 'false'}, RequestContext(request))
    else:
        transaction.rollback()
        return render_to_response("index.html", None, RequestContext(request))

@login_required
def confirm(request):
    return HttpResponseRedirect("/confirm/")

@login_required
def dashboard(request):
    pass

def logout_view(request):
    logout(request)
    return redirect('/')
