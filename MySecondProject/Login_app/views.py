from django.shortcuts import render
from Login_app.forms import UserForm, UserInfoForm
from Login_app.models import UserInfo
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def login_page(request):
    dict = {}
    return render(request,'Login_app/login.html',context=dict)

def user_login(request):
    dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                print("Login Successfull!!")
                return HttpResponseRedirect(reverse('Login_app:index'))
            else:
                return HttpResponse("Accoutn is not active.")
        else:
            return HttpResponse("Login details are not correct.")
    else:
        #return render(request, 'Login_app/login.html',context=dict)
        return HttpResponseRedirect(reverse('Login_app:login'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:index'))

def index(request):
    dict={}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        dict = {'user_basic_info':user_basic_info,'user_more_info':user_more_info}
    return render(request,'Login_app/index.html',context=dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) #password encryption
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user #user_info and user table connected each other for this line

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic'] #this line use for upload profile pic and save picture in profile pic

            user_info.save()
            registered = True
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    dict = {'user_form': user_form, 'user_info_form':user_info_form, 'registered':registered}
    return render(request, 'Login_app/register.html', context=dict)
