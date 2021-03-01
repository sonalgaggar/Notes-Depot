from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date
from django.contrib import messages
from .forms import signupform,loginform,addsubject
from django.shortcuts import get_object_or_404


# Create your views here.
def story(request,category_slug=None):
    category=None
    categories=Category.objects.all()
    notes=Notes.objects.filter(status="ACCEPT")
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        notes=notes.filter(subject=category)
    return render(request,'story.html',{'categories':categories,'notes':notes,'category':category})

def viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.filter(status="ACCEPT")
    print(notes)
    d={'notes':notes}
    return render(request,'viewallnotes.html',d)


def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def userlogin(request):
    
    if request.method=="POST":
        form=loginform(request=request,data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            upass=form.cleaned_data['password']
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,'logged in successfully')
                return render(request,'login.html',{'error':"no"})
    else:
        form=loginform()
    d={'form':form}
    return render(request,'login.html',d)
    

    

    

def login_admin(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                redirect('view_users')
                error="no"
            else:
                error="yes"
        except:
            error="yes"
        
    d={'error':error}
    return render(request,'login_admin.html',d)

def signup1(request):
    if request.method=="POST":
        form=signupform(request.POST)
        if form.is_valid():
            messages.success(request,'congratulations!!! you have become a user')
            form.save()
    else:
        form=signupform()
    d={'form':form}
    return render(request,'signup.html',d)

def add_subject(request):
    if request.method=="POST":
        form=addsubject(request.POST)
        if form.is_valid():
            messages.success(request,'subject added succesfully')
            form.save()
            return redirect('upload_notes')
    else:
        form=addsubject()
    d={'form':form}
    return render(request,'add_subject.html',d)
     
    
            
    
    
    



def Logout(request):
    logout(request)
    return redirect('index')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    #data=Signup.objects.get(user=user)
    #d={'data':data,'user':user}
    d={'user':user}
    return render(request,'profile.html',d)


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    #data=Signup.objects.get(user=user)
    error= False
    if request.method =='POST':
        f=request.POST['firstname']
        l=request.POST['lastname']
        e=request.POST['emailid']
        user.first_name=f
        user.last_name=l
        user.email=e
        user.save()
        
        error=True
    d={'user':user,'error':error}
    return render(request,'edit_profile.html',d)


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=="POST":
        o = request.POST['old']
        n=request.POST['new']
        c=request.POST['confirm']
        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render(request,'changepassword.html',d)

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        
        sid=request.POST['subject']
        s=Category.objects.get(id=sid)
        n=request.FILES['notesfile']
        f=request.POST['filetype']
        d=request.POST['description']
        u=User.objects.filter(username=request.user.username).first()
        print(u)
        try:
            
            Notes.objects.create(user=u,uploadingdate=date.today(),subject=s,notesfile=n,filetype=f,descriptions=d,status='pending')
            print("hello")
            error="no"
           
        except:
            error="yes"
    
    
    d={'error':error,'category':Category.objects.all()}

    return render(request,'upload_notes.html',d)

def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    notes=Notes.objects.filter(user=user)
    
    d={'notes':notes}
    return render(request,'view_mynotes.html',d)


def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('view_myotes')


def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user=User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')




def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users=User.objects.filter(is_staff=False)
    
    d={'users':users}
    return render(request,'view_users.html',d)

    
def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.filter(status='pending')
    
    d={'notes':notes}
    return render(request,'pending_notes.html',d)


def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.filter(status="ACCEPT")
    
    d={'notes':notes}
    return render(request,'accepted_notes.html',d)


def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.filter(status="REJECT")
    
    d={'notes':notes}
    return render(request,'rejected_notes.html',d)


def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.all()
    
    d={'notes':notes}
    return render(request,'all_notes.html',d)

def assign_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.get(id=pid)
    error=""
    if request.method=='POST':
        s=request.POST['status']
        try:
            notes.status=s
            notes.save()
            error="no"
        except:
            error="yes"
    d={'notes':notes,'error':error}
    return render(request,'assign_status.html',d)


def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('all_notes')


