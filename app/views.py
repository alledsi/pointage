from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.http import HttpResponse, JsonResponse
import xlwt
from .form import LoginForm
from .models import pointage
from time import strftime, gmtime
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

sites = {
    0 : "SIEGE DAKAR",
    1 : "SIEGE DAKAR",
    2 : "SIEGE DAKAR",
    3 : "SIEGE DAKAR",

    102 : "Colobane(cast/O Niayes)",
    5   : "Grand Yoff",
    14  : "HLM",
    16  : "Scat Urbam",
    110 : "Dieuppeul",

    6 : "AGENCE Parcelles",
    18 : "Golf",
    11 : "Parcelles U20",

    7  : "AGENCE VDN",
    9  : "Yoff",
    15 : "Maristes",
    8  : "Dalifort",

    181 : "AGENCE Pikine",
    4   : "Thiaroye",
    10  : "Guédiawaye",
    13  : "Yeumbeul",
    163 : "Chavanel",
    164 : "Guédiawaye 2",
    165 : "Guédiawaye 3",


    140 : "Sandaga",
    17  :  "Ouakam",
    101 : "Médina/dkr centre",

    162 : "AGENCE Rufisque",
    103 : "Rufisque",
    12  : "Poste Thiaroye",
    19  : "Keur Massar",
    160 : "Bayakh",
    161 : "Diamniadio",

    23 :  "AGENCE KAOALACK",
    22 :  "Sokone / Passy",
    27 :  "Kaolack Nord",
    20 :  "Ndorong",
    24 :  "Fatick",
    28 :  "Nioro",

    170 : "AGENCE Kaffrine",
    25  : "Kounghel",
    26  : "Guinguinéo",
    21  : "Birkilane",
    29  : "Koupentoum",

    30  : "AGENCE Ziguinchor",
    31  : "Bignona",
    32  : "Boucotte",
    33  : "Cap Skirring",

    40  : "AGENCE Kolda",
    41  : "Vélingara",
    42  : "Sédhiou",
    190 : "Diaobé",

    57  : "AGENCE Saint Louis",
    52  : "Richard Toll",
    53  : "Saint Louis II (Pikine)",
    56  : "Santhiaba",
    50  : "Ngalèle",


    51  : "AGENCE Louga",
    54  : "Kébémer",
    55  : "Dahra",
    58  : "Louga Artillerie",
    59  : "Niomré",

    60  : "AGENCE Diourbel",
    62  : "Bambey",
    63  : "Marché Central",

    70  : "AGENCE Ourossogui ",
    71  : "Ndioum ",
    72  : "Galoya" ,

    80  : "AGENCE Tamba",
    81  : "Kédougou",
    82  : "Bakel",
    83  : "Tamba2 (pont)",
    84  : "Kidira",

    120 : "AGENCE Mbour ",
    121 : "MbourII ",
    122 : "Nguékhokh ",
    123 : "Joal" ,
    124 : "11-nov ",

    130 : "AGENCE TOUBA",
    131 : "Darou Khoudoss",
    134 : "Mabcké",
    132 : "Touba Ocass",
    133 : "Darou mousty",
    135 : "Touba 28",

    90  : "AGENCE Thies",
    92  : "Khombole",
    93  : "Marché Central",
    94  : "Hersent",
    97  : "Route de Mbour",

    98  : "AGENCE TIVAOUANE",
    91  : "Tivaouane",
    95  : "Mboro",
    96  : "Mékhé",

}

@login_required
def accueil(request):
    mois = {1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'}
    current_dateTime = datetime.datetime.now()
    #m = mois[int(current_dateTime.strftime("%m"))].capitalize()
    m = mois[int(strftime('%m', gmtime()))].capitalize()
    y = strftime('%Y', gmtime())
    jour = {0:'Dimanche', 1:'Lundi', 2:'Mardi', 3:'Mercredi', 4:'Jeudi', 5:'Vendredi', 6:'Samedi'}
    #j = jour[int(current_dateTime.strftime("%w"))].capitalize()
    j = jour[int(strftime('%w', gmtime()))].capitalize()
    #y = current_dateTime.strftime("%Y")
    dn = str(j)+" "+strftime('%d', gmtime())+" "+str(m)+" "+str(y)
    hm = strftime("%H:%M", gmtime())
    p = pointage.objects.filter(date__exact=strftime("%d/%m/%Y", gmtime()), matricule__exact=request.user.username)
    pa = pointage.objects.filter(date__endswith=strftime("%Y", gmtime()), matricule__exact=request.user.username)
    pm = pointage.objects.filter(date__endswith=strftime("%m/%Y", gmtime()), matricule__exact=request.user.username)
    hier = current_dateTime - datetime.timedelta(days=1)
    pH = pointage.objects.filter(date__exact=hier.strftime("%d/%m/%Y"), matricule__exact=request.user.username)
    
    def additionner_durees(duree1, duree2):
        # Extraire les heures et les minutes des deux durées
        heures1, minutes1 = duree1
        heures2, minutes2 = duree2
        
        # Additionner les minutes et les heures
        total_minutes = minutes1 + minutes2
        total_heures = heures1 + heures2 + total_minutes // 60
        
        # Calculer les minutes restantes après conversion en heures
        minutes_restantes = total_minutes % 60
        
        return total_heures, minutes_restantes

    hweek = (00, 00)
    nd = 0
    for pi in pa:
        pisplit = pi.date.split("/")
        if datetime.datetime(int(pisplit[2]), int(pisplit[1]), int(pisplit[0])).strftime("%W") == strftime("%W", gmtime()) and pi.depart is not None:
            nd += 1
            d = datetime.datetime.strptime(pi.depart, "%H:%M")
            a = datetime.datetime.strptime(pi.arrivee, "%H:%M")
            hj = d - a
            hj = (int(str(hj).split(":")[0]), int(str(hj).split(":")[1]))
            hweek = additionner_durees(hweek, hj)
    #hweek = datetime.datetime(2024, 1, 1, hweek[0], hweek[1]).strftime("%H:%M")
    hweek = str(hweek[0])+":"+str(hweek[1])+" de présence"
    nd = str(nd)+" jours" if nd>1 else str(nd)+" jour"

    hmois = (00, 00)
    nday = 0
    for pi in pm:
        pisplit = pi.date.split("/")
        if pi.depart is not None:
            nday += 1
            d = datetime.datetime.strptime(pi.depart, "%H:%M")
            a = datetime.datetime.strptime(pi.arrivee, "%H:%M")
            hj = d - a
            hj = (int(str(hj).split(":")[0]), int(str(hj).split(":")[1]))
            hmois = additionner_durees(hmois, hj)
    #hmois = datetime.datetime(2024, 1, 1, hmois[0], hmois[1]).strftime("%H:%M")
    hmois = str(hmois[0])+":"+str(hmois[1])+" de présence"
    nday = str(nday)+" jours" if nday>1 else str(nday)+" jour"
    
    dp = None
    fp = None
    statutP = "Aucune pause"
    dep = None
    statut = "Aucun pointage"
    if len(p[:1])!=0:
        dep = p[0].depart
        arr = p[0].arrivee
        dp = p[0].debutpause
        fp = p[0].finpause
        timeref = datetime.time(8, 0)
        timepoint = datetime.time(int(arr.split(":")[0]), int(arr.split(":")[1]))
        statut = "A l'heure: "+str(arr) if timeref > timepoint else "En retard: "+str(arr)
        if dp is not None and fp is not None:
            statutP = "Pause: "+str(dp)+" à "+str(fp)
        elif dp is not None:
            statutP = "Début pause: "+str(dp)
        if dep is not None:
            statut = "Présent: "+str(arr)+" à "+str(dep)
    
    dpH = None
    fpH = None
    statutPH = "Aucune pause"
    depH = None
    statutH = "Aucun pointage"
    if len(pH[:1])!=0:
        depH = pH[0].depart
        arrH = pH[0].arrivee
        dpH = pH[0].debutpause
        fpH = pH[0].finpause
        timeref = datetime.time(8, 0)
        timepoint = datetime.time(int(arrH.split(":")[0]), int(arrH.split(":")[1]))
        statutH = "A l'heure: "+str(arrH) if timeref > timepoint else "En retard: "+str(arrH)
        if dpH is not None and fpH is not None:
            statutPH = "Pause: "+str(dpH)+" à "+str(fpH)
        elif dpH is not None:
            statutPH = "Début pause: "+str(dp)
        if depH is not None:
            statutH = "Présent: "+str(arrH)+" à "+str(depH)
    return render(request, 'app/accueil.html' ,{'d': dn, 'p': p, 'dep': dep, 'hm': hm, 'statut': statut, 'statutH': statutH, 'statutP': statutP, 'statutPH': statutPH, 'hweek': hweek, 'nd': nd, 'hmois': hmois, 'nday': nday, 'dp': dp, 'fp': fp})

@login_required
def pannee(request):
    mois = {1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'}
    current_dateTime = datetime.datetime.now()
    m = mois[int(current_dateTime.strftime("%m"))].capitalize()
    jour = {0:'Dimanche', 1:'Lundi', 2:'Mardi', 3:'Mercredi', 4:'Jeudi', 5:'Vendredi', 6:'Samedi'}
    j = jour[int(current_dateTime.strftime("%w"))].capitalize()
    y = current_dateTime.strftime("%Y")
    dn = str(j)+" "+strftime('%d', gmtime())+" "+str(m)+" "+str(y)
    hm = strftime("%H:%M", gmtime())
    pa = pointage.objects.filter(date__endswith=strftime("%Y", gmtime()), matricule__exact=request.user.username)

    return render(request, 'app/p_annee.html', {'pa': pa, 'd': dn, 'hm': hm})

@login_required
def pmois(request):
    mois = {1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'}
    current_dateTime = datetime.datetime.now()
    m = mois[int(current_dateTime.strftime("%m"))].capitalize()
    jour = {0:'Dimanche', 1:'Lundi', 2:'Mardi', 3:'Mercredi', 4:'Jeudi', 5:'Vendredi', 6:'Samedi'}
    j = jour[int(current_dateTime.strftime("%w"))].capitalize()
    y = current_dateTime.strftime("%Y")
    dn = str(j)+" "+strftime('%d', gmtime())+" "+str(m)+" "+str(y)
    hm = strftime("%H:%M", gmtime())
    pm = pointage.objects.filter(date__endswith=strftime("%m/%Y", gmtime()), matricule__exact=request.user.username)

    return render(request, 'app/p_mois.html', {'pm': pm, 'd': dn, 'hm': hm})

@login_required
def psemaine(request):
    mois = {1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'}
    current_dateTime = datetime.datetime.now()
    m = mois[int(current_dateTime.strftime("%m"))].capitalize()
    jour = {0:'Dimanche', 1:'Lundi', 2:'Mardi', 3:'Mercredi', 4:'Jeudi', 5:'Vendredi', 6:'Samedi'}
    j = jour[int(current_dateTime.strftime("%w"))].capitalize()
    y = current_dateTime.strftime("%Y")
    dn = str(j)+" "+strftime('%d', gmtime())+" "+str(m)+" "+str(y)
    hm = strftime("%H:%M", gmtime())
    psem = pointage.objects.filter(date__endswith=strftime("%Y", gmtime()), matricule__exact=request.user.username)
    ps = []
    for p in psem:
        pisplit = p.date.split("/")
        #print(datetime.datetime(int(pisplit[2]), int(pisplit[1]), int(pisplit[0])).strftime("%W"))
        if datetime.datetime(int(pisplit[2]), int(pisplit[1]), int(pisplit[0])).strftime("%W") == strftime("%W", gmtime()):
            l = [p.date, p.matricule, p.arrivee, p.debutpause, p.finpause, p.depart]
            ps.append(l)
    return render(request, 'app/p_semaine.html', {'ps': ps, 'd': dn, 'hm': hm})

def json_pointage(request):
    data = list(pointage.objects.all().values('date', 'matricule', 'agent', 'arrivee', 'locarrivee', 'debutpause', 'locdebutpause', 'finpause', 'locfinpause', 'depart', 'locdepart'))
    return JsonResponse(data, safe=False)

@login_required
def export_pannee(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-disposition'] = 'attachment; filename="pointage_annee.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    y = strftime("%Y", gmtime())
    ws = wb.add_sheet(y)
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Date', 'Matricule', 'Arrivée', 'Début pause', 'Fin pause', 'Départ']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = pointage.objects.filter(date__endswith=strftime("%Y", gmtime()), matricule__exact=request.user.username).values_list('date', 'matricule', 'arrivee', 'debutpause', 'finpause', 'depart')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response

@login_required
def export_pmois(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-disposition'] = 'attachment; filename="pointage_mois.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    m = strftime("%B", gmtime())
    ws = wb.add_sheet(m)
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Date', 'Matricule', 'Arrivée', 'Début pause', 'Fin pause', 'Départ']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = pointage.objects.filter(date__endswith=strftime("%m/%Y", gmtime()), matricule__exact=request.user.username).values_list('date', 'matricule', 'arrivee', 'debutpause', 'finpause', 'depart')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response

@login_required
def arrivee(request):
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        print(ip)
        dt = strftime("%d/%m/%Y", gmtime())
        mat = request.user.username
        ag = request.user.get_full_name()
        ar = strftime("%H:%M", gmtime())
        locar = ip
        if int(locar.split('.')[0])==10:
            locar = "VPN"
        else:
            locar = sites[int(locar.split('.')[2])]
        a = pointage(date=dt, matricule=mat, agent=ag, arrivee=ar, locarrivee=locar)
        a.save()
        return  HttpResponseRedirect('/')

@login_required
def depart(request, id):
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        dep = strftime("%H:%M", gmtime())
        locdep = ip
        if int(locdep.split('.')[0])==10:
            locdep = "VPN"
        else:
            locdep = sites[int(locdep.split('.')[2])]
        pointage.objects.filter(pk=id).update(depart=dep, locdepart=locdep)
        return  HttpResponseRedirect('/')

@login_required
def debutpause(request, id):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    dp = strftime("%H:%M", gmtime())
    locdp = ip
    if int(locdp.split('.')[0])==10:
        locdp = "VPN"
    else:
        locdp = sites[int(locdp.split('.')[2])]
    pointage.objects.filter(pk=id).update(debutpause=dp, locdebutpause=locdp)
    return  HttpResponseRedirect('/')

@login_required
def finpause(request, id):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    fp = strftime("%H:%M", gmtime())
    locfp = ip
    if int(locfp.split('.')[0])==10:
        locfp = "VPN"
    else:
        locfp = sites[int(locfp.split('.')[2])]
    pointage.objects.filter(pk=id).update(finpause=fp, locfinpause=locfp)
    return  HttpResponseRedirect('/')
    
def login(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username ou password incorrect')
            msg = "Nom d'utilisateur ou mot de passe incorrect."
    return render(request, 'app/login.html', {'form': LoginForm, 'msg':msg})

def logout(request):
    auth.logout(request)
    messages.info(request, 'Déconnecté !')
    return redirect('/login')