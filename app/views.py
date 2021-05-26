# sample content of views for registration
from typing import Protocol
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        return render(request,'home.html',context={'username':username})
    return render(request,'home.html')




def register(request):
    userform=UserForm()
    profileform=ProfileForm()
    if request.method=='POST' and request.FILES:
        userdata=UserForm(request.POST)
        profiledata=ProfileForm(request.POST,request.FILES)
        if userdata.is_valid() and profiledata.is_valid():
            UD=userdata.save(commit=False)
            password=userdata.cleaned_data['password']
            UD.set_password(password)
            UD.save()

            PD=profiledata.save(commit=False)
            PD.user=UD
            PD.save()
            send_mail('Registration','Thanks for Registration,it is successfull',
            'harshadvali09@gmail.com',
            [UD.email],
            fail_silently=False)

            return HttpResponse('user is created Successfully')

    return render(request,'register.html',context={'userform':userform,'profileform':profileform})

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('user is a not active user')
      
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



