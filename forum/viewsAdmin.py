__author__ = 'Milena Farfulowska'

from django.http import HttpResponse
from django.template import loader, RequestContext
from forum.models import Category, Thread, User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forum.forms import UserFormAdmin, ThreadForm, UserForm1, UserForm2, ResponseForm, CategoryForm
from forum.models import Thread, Response, ReportedThreads, ReportedResponses
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def editUser(request, id):
    if 'admin' in request.session:
        us = User.objects.get(id=id)
    else:
        return HttpResponseRedirect('/error/2/')
    form = UserFormAdmin(request.POST or None, instance=us)
    if form.is_valid():
        form.save()
        return redirect('/usersAdmin/')
    else:
        return render_to_response('editUserAdmin.html', RequestContext(request, {'form': form}))

def delUser(request, id):
    if 'admin' in request.session:
        try:
            usr = User.objects.get(id=id)
            usr.delete()
            return HttpResponseRedirect('/usersAdmin')
        except:
            return HttpResponseRedirect('/error/1')
    else:
        return HttpResponseRedirect('/error/2')

def categories(request):
    if 'admin' in request.session:
        try:
            categories = Category.objects.all()
        except Category.DoesNotExist:
            return HttpResponseRedirect('/error/1/')
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = CategoryForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/categoriesAdmin/')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = CategoryForm()
        return render(request, 'categoriesAdmin.html', {'form': form})

        # template = loader.get_template('categoriesAdmin.html')
        # context = RequestContext(request, {
        #     'form': form,
        #     'categories': categories,
        # })
        # return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/error/2/')

def editCategory(request, id):
    if 'admin' in request.session:
        cat = Category.objects.get(id=id)
    else:
        return HttpResponseRedirect('/error/2/')
    form = CategoryForm(request.POST or None, instance=cat)
    if form.is_valid():
        form.save()
        return redirect('/categoriesAdmin/')
    else:
        return render_to_response('categoriesAdmin.html', RequestContext(request, {'form': form}))

# def addCategory(request):
#     if 'admin' in request.session:
        # if this is a POST request we need to process the form data
        # if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            # form = CategoryForm(request.POST)
            # check whether it's valid:
            # if form.is_valid():
            #     form.save()
            #     return HttpResponseRedirect('/categoriesAdmin/')
        # if a GET (or any other method) we'll create a blank form
        # else:
        #     form = CategoryForm()
        #     return render(request, 'categoriesAdmin.html', {'form': form})
    # else:
    #     return HttpResponseRedirect('/error/2/')

def users(request):
    if 'admin' in request.session:
        template = loader.get_template('usersAdmin.html')
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

def reportedThreads(request):
    if 'admin' in request.session:
        template = loader.get_template('reportedThreads.html')
        reportedList = ReportedThreads.objects.all()
        paginator = Paginator(reportedList, 15)
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
            'categories': categories,
            'threads': threads,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/error/2')

def reportedResponses(request):
    if 'admin' in request.session:
        template = loader.get_template('reportedResponses.html')
        reportedList = ReportedResponses.objects.all()
        paginator = Paginator(reportedList, 15)
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
        context = RequestContext(request, {
            'categories': categories,
            'responses': responses,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/error/2')

# def banThread(request, id):
#     if 'admin' in request.session:
#         try:
#             thrd = ReportedThreads.objects.get(id=id)
#             thrd.thread.ban = True
#             thrd.checked = True
#             thrd.save()
#         except:
#             return HttpResponseRedirect('/error/1')
#         return HttpResponseRedirect('/reportedThreads/')
#
#     else:
#         return HttpResponseRedirect('/error/2')

# unreport the thread
def setOkThread(request, id):
    if 'admin' in request.session:
        try:
            thrd = ReportedThreads.objects.get(id=id)
            thrd.delete()
        except:
            return HttpResponseRedirect('/error/1')
        return HttpResponseRedirect('/reportedThreads/')
    else:
        return HttpResponseRedirect('/error/2')

def setOkResponse(request, id):
    if 'admin' in request.session:
        try:
            resp = ReportedResponses.objects.get(id=id)
            resp.delete()
        except:
            return HttpResponseRedirect('/error/1')
        return HttpResponseRedirect('/reportedResponses/')
    else:
        return HttpResponseRedirect('/error/2')
