#2_Laes_Navnetjek_2019M.py
from app.models import Klub, Grunddata, Konkurrence, Baner, PostBaner, deltager_strak, Deltager, Medlemmer
#from modelloeb import Klub, Konkurrence, Medlemmer, Deltager
from app import db
import math
import json
import os
import sqlite3
from fuzzywuzzy import fuzz, process
from itertools import chain
#from sqlalchemy.orm import sessionmaker, Session, relationship, backref
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Table, MetaData
from datetime import datetime

#engine = create_engine('sqlite:///C:\\Users\\sba.PCB68\\Desktop\\TestPython\\trainingsloeb.db', echo=True)
#Base = declarative_base()
#Session = sessionmaker(bind=engine)
#session = Session()

#Skov1 = Konkurrence.query.filter_by(id=loebnr).first_or_404()

def hent_medlemmer():
    '''Henter alle medlemmer og danner en liste'''
    #temp = session.query(Medlemmer).all()
    temp = Medlemmer.query.all()
    medlemmer_liste = []
    for c in temp:
        #print (c.navn)
        medlemmer_liste.append(c.navn)

    return medlemmer_liste

def hent_klubber():
    '''Henter alle klubber og danner liste'''
    #temp_klub = session.query(Klub).all()
    temp_klub = Klub.query.all()
    klubber_liste = []
    #Klubber_liste1 = []
    #Klubber_liste1 = d.tom
    for d in temp_klub:
        #print (d.kortnavn)
        klubber_liste.append(d.tom)

    return klubber_liste

def tjek_klub(klub):
    ''' Tjekker at klubben allerede eksisterer. Hvis den ikke eksiterer oprettes den.
    Returnerer klubbens ID '''

    temp_klub = Klub.query.all()
    ok = 0
    for w in temp_klub:
        dbklub = w.tom
        if klub.lower() in dbklub.lower():
            klub = w.langtnavn
            ok = 1
            #print (w)
    
    if ok == 1:
        temp_klub = Klub.query.filter(Klub.langtnavn == klub).first()
        KlubID = temp_klub.id
        return KlubID
    elif ok == 0:
        print (klub + " Findes ikke - stav klubnavnet rigtigt:" )
        x = input()
        klub = x
        c2 = Klub(langtnavn=klub, kortnavn="", tom="")
        db.session.add(c2)
        db.session.commit()
        KlubID = c2.id
        return KlubID
        

def opdater_rigtig_navn(medlem, medlemmer_liste, emitbrik1, KlubID):
    ''' Finder navne der allerede eksiterer. Sammenligner, hvis der er navne der er fejlstavede bliver de rettet via input '''

    #temp_navn = session.query(Medlemmer).filter(Medlemmer.navn == medlem).first()   
    temp_navn = Medlemmer.query.filter(Medlemmer.navn == medlem).first()
    resultat = ""
    #print (temp_navn.navn)
    if temp_navn == None:
        highest = process.extract(str(medlem),medlemmer_liste, scorer = fuzz.token_sort_ratio, limit = 1)
        #stig = highest[0]
        #stig1 = stig[1]
        #print (highest)
        if highest[0][1] <= 80:
            resultat = "opret"
        elif highest[0][1] == 100:
             resultat = "allerede_oprettet"
        else:
            #temp_kontrolleret = session.query(Medlemmer).filter(Medlemmer.navn == str(highest[0])).all()
            temp_kontrolleret = Medlemmer.query.filter(Medlemmer.navn == str(highest[0][0])).all()
            for kontrolleret in temp_kontrolleret:
                kontrol = kontrolleret.navn_ok
            if kontrol != 1:
                print ("Databasen: " + str(highest[0][0]) + " - Dagens deltager: " + medlem)
                print("Er det den samme person (J/N)?:")
                x = input()
                x = x.lower()
                if x == "j":
                    y = ""
                    print ("Er databasenavnet korrekt? " + str(highest[0][0]) + " tast 1 " + " - Er Dagens deltagernavn korrekt? " + medlem + " tast 2" + " - Matcher ingen? Tast 3")
                    z = str(input())
                    if z == "1":
                        y = str(highest[0][0])
                    elif z == "2":
                        y = medlem
                    elif z == "3":
                        print ("Stav navnet rigtigt:")
                        y = input()
            
                    temp1 = db.session.query(Medlemmer).filter(Medlemmer.navn == str(highest[0][0])).first()
                    temp1.navn = str(y)
                    temp1.navn_ok = 1
                    temp1.emitbrik = emitbrik1
                    db.session.add(temp1)
                    #session.commit()
                    medlem = y
                    resultat = "indlaes"
                elif x == "n":
                    resultat = "opret"
            else:
                medlem = str(highest[0][0])
    else:
        medlem = medlem

    if resultat == "opret":
        opret_medlem(medlem, emitbrik1, KlubID)
        return medlem
    elif resultat == "allerede_oprettet":
        medlem = str(highest[0][0])
        return medlem
    else:
        return medlem

def opret_medlem(medlem, emitbrik1, KlubID):
    ''' Hvis medlemmet ikke eksiterer opretter funktionen medlemme´,
    og kalder funktionen der indlæser resultatet '''
    
    c1 = Medlemmer(navn=medlem, navn_ok=0, emitbrik=emitbrik1, samlet_point=0, klub_id=KlubID)
    db.session.add(c1)
    db.session.commit()

def NavneTjek(loebnr, mappe, path):

    medlemmer_liste = hent_medlemmer()
    #klub_liste = hent_klubber()

    #temp1 = session.query(Medlemmer).filter(Medlemmer.navn == 'Stig Barrett').all()

    '''Variable der skal sættes inden hvert løb'''
    #path = 'C:\\Users\\sba.PCB68\\Desktop\\TestPython\\'
    #path = 'C:\\Users\\sba.PCB68\\OneDrive\\Orientering\\O-trainingsloeb_2019\\'
    #skov = '01_FeldborgNord'
    #skov = skov
    #fil_resultat = 'Resultat.dat'
    #fil_baner = 'PostBaner1.json'
    fil_bearbejdet = 'Bearbejdet1.json'
    fil_endelig = 'Endelig1.json'
    #konkurrenceID1 = 1
    #konkurrenceID1 = loebnr
    #global medlem

    fil = (path + mappe + '\\' + fil_bearbejdet)
    Test2 = dict()
    placbane = 0
    placnr = 0
    Point = 100
    with open(fil, 'r', encoding='utf8') as f:
        final = json.load(f)

        for i in range(len(final)):
            data1 = final[i]
            #print (data1)
            bnr = data1['Bane']
            if (data1['Status']) == "OK":
                if int(bnr[-1]) == placbane:
                    placnr = placnr + 1
                    #plac = placnr
                    #print ("ha")
                    Nedrundet = math.floor((data1['TidSek']/60))
                    Point = 100 - (Nedrundet - NedrundetOld)
                else:
                    placnr = 1
                    #plac = placnr
                    placbane = placbane + 1
                    Nedrundet = math.floor((data1['TidSek']/60))
                    Point = 100 - (Nedrundet - Nedrundet)
                    NedrundetOld = Nedrundet
            else:
                placnr = 0
                Point = 1
            klub = (data1['Klub'])
            medlem = (data1['Navn'])
            emitbrik1 = (data1['Emit'])
            #bane1 = (data1['Bane'])
            #status = (data1['Status'])
            #plac = (data1['Placering'])
            #point = (data1['Point'])
            #tid = (data1['Tid'])
            #strak = str(data1['StrakTider'])
            #klublang = ""
            KlubID = tjek_klub(klub)

            #klubID = tjek_klub(klub, klub_liste)
            okmedlem = 0
            if medlem in medlemmer_liste:
                okmedlem = 1

            if okmedlem == 0:
                medlem = opdater_rigtig_navn(medlem, medlemmer_liste, emitbrik1, KlubID)
            
            DeltagerKlar = dict()
            Deltager = dict()
            deltagernr = "Deltager" + (str(i + 1))
            Deltager['Bane'] = (data1['Bane'])
            Deltager['Status'] = (data1['Status'])
            Deltager['Statuskode'] = (data1['Statuskode'])
            Deltager['Placering'] = placnr
            Deltager['Navn'] = medlem
            Deltager['Klub'] = (data1['Klub'])
            Deltager['Emit'] = (data1['Emit'])
            Deltager['Point'] = Point
            Deltager['Tid'] = (data1['Tid'])
            Deltager['StrakTider'] = (data1['StrakTider'])
                
            ''' Danner deltageren klar til at skrive til fil'''
            Test2[deltagernr] = Deltager
            ''' Skriver deltager til et dictionarie som til slut skrives til json fil '''
            DeltagerKlar.update(Test2)
            #print (DeltagerKlar)

            #print ('Næste    !!')
            db.session.commit()

    with open(path + mappe + '\\' + fil_endelig, 'w', encoding='utf8') as DeltagerSkriv:
        DeltagerJson = json.dumps(DeltagerKlar, ensure_ascii=False)
        DeltagerSkriv.write(DeltagerJson)

    done = "Gennemført beregn2"
    return done