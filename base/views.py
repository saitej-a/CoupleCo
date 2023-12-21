from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse
import random
import string
from .models import Participant,Room,Messages
# Create your views here.


def homepage(request,pk=0):
    if request.user.is_authenticated :
        username=request.user
        
        characters = string.digits + string.ascii_lowercase
    # Generate a random room ID of the specified length
        room_id = ''.join(random.choice(characters) for _ in range(9))
        return render(request,'home.html',{'username':username,'roomid':room_id})
        
    else:
        return redirect("signup")
    

def signup(request):
    reg=True
    form=UserCreationForm()
    
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        
        if form.is_valid:
            form.save()
        else:
            message="something went wrong"
            
    return render(request,'room.html',{'login1':reg,"form":form,})
def loginpage(request):
    
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
       
        user=authenticate(request,username=username,password=password)
            
        login(request=request,user=user)
        return redirect('home')
            

        
    return render(request,'room.html')
def logoutpage(request):
    logout(request=request)
    return redirect('home')


    

def join(request):
    username=request.user
    
        
    return render(request,'creation.html',{'username':username,})

def room(request):
    username=str(request.user)
    room_id=""
    if request.method=="POST":
        room_id=request.POST.get('room_id')
        room,bl2=Room.objects.get_or_create(id=room_id)
        participat,bl=Participant.objects.get_or_create(users=request.user,room=room)

    
    

    return render(request,'group.html',{'username':username,"roomid":room_id})
