from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def createuser(self,request):
        is_valid = True
        if len(request.POST['name']) == 0:
            is_valid = False
            messages.error(request,'Name is required.')
        if len(request.POST['alias']) == 0:
            is_valid = False
            messages.error(request,'Alias is required.')
        if len(request.POST['bday'])== 0:
            is_valid = False
            messages.error(request,'Birthday is required.')
        if len(request.POST['email']) == 0:
            is_valid = False
            messages.error(request,'Email is required.')
        email_check = User.objects.filter(email=request.POST['email'])
        if len(email_check) > 0:
            is_valid= False
            messages.error(request, 'Email is already exist')
        if len(request.POST['password'])< 8:
            is_valid = False
            messages.error(request, 'Password requires at least 8 characters')
        if request.POST['password'] != request.POST['confirm_password']:
            messages.error(request, 'Password and confirm password do not match')
            is_valid = False
        if not is_valid:
            return is_valid
        hashed = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User(
            name=request.POST['name'],
            alias=request.POST['alias'],
            bday = request.POST['bday'],
            email=request.POST['email'],
            password=hashed,
        )
        new_user.save()
        request.session['logged_in'] = new_user.id;
        is_valid = True
        return is_valid

    def login(self,request):
        is_valid = True
        if len(request.POST['email']) == 0:
            messages.error(request, "Email is required")
            is_valid = False
            return is_valid
        if len(request.POST['password']) == 0:
            messages.error(request, "Password is required")
            is_valid = False
            return is_valid
        users= User.objects.filter(email=request.POST['email'])
        if len(users) > 0:
            check_user=users[0]
            dbpw=bcrypt.hashpw(request.POST['password'].encode('utf-8'), check_user.password.encode('utf-8'))
            if dbpw == check_user.password:
                request.session['logged_in'] = check_user.id
                is_valid = True
                return is_valid
            else:
                messages.error(request, "Either email or password is incorrect")
                is_valid = False
                return is_valid
        else:
            messages.error(request, "User does not exist")
            is_valid = False
            return is_valid
    def add_friend(self,request,id):
        friend=Friend.objects.filter(user__id=id)
        if len(friend) == 0:
            curr_user=User.objects.get(id=request.session['logged_in'])
            friend=User.objects.filter(id=id).first()
            new_friend=Friend.objects.create(user=curr_user,friend=friend)
            new_friend.save()
            is_valid = True
            return is_valid
        else:
            messages.error(request, "Friend already exist")
            is_valid = False
            return is_valid
    def remove_friend(self,request,id):
        friend=Friend.objects.filter(friend_id=id)
        if len(friend) > 0:
            friend=Friend.objects.filter(friend_id=id)
            friend.delete()
            is_valid = True
            return is_valid
        else:
            messages.error(request, "No Friend found")
            is_valid = False
            return is_valid

    def logout(self,request):
        is_valid=True
        del request.session['logged_in']
        return True
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    bday = models.DateField(auto_now=False, auto_now_add=False)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
class Friend(models.Model):
    user = models.ForeignKey(User, related_name="curr_user")
    friend = models.ForeignKey(User, related_name = "friends")
