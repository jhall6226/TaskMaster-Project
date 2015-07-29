from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from taskmaster_app.models import Resource
from django.utils.text import slugify

def home_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        
        auth = authenticate(username=username, password=password)
        if auth is not None:
            login(request,auth)
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
        
        else:
            messages.add_message(request, messages.INFO, 'Login Failed. The username and password combination is invalid. Please try again.')
            return HttpResponseRedirect(reverse('home'))
    
    return render(request, 'home.html')
    
def register_view(request):
        
    if request.method == 'POST':
        if request.POST.get('control') == 'cancel':
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
            
        form = UserCreationForm(request.POST) #Doesn't have First Name, Last Name, and E-mail fields
        if form.is_valid():
            u = form.save()
            u.slug = slugify(u.get_full_name())
            u.save()
            r = Resource(user=u,slug=slugify(u.username))
            r.save()
            
            messages.add_message(request, messages.INFO, 'User added!')

            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))

    else:
        form = UserCreationForm()
    
    return render(request, 'register.html',{'form':form})