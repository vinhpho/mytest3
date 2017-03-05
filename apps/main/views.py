from django.shortcuts import render, redirect,HttpResponse
from . models import *
others=[]
print "*"*50
print others
# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def createuser(request):
    did_create = User.objects.createuser(request)
    if did_create:
        return redirect('/')
    else:
        return redirect('/')
def login(request):
    did_login = User.objects.login(request)
    if did_login:
        return redirect('/user_dashboard')
    else:
        return redirect('/')
def user_dashboard(request):
    if 'logged_in'in request.session:
        curr_names = User.objects.filter(id=request.session['logged_in'])
        users=User.objects.all().exclude(id=request.session['logged_in'])
        friends = Friend.objects.filter(user__id=request.session['logged_in'])


        if len(friends) > 0:
            others = users
            alist=Friend.objects.filter(user__id=request.session['logged_in']).values_list('friend_id', flat=True)
            for i in range(len(alist)):
                others=others.exclude(id=alist[i])
        else:
            others = users
        context = {
            "curr_names":curr_names,
            "users":users,
            "friends":friends,
            "others":others,
        }
        return render(request, 'main/user_dashboard.html', context)
    else:
        return redirect('/')
def show_user(request,id):
    context = {
        "users":Friend.objects.filter(friend_id=id),
    }
    return render(request, 'main/show_user.html',context)

def show_non_user(request,id):
    context = {
        "nonusers":User.objects.filter(id=id),
    }
    return render(request, 'main/shownonuser.html',context)
def add_friend(request,id):
    add_friend = User.objects.add_friend(request,id)
    if add_friend:
        return redirect('/user_dashboard')
    else:
        return redirect('/user_dashboard')

def remove_friend(request,id):
    remove_friend = User.objects.remove_friend(request,id)
    if remove_friend:
        return redirect('/user_dashboard')
    else:
        return redirect('/user_dashboard')


def logout(request):
    try:
        del request.session['logged_in']
    except KeyError:
        pass
    return redirect('/')
