from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from . import models
from .models import User, Appointment
from django.db.models import Q
import bcrypt
import datetime
import re
import unicodedata

val_regex =re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    request.session['id'] = 0

    return render(request, 'appointment/index.html')

def register(request):
    request.session['message']=[]
    request.session['check'] = 1
    any_user = User.objects.filter(email = request.POST['email'])
    if len(request.POST['fullname'])<1:
        message = "Name cannot be empty"
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if not val_regex.match(request.POST['email']):
        message = "Please enter a valid email"
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if request.POST['password'] != request.POST['password_confirm']:
        message = "Password do not match"
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if len(request.POST['password'])<8:
        message = 'Password must be 8 characters or longer'
        request.session['message'].insert(0, message)
        request.session['check'] = 0
    if any_user:
        message = 'This email has already been used'
        request.session['message'].insert(0, message)
        request.session['check'] = 0
    if request.session['check'] == 1:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        User.objects.create(name = request.POST['fullname'], email = request.POST['email'], password = pw_hash, date_of_birth = request.POST['date'])
        the_user = User.objects.get(email = request.POST['email'])
        request.session['id'] = the_user.id
        return redirect('/appointments')
    else:
        return redirect('/')

def login(request):
    request.session['message'] = []
    the_user = User.objects.filter(email = request.POST['email'])
    if the_user:
        if bcrypt.hashpw(request.POST['password'].encode('utf-8'), the_user[0].password.encode('utf-8')) == the_user[0].password:
            request.session['id'] = the_user[0].id
            return redirect('/appointments')
        else:
            message = "Your input did not match our record"
            request.session['message'].insert(0, message)
            return redirect('/')
    else:
        message = "Your input did not match our record"
        request.session['message'].insert(0, message)
        return redirect('/')

def appointments(request):
    the_user = User.objects.get(id = request.session['id'])
    today_app = Appointment.objects.filter(user = the_user, date = datetime.datetime.now().strftime("%Y-%m-%d"))
    # other_app = Appointment.objects.filter(user = the_user, ~Q(date = datetime.datetime.now().strftime("%Y-%m-%d")), date__gt = datetime.datetime.now().strftime("%Y-%m-%d") )
    other_app = Appointment.objects.filter(user = the_user).filter(~Q(date = datetime.datetime.now().strftime("%Y-%m-%d"))).filter(date__gt = datetime.datetime.now().strftime("%Y-%m-%d"))
    context = {'user' : the_user, 'today_app': today_app, 'other_app':other_app}
    return render(request, 'appointment/appointments.html', context)

def add(request):
    request.session['message'] = []
    request.session['check'] = 1
    print '##################'
    print request.POST['date']
    if len(request.POST['date'])<1:
        message = 'Please pick a date'
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if len(request.POST['tasks'])<1:
        message = 'Tasks cannot be empty'
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if request.POST['date']<datetime.datetime.now().strftime("%Y-%m-%d"):
        message = 'Please pick a future date'
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    # if request.POST['time']<datetime.datetime.now().strftime("%H:%i"):
    #     message = 'Please pick a future time'
    #     request.session['check'] = 0
    #     request.session['message'].insert(0, message)
    check_app = Appointment.objects.filter(date = request.POST['date'], time = request.POST['time'])
    print '^^^^^^^^^^^^^^^^^^^^^'
    print check_app
    if check_app:
        message = "The time and date is already occupied"
        request.session['check'] = 0
        request.session['message'].insert(0, message)
    if request.session['check'] == 1:
        the_user = User.objects.get(id = request.session['id'])
        Appointment.objects.create(user = the_user, task = request.POST['tasks'], date = request.POST['date'], time = request.POST['time'])
        return redirect('/appointments')
    else:

        return redirect('/appointments')



def edit(request, id):
    the_app = Appointment.objects.get(id = id)
    context = {'app': the_app}
    return render(request, 'appointment/edit.html', context)

def update(request, id):
    request.session['editmessage'] = []
    request.session['check'] = 1
    if len(request.POST['tasks'])<1:
        message = 'Tasks cannot be empty'
        request.session['check'] = 0
        request.session['editmessage'].insert(0, message)
    if request.POST['date']<datetime.datetime.now().strftime("%Y-%m-%d"):
        message = "Pleaase pick a future date"
        request.session['check'] = 0
        request.session['editmessage'].insert(0, message)
    check_app = Appointment.objects.filter(date = request.POST['date'], time = request.POST['time'])
    print "*******************************"
    # print check_app[0].id
    print id
    print "*******************************"
    # if check_app[0].id == id:
    #     if check_app is not None:
    #         message = "The time and date is already occupied"
    #         request.session['check'] = 0
    #         request.session['editmessage'].insert(0, message)
    if request.session['check'] ==1:
        Appointment.objects.filter(id = id).update(task = request.POST['tasks'], status = request.POST['status'], date = request.POST['date'], time = request.POST['time'])
        return redirect('/appointments')
    else:
        return redirect('/edit/'+str(id))


def delete(request, id):
    Appointment.objects.filter(id = id).delete()
    return redirect('/appointments')
