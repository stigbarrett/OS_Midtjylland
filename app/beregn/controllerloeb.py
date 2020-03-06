
from app.models import Klub, Grunddata, Konkurrence, Baner, PostBaner, deltager_strak, Deltager, Medlemmer
from app import db
import time
from flask import jsonify
from datetime import datetime, date
from sqlalchemy import and_
from operator import itemgetter

def hent_baner(loebnr):
    baner = db.session.query(Baner).filter_by(id=loebnr).all()
    #Baner.query.filter_by(konkurrence_id=loebnr)
    return baner

def hent_sensteskov(loebnr):
    Skov1 = Konkurrence.query.filter_by(id=loebnr).first_or_404()
    return Skov1

def hent_klub(klubid):
    klub1 = Klub.query.filter_by(id=klubid).first_or_404()
    return klub1

def hent_konkurrencer():
    temp1_Konkurrencer = Konkurrence.query.all()
    Konkurrencer = dict()
    for x in temp1_Konkurrencer:
        skov = temp1_Konkurrencer
    return Konkurrencer

def antal_konkurrencer():
    #test3 = db.session.query(Medlemmer.id, db.func.count(Deltager.medlemmer_id)).outerjoin(Deltager, Medlemmer.id==Deltager.medlemmer_id).filter(Deltager.bane==bane).group_by(Medlemmer.navn).all()
    Antal = db.session.query(Konkurrence.id, db.func.count(Konkurrence.id)).filter(Konkurrence.resultatOK==1).all()
    Antal = Antal[0][1]
    return Antal

def hent_k():
    Konkurrencer = dict()
    Konkurrencerklar = list()
    now1 = str(date.today())
    for s, k in db.session.query(Konkurrence, Klub).filter(Konkurrence.klub_id==Klub.id).filter(Konkurrence.dato>=now1).order_by(Konkurrence.dato.asc()).all():
        Konkurrencer['Skov'] = s.skov
        Konkurrencer['Dato'] = s.dato
        Konkurrencer['Klub'] = k.langtnavn

        Konkurrencerklar.append(Konkurrencer)
        #print (pointklar)
        Konkurrencer = dict()

    return Konkurrencerklar

def resultater_strak(bane, loebnr):
    
    strakpost = dict()
    #deltagerklar = []
    bane = bane
    loebnr = loebnr
    #deltagerklartemp = []
    strak = dict()
    strakklar = []
    
    for d, m in db.session.query(Deltager, Medlemmer).\
        filter(Deltager.konkurrence_id==loebnr).\
        filter(Deltager.bane==bane).\
        filter(Deltager.medlemmer_id==Medlemmer.id).all():
        #deltagerklartemp = []
        deltagerID = d.id
        #deltagere.append(m.navn)
        strak['Navn'] = m.navn

        status = d.status
        statuskode = d.statuskode
        #medlem_id = d.medlemmer_id

        if statuskode == 1:
            strak['Samlet'] = d.tid
        else:
            strak['Samlet'] = str(status)

        loberdata = db.session.query(deltager_strak).filter(deltager_strak.deltager_id==deltagerID).all()

        for s in loberdata:
            strakpost = dict()
            kode = s.post_code
            postnr = s.postnr
            if postnr < 10:
                strak['0' + str(postnr) + ' - ' + str(kode) + ""] = strakpost
                #strak['0' + str(postnr) + ' - ' + str(kode) + ""] = strakpost
            else:
                strak['' + str(postnr) + ' - ' + str(kode) + ''] = strakpost
                #strak['' + str(postnr) + '  -  ' + str(kode) + ''] = strakpost
            if s.tidTil == 0:
                strakpost['tid'] = '   -'
                strakpost['tidplac'] = ""
            else:
                strakpost['tid'] = time.strftime("%M:%S", time.gmtime(s.tidTil))
                strakpost['tidplac'] = str(s.tidTilPlac)
            
            if s.tidIalt == 0:
                strakpost['ialt'] = '   -'
                strakpost['ialtplac'] = ""
            elif s.tidIalt >= 3600:
                strakpost['ialt'] = time.strftime("%H:%M:%S", time.gmtime(s.tidIalt))
                strakpost['ialtplac'] = str(s.tidIaltPlac)
            else:
                strakpost['ialt'] = time.strftime("%M:%S", time.gmtime(s.tidIalt))
                strakpost['ialtplac'] = str(s.tidIaltPlac)

           
        strakklar.append(strak)
        strakpost = dict()
        strak = dict()
        
    #db.session.close()
    #print (strakklar)
    return strakklar

def resultater(bane, loeb):
    #session = connect_to_database()
    deltagerklar = []
    deltager = dict()
    
    for k, d, m in db.session.query(Konkurrence, Deltager, Medlemmer).\
        filter(Konkurrence.id==loeb).\
        filter(Konkurrence.id==Deltager.konkurrence_id).\
        filter(Deltager.medlemmer_id==Medlemmer.id).\
        filter(Deltager.bane==bane).all():
            deltager = dict()
            deltager['Bane'] = d.bane
            deltager['Placering'] = str(d.placering)
            deltager['Navn'] = m.navn
            deltager['Tid'] = d.tid
            deltager['Point'] = str(d.point)
            deltagerklar.append(deltager)
    #print (deltagerklar)
    return deltagerklar

def hentPoint(bane):
    pointklar = []
    test1 = db.session.query(Deltager, Medlemmer).\
        filter(Deltager.bane==bane).\
        filter(Deltager.medlemmer_id==Medlemmer.id).\
        order_by(Deltager.medlemmer_id.asc()).all()

    temp2 = db.session.query(Medlemmer).join(Deltager).\
        filter(Deltager.bane == bane).all()
    
    #test2 = db.session.query(Deltager).outerjoin(Medlemmer, Deltager.medlemmer_id==Medlemmer.id).filter(Deltager.bane==bane).group_by(Medlemmer.id).all()
    #test3 = db.session.query(Medlemmer.id, db.func.count(Deltager.medlemmer_id)).outerjoin(Deltager, Medlemmer.id==Deltager.medlemmer_id).filter(Deltager.bane==bane).group_by(Medlemmer.navn).all()
    #test4 = db.session.query(Medlemmer.id, db.func.sum(Deltager.point)).outerjoin(Deltager, Medlemmer.id==Deltager.medlemmer_id).filter(Deltager.bane==bane).group_by(Medlemmer.navn).all()
    
    Resultat = {}
    Antalloeb = antal_konkurrencer()
    i = 0
    p = 0
    TResultat = {}
    T2Resultat = {}
    alle_navne = temp2

    for row in alle_navne:
        temptest=test1[p]
        i = i + 1
        navn = row.navn
        temp_deltager1 = db.session.query(Medlemmer).join(Deltager).\
            filter(and_(Medlemmer.navn == navn, Deltager.bane == bane)).all()
        temp_deltager = db.session.query(Deltager).join(Medlemmer).\
            filter(and_(Medlemmer.navn == navn, Deltager.bane == bane)).all()
        deltager1 = temp_deltager1[0]
        deltager0 = temp_deltager
        Resultat['Navn'] = deltager1.navn
        test44 = db.session.query(Medlemmer.id, db.func.sum(Deltager.point)).join(Deltager).filter(and_(Medlemmer.navn==navn, Deltager.bane==bane)).group_by(Medlemmer.navn).all()
        Resultat['Sum'] = test44[0][1]

        for xx in range(Antalloeb):
            Resultat["L" + str(xx + 8)] = 0

        for ii in range(len(deltager0)):
            indholdlist = deltager0[ii]
            for x in range (Antalloeb):
                if indholdlist.konkurrence_id == (x + 8):
                    Resultat["L" + str(x + 8)] = indholdlist.point
            TResultat = Resultat
        Resultat = {}
        T2Resultat.update(TResultat)
        pointklar.append(TResultat)
        
        p = p + 1
    pointklar2 = sorted(pointklar, key=itemgetter('Sum'), reverse=True)
    return pointklar2

def hent_brugerdata(id):
    deltagerklar = []
    deltager = dict()
    for m, d, k in db.session.query(Medlemmer, Deltager, Konkurrence).\
        filter(Medlemmer.id==id).\
        filter(Deltager.medlemmer_id==Medlemmer.id).\
        filter(Konkurrence.id==Deltager.konkurrence_id).all():

        deltager = dict()
        deltager['Løb'] = (k.skov)
        deltager['Bane'] = d.bane
        deltager['Placering'] = d.placering
        deltager['Tid'] = d.tid
        deltager['point'] = d.point
        deltager['Status'] = d.status
        deltagerklar.append(deltager)
        Navn = m.navn

    return deltagerklar, Navn

def hent_statistik1():
    deltagerklar = []
    deltager = dict()
    #test3 = db.session.query(Medlemmer.id, db.func.count(Deltager.medlemmer_id)).outerjoin(Deltager, Medlemmer.id==Deltager.medlemmer_id).filter(Deltager.bane==bane).group_by(Medlemmer.navn).all()

    """Deltagere pr. løb"""
    test = db.session.query(Klub, Konkurrence, db.func.count(Deltager.medlemmer_id)).\
        filter(Klub.id==Konkurrence.klub_id).\
        filter(Konkurrence.id==Deltager.konkurrence_id).\
        group_by(Konkurrence.skov).all()

    for row in test:
        deltager = dict()

        deltager['Navn'] = row.Klub.langtnavn
        deltager['Løb'] = row.Konkurrence.skov
        deltager['Antal'] = row[2]

        deltagerklar.append(deltager)

    return deltagerklar

def hent_statistik2():
    deltagerklar = []
    deltager = dict()
    
    """Deltagere pr. klub"""

    test1 = db.session.query(Klub, Medlemmer, db.func.count(Deltager.medlemmer_id)).\
        filter(Deltager.medlemmer_id==Medlemmer.id).\
        filter(Medlemmer.klub_id==Klub.id).\
        group_by(Klub.kortnavn).all()

    for row in test1:
        deltager = dict()

        deltager['Klub'] = row.Klub.kortnavn
        #deltager['Løb'] = row.Konkurrence.skov
        deltager['Antal'] = row[2]

        deltagerklar.append(deltager)
    
    deltagerklar = sorted(deltagerklar, key=itemgetter('Antal'), reverse=True)


    return deltagerklar

def hent_statistik3():
    deltagerklar = []
    deltager = dict()
    """Deltagere pr. bane"""

    test2 = db.session.query(Deltager, db.func.count(Deltager.bane)).\
            group_by(Deltager.bane).all()

    for row in test2:
        deltager = dict()

        deltager['Bane'] = row.Deltager.bane
        #deltager['antal'] = row.Konkurrence.skov
        deltager['Antal'] = row[1]

        deltagerklar.append(deltager)

    return deltagerklar