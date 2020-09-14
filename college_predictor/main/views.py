from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import college_details, cutoff
import pandas as pd
import numpy as np
import math as m
from main.forms import SignUpForm


# Create your views here.

def index(request):
    if request.user.is_authenticated:
         return render(request, "main/index.html", {
             'check': True,
         })
    return render(request,"main/index.html", {
        'check': False,
    })


def home(request):
    if request.user.is_authenticated:
        return render(request, "main/home.html", {
             'check': True,
         })
    return render(request,"main/home.html", {
        'check': False,
    })


def searchresult(request):
    if request.method == 'GET':
        searchname=request.GET['search-box']
        q01=cutoff.objects.all().values('Eamcet_Code','Course_Code')
        q01=pd.DataFrame(list(q01))
        q02=pd.DataFrame(list(college_details.objects.all().values('Eamcet_Code','College_Name','District','Place','Contact_No','Website','NBA','NAAC','NIRF').filter(College_Name__icontains=searchname)))
        if q02.empty:
            return render(request, "main/search.html", {
            'check': request.user.is_authenticated,
            'qs':list(pd.DataFrame()),
            'errors':True,
        })
        q0=pd.merge(q01,q02,how="inner",left_on="Eamcet_Code",right_on="Eamcet_Code")
        q0=q0.applymap(lambda x: None if x == '' else x)
        return render(request, "main/search.html", {
            'check': request.user.is_authenticated,
            'qs':list(q0.T.to_dict().values()),
            'errors':False,
        })
    return render(request, "main/search.html", {
            'check': request.user.is_authenticated,
            'qs':list(pd.DataFrame()),
            'errors':True,
        })


def mail(request):
    if 'curr_user' in request.session and request.user.username == request.session['curr_user']:
        html_message = render_to_string('main/email.html', {
            'user':request.session['curr_user'],
            'qs':request.session['result'],
            'preferences':request.session['preferences'],
            'querytype':request.session['querytype']
            })
        plain_message = strip_tags(html_message)
        send_mail(
                "Your College List From College Predictor",
                plain_message,
                '18135a0520@gvpce.ac.in',
                [request.user.email],
                html_message=html_message
            )
        return render(request,"main/success.html")
    return HttpResponseRedirect(reverse("main:login"))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            request.session['curr_user']=username
            login(request, user)
            return HttpResponseRedirect(reverse('main:home'))
        # else:
        #     form = SignUpForm()
        #     return render(request, 'main/login.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'main/login.html', {'form': form})


def loginview(request):
    if request.user.is_authenticated:
         return render(request, "main/login.html", {
             'check': True,
         })
    
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['curr_user']=username
            login(request, user)
            return HttpResponseRedirect(reverse("main:home"))
        else:
            form=SignUpForm()
            return render(request, "main/login.html", {
                "message": "Invalid Credentials",
                'form':form,
            })
    else:
        form=SignUpForm()
    return render(request,"main/login.html",{
        'check':False,
        'form': form
    })


def logoutview(request):
    logout(request)
    return render(request, "main/logout.html")


def aboutUs(request):
    if request.user.is_authenticated:
         return render(request, "main/about.html", {
             'check': True,
         })
    return render(request,"main/about.html", {
        'check': False,
    })


def contactUs(request):
    if request.user.is_authenticated:
         return render(request, "main/contact.html", {
             'check': True,
         })
    return render(request,"main/contact.html", {
        'check': False,
    })


def query1(request):
    if request.method == 'GET':
        district=request.GET['choice-district']
        q11=cutoff.objects.filter(District__exact=district).all().values('Eamcet_Code','Course_Code')
        q11=pd.DataFrame(list(q11))
        q12=pd.DataFrame(list(college_details.objects.filter(District__exact=district).all().values()))
        if 'Gender' in request.GET:
            gender=request.GET['Gender']
        else:
            gender='B'
        q12, preferences_list,academics,placements,coll_size,coll_type=clean_data(request,df= q12, gender=gender)
        preferences=False
        q12['percentage']=0
        if 'preferences-checkbox' in request.GET and request.GET['preferences-checkbox']=="on":
            preferences=True
            q12['percentage'] = q12.apply(lambda row:calculate_percentage(row,preferences_list=preferences_list,academics=academics,placements=placements,coll_size=coll_size,coll_type=coll_type),axis=1) 
        q1=pd.merge(q11,q12,how="inner",left_on="Eamcet_Code",right_on="Eamcet_Code")
        q1=q1[['Eamcet_Code','College_Name','Course_Code','District','Place','Contact_No','Website','NBA','NAAC','NIRF','percentage']]
        if not 'result' in request.session:
            request.session['result']=list(q1.T.to_dict().values())
        else:
            request.session['result']=list(q1.T.to_dict().values())

        if not 'preferences' in request.session:
            request.session['preferences']=preferences
        else:
            request.session['preferences']=preferences

        if not 'querytype' in request.session:
            request.session['querytype']=1
        else:
            request.session['querytype']=1
        return render(request, "main/result.html", {
            'check': request.user.is_authenticated,
            'qs':list(q1.T.to_dict().values()),
            'preferences':preferences,
            'querytype':1,
        })
    return render(request,"main/home.html", {
        'check': request.user.is_authenticated,
    })


def query2(request):
    if request.method == 'GET':
        rank=int(request.GET["rank"])
        category=request.GET["choice-caste"]
        if request.GET["gender-out"] == 'Male':
            category+='b'
            gender='B'
        elif request.GET["gender-out"] == 'Female':
            category+='g'
            gender='G'
        q21=cutoff.objects.all().values('Eamcet_Code','Course_Code',category)
        q21=pd.DataFrame(list(q21))
        q21=q21[q21[category]!='']
        q21[category]=(q21[category]).astype(int)
        q21=q21[q21[category]>=rank]
        q22=pd.DataFrame(list(college_details.objects.all().values()))
        q22, preferences_list,academics,placements,coll_size,coll_type=clean_data(request,df= q22, gender=gender)
        preferences=False
        q22['percentage']=0
        if 'preferences-checkbox' in request.GET and request.GET['preferences-checkbox']=="on":
            preferences=True
            q22['percentage'] = q22.apply(lambda row:calculate_percentage(row,preferences_list=preferences_list,academics=academics,placements=placements,coll_size=coll_size,coll_type=coll_type),axis=1) 
        q2=pd.merge(q21,q22,how="inner",left_on="Eamcet_Code",right_on="Eamcet_Code")
        q2=q2[['Eamcet_Code','College_Name','Course_Code','District','Place','Contact_No','Website','NBA','NAAC','NIRF','percentage']]
        if not 'result' in request.session:
            request.session['result']=list(q2.T.to_dict().values())
        else:
            request.session['result']=list(q2.T.to_dict().values())

        if not 'preferences' in request.session:
            request.session['preferences']=preferences
        else:
            request.session['preferences']=preferences

        if not 'querytype' in request.session:
            request.session['querytype']=2
        else:
            request.session['querytype']=2
        return render(request, "main/result.html", {
            'check': True,
            'qs':list(q2.T.to_dict().values()),
            'preferences':preferences,
            'querytype':2,
    })
    return render(request,"main/home.html", {
        'check': request.user.is_authenticated,
    })
    

def query3(request):
    if request.method == 'GET':
        district=request.GET["choice-district"]
        rank=int(request.GET["rank"])
        category=request.GET["choice-caste"]
        if request.GET["gender-out"] == 'Male':
            category+='b'
            gender='B'
        elif request.GET["gender-out"] == 'Female':
            category+='g'
            gender='G'
        q31=cutoff.objects.all().filter(District__exact=district).values('Eamcet_Code','Course_Code',category)
        q31=pd.DataFrame(list(q31))
        q31=q31[q31[category]!='']
        q31[category]=(q31[category]).astype(int)
        q31=q31[q31[category]>=rank]
        q32=pd.DataFrame(list(college_details.objects.filter(District__exact=district).all().values()))
        q32, preferences_list,academics,placements,coll_size,coll_type=clean_data(request,df= q32, gender=gender)
        preferences=False
        q32['percentage']=0
        if 'preferences-checkbox' in request.GET and request.GET['preferences-checkbox']=="on":
            preferences=True
            q32['percentage'] = q32.apply(lambda row:calculate_percentage(row,preferences_list=preferences_list,academics=academics,placements=placements,coll_size=coll_size,coll_type=coll_type),axis=1) 
        q3=pd.merge(q31,q32,how="inner",left_on="Eamcet_Code",right_on="Eamcet_Code")
        q3=q3[['Eamcet_Code','College_Name','Course_Code','District','Place','Contact_No','Website','NBA','NAAC','NIRF','percentage']]
        if not 'result' in request.session:
            request.session['result']=list(q3.T.to_dict().values())
        else:
            request.session['result']=list(q3.T.to_dict().values())

        if not 'preferences' in request.session:
            request.session['preferences']=preferences
        else:
            request.session['preferences']=preferences

        if not 'querytype' in request.session:
            request.session['querytype']=3
        else:
            request.session['querytype']=3
        return render(request, "main/result.html", {
            'check': True,
            'qs':list(q3.T.to_dict().values()),
            'preferences':preferences,
            'querytype':3,
    })
    return render(request,"main/home.html", {
        'check': request.user.is_authenticated,
    })


def clean_data(request, df=None, gender=None):
    preferences_list = []
    academics,placements,coll_size,coll_type=0,0,0,0
    df=df.applymap(lambda x: None if x == '' else x)
    if 'college-type' in request.GET:
        preferences_list.append('College_type')
        coll_type = int(request.GET['college-type'])
        df['College_Type']=df['College_Type'].apply(lambda x:np.nan if x == None else int(x))
    if 'coed' in request.GET and request.GET['coed']=='1':
        preferences_list.append('Coed')
        df['Coed']=df['Coed'].apply(lambda x:np.nan if x == None else int(x))
    if 'college-size' in request.GET:
        preferences_list.append('Size')
        coll_size = int(request.GET['college-size'])
        df['Size']=df['Size'].apply(lambda x:np.nan if x == None else int(x))
    if 'academics' in request.GET: 
        preferences_list.append('Academics_Quality')
        academics = int(request.GET['academics'])
        df['Academics_Quality']=df['Academics_Quality'].apply(lambda x:np.nan if x == None else float(x))
    if 'placements' in request.GET: 
        preferences_list.append('Placements_Rating')
        placements = int(request.GET['placements'])
        df['Placement_Rating']=df['Placement_Rating'].apply(lambda x:np.nan if x == None else float(x))
    if 'sports' in request.GET and request.GET['sports']=='1':
        preferences_list.append('Sports')
        df['Sports']=df['Sports'].apply(lambda x:np.nan if x == None else int(x))
    if 'hostel' in request.GET and request.GET['hostel']=='1':
        if gender=='B':
            preferences_list.append('Hostel_B')
        else:
            preferences_list.append('Hostel_G')
        df['Hostel_B']=df['Hostel_B'].apply(lambda x:np.nan if x == None else int(x))
        df['Hostel_G']=df['Hostel_G'].apply(lambda x:np.nan if x == None else int(x))
    if 'bus' in request.GET and request.GET['bus']=='1':
        preferences_list.append('Bus_Facility')
        df['Bus_Facility']=df['Bus_Facility'].apply(lambda x:np.nan if x == None else int(x))
    if 'clubs' in request.GET and request.GET['clubs']=='1':
        preferences_list.append('Clubs')
        df['Clubs']=df['Clubs'].apply(lambda x:np.nan if x == None else int(x))
    if 'medical' in request.GET and request.GET['medical']=='1':
        preferences_list.append('Medical_Care')
        df['Medical_Care']=df['Medical_Care'].apply(lambda x:np.nan if x == None else int(x))        
    return (df,preferences_list,academics,placements,coll_size,coll_type)


def calculate_percentage(row, preferences_list=None,academics=None,placements=None,coll_size=None,coll_type=None):
    if len(preferences_list)==0:
        row['percentage']=0
    else:
        factor = 0
        score = 0
        if 'College_Type' in preferences_list:
            if row['College_Type']==coll_type:
                score+=1
            if not m.isnan(row['College_Type']):
                factor+=1
        if 'Coed' in preferences_list:
            if row['Coed']==1:
                score+=1
            if not m.isnan(row['Coed']):
                factor+=1
        if 'Size' in preferences_list:
            if row['Size']==coll_size:
                score+=1
            if not m.isnan(row['Size']):
                factor+=1
        if 'Academics_Quality' in preferences_list:
            if row['Academics_Quality']>=academics:
                score+=1
            if not m.isnan(row['Academics_Quality']):
                factor+=1
        if 'Placement_Rating' in preferences_list:
            if row['Placement_Rating']>=placements:
                score+=1
            if not m.isnan(row['Placement_Rating']):
                factor+=1
        if 'Sports' in preferences_list:
            if row['Sports']==1:
                score+=1
            if not m.isnan(row['Sports']):
                factor+=1
        if 'Hostel_B' in preferences_list:
            if row['Hostel_B']==1:
                score+=1
            if not m.isnan(row['Hostel_B']):
                factor+=1
        elif 'Hostel_G' in preferences_list:
            if row['Hostel_G']==1:
                score+=1
            if not m.isnan(row['Hostel_G']):
                factor+=1
        if 'Bus_Facility' in preferences_list:
            if row['Bus_Facility']==1:
                score+=1
            if not m.isnan(row['Bus_Facility']):
                factor+=1
        if 'Clubs' in preferences_list:
            if row['Clubs']==1:
                score+=1
            if not m.isnan(row['Clubs']):
                factor+=1
        if 'Medical_Care' in preferences_list:
            if row['Medical_Care']==1:
                score+=1
            if not m.isnan(row['Medical_Care']):
                factor+=1
        if factor==0:
            row['percentage']=0
        else:
            row['percentage']=round((score/factor)*100)
    return row['percentage']
    