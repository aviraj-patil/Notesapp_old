from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Notes
from .forms import NotesForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    notes = Notes.objects.filter(user=request.user).order_by('-dateedited')
    return render(request, 'notes/home.html',{'notes': notes})

def signupuser(request):
    if request.method == 'GET':
        return render (request, 'notes/signupuser.html', {'form':UserCreationForm()})
    else:
        if (request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render (request, 'notes/signupuser.html', {'form':UserCreationForm(), 'error':'Username has already been taken, plz choose new username'})                
        else:
            return render (request, 'notes/signupuser.html', {'form':UserCreationForm(), 'error':'Password did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render (request, 'notes/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render (request, 'notes/loginuser.html', {'form':AuthenticationForm(), 'error':'username or password did not match'})
        else:
            login(request, user)
            return redirect('home')

@login_required            
def createnote(request):
    if request.method == 'GET':
        return render (request, 'notes/createnote.html', {'form':NotesForm()})
    else:
        try:
            form = NotesForm(request.POST)
            newnote = form.save(commit=False)
            newnote.user = request.user 
            newnote.save()                
            return redirect('home')
        except ValueError:
            return render (request, 'notes/home.html', {'form':NotesForm(), 'error':'Bad data passed in'})   

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required    
def viewnotes(request, notes_pk):
    notes = get_object_or_404(Notes,pk=notes_pk,user=request.user)
    if request.method == 'GET':
        form = NotesForm(instance=notes)
        return render(request, 'notes/viewnotes.html', {'notes': notes, 'form':form})
    else:
        try:
            form = NotesForm(request.POST, instance=notes)
            form.save()
            return redirect('home')
        except ValueError:
            return render (request, 'notes/viewnotes.html', {'form':NotesForm(), 'form':form, 'error':'Bad data passed in'})

@login_required
def deletenote(request, notes_pk):
    notes = get_object_or_404(Notes,pk=notes_pk,user=request.user)
    if request.method == 'POST':
        notes.delete()
        return redirect('home')
    
def greetings(request):
    return render(request, 'notes/greetings.html')