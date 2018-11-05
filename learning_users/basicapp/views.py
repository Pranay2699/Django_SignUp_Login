from django.shortcuts import render
from basicapp.forms import UserForm,UserProfileInfoForms


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,"basicapp/index.html")

@login_required
def special(request):
    return HttpResponse("Logged in success,Nice...")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):

    registered=False

    if request.method == "POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForms(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user #Since it has OneToOne relationship.Mentioned in the models

            if "profile_pic" in request.FILES:
                profile.profile_pic=request.FILES["profile_pic"]

            profile.save()

            registered=True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForms()

    return render(request,"basicapp/registration.html",{"user_form":user_form,
                                                        "profile_form":profile_form,
                                                        "registered":registered})


def user_login(request):
    if request.method == "POST":
        username=request.POST.get("username") #username is the name of the "input field" and we are using "get" method because it is just a simple form
        password=request.POST.get("password") #Getting the password and the above method is done

        user=authenticate(username=username,password=password) # It authenticates the user for us.

        if user:
            if user.is_active:# checking if user is active or not
                login(request,user)#Logging in user
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT IS NOT ACTIVE')
        else:
            print("Someone tried to login and failed")
            print("username:{} and password:{}".format(username,password))
            return HttpResponse("INVALID LOGIN DETAILS SUPPLIED")
    else:
        return render(request,"basicapp/login.html")
