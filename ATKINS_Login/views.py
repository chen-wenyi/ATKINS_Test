from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ATKINS_Login.form import UserForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    user_form = UserForm()

    return render(request, 'index.html', {'user_form': user_form})


def register(request):
    registed = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.save()
            print user

            registed = True



    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    return render(request, 'index.html', {'user_form': user_form, 'registed': registed})


def login(request):
    email_error = ''
    password_error = ''
    user_form = UserForm()

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            email_valid = User.objects.get(username=email)
        except ObjectDoesNotExist:
            email_valid = None

        if not email:
            global email_error
            email_error = '--- Email is required ---'
        if not password:
            global password_error
            password_error = '--- Password is required ---'
        if not email_valid:
            email_error = '--- Invalid Email ---'
        if not email or not password or not email_valid:
            return render(request, 'index.html',
                          {'user_form': user_form, 'password_error': password_error, 'email_error': email_error,})

        user = authenticate(username=email, password=password)

        if user:

            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse("Your account is disabled.")
        else:

            global password_error
            password_error = '--- Wrong password ---'

            return render(request, 'index.html',
                          {'user_form': user_form, 'password_error': password_error, 'email_error': email_error,})


    else:
        return render(request, 'index.html',
                      {'user_form': user_form, 'password_error': password_error, 'email_error': email_error,})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
