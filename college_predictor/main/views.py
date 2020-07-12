from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from main.forms import SignUpForm

# Create your views here.

def index(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('main:login'))
    return render(request,"main/index.html")

def home(request):
    return render(request,"main/home.html")

def headerright(request):
    return render(request,"main/headerright.html")

def headerleft(request):
    return render(request,"main/headerleft.html")

def default(request):
    return render(request,"main/default.html")

def searchresult(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
    if not q:
        errors.append('Enter a search term.')
    else:
        ##books = Book.objects.filter(title__icontains=q)
        # database object and data retrieval statement
        # look searchbar in hello app in demo project
        return render(request,''' search html page ''',{
            #college table object ,
            'query': q,
            })
    return render(request,''' search html page ''',{
        'errors': errors
        })
    

def mail(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('e-mail') and '@' not in request.POST['e-mail']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
            request.POST['subject'],
            request.POST['message'],
            'koidalasai21@gmail.com',
            [request.POST.get('e-mail')],
        )
        return HttpResponseRedirect(reverse('main:success'))
    return render(request,'main/email.html', {
        'errors': errors,
        'subject': request.POST.get('subject', ''),
        'message': request.POST.get('message', ''),
        'e-mail': request.POST.get('e-mail', ''),
        }) 

def emailview(request):
    return render(request,"main/email.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def loginview(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("main:home"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid Credentials",
            })
    return render(request,"main/login.html")


def logoutview(request):
    logout(request)
    return render(request, "main/login.html", {
        "message": "Logged out."
    })

def aboutUs(request):
    pass

def contactUs(request):
    pass

def success(request):
    return render(request,"main/success.html")