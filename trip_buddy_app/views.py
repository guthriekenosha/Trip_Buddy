from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trips
import bcrypt


def login_reg(request):
    return render(request, 'login_reg.html')

def create_user(request):
    errors = User.objects.user_validator(request.POST)
    user_list = User.objects.filter(email=request.POST['email'])
    if user_list:
        messages.error(request, "Email already exists")
        return redirect('/')

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    print(request.POST['password'])
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    print(hashed_pw)

    user1 = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
    )
    request.session['log_user_id'] = user1.id
    return redirect('/dashboard')
    
def login_user(request):
    user_list = User.objects.filter(email=request.POST['email'])
    if user_list:
        logged_user = user_list[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['log_user_id'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('/')
    messages.error(request, "Email does not exist")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def trips (request):
    if 'log_user_id' not in request.session:
        return redirect('/')
    context = {
        'log_user_id' : User.objects.get(id=request.session['log_user_id']),
        'trips': Trips.objects.all()
    }
    return render(request,'dashboard.html', context)

def create_trip(request):
    # if 'logged_user' not in request.session:
    #     messages.error(request, "Please register or log in first!")
    #     return redirect('/')
    print(request.POST['destination'])
    errors = Trips.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_trip')
    else:
        Trips.objects.create(
            destination = request.POST['destination'],
            plan = request.POST['plan'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date']
        )
    return redirect('/dashboard')

def add_trip(request):
    return render(request, 'create_trip.html')

def trip_details (request, trip_id):
    details = Trips.objects.get(id=trip_id)
    context = {
        'log_user_id' : User.objects.get(id=request.session['log_user_id']),
        'trips': details
    }
    return render(request, 'trip_details.html', context)

def edit_trips(request,trip_id):
    if 'log_user_id' not in request.session:
        return redirect('/')
    details = Trips.objects.get(id=trip_id)
    context = {
        'log_user_id' : User.objects.get(id=request.session['log_user_id']),
        'trips': details 
    }
    return render(request, 'edit_trip.html', context)

def update(request,trip_id):
    print(request.POST['destination'])
    errors = Trips.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_trips')
    else:
        edit = Trips.objects.get(id=trip_id)
        edit.destination = request.POST['destination']
        edit.plan = request.POST['plan']
        edit.start_date = request.POST['start_date']
        edit.end_date = request.POST['end_date']
        edit.save()
    return redirect('/dashboard')

    # edit = Trips.objects.get(id=trip_id)
    # edit.destination = request.POST['destination']
    # edit.plan = request.POST['plan']
    # edit.start_date = request.POST['start_date']
    # edit.end_date = request.POST['end_date']
    # edit.save()

    return redirect('/dashboard')

def delete(request, trip_id):
    delete = Trips.objects.get(id=trip_id)
    delete.delete()

    return redirect('/dashboard')