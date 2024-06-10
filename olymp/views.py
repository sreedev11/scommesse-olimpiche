from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth

import pandas as pd
import joblib

import warnings
warnings.filterwarnings("ignore")


def home(request):
   return render(request,'tem/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'Invalid credentials')
            return redirect('login')
        auth.login(request, user)
        if Registration.objects.filter(user = user, password = password).exists():
            logs = Registration.objects.filter(user = user, password = password)
            for value in logs:
                user_id = value.id
                usertype  = value.user_role
            
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    return redirect('admin_home')

                elif usertype == 'user':
                    request.session['logg'] = user_id
                    return redirect('user_home')

                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return redirect('login')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return redirect('login')
    else:
       return render(request, 'login.html')


def adminHome(request):
    gtg = Registration.objects.get(id = request.session['logg'])
    try:
        kmk = Bankk.objects.get(bank_reg = gtg)
    except:
        kmk = 0
    return render(request,'admin_home.html',{'gtg':gtg,'kmk':kmk})


def userHome(request):
    gtg = Registration.objects.get(id=request.session['logg'])
    try:
        kmk = Bankk.objects.get(bank_reg=gtg)
    except:
        kmk = 0
    return render(request,'user_home.html',{'gtg':gtg,'kmk':kmk})


def logout(request):
    auth.logout(request)
    return redirect('home')
    

def adminRegister(request):
   if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.user_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('home')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
       
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('admin_reg')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('admin_reg')

        user = User.objects.create_user(username = user_name, email = email, password = psw, first_name = first_name, last_name = last_name)
        user.save()

        t = Registration()
        t.password= psw
        t.user_role = 'admin'
        t.bet_amt = 100
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('home')
   else:
       return render(request,'admin_reg.html')


def userRegister(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
       
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('login')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('login')

        user = User.objects.create_user(username = user_name, email = email, password = psw, first_name = first_name, last_name = last_name)
        user.save()

        t = Registration()
        t.password= psw
        t.user_role = 'user'
        t.bet_amt = 20
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as user')
        return redirect('home')
    else:
        return render(request,'user_reg.html')

def olym_med_prd_usr(request):
    ggg = Olympic_prediction.objects.filter(olym_reg = request.session['logg'])
    return render(request, 'olym_med_prd_usr.html', {'ggg': ggg})


def prdct_olym(request):
    jjk = Registration.objects.get(id=request.session['logg'])
    excel_file_path = 'C:\\main_project\\keystoteam.csv'
    excel_file_path1 = 'C:\\main_project\\keystoevent.csv'

    # Read Excel file using pandas
    df = pd.read_csv(excel_file_path)
    df1 = pd.read_csv(excel_file_path1)

    # Convert DataFrame to a list of dictionaries for easy rendering in HTML
    data = df.to_dict('records')
    data1 = df1.to_dict('records')


    team_m = []
    team_enc = []
    for t in data:
        for k, v in t.items():
            if k == 'Team':
                team_m.append(v)
            if k == 'Team_encode':
                v = int(v)
                team_enc.append(v)

    event_t = []
    event_enc = []
    for t in data1:
        for k1, v1 in t.items():
            if k1 == 'Event':
                event_t.append(v1)
            if k1 == 'Event_encode':
                v = int(v1)
                event_enc.append(v)



    team_m1 = []
    team_enc1 = []

    for i, j in zip(team_m, team_enc):
        if i not in team_m1:
            team_m1.append(i)
            team_enc1.append(j)

    tma = zip(team_m1, team_enc1)



    event_t1 = []
    event_enc1 = []

    for i, j in zip(event_t, event_enc):
        if i not in event_t1:
            event_t1.append(i)
            event_enc1.append(j)
    tma1 = zip(event_t1, event_enc1)


    if request.method == 'POST':
        gender = int(request.POST.get('gender'))
        age = float(request.POST.get('age'))
        hgt = float(request.POST.get('hgt'))
        wgt = float(request.POST.get('wgt'))
        try:
            you_team = int(request.POST.get('you_team'))
        except:
            messages.success(request, 'Please select team from suggestion')
            return redirect('prdct_olym')

        try:
            you_event = int(request.POST.get('you_event'))
        except:
            messages.success(request, 'Please select event from suggestion')
            return redirect('prdct_olym')
        

        loaded_model = joblib.load("C:\\Users\\sreed\\Desktop\\olympic3\\olymp\\random_forest_model.joblib")
        input_data = [[gender, age, hgt, wgt, you_team, you_event]]
        # If it's a scikit-learn model
        result = loaded_model.predict(input_data)
        prd = 0
        rslt = None
        for e in result:
            prd = int(e)
        if prd == 0:
            rslt = 'Bronze'
        elif prd == 1:
            rslt = 'Do not win'
        elif prd == 2:
            rslt = 'Gold'
        else:
            rslt = 'Silver'

        ccb = Olympic_prediction()
        if gender:
            ccb.gender = 'Male'
        else:
            ccb.gender = 'Female'
        ccb.age = int(age)
        ccb.height = hgt
        if you_team in team_enc:
            tmt = team_enc.index(you_team)
            ccb.team = team_m[tmt]
        else:
            ccb.team = you_team


        if you_event in event_enc:
            tmt = event_enc.index(you_event)
            ccb.event = event_t[tmt]
        else:
            ccb.event = you_event

        ccb.medal_status = rslt
        ccb.olym_reg = jjk
        ccb.save()

        messages.success(request, 'Prediction done successfully')
        return redirect('olym_med_prd_usr')

    return render(request,'prdct_olym.html',{'tma':tma,'tma1':tma1})


def delete_predict_user(request, id):
    Olympic_prediction.objects.get(id = id).delete()
    messages.success(request, 'Prediction deleted successfully')
    return redirect('olym_med_prd_usr')


def olym_med_prd_adm(request):
    ggg = Olympic_prediction.objects.all()
    return render(request, 'olym_med_prd_adm.html', {'ggg': ggg})


def user_message(request):
    nme = request.POST.get('nme')
    emm = request.POST.get('emm')
    pho = request.POST.get('pho')
    msg = request.POST.get('msg')
    dc = Contact()
    dc.name = nme
    dc.email = emm
    dc.phone = pho
    dc.message = msg
    dc.save()
    messages.success(request, 'Message sent successfully')
    return redirect('home')


def user_msg_adm(request):
    bn = Contact.objects.all()
    return render(request,'user_msg_adm.html',{'bn':bn})


def delete_message(request, id):
    Contact.objects.get(id = id).delete()
    messages.success(request, 'Message deleted successfully')
    return redirect('user_msg_adm')





def play_for_bet_adm(request):
    ggg = Playss.objects.all()
    return render(request, 'play_for_bet_adm.html', {'ggg': ggg})



def add_fail(request, id):
    sas = Playss.objects.get(id=id)
    if sas.final_result:
        messages.success(request, 'Result already declared')
        return redirect('play_for_bet_adm')
    sas.final_result = sas.country
    gtg = Betting.objects.filter(bet_playy = sas, pred_coun = sas.country)

    gmf0 = Betting.objects.filter(bet_playy=sas, pred_coun=sas.country).count()
    gmf1 = Betting.objects.filter(bet_playy=sas, pred_coun=sas.country1).count()
    print(gmf1)
    gmf2 = 5 * gmf0
    print(gmf2)
    gmf33 = None
    try:
        gmf3 = gmf2 / gmf1
    except:
        gmf3 = gmf2
        gmf33 = gmf3
    print(gmf3)
    gmf4 = (2 / 100) * gmf3
    print(gmf4)
    gmf4 = round(gmf4,2)
    print(gmf4)
    gmf3 = gmf3 - gmf4
    print(gmf3)
    gmf3 = round(gmf3,2)

    for t in gtg:
        uet = int(t.bet_reg.id)
        uet = Registration.objects.get(id = uet)

        if gmf33 == gmf2:
            zzm = float(t.bet_reg.bet_amt)
            zzm = round(zzm, 2)
        else:
            zzm = float(t.bet_reg.bet_amt) + 5
            zzm = round(zzm,2)


        idm = int(t.bet_reg.id)

        yty = Registration.objects.get(id=idm)
        yty.bet_amt = zzm
        yty.save()

        if gmf33 != gmf2:
            yty1 = Registration.objects.get(user_role = 'admin')
            zzp = float(yty1.bet_amt) + gmf4
            yty1.bet_amt = round(zzp,2)
            yty1.save()

            yty2 = Betting_admin_amount()
            yty2.amount = gmf4
            yty2.bet_playy_admin = sas
            yty2.bet_reg_admin = uet
            yty2.save()

            yty2 = Betting_user_amount()
            yty2.amount = '+5'
            yty2.bet_playy_user = sas
            yty2.bet_reg_user = yty
            yty2.save()

        else:
            yty1 = Registration.objects.get(user_role='admin')
            zzp = float(yty1.bet_amt)
            yty1.bet_amt = round(zzp, 2)
            yty1.save()

            yty2 = Betting_admin_amount()
            yty2.amount = 0
            yty2.bet_playy_admin = sas
            yty2.bet_reg_admin = uet
            yty2.save()

            yty2 = Betting_user_amount()
            yty2.amount = 0
            yty2.bet_playy_user = sas
            yty2.bet_reg_user = yty
            yty2.save()


    gtg = Betting.objects.filter(bet_playy=sas, pred_coun=sas.country1)
    for t in gtg:
        if gmf3 <5:
            zzm = float(t.bet_reg.bet_amt) - gmf3
            zzm = round(zzm,2)
    
            idm = int(t.bet_reg.id)
            yty = Registration.objects.get(id=idm)
            yty.bet_amt = zzm
            yty.save()
    
            yty2 = Betting_user_amount()
            yty2.amount = '-'+str(gmf3)
            yty2.bet_playy_user = sas
            yty2.bet_reg_user = yty
            yty2.save()
        else:
            zzm = float(t.bet_reg.bet_amt) - 5
            zzm = round(zzm, 2)
            idm = int(t.bet_reg.id)
            yty = Registration.objects.get(id=idm)
            yty.bet_amt = zzm
            yty.save()

            yty2 = Betting_user_amount()
            yty2.amount = '-5'
            yty2.bet_playy_user = sas
            yty2.bet_reg_user = yty
            yty2.save()

    sas.save()
    return redirect('play_for_bet_adm')






def add_pass(request, id):
    sas = Playss.objects.get(id=id)
    if sas.final_result:
        messages.success(request, 'Result already declared')
        return redirect('play_for_bet_adm')
    sas.final_result = sas.country1

    gtg = Betting.objects.filter(bet_playy = sas, pred_coun = sas.country1)
    gmf0 = Betting.objects.filter(bet_playy = sas, pred_coun = sas.country1).count()
    gmf1 = Betting.objects.filter(bet_playy=sas, pred_coun=sas.country).count()
    gmf2 = 5 * gmf0
    gmf33 = None
    try:
        gmf3 = gmf2 / gmf1
    except:
        gmf3 = gmf2
        gmf33 = gmf3
    gmf4 = (2/100) * gmf3
    gmf4 = round(gmf4,2)
    gmf3 = gmf3 - gmf4
    gmf3 = round(gmf3, 2)
    for t in gtg:
        uet = int(t.bet_reg.id)
        uet = Registration.objects.get(id = uet)

        if gmf33 != gmf2:
            zzm = float(t.bet_reg.bet_amt) + 5
            zzm = round(zzm,2)
        else:
            zzm = float(t.bet_reg.bet_amt)
            zzm = round(zzm, 2)


        idm = int(t.bet_reg.id)
        yty = Registration.objects.get(id=idm)
        yty.bet_amt = zzm
        yty.save()

        if gmf33 != gmf2:
            yty1 = Registration.objects.get(user_role='admin')
            kpz = float(yty1.bet_amt) + gmf4
            yty1.bet_amt = round(kpz,2)
            yty1.save()
            yty2 = Betting_admin_amount()
            yty2.amount = gmf4
            yty2.bet_playy_admin = sas
            yty2.bet_reg_admin = uet
            yty2.save()

            yty2 = Betting_user_amount()
            yty2.amount = '+5'
            yty2.bet_playy_user = sas
            yty2.bet_reg_user = yty
            yty2.save()

        else:

            yty1 = Registration.objects.get(user_role='admin')
            zzp = float(yty1.bet_amt)
            yty1.bet_amt = round(zzp, 2)
            yty1.save()

            yty2 = Betting_admin_amount()
            yty2.amount = 0
            yty2.bet_playy_admin = sas
            yty2.bet_reg_admin = uet
            yty2.save()

            yty2 = Betting_user_amount()
            yty2.amount = 0
            yty2.bet_playy_user = sas
            yty2.bet_reg_user = yty
            yty2.save()



    gtg = Betting.objects.filter(bet_playy=sas, pred_coun=sas.country)
    for t in gtg:
        if gmf3 < 5:
            zzm = float(t.bet_reg.bet_amt) - gmf3
            zzm = round(zzm,2)
    
            idm = int(t.bet_reg.id)
            yty = Registration.objects.get(id = idm)
            yty.bet_amt = zzm
            yty.save()
    
            yty2 = Betting_user_amount()
            yty2.amount = '-'+str(gmf3)
            yty2.bet_playy_user = sas
            yty2.bet_reg_user = yty
            yty2.save()
            
        else:

            zzm = float(t.bet_reg.bet_amt) - 5
            zzm = round(zzm, 2)

            idm = int(t.bet_reg.id)
            yty = Registration.objects.get(id=idm)
            yty.bet_amt = zzm
            yty.save()

            yty2 = Betting_user_amount()
            yty2.amount = '-5'
            yty2.bet_playy_user = sas
            yty2.bet_reg_user = yty
            yty2.save()

    sas.save()
    return redirect('play_for_bet_adm')



      



def delete_play_adm(request, id):
    Playss.objects.get(id = id).delete()
    messages.success(request, 'Play deleted successfully')
    return redirect('play_for_bet_adm')


def add_play_adm(request):
    if request.method == 'POST':
        spp = request.POST.get('spp')
        coun = request.POST.get('coun')
        coun1 = request.POST.get('coun1')

        ccb = Playss()
        ccb.sport = spp
        ccb.country = coun
        ccb.country1 = coun1
        ccb.save()

        messages.success(request, 'Play added successfully')
        return redirect('play_for_bet_adm')

    return render(request,'add_play_adm.html')



def bettings_adm(request):
    fdf = Betting.objects.all()
    return render(request, 'bettings_adm.html', {'fdf': fdf})




def del_bet_adm(request, id):
    Betting.objects.get(id = id).delete()
    messages.success(request, 'Betting deleted successfully')
    return redirect('bettings_adm')



def plays_for_bet_usr(request):
    hello = []
    gpg = Betting.objects.filter(bet_reg = request.session['logg'])
    for t in gpg:
        d = int(t.bet_playy.id)
        hello.append(d)
    pp = Playss.objects.exclude(id__in = hello)
    rt = Registration.objects.get(id = request.session['logg'])
    return render(request,'plays_for_bet_usr.html',{'pp':pp,'rt':rt})



def coun_pass_usr(request, id):
    hyh = Registration.objects.get(id = request.session['logg'])
    sas = Playss.objects.get(id=id)
    if sas.final_result:
        messages.success(request, "Final result declared. You cannot bet this play")
        return redirect('plays_for_bet_usr')
    jkj = Betting()
    jkj.pred_coun = sas.country
    jkj.bet_playy = sas
    jkj.bet_reg = hyh
    jkj.save()
    return redirect('plays_for_bet_usr')



def coun_pass_usr1(request, id):
    hyh = Registration.objects.get(id = request.session['logg'])
    sas = Playss.objects.get(id=id)
    if sas.final_result:
        messages.success(request, "Final result declared. You cannot bet this play")
        return redirect('plays_for_bet_usr')
    jkj = Betting()
    jkj.pred_coun = sas.country1
    jkj.bet_playy = sas
    jkj.bet_reg = hyh
    jkj.save()
    return redirect('plays_for_bet_usr')


def my_bettings_usr(request):
    fdf = Betting.objects.filter(bet_reg = request.session['logg'])
    return render(request, 'my_bettings_usr.html',{'fdf':fdf})


def purchase_mon_usr1(request):
    request.session['purch_amt'] = amt = request.POST.get('amt')
    return render(request, 'purchase_mon_usr1.html',{'amt':amt})



def purchase_mon_usr(request):
    if request.method == 'POST':
        amt = request.session['purch_amt']
        amt = float(amt)
        nbn = Registration.objects.get(id = request.session['logg'])
        if nbn.bet_amt:
            vbg = float(nbn.bet_amt)
            vbg += amt
            nbn.bet_amt = vbg
            nbn.save()
        else:
            nbn.bet_amt = amt
            nbn.save()
        msgb = 'Rs '+str(amt)+' credited'
        messages.success(request,msgb)
        return render(request,'purchase_mon_usr2.html')
    return render(request, 'purchase_mon_usr.html')



def trans_adm(request):
    gtg = Betting_admin_amount.objects.all()
    return render(request, 'trans_adm.html',{'gtg':gtg})




def delete_trans_adm(request, id):
    Betting_admin_amount.objects.get(id=id).delete()
    messages.success(request, 'Transaction deleted successfully')
    return redirect('trans_adm')




def bet_hist_user(request):
    gtg = Betting_user_amount.objects.filter(bet_reg_user = request.session['logg'])
    return render(request, 'bet_hist_user.html', {'gtg': gtg})


def delete_trans_usr(request, id):
    Betting_user_amount.objects.get(id=id).delete()
    messages.success(request, 'History deleted successfully')
    return redirect('bet_hist_user')



def m_to_b_adm(request):
    kmk = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        amt = request.POST.get('amt')
        jyu = float(kmk.bet_amt) - float(amt)
        if float(jyu) < -50:
            messages.success(request, 'Insufficient bet amount balance. Please purchase money.')
            return redirect('admin_home')

        rer = float(kmk.bet_amt) - float(amt)
        rer = round(rer,2)
        kmk.bet_amt = rer
        kmk.save()

        if Bankk.objects.filter(bank_reg = kmk).exists():
            njn = Bankk.objects.get(bank_reg = kmk)
            rer = float(njn.amount) + float(amt)
            rer = round(rer, 2)
            njn.amount = rer
            njn.save()
        else:
            njn = Bankk()
            njn.amount = amt
            njn.bank_reg = kmk
            njn.save()


        messages.success(request, 'Money tranferred from bet balance to bank.')
        return redirect('admin_home')
    return render(request,'m_to_b_adm.html')


                

def m_from_b_adm(request):
    kmk = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        amt = request.POST.get('amt')
        if Bankk.objects.filter(bank_reg = kmk).exists():
            njn = Bankk.objects.get(bank_reg = kmk)
            if ( float(njn.amount) <= 0 ) or ( float(njn.amount) < float(amt) ):
                messages.success(request,'Insufficient balance')
                return redirect('admin_home')

            rer = float(kmk.bet_amt) + float(amt)
            rer = round(rer, 2)
            kmk.bet_amt = rer
            kmk.save()

            amtt = float(njn.amount) - float(amt)
            amtt = round(amtt,2)
            njn.amount = amtt
            njn.bank_reg = kmk
            njn.save()


            messages.success(request, 'Money transferred from bank to bet balance')
            return redirect('admin_home')
        else:
            messages.success(request, 'Your bank is not connected. Please credit a minimum balance.')
            return redirect('admin_home')
    return render(request,'m_from_b_adm.html')



def m_to_b_usr(request):
    kmk = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        amt = request.POST.get('amt')
        jyu = float(kmk.bet_amt) - float(amt)
        if float(jyu) < -50:
            messages.success(request, 'Insufficient bet amount balance. Please purchase money.')
            return redirect('user_home')

        rer = float(kmk.bet_amt) - float(amt)
        rer = round(rer, 2)
        kmk.bet_amt = rer
        kmk.save()

        if Bankk.objects.filter(bank_reg=kmk).exists():
            njn = Bankk.objects.get(bank_reg=kmk)
            rer = float(njn.amount) + float(amt)
            rer = round(rer, 2)
            njn.amount = rer
            njn.save()
        else:
            njn = Bankk()
            njn.amount = amt
            njn.bank_reg = kmk
            njn.save()

        messages.success(request, 'Money tranferred from bet balance to bank.')
        return redirect('user_home')
    return render(request, 'm_to_b_usr.html')




def m_from_b_usr(request):
    kmk = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        amt = request.POST.get('amt')
        if Bankk.objects.filter(bank_reg=kmk).exists():
            njn = Bankk.objects.get(bank_reg=kmk)
            if (float(njn.amount) <= 0) or (float(njn.amount) < float(amt)):
                messages.success(request, 'Insufficient balance')
                return redirect('user_home')

            rer = float(kmk.bet_amt) + float(amt)
            rer = round(rer, 2)
            kmk.bet_amt = rer
            kmk.save()

            amtt = float(njn.amount) - float(amt)
            amtt = round(amtt, 2)
            njn.amount = amtt
            njn.bank_reg = kmk
            njn.save()

            messages.success(request, 'Money transferred from bank to bet balance')
            return redirect('user_home')
        else:
            messages.success(request, 'Your bank is not connected. Please credit a minimum balance.')
            return redirect('user_home')
    return render(request, 'm_from_b_usr.html')



def purchase_mon_adm(request):
    if request.method == 'POST':
        amt = request.POST.get('amt')
        amt = float(amt)
        nbn = Registration.objects.get(id = request.session['logg'])
        vbg = float(nbn.bet_amt)
        vbg += amt
        nbn.bet_amt = vbg
        nbn.save()
        msgb = 'Rs '+str(amt)+' credited'
        messages.success(request,msgb)
        return redirect('admin_home')
    return render(request, 'purchase_mon_adm.html')
