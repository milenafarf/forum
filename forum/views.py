__author__ = 'Milena Farfulowska'

from django.http import HttpResponse
from django.template import loader, RequestContext
from forum.models import Category, Thread, Message, User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forum.forms import ThreadForm, UserForm
from django.shortcuts import render_to_response, redirect
from django.db.models import Q

def home(request):
    template = loader.get_template('home.html')
    threads = Thread.objects.order_by('-date_created')
    categories = Category.objects.all()
    popular = Thread.objects.order_by('rating', 'date_created')
    context = RequestContext(request, {
        'threads': threads,
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
    context = RequestContext(request, {
        'threads': threads,
        'message': message,
    })
    return HttpResponse(template.render(context))

def thread(request, id=-1):
    if id != -1:
        thread = Thread.objects.filter(id=id)
    template = loader.get_template('thread.html')
    context = RequestContext(request, {
        'thread': thread,
    })
    return HttpResponse(template.render(context))

def new_thread(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ThreadForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('home.html') # Redirect after POST
    else:
        form = ThreadForm() # An unbound form
    return render(request, 'new_thread.html', {
        'form': form,
    })

def signUp(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    return render(request, 'signUp.html', {
        'formset': form,
    })


def signIn(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        try:
            us = User.objects.get(login=form.data['login'], password=form.data['password'])
        except:
            return redirect('/signIn')
        request.session.set_expiry(3600) # ustawienie czasu trwania sesji na 1h
        request.session['user'] = us.id
        request.session['login'] = us.login
        request.session['type'] = us.type
        return redirect('/')
    else:
        form = UserForm()
        return render_to_response('signIn.html', RequestContext(request, {'formset': form}))