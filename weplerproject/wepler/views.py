from django.shortcuts import render, redirect
from .models import Plus, Plz
from .form import PlusForm, PlzForm

def home(request):
    plus_user = Plus.objects
    plz_user = Plz.objects
    return render(request, 'home.html', {'plz_user': plz_user, 'plus_user' : plus_user})

def plus_signup(request):
    if request.method =='POST':
        form = PlusForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('home')
        else:
            return redirect('home')
    else:
        form = PlusForm()
        return render(request, 'plus_signup.html', {'form':form} )

def plz_signup(request):
    if request.method =='POST':
        form = PlzForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('home')
        else:
            return redirect('home')
    else:
        form = PlzForm()
        return render(request, 'plz_signup.html', {'form':form} )
