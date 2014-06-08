from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

def home(request):
    template = loader.get_template('home.html')
    hello = "hello!"
    context = RequestContext(request, {
        'hello': hello,
    })
    return HttpResponse(template.render(context))