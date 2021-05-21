# sample content of views for registration
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from app.forms import *

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
            return HttpResponse('user is created Successfully')

    return render(request,'register.html',context={'userform':userform,'profileform':profileform})