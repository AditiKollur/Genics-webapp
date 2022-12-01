from django.shortcuts import render, HttpResponse
import pyrebase
from django.core.files.storage import default_storage
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import os as os123
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime



cred = credentials.Certificate("path to service account")
firebase_admin.initialize_app(cred)

config={
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
}


# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
db = firestore.client()



def signIn(request):
    return render(request,"Login.html")

def home(request):
    return render(request,"SignUpFormReg.html")
 
def projects(request):
    return render(request, "projects.html")
  
def contacts(request):
    return render(request, "contacts.html")

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    print(email)
    print(pasw)

    if(email == 'admin@admin.com' and pasw == 'admin'):

        blood_group = {}
        gGender = {}

        dis_dict = {'Episodic Ataxia type 2' : [], 'Huntingtin' : [], 'Spino cerebellar Ataxia type 1' : [],'Spino cerebellar Ataxia type 2' : [], 'Spino cerebellar Ataxia type 3' : [], 'Spino cerebellar Ataxia type 7' : []}

        

        result = db.collection("User Information").stream()
        for doc in result:
            docId = str(doc.id)
            print(docId)
            result1 = db.collection("User Information").document(docId).collection("Patient Details").stream()

            for d in result1:

                dId = str(d.id)
                
                res = db.collection("User Information").document(docId).collection("Patient Details").document(dId).get()
                if(res.exists):
                    r = res.to_dict()
                    gen=r['gender']
                    bg=r['Blood']
                    
                    if(gen not in gGender):
                        gGender[gen] = 1
                    else:
                        gGender[gen] = gGender[gen] + 1
                    if(bg not in blood_group):
                        blood_group[bg] = 1
                    else:
                        blood_group[bg] = blood_group[bg] + 1

                result2=db.collection("User Information").document(docId).collection("Patient Details").document(dId).collection("Results").stream()

                

                for dis_list in result2:
                    
                    disId = str(dis_list.id)
                    
                    res2 = db.collection("User Information").document(docId).collection("Patient Details").document(dId).collection("Results").document(disId).get()

                    if(res2.exists):
                        r2 = res2.to_dict()
                        dis_risk = r2['Risk']
                        dis_dict[disId].append(dis_risk)                        
        print(dis_dict)

        x1 = []
        y1 = []

        x2 = []
        y2 = []

        for key, values in gGender.items():
            x1.append(values)      
            y1.append(key) 

        for key, values in blood_group.items():
            x2.append(values)      
            y2.append(key) 


        print("x1: " + str(x1))
        print("y1: " + str(y1))

        print("x2: " + str(x2))
        print("y2: " + str(y2))        

        fig1=go.Figure()
        fig1.add_trace(go.Bar(x=y1,y=x1))
        fig1.update_xaxes(title_text="Gender")
        fig1.update_yaxes(title_text="Count")
        layout=go.Layout(hovermode="x unified")
        plot1=plot({'data':fig1,'layout':layout},output_type='div')


        fig2=go.Figure()
        fig2.add_trace(go.Bar(x=y2,y=x2))
        fig2.update_xaxes(title_text="Blood group")
        fig2.update_yaxes(title_text="Count")
        plot2=plot({'data':fig2,'layout':layout},output_type='div')


        fig3=go.Figure()

        fig3.add_traces(go.Pie(labels = pd.Series(dis_dict["Episodic Ataxia type 2"]).value_counts().index, values = pd.Series(dis_dict["Episodic Ataxia type 2"]).value_counts().values, title = "Episodic Ataxia type 2", visible = True))
        fig3.add_traces(go.Pie(labels = pd.Series(dis_dict["Huntingtin"]).value_counts().index, values = pd.Series(dis_dict["Huntingtin"]).value_counts().values, title = "Huntingtin", visible = False))
        fig3.add_traces(go.Pie(labels = pd.Series(dis_dict["Spino cerebellar Ataxia type 1"]).value_counts().index, values = pd.Series(dis_dict["Spino cerebellar Ataxia type 1"]).value_counts().values, title = "Spino cerebellar Ataxia type 1", visible = False))
        fig3.add_traces(go.Pie(labels = pd.Series(dis_dict["Spino cerebellar Ataxia type 2"]).value_counts().index, values = pd.Series(dis_dict["Spino cerebellar Ataxia type 2"]).value_counts().values, title = "Spino cerebellar Ataxia type 2", visible = False))
        fig3.add_traces(go.Pie(labels = pd.Series(dis_dict["Spino cerebellar Ataxia type 3"]).value_counts().index, values = pd.Series(dis_dict["Spino cerebellar Ataxia type 3"]).value_counts().values, title = "Spino cerebellar Ataxia type 3", visible = False))
        fig3.add_traces(go.Pie(labels = pd.Series(dis_dict["Spino cerebellar Ataxia type 7"]).value_counts().index, values = pd.Series(dis_dict["Spino cerebellar Ataxia type 7"]).value_counts().values, title = "Spino cerebellar Ataxia type 7", visible = False))



        updatemenus = [
        dict(
            buttons = list([
                dict(label = "Episodic Ataxia type 2",method = "update", args = [{"visible":[True,False,False,False,False,False]}]),
                dict(label = "Huntingtin",method = "update", args = [{"visible":[False,True,False,False,False,False]}]),
                dict(label = "Spino cerebellar Ataxia type 1",method = "update", args = [{"visible":[False,False,True,False,False,False]}]),
                dict(label = "Spino cerebellar Ataxia type 2",method = "update",  args = [{"visible":[False,False,False,True,False,False]}]),
                dict(label = "Spino cerebellar Ataxia type 3",method = "update",  args = [{"visible":[False,False,False,False,True,False]}]),
                dict(label = "Spino cerebellar Ataxia type 7",method = "update",  args = [{"visible":[False,False,False,False,False,True]}]),
            ]),
            direction="down",
            pad={"r": 0, "t": 0, "l":0, "b":0},
            showactive=False,
            x=0.89,
            xanchor="left",
            y=1.2,
            yanchor="top",
        ),
        ]

        fig3.update_layout(updatemenus=updatemenus, showlegend = True)

        
        plot3=plot({'data':fig3},output_type='div')



        return render(request, "Admin.html",context={'plot1':plot1,'plot2':plot2,'plot3': plot3})


    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
        session_id = user['idToken']
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    session_id=user['localId']
    request.session['uid']=str(session_id)
    print(session_id)
    result = db.collection("User Information").document(session_id).get()

    return render(request,"SignUpFormReg.html",{"email":email})



def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")
 
def signUp(request):
    return render(request,"Registration.html")
 
def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        print(uid)
     except:
        return render(request, "Registration.html")
     return render(request,"Login.html")

def loadform(request):
    print("Hello")
    fname=str(request.POST.get('fname'))
    lname=str(request.POST.get('lname'))
    gender=str(request.POST.get('gender'))

    if gender=="Gender":
        return render(request,"SignUpFormReg.html",{'message':"Please select blood group"})

    bg=str(request.POST.get('bg'))
    if bg=="Blood Group":
        return render(request,"SignUpFormReg.html",{'message':"Please select blood group"})

    dt=str(request.POST.get('dob'))
    dt = datetime.strptime(dt, "%Y-%m-%d")
    current_date = datetime.now()

    if(dt.date() > current_date.date()):
        return render(request,"SignUpFormReg.html",{'message':"Invalid date"})

    
    phone=str(request.POST.get('phone'))
    if len(phone)!=10:
        return render(request,"SignUpFormReg.html",{'message':"Invalid phone number"})

    mstatus=str(request.POST.get('mstatus'))
    if mstatus=='Marital Status':
        return render(request,"SignUpFormReg.html",{'message':"Please select marital status"})


    uid=request.session['uid']
    print(uid)
    request.session.set_expiry(300)

    name = fname + " "+ lname

    request.session["name"] = name

    result = db.collection("User Information").document(uid).collection("Patient Details").document(name).get()
    if(result.exists):
        res = result.to_dict()
        fname=res['fname']
        return render(request,"Home.html",{'message':"Data already exists"})

    data1 = {"uid": uid}
    db.collection("User Information").document(uid).set(data1)
    data={'fname':fname,'lname':lname,'Blood':bg,'phone':phone,'gender':gender,'mstatus':mstatus}
    db.collection("User Information").document(uid).collection("Patient Details").document(name).set(data)
    return render(request,"Home.html",{'message':"Data entered successfully"})



def selection(request):
    u=str(request.POST.get('u'))
    print(u)
    if u=="user":
        return render(request,"Home.html",{'message':"Please select user"})
    request.session.set_expiry(300)

    return render(request,"Upload.html",{'u':u})


def upload(request):
    request.session.set_expiry(300)

    return render(request,"Upload.html")


def solve(s, w, start, end):        ##Function to find maximum k-repeating substring from sequence in Python
    s = s[start:end]
    Count=s.count(w)
    if Count==0:
        return 0
    for i in range(Count,0,-1):
        if w*i in s:
            return i


def algorithm(request):   
    file = request.FILES['textFile']
    file_name = default_storage.save(file.name, file)
    file_url = default_storage.path(file_name)

    s=open(file_url).readlines()
    t= "" 
    numList = []
    
    lst = []
    for i in s:
        h = str(i)
        if(h.find("chromosome")!= -1):
            numList.append(h.split(",")[0].split()[-1])
            lst.append(t)
            t = ""
        else:
            t = t + h

    report = []
    report1 = []
    gene=[]
    flag = True
    for i in range(len(lst)):
        try:
            if((int(numList[i]) >= 0 and int(numList[i]) <= 22)):
                flag = True
            else:
                flag = False
        except:
            if((numList[i] == 'X') or (numList[i] == 'Y')):
                flag = True
            else:
                flag = False

        if(not flag):
            break
        else:
            s = lst[i]
            s = s.replace('\n', '')

            # startInd=[0,0,63850225,3076237,0,16299337,0,0,0,0,0,111887518,0,92511111,0,0,0,0,13743839,0,0,0,0,0]#start index chr number
            # endInd=  [0,0,63989307,3245692,0,16761724,0,0,0,0,0,112037755,0,92572964,0,0,0,0,13317251,0,0,0,0,0]

            #startInd=[0,0,0,0,0,0]#start index chr number
            #endInd=[214,0,0,0,0,214]
            startInd=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
            endInd=[22,20,413,414,15,16,17,18,219,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]

        
            #startInd=[0,0,0,0,0,0]#start index chr number
            #endInd=[214,0,0,0,0,214]
        
            w = "CAG"

            ch=numList[i]
        
            #print(ch)
            if(ch == "X"):
                ch = "23"
            elif ch == "Y":
                ch = "24"
        
            u = int(ch)
            start = startInd[u-1]
            end = endInd[u-1]
        
            sol=solve(s, w,start, end)

            if ch=="3":
                gene="ATXN7"
                dis="Spino cerebellar Ataxia type 7"
                sym="""Eventual loss of vision,Severe dysarthria and dysphagia,Bedridden state with loss of motor control"""
                if sol<306 and sol>36:
                    risk="100%"
                    risk_fut="50%"
                elif sol<35 and sol>6:
                    risk="75%"
                    risk_fut="35%"
                else:
                    risk="No risk detected"
                    risk_fut="No potential risk detected"
                report1.append([ch,gene,dis,risk, risk_fut,sym]) 
                report.append([ch,gene,start,end,dis,sol,risk, risk_fut])

            elif ch=="4":
                gene="HTT"
                dis="Huntingtin"
                sym="""Difficulty concentrating,Memory lapses,Involuntary jerking or fidgety movements of the limbs and body,Increasingly slow or rigid movements"""
                if sol>36 and sol<180:
                    risk="100% "
                    risk_fut="50%"
                elif sol<35 and sol>6:
                    risk="75%"
                    risk_fut="35%"
                else:
                    risk="No risk detected"
                    risk_fut="No potential risk detected"
                
                report1.append([ch,gene,dis,risk, risk_fut,sym]) 
                report.append([ch,gene,start,end,dis,sol,risk, risk_fut])

            elif ch=="6":
                gene="ATXN1"
                dis="Spino cerebellar Ataxia type 1"
                sym="""Numbness, tingling, or pain in the arms and legs(sensory neuropathy),Uncontrolled muscle tensing(dystonia),Muscle wasting (atrophy),Muscle twitches (fasciculations)"""
                if sol>39 and sol<83:
                    risk="100% "
                    risk_fut="50%"
                elif sol<35 and sol>6:
                    risk="75%"
                    risk_fut="35%"
                else:
                    risk="No risk detected"
                    risk_fut="No potential risk detected"
                    
                report1.append([ch,gene,dis,risk, risk_fut,sym]) 
                report.append([ch,gene,start,end,dis,sol,risk, risk_fut])



            elif ch=="12":
                gene="ATXN2"
                dis="Spino cerebellar Ataxia type 2"
                sym="""Loss of sensation and weakness in the limbs (peripheral neuropathy),Muscle wasting (atrophy),Uncontrolled muscle tensing (dystonia),Involuntary jerking movements (chorea)"""
                if sol>39 and sol<83:
                    risk="100% "
                    risk_fut="50%"
                elif sol<35 and sol>6:
                    risk="75%"
                    risk_fut="35%"
                else:
                    risk="No risk detected"
                    risk_fut="No potential risk detected"
                    
                report1.append([ch,gene,dis,risk, risk_fut,sym]) 
                report.append([ch,gene,start,end,dis,sol,risk, risk_fut])



            elif ch=="14":
                gene="ATXN3"
                dis="Spino cerebellar Ataxia type 3"
                sym="""Speech difficulties,Uncontrolled muscle tensing (dystonia),Muscle stiffness (spasticity),Rigidity, tremors,Bulging eyes, and double vision"""
                if sol>39 and sol<83:
                    risk="100% "
                    risk_fut="50%"
                elif sol<41 and sol>12:
                    risk="75%"
                    risk_fut="35%"
                else:
                    risk="No risk detected"
                    risk_fut="No potential risk detected"
                    
                report1.append([ch,gene,dis,risk, risk_fut,sym]) 
                report.append([ch,gene,start,end,dis,sol,risk, risk_fut])



            elif ch=="19":
                gene="CACNA1A"
                dis="Episodic Ataxia type 2"
                sym="""Recurrent episodes of poor coordination and balance (ataxia),Experience dizziness (vertigo) and ringing in the ears (tinnitus),Nausea and vomiting, migraine headaches,Blurred or double vision, slurred speech"""
                if sol>39 and sol<83:
                    risk="100% "
                    risk_fut="50%"
                elif sol<35 and sol>6:
                    risk="75%"
                    risk_fut="35%"
                else:
                    risk="No risk detected"
                    risk_fut="No potential risk detected"

                report1.append([ch,gene,dis,risk, risk_fut,sym]) 
                report.append([ch,gene,start,end,dis,sol,risk, risk_fut])


            #elif ch=="1" or ch=="2" or ch=="3" or ch=="2" or ch=="1" or ch=="2" or ch=="1" or ch=="13" or ch=="15" or ch=="16" or ch=="17" or ch=="18" or ch=="20" or ch=="21" or ch=="22" or ch=="X" or ch=="Y"
            else:
                gene="--"
                risk="Not applicable"
                risk_fut="Not applicable"
                sol=0
                dis="--"
                sym="----"
                report1.append([ch,gene,dis,risk, risk_fut,sym]) 
                report.append([ch,gene,start,end,dis,sol,risk, risk_fut])



    user = request.POST.get('u')

    os123.remove(file_url)


    uid=request.session['uid']
    name = request.session['name']



    if(user == 'general'):
        request.session['ReportRes'] = report1
        print(uid)
        print(name)
        di = [d[2] for d in report1]
        r = [d[3] for d in report1]
        print(di)
        print(r)

        for i in range(len(di)):
            if(di[i] == "--"):
                continue
            data={'Risk': r[i]}
            db.collection("User Information").document(uid).collection("Patient Details").document(name).collection("Results").document(di[i]).set(data)
        return render(request, "ResultPage.html", {'report1': report1})


    elif(user=='expert'):
        request.session['ReportExpert'] = report
        print(uid)
        print(name)
        di = [d[4] for d in report]
        r = [d[6] for d in report]
        print(di)
        print(r)

        for i in range(len(di)):
            if(di[i] == "--"):
                continue
            data={'Risk': r[i]}
            db.collection("User Information").document(uid).collection("Patient Details").document(name).collection("Results").document(di[i]).set(data)

        return render(request, "Expert.html", {'report': report})





def downloadExpert(request):
    print("Came here")
    report = request.session['ReportExpert']
    gene_name = []
    st_index = []
    end_index = []
    disease = []
    un_repititons = []
    risk = []
    risk_future = []
    for i in range(len(report)):
        print(report[i])
        gene_name.append(report[i][0])
        st_index.append(report[i][1])
        end_index.append(report[i][2])
        disease.append(report[i][3])
        un_repititons.append(report[i][4])
        risk.append(report[i][5])
        risk_future.append(report[i][6])

    df = pd.DataFrame({"Gene name": gene_name, "Start index of base pair": st_index, "End index of base pair": end_index, "Disease": disease, "Uninterrupted CAG reptitions": un_repititons,
        "Risk for patient": risk, "Risk for Future Generation": risk_future})

    df.to_csv("report.csv")

    filename = "report.csv"
    fl_path = filename
    ## return FileResponse("", as_attachment=True)
    fl = open(fl_path, 'r')
    
    response = HttpResponse(fl, content_type="text/csv")
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    os123.remove("report.csv")
    return response


def downloadRes(request):
    print("Came here")
    report1 = request.session['ReportRes']
    chromosome=[]
    gene_name = []
    disease = []
    risk = []
    risk_future = []
    sym=[]
    for i in range(len(report1)):
        print(report1[i])
        chromosome.append(report1[i][0])
        gene_name.append(report1[i][1])
        disease.append(report1[i][2])
        risk.append(report1[i][3])
        risk_future.append(report1[i][4])
        sym.append(report1[i][5])

    df = pd.DataFrame({"Chromosome":chromosome,"Gene name": gene_name,"Disease": disease,"Risk for patient": risk, "Risk for Future Generation": risk_future,"Symptoms expected":sym})

    df.to_csv("report1.csv")

    filename = "report1.csv"
    fl_path = filename
    ## return FileResponse("", as_attachment=True)
    fl = open(fl_path, 'r')
    
    response = HttpResponse(fl, content_type="text/csv")
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    os123.remove("report1.csv")
    return response


