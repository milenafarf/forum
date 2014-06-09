from django.http import HttpResponse
from django.template import loader, RequestContext
from forum.models import Category, Thread, Message
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

def home(request):
    template = loader.get_template('home.html')
    categories = Category.objects.order_by('name')
    context = RequestContext(request, {
        'categories': categories,
    })
    return HttpResponse(template.render(context))