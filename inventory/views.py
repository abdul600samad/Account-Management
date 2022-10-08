from django.shortcuts import render,redirect
from inventory.models import atten
from django.db.models import Sum
import sqlite3
from inventory.forms import attenform
from inventory.models import work
db=sqlite3.connect('data.db',check_same_thread=False)
cur=db.cursor()
cur.execute('create table if not exists login (username varchar(50),email varchar(50),first_name varchar(50),last_name varchar(50),password varchar(20));')
db.commit()

cur.execute('create table if not exists work (number varchar(50), name varchar(50),quantity varchar(50), price varchar(10),total_price varchar(20));')
db.commit()
def signup(request):
    if 'name' in request.session:
        return redirect('index')
    else:
        if request.method=="POST":
            un=request.POST['username']
            em=request.POST['email']
            fn=request.POST['first_name']
            ln=request.POST['last_name']
            pw1=request.POST['password1']
            pw2=request.POST['password2']
            if pw1!=pw2:
                error="Both Passwords do not match"
                return render(request,'inventory/signup.html',{'error':error})
            else:
                cur.execute(f"insert into login values ('{un}', '{em}', '{fn}', '{ln}', '{pw1}');")
                db.commit()
                
                request.session['name']=un
                return redirect('index')
    return render(request,'inventory/signup.html')

def login(request):
    if 'name' in request.session:
        return redirect('index')
    else:
        if request.method=="POST":
            un=request.POST['username']
            pw=request.POST['password']
            cur.execute(f"select * from login where username='{un}' and password='{pw}';")
            record=cur.fetchone()
            if record==None:
                error="Invalid username or password"
                return render(request,'inventory/login.html',{'error':error})
            else:
                request.session['name']=un
                return redirect('index')
    return render(request,'inventory/login.html')
def logout(request):
    if 'name' not in request.session:
        return redirect('login')
    else:
        request.session.pop('name')
        return redirect('login')



# Create your views here.
def index(request):
    if 'name' in request.session:
        obj=atten.objects.all()
        total_mud=atten.objects.aggregate(Sum('mudeem')) 
        total_mud=total_mud['mudeem__sum']

        total_hour_mud=atten.objects.aggregate(Sum('mudeem_hour'))
        total_hour_mud=total_hour_mud['mudeem_hour__sum']
        price_mud=(total_mud)*500+(total_hour_mud*70)

        total_naj=atten.objects.aggregate(Sum('najim'))  
        total_naj=total_naj['najim__sum']
        total_hour_naj=atten.objects.aggregate(Sum('najim_hour'))
        total_hour_naj=total_hour_naj['najim_hour__sum']
        price_naj=(total_naj)*500+(total_hour_naj)*70
        

        total_nij=atten.objects.aggregate(Sum('nijam'))  
        total_nij=total_nij['nijam__sum']
        total_hour_nij=atten.objects.aggregate(Sum('nijam_hour'))
        total_hour_nij=total_hour_nij['nijam_hour__sum']
        price_nij=(total_nij)*500+(total_hour_nij)*70

        cont={'obj':obj,'total_mud':total_mud,'total_naj':total_naj,'total_nij':total_nij,'price_mud':price_mud,'price_naj':price_naj,'price_nij':price_nij,'total_hour_mud':total_hour_mud,'total_hour_naj':total_hour_naj,'total_hour_nij':total_hour_nij}
        print("request.user:",request.user)
        print("Hiii")
        print("request.session['name']:",request.session['name'])
        return render(request,'inventory/index.html',cont)
    else:
        return redirect('login')

def attendence(request):
    if 'name' in request.session:
        if request.method=="POST":
            fm=attenform(request.POST)
            if fm.is_valid():
                day=fm.cleaned_data['day']
                mud=fm.cleaned_data['mudeem']
                naj=fm.cleaned_data['najim']
                nij=fm.cleaned_data['nijam']
                mud_hour=fm.cleaned_data['mudeem_hour']
                naj_hour=fm.cleaned_data['najim_hour']
                nij_hour=fm.cleaned_data['nijam_hour']
                obj=atten(day=day,mudeem=mud,mudeem_hour=mud_hour,najim=naj,najim_hour=naj_hour,nijam=nij,nijam_hour=nij_hour)
                obj.save()
                return redirect('index')
        else:
            fm=attenform()
        return render(request,'inventory/atten.html',{'form':fm})
    else:
        return redirect('login')

def delete(request,id):
    if 'name' in request.session:
        pi=atten(pk=id)
        pi.delete()
        return redirect('index')
    else:
        return redirect('login')

def update(request,id):
    if 'name' in request.session:
        if request.method=="POST":
            pi=atten.objects.get(pk=id)
            fm=attenform(request.POST,instance=pi)
            if fm.is_valid():
                id=fm.cleaned_data['id']
                day=fm.cleaned_data['day']
                mud=fm.cleaned_data['mudeem']
                naj=fm.cleaned_data['naj']
                nij=fm.cleaned_data['nijam']
                obj=atten(id=id,day=day,mudeem=mud,najim=naj,nijam=nij)
                obj.save()
                return redirect('index')
        else:
            pi=atten.objects.get(pk=id)
            fm=attenform(instance=pi)
        return render(request,'inventory/update.html',{'form':fm})
    else:
        return redirect('login')
                
def add_items(request):
    if 'name' in request.session:
        if request.method=="POST":
            nb=request.POST['num']
            nm=request.POST['name']
            qt=request.POST['quantity']
            pr=request.POST['price']
            qt=int(qt)
            pr=int(pr)
            tp=qt*pr
            cur.execute(f"insert into work values('{nb}','{nm}','{qt}','{pr}','{tp}');")
            db.commit()
        return render(request,'inventory/work.html')
    else:
        return redirect('login')

def view_items(request):
    if 'name' in request.session:
        cur.execute("select * from work;")
        obj1=cur.fetchall()
        cur.execute("select sum(total_price) from work;")
        total_sum=cur.fetchone()
        total_sum=list(total_sum)
        return render(request,'inventory/viewitems.html',{'obj1':obj1,'total_sum':total_sum[0]})
    else:
        return redirect('login')