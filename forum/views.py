__author__ = 'Milena Farfulowska'

from django.http import HttpResponse
from django.template import loader, RequestContext
from forum.models import Category, User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forum.forms import ThreadForm, UserForm1, UserForm2, ResponseForm
from forum.models import Thread, Response, ReportedThreads, ReportedResponses
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_mongodb_engine.contrib import MongoDBManager
from bson.objectid import ObjectId
from django.forms.util import ErrorList



def home(request):
    template = loader.get_template('home.html')
    threads = Thread.objects.order_by('-date_created')[:10]
    categories = Category.objects.all()
    popular = Thread.objects.order_by('rating', 'date_created')
    context = RequestContext(request, {
        'threads': threads,
        'categories': categories,
        'popular': popular
    })
    return HttpResponse(template.render(context))

def userProfile(request, id):
    try:
        usr = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponseRedirect('/error/1/')
    template = loader.get_template('userProfile.html')
    categories = Category.objects.all()
    popular = Thread.objects.order_by('rating', 'date_created')
    context = RequestContext(request, {
        'usr': usr,
        'categories': categories,
        'popular': popular
    })
    return HttpResponse(template.render(context))

def found(request):
    # if 'key' in request.GET:
    #      message = 'You searched for: %r' % request.GET['key']
    # else:
    #     message = 'You submitted an empty form.'
    # return HttpResponse(message)
    order_by = request.GET.get('order_by', '-date_created')
    key = request.GET.get('key')
    if key != '' :
        threads = Thread.objects.filter(Q(title__contains=key) | Q(content__contains=key)).order_by(
        '-date_created')
        message = 'Wyszukiwanie dla tekstu: %s' % request.GET['key']
    else:
        threads = []
        message = 'Wpisz tekst, ktory chcesz znalezc'
    template = loader.get_template('found.html')
    categories = Category.objects.all()
    context = RequestContext(request, {
        'threads': threads,
        'message': message,
        'categories' : categories,
    })
    return HttpResponse(template.render(context))

def category(request, id):
    template = loader.get_template('category.html')
    try:
        c = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return HttpResponseRedirect('/error/1/')
    threadsList = Thread.objects.filter(category__id=id).order_by('-date_created')
    paginator = Paginator(threadsList, 15)
    page = request.GET.get('page')
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        threads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        threads = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    context = RequestContext(request, {
        'threads': threads,
        'categories' : categories
    })
    return HttpResponse(template.render(context))

def thread(request, id):
    try:
        thread = Thread.objects.get(id=id)
    except Thread.DoesNotExist:
        return HttpResponseRedirect('/error/1/')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ResponseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cont = form.cleaned_data['content']      # get content or response
            if 'login' in request.session:
                lg = request.session['login']
            else:
                HttpResponseRedirect('/error/2/')
            try:
                u= User.objects.get(login=lg)
            except User.DoesNotExis:
                HttpResponseRedirect('/error/2/')
            resp = Response(
                user= u,
                content = cont
            )
            resp.save()

            thread = Thread.objects.get(id=id)
            thread.response.append(resp)
            thread.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thread/' + id)
    else:
        form = ResponseForm()
        responsesList = thread.response
        paginator = Paginator(responsesList, 15)
        page = request.GET.get('page')
        try:
            responses = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            responses = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            responses = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    return render(request, 'thread.html',
                  {'form': form, 'thread': thread,'responses': responses, 'categories': categories, })

def newThread(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ThreadForm(request.POST) # A form bound to the POST data
        if 'login' in request.session:
                usr = User.objects.get(login= request.session['login'])
        else:
            return HttpResponseRedirect('/error/2/')
        if form.is_valid(): # All validation rules pass

            thread = Thread(
                title= form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                category = form.cleaned_data['category'],
                user = usr,
                response = [],
                rating = []
            )
            thread.save()
            return HttpResponseRedirect('/thread/' + str(thread.id)) # Redirect after POST
    else:
        form = ThreadForm() # An unbound form
    categories = Category.objects.all()
    return render(request, 'newThread.html', {
        'form': form,
        'categories' : categories,
    })

def delThread(request, id):
    if 'login' in request.session:
        lg = request.session['login']
    else:
        return HttpResponseRedirect('/error/2/')
    try:
        thrd = Thread.objects.get(id=id)
        usr = User.objects.get(login = lg)
    except:
        return HttpResponseRedirect('/error/1/')

    if usr.type == 'admin':
        thrd.delete()
    # is user author of this post?
    elif usr.lg == thrd.user.id:
        thrd.delete()
    else:
        return HttpResponseRedirect('/error/2/')
    return HttpResponseRedirect('/success/3/')

def editThread(request, id):
    categories = Category.objects.all()
    if 'userId' in request.session:
        try:
            usr = request.session['userId']
            us = User.objects.get(id=usr)
            thrd = Thread.objects.get(id=id)
        except User.DoesNotExist or Thread.DoesNotExist:
            return HttpResponseRedirect('/error/1/')
    else:
        return HttpResponse('/error/2/')
    form = ThreadForm(request.POST or None, instance=thrd)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/thread/' + id)
    else:
        return render_to_response('editThread.html', RequestContext(request, {'form': form, 'categories': categories}))

def reportThread(request, id):
    if 'userId' in request.session:
        try:
            usr = request.session['userId']
            us = User.objects.get(id=usr)
            thrd = Thread.objects.get(id=id)
        except User.DoesNotExist or Thread.DoesNotExist:
            return HttpResponseRedirect('/error/1/')
    else:
        return HttpResponseRedirect('/error/2/')
    try:
        reported = ReportedThreads (
            thread = thrd,
            user = us
        )
        reported.save()
        return HttpResponseRedirect('/info/1/')
    except:
        return HttpResponseRedirect('/error/3/')


def signUp(request):
    categories = Category.objects.all()
    message = ""
    if request.method == 'POST':
        form = UserForm2(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            confirmpassword=form.cleaned_data["confirmpassword"]
            if password == confirmpassword:
                if User.objects.filter(login=form.data['login']) or User.objects.filter(email=form.data['email']):
                    message = "Login lub haslo juz istnieja w bazie"
                else:
                    form.save()
                    return HttpResponseRedirect('/success/2')

            else:
                message = "hasla sie nie zgadzaja"

            return render(request, 'signUp.html', {'form': form, 'categories': categories,'message': message})
    else:
        form = UserForm2()
    return render(request, 'signUp.html', {
        'form': form,
        'categories' : categories,
        'message': message
    })

def response(request, id):
    return HttpResponseRedirect('/info/6/')

def editResponse(request, id):
    return HttpResponseRedirect('/info/6/')

def delResponse(request, id):
    return HttpResponseRedirect('/info/6/')

def reportResponse(request, id):
    if 'userId' in request.session:
        try:
            usr = request.session['userId']
            us = User.objects.get(id=usr)
            resp = Response.objects.get(id=id)
        except User.DoesNotExist or Response.DoesNotExist:
            return HttpResponseRedirect('/error/1/')
    else:
        return HttpResponseRedirect('/error/2/')
    try:
        reported = ReportedResponses (
            response = resp,
            user = us
        )
        reported.save()
        return HttpResponseRedirect('/info/1/')
    except:
        return HttpResponseRedirect('/error/3/')


def signIn(request):
    categories = Category.objects.all()
    message=''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm1(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                us = User.objects.get(login=form.cleaned_data['login'], password=form.cleaned_data['password'])
            except:
                message = "Wprowadzono niepoprawne dane."
                return render(request, 'signIn.html', {'form': form, 'categories': categories,'message': message})
            request.session['userId'] = str(us.id)
            request.session['login'] = str(us.login)
            if us.ban:
                request.session['ban'] = True
            if us.type == "admin":
                request.session['admin'] = str(us.login)
            if not form.cleaned_data['rememberMe']:
                request.session.set_expiry(0)
            # request.session['type'] = us.type
            return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm1()
    return render(request, 'signIn.html', {'form': form, 'categories': categories, 'message': message})

def editUser(request):
    categories = Category.objects.all()
    if 'userId' in request.session:
        try:
            usr = request.session['userId']
            us = User.objects.get(id=usr)
        except User.DoesNotExist:
            return HttpResponseRedirect('/error/1/')
    else:
        return HttpResponse('/error/2/')
    form = UserForm2(request.POST or None, instance=us)
    if form.is_valid():
        form.save()
        return redirect('/success/1/')
    else:
        return render_to_response('editUser.html', RequestContext(request, {'form': form, 'categories': categories}))

def delUser(request, id):
    if 'userId' in request.session:
        try:
            usr = User.objects.get(id=id)
            usr2 = User.objects.get(id=request.session['userId'])
            if usr.id == usr2.id:
                usr.delete()
            else:
                HttpResponseRedirect('/error/2')
            return HttpResponseRedirect('/success/3')
        except User.DoesNotExist:
            return HttpResponseRedirect('/error/1')
    else:
        return HttpResponseRedirect('/error/2')

def logOut(request):
    if 'userId' and 'login' in request.session:
        del request.session["userId"]
        del request.session["login"]
        request.session.modified = True
    if 'ban' in request.session:
        del request.session["ban"]
        request.session.modified = True
    if 'admin' in request.session:
        del request.session['admin']
        request.session.modified = True
    return redirect('/')

def success(request, msg):
    message = ""
    if msg == '1':
        message = "Dane zostaly zmienione."
    if msg == '2':
        message = "Rejestracja sie powiodla."
    if msg == '3':
        message = "Usunieto dane."
    template = loader.get_template('success.html')
    categories = Category.objects.all()
    context = RequestContext(request, {
        'categories': categories,
        'message': message
    })
    return HttpResponse(template.render(context))

def error(request, msg):
    message = ""
    if msg == '1':
        message = "Wystapil blad podczas pobierania dnaych z bazy."
    if msg =='2':
        message = "Brak uprawnien."
    if msg == '3':
        message = "Blad poczas zapisu danych"
    template = loader.get_template('error.html')
    categories = Category.objects.all()
    context = RequestContext(request, {
        'categories': categories,
        'message': message
    })
    return HttpResponse(template.render(context))

def info(request, msg):
    message = ""
    if msg == '1':
        message = "Watek zgloszony."
    if msg == '6':
        message = "ta metoda jeszcze nie dziala"
    categories = Category.objects.all()
    template = loader.get_template('info.html')
    context = RequestContext(request, {
        'categories': categories,
        'message': message
    })
    return HttpResponse(template.render(context))