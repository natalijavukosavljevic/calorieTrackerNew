from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Food, Consume, Profile
from .forms import FoodForm, NewUserForm
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime
import numpy as np
import json


# Create your views here.
def getCalories(request):
    today = date.today()
    if request.user.is_authenticated:
        form = FoodForm()
        profileObj = Profile.objects.get(user__id=request.user.id)
        #get consume for today
        profileObj.ConsumeSetbyDate(
            chosenDateYear=today.year,
            chosenDateMonth=today.month,
            chosenDateDay=today.day,
        )
        consumeSet = profileObj.consumeSet
        #adding food to consume
        if request.GET:
            temp = request.GET["food"]
            foodItem = Food.objects.get(name=temp)
            consumed = Consume.objects.create(
                food=foodItem, owner=request.user, quantity=request.GET["quantity"]
            ).save()
            return redirect("calories")

        context = {
            "consumeSet": consumeSet,
            "form": form,
            "profileObj": profileObj,
            "today": today,
            "procentProgress": (profileObj.caloriesSum / profileObj.limitCalories)
            * 100,
        }
        return render(request, "calories/calories.html", context=context)
    else:
        return render(request, "calories/home.html")


@login_required(login_url="login")
def delete_consume(request, pk):
    try:
        consumeDelete = Consume.objects.get(id=pk)
    except:
        print("An exception occurred")

    if request.method == "POST":
        consumeDelete.delete()
        return HttpResponseRedirect("/")

    return render(
        request, "calories/delete_food.html", context={"consumeDelete": consumeDelete}
    )


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("calories")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="calories/register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("calories")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="calories/login.html",
        context={"login_form": form},
    )


@login_required(login_url="login")
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("calories")


@login_required(login_url="login")
def caloriesByDate(request):
    #function for selecting last five days consume
    today = date.today()
    profileObj = Profile.objects.get(user__id=request.user.id)
    profileObj.ConsumeSetbyDate(
        chosenDateYear=today.year, chosenDateMonth=today.month, chosenDateDay=today.day
    )
    consumeSet = Consume.objects.filter(owner__id=request.user.id)
    uniqueDates = list(
        {
            (consume.created.year, consume.created.month, consume.created.day)
            for consume in consumeSet
        }
    )
    diffrence = [abs(today - date(el[0], el[1], el[2])).days for el in uniqueDates]
    selectedDates = [uniqueDates[i] for i in list(np.argsort(diffrence)[::-1])]
    print(selectedDates)
    if (len(selectedDates)) > 5:
        selectedDates = selectedDates[-5:]
    caloriesList = []
    carbsList = []
    fatsList = []
    proteinsList = []
    stringDates = []
    for per_date in selectedDates:
        profileObj.ConsumeSetbyDate(per_date[0], per_date[1], chosenDateDay=per_date[2])
        caloriesList.append(profileObj.caloriesSum)
        carbsList.append(profileObj.carbsSum)
        fatsList.append(profileObj.fatsSum)
        proteinsList.append(profileObj.proteinsSum)
        stringDates.append(
            str(per_date[2]) + "." + str(per_date[1]) + "." + str(per_date[0])
        )

    context = {
        "profileObj": profileObj,
        "selectedDates": json.dumps(stringDates),
        "caloriesList": json.dumps(caloriesList),
        "proteinsList": json.dumps(proteinsList),
        "carbsList": json.dumps(carbsList),
        "fatsList": json.dumps(fatsList),
    }
    return render(
        request=request, template_name="calories/caloriesbydate.html", context=context
    )


@login_required(login_url="login")
def limitChange(request):
    #function for changing calories Limit
    if request.GET:
        temp = request.GET["caloriesLimit"]
        profileObj = Profile.objects.get(user__id=request.user.id)
        profileObj.limitCalories = temp
        profileObj.save()
        return redirect("calories")

    context = {}
    return render(
        request=request, context=context, template_name="calories/changeLimit.html"
    )
