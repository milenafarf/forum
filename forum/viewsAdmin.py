__author__ = 'Milena Farfulowska'

from django.http import HttpResponse
from django.template import loader, RequestContext
from forum.models import Category, Thread, User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forum.forms import UserFormAdmin, ThreadForm, UserForm1, UserForm2, ResponseForm
from forum.models import Thread, Response
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def editUser(request, id):
    if 'admin' in request.session:
        us = User.objects.get(id=id)
    else:
        return HttpResponse('/error/2/')
    form = UserFormAdmin(request.POST or None, instance=us)
    if form.is_valid():
        form.save()
        return redirect('/success/1/')
    else:
        return render_to_response('editUserAdmin.html', RequestContext(request, {'form': form}))

def usersAdmin(request):
    if 'admin' in request.session:
        template = loader.get_template('users.html')
        usersList = User.objects.all()
        paginator = Paginator(usersList, 25)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            users = paginator.page(paginator.num_pages)
        categories = Category.objects.all()
        context = RequestContext(request, {
            'categories': categories,
            'users': users,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/error/2')