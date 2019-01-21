from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
import json
from Chat.models import Profile


def index(request):
    user: User = request.user
    if user.is_authenticated:
        username = user.username
    else:
        username = None

    context = {
        'username': username,
    }
    if request.method == 'GET':
        return render(request, 'index.html', context)

    room_name = request.POST['room_name']
    return redirect('room', room_name)


def log_in(request):
    user: User = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        return render(request, 'login.html')

    login(request, user)
    return redirect('index')


def log_out(request):
    logout(request)
    return redirect('index')


def register(request):
    user: User = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.create_user(username, password=password)
        Profile.objects.create(user=user)
    except Exception as exc:
        print(exc, type(exc))
        return render(request, 'register.html')

    login(request, user)
    return redirect('index')


def room(request, room_name):
    user: User = request.user
    if user.is_authenticated:
        username = user.username
    else:
        return redirect('login')

    context = {
        'room_name': mark_safe(json.dumps(room_name)),
        'username': username
    }

    return render(request, 'room.html', context)


def personal_area(request, user_name):
    person = User.objects.get(username=user_name)

    user: User = request.user
    if user.is_authenticated:
        username = user.username
    else:
        return redirect('login')

    if person.profile.avatar == '':
        avatar = None
    else:
        avatar = person.profile.avatar.url

    context = {
        'user': {
            'avatar': avatar,
            'username': person.username,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'age': person.profile.age,
            'birthday': person.profile.birthday,
            'phone': person.profile.phone,
            'email': person.email,
            'site': person.profile.site,
        },
        'username': username
    }

    return render(request, 'personal_area.html', context)


def personal_area_change(request):
    user: User = request.user
    if not user.is_authenticated:
        return redirect('login')

    context = {
        'user': {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.profile.age,
            'birthday': str(user.profile.birthday),
            'phone': user.profile.phone,
            'email': user.email,
            'site': user.profile.site,
        }
    }

    if request.method == 'GET':
        return render(request, 'personal_area_change.html', context)

    if request.POST['age'] == '':
        age = None
    else:
        age = request.POST['age']

    if request.POST['birthday'] == '':
        birthday = None
    else:
        birthday = request.POST['birthday']

    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()

    profile = user.profile
    profile.avatar = request.FILES.get('avatar', user.profile.avatar)
    profile.age = age
    profile.birthday = birthday
    profile.phone = request.POST['phone']
    profile.site = request.POST['site']
    profile.save()

    return redirect('personal_area', user.username)
