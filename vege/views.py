from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.paginator import Paginator
# Create your views here.

@login_required(login_url="/login")
def receipe(request):
    if request.method == "POST":
        data = request.POST
        
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')

        Receipe.objects.create(
            receipe_image = receipe_image,
            receipe_name = receipe_name,
            receipe_description = receipe_description
            )
        
        return redirect('/receipe/')
    
    queryset = Receipe.objects.all()
    paginator = Paginator(queryset,3)
    page_no = request.GET.get('page')
    querysetdatafinal = paginator.get_page(page_no)
    totalpage = querysetdatafinal.paginator.num_pages

    

    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))

    context = {'receipe' : querysetdatafinal,
               'lastpage' : totalpage,
                'totalpagenumber' : [n+1 for n in range(totalpage)] }

    return render(request , "receipe.html", context)

def update_receipe(request,id):
    queryset = Receipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST

        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        return redirect('/receipe/')


    context = {'receipe' : queryset}
    return render(request , "update_receipe.html", context)



def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipe/')


def login_page(request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not User.objects.filter(username=username).exists():
                messages.error(request, "Invalid username .")
                return redirect('/login/')
            
            user = authenticate(username = username, password = password)

            if user is None:
                messages.error(request, "Invalid username or password.")
                return redirect('/login/')
            
            else:
                login(request, user)
                return redirect('/receipe/')
            
            

        return render (request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')



def register(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        # if not first_name:
        #     messages.error(request, "First Name required.")
        last_name = request.POST.get('last_name')
        # if not last_name:
        #     messages.error(request, "Last Name required.")

        username = request.POST.get('username')
        # if not username:
        #     messages.error(request, "Username required.")

        password = request.POST.get('password')
        # if not password:
        #     messages.error(request, "Password required.")


        user = User.objects.filter(username=username)

        if user.exists():
            messages.error(request, "Username already exisits.")
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
            )
        user.set_password(password)
        user.save()

        messages.info(request, "Account Created Successfully.")


        return redirect('/register/')

    return render (request, 'register.html')
