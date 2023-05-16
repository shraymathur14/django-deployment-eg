from django.shortcuts import render
from basic_app import forms

#these library are for login purposes
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    registered=False
    
    if request.method == "POST":
        #creating instances for both forms using data from the request
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST) 


        if user_form.is_valid() and profile_form.is_valid():
            
            #saving userform and setting the password for the user
            user = user_form.save() 
            user.set_password(user.password)
            user.save()

            #saving profile form and associates the profile with the user
            #if we do not write commit = false then it will not allow any modificaiton and will give error of 
            #integrity something
            profile = profile_form.save(commit=False)
            profile.user = user

            #saves the profile picture if provided
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            # print(request.FILES)
            profile.save()

            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()
    
    return render(request, 'basic_app/registration.html',{'user_form':user_form,                                                
                                                          'profile_form':profile_form,
                                                          'registered':registered})
    
     
#the below line is decorater which means that to logout we requred to be logged in
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!!")

def user_login(request):
    if request.method == "POST":
        #username is same as written in html page where name has value username
        un = request.POST.get('username')
        pd = request.POST.get('pass')

        #automatically check the credentials
        user = authenticate(username=un, password=pd)

        #check if user exist means the authentication is successful
        if user:
            #checking if user is active or not
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        #wrong credentials will go to else 
        else:
            print("Someone tried to login and failed")
            print(f"Username :{un} and password: {pd}")
            return HttpResponse("Invalid Credintials")
    else:
        return render(request, 'basic_app/login.html')