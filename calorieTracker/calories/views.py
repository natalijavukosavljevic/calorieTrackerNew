from django.shortcuts import render,redirect
from django.db.models import Q
from . models import Food, Consume,Profile
from .forms import FoodForm, NewUserForm
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from datetime import date,timedelta,datetime
import numpy as np
import json



# Create your views here.

def getCalories(request):
     #foodSet=Food.objects.all()
     today = date.today()
     if request.user.is_authenticated:
        form=FoodForm()
        #  profile = request.user.profile ovo je problem mozda cu morati ponovo aplikaciju napraviti proveri sta je sa migracijom
        owner=request.user.username
        profileObj=Profile.objects.get(user__id=request.user.id)
        profileObj.ConsumeSetbyDate(chosenDateYear=today.year,chosenDateMonth=today.month,chosenDateDay=today.day)
        print('owner je ',profileObj.caloriesSum)
        #print(profileObj.carbsSum(chosenYear=today.year, chosenMonth=today.month, chosenDay=today.day))
        print(today)
        consumeSet=profileObj.consumeSet #moze i all jer za sad imamo jednog korisnika get je jedan samo korisnik Consume.objects.filter(owner__id=request.user.id)
        #print('priv',consumeSet[0].food.carbs)
        if request.GET:
            temp = request.GET['food'] #videces da li ces sa POSTOM  kasnije
            foodItem=Food.objects.get(name=temp)
            print('izabrani item je ',request.GET['quantity'] )
            consumed=Consume.objects.create(food=foodItem, owner=request.user,quantity=request.GET['quantity'] ).save() #nek ima vise banana ako hoce get_or_create tako nestp
            return redirect('calories')
	    
	      
        print('progress je ',(profileObj.caloriesSum/profileObj.limitCalories)) #dodaj u property
        context={'consumeSet':consumeSet, 'form':form, 'profileObj':profileObj, 'today':today, 'procentProgress':(profileObj.caloriesSum/profileObj.limitCalories)*100}
        return render(request, 'calories/calories.html',context=context)
     else:
	      return render(request, 'calories/home.html')
	     

def delete_consume(request, pk):
    # dictionary for initial data with
    # field names as keys
    print('id je ', pk)
 
    # fetch the object related to passed id
    #foodObj = get_object_or_404(Consume, id = pk)

    try:
     consumeDelete=Consume.objects.get(id=pk)
     print('objekat za brisanje ', consumeDelete)
    except:
     print("An exception occurred")
 
 
    if request.method =="POST":
    
        consumeDelete.delete() # foodObj.delete() ovo ce izrbisati food , ali nece consume kada se consume izbrise izbrisace se i foood cascade?
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")
 
    return render(request, "calories/delete_food.html", context={'consumeDelete': consumeDelete})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			login(request, user)
			messages.success(request, "Registration successful." ) 
			return redirect("calories")
		#messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="calories/register.html", context={"register_form":form})



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("calories")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="calories/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("calories")

def same_week(date1, date2):
    return date1.isocalendar()[1] == date2.isocalendar()[1] \
              and date1.year == date2.year

@login_required(login_url='login')
def caloriesByDate(request):
	today = date.today()
	#videcemo ovo za same week
	profileObj=Profile.objects.get(user__id=request.user.id)
	profileObj.ConsumeSetbyDate(chosenDateYear=today.year, chosenDateMonth=today.month, chosenDateDay=today.day)
	consumeSet=Consume.objects.filter(owner__id=request.user.id)
	print('datumi')
	uniqueDates = list({(consume.created.year, consume.created.month, consume.created.day) for consume in consumeSet})
	diffrence=[abs(today - date(el[0],el[1],el[2])).days for el in uniqueDates]
	print('razlike ', diffrence)
	selectedDates = [ uniqueDates[i] for i in list(np.argsort(diffrence)[::-1])]
	print(selectedDates)
	if (len(selectedDates))>5:
		selectedDates=selectedDates[0:5] #zadnjih 5 dana da pokaze statistiku
	

	#sortirati datume koji su najblizi ovom datumi ili posmatrati datume za samo tekucu nedelju
    #last ten inputs ili tako nesto
	caloriesList=[]
	carbsList=[]
	fatsList=[]
	proteinsList=[]
	stringDates=[]
	for per_date in selectedDates:
		profileObj.ConsumeSetbyDate(per_date[0], per_date[1], chosenDateDay=per_date[2])
		caloriesList.append(profileObj.caloriesSum)
		carbsList.append(profileObj.carbsSum)
		fatsList.append(profileObj.fatsSum)
		proteinsList.append(profileObj.proteinsSum)
		stringDates.append(str(per_date[2])+'.'+str(per_date[1])+'.'+str(per_date[0]))

	

	print(today.strftime("%A"))
	tommorow=today+timedelta(1)
	print(stringDates)
	print(tommorow.strftime("%A"))
	context={'profileObj':profileObj, 'selectedDates':json.dumps(stringDates), 
	  'caloriesList':json.dumps(caloriesList), 'proteinsList':json.dumps(proteinsList),
	  'carbsList':json.dumps(carbsList), 'fatsList':json.dumps(fatsList)}
	return render(request=request, template_name="calories/caloriesbydate.html", context=context)
	
@login_required(login_url='login')
def limitChange(request):
	if request.GET:
		temp=request.GET['caloriesLimit']
		profileObj=Profile.objects.get(user__id=request.user.id)
		profileObj.limitCalories=temp
		profileObj.save()
		return redirect('calories')
		
           
	context={}
	return render(request=request, context=context, template_name="calories/changeLimit.html")
    
    