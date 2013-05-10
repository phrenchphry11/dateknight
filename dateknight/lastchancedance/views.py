from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from form import AddCrush, DeleteCrush
from models import Student
from utils import carl_to_dict

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
                return redirect("/dashboard/")
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
    add_crush = AddCrush()
    delete_crush = DeleteCrush()

    if "add_crush" in request.POST:
        add_crush = AddCrush(request.POST)
        if add_crush.is_valid():
            pass

    if "delete_crush" in request.POST:
        delete_crush = DeleteCrush(request.POST)
        if delete_crush.is_valid():
            pass

    carl = carl_to_dict(request.user.carl)
    carl['crushed_on'] = request.user.carl.crushed_on

    crushes = request.user.carl.out_crushes.all().filter(deleted=False)
    crush_list = [carl_to_dict(crush.chicken) for crush in crushes]

    recommendations = [carl_to_dict(r) for r in make_recommendations(request.user.carl)]

    matches = Match.objects.filter(egg=request.user.carl)
    match_list = [carl_to_dict(match.chicken) for match in matches]

    page_data = {'crushes': crush_list, 'suggestions': recommendations, 'matches': match_list, 'me': carl}
    return render_to_response("dashboard.html", page_data, RequestContext(request))

def logout_view(request):
    logout(request)
    return redirect('/')
