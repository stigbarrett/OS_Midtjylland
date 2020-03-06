#3a_Opdater_Placering_StraktiderDB_2019M.py

from app.models import Klub, Konkurrence, Medlemmer, Deltager, Grunddata, Baner, PostBaner, deltager_strak
from app import db
import json
import sqlite3
from operator import itemgetter

def antalBaner(loebnr):
    antal = db.session.query(Baner).filter(Baner.konkurrence_id == loebnr).count()
    return antal


def straktider_nr_org(loebnr):
    antalbaner = antalBaner(loebnr)
    alle = []
    hver = dict()
    for q in range (0, antalbaner):
        bane = "Bane " + str(q + 1) 
        for s in db.session.query(deltager_strak).\
            filter(Konkurrence.id==loebnr).\
            filter(Deltager.bane==bane).\
            filter(deltager_strak.deltager_id==Deltager.id).all():
            hver['id'] = s.id
            hver['deltager_id'] = s.deltager_id
            hver['postnr'] = s.postnr
            hver['post_code'] = s.post_code
            hver['tidTil'] = s.tidTil
            hver['tidTilPlac'] = s.tidTilPlac
            hver['tidIalt'] = s.tidIalt
            hver['tidIaltPlac'] = s.tidIaltPlac
            alle.append(hver)
            hver = dict()
        newlist = []
        newlistsamlet = []
        #newlist = sorted(alle, key=lambda k: (k['postnr'], k['tidTil']))
        newlist = sorted(alle, key=itemgetter('postnr', 'tidTil'))
        #testlist = list(enumerate(newlist,1))
        #newlistsamlet = sorted(alle, key=lambda l: (l['postnr'], l['tidIalt']))
        newlistsamlet = sorted(alle, key=itemgetter('postnr', 'tidIalt'))
        antaltemp1 = (len(newlist))
        
        antal = sum(x.get('postnr') == 1 for x in newlist)
        y = 0
        for x in range(int(antaltemp1/antal)):
            i = 0
            while i < antal:
                tempdict = newlist[y]
                baneid = tempdict['id']
                posttid = tempdict['tidTil']
                #posttidialt = tempdict['ialt']
                if posttid == 0:
                    banepostplac = 0
                    #c1 = deltager_strak(id = baneid, tidTilPlac = banepostplac)
                    #c1 = db.session.query(deltager_strak).get(baneid)
                    #c1.tidTilPlac = banepostplac
                else:
                    banepostplac = i + 1
                i = i + 1
                y = y + 1
                if baneid == 14:
                    print ('stop')
                c1 = deltager_strak(id=baneid, deltager_id=tempdict['deltager_id'], postnr=tempdict['postnr'], post_code=tempdict['post_code'], tidTil=tempdict['tidTil'], tidTilPlac=banepostplac, tidIalt=tempdict['tidIalt'], tidIaltPlac=tempdict['tidIaltPlac'])
                    #c1 = db.session.query(deltager_strak).get(baneid)
                    #c1.tidTilPlac = banepostplac
                
                #c2 = deltager_strak(id = baneid, TidTilPlac = banepostplac)
                db.session.merge(c1)
                db.session.commit()
                if y == (len(newlist) - 1):
                    print (y)
                    print (len(newlist))
   
        antaltemp2 = (len(newlistsamlet))
        #antal = sum(x.get('post') == 1 for x in newlist)

        yy = 0
        for xx in range(int(antaltemp2/antal)):
            ii = 0
            while ii < antal:
                tempdict2 = newlistsamlet[yy]
                baneid2 = tempdict2['id']
                posttidialt = tempdict2['tidIalt']
                if posttidialt == 0:
                    banesamletpostplac = 0
                else:
                    banesamletpostplac = ii + 1
                ii = ii + 1
                yy = yy + 1
                c8 = deltager_strak(id=baneid2, deltager_id=tempdict2['deltager_id'], postnr=tempdict2['postnr'], post_code=tempdict2['post_code'], tidTil=tempdict2['tidTil'], tidTilPlac=banesamletpostplac, tidIalt=tempdict2['tidIalt'], tidIaltPlac=tempdict2['tidIaltPlac'])
                #c8 = db.session.query(deltager_strak).get(baneid2)
                #c8.tidIaltPlac = banesamletpostplac
                db.session.merge(c8)
                db.session.commit()
            
    #c3 = deltager_strak(id = baneid, TidTilPlac = banepostplac)
    #db.session.commit()
    #print ('Næste    !!')
    #q = q + 1
    #db.session.commit()

    done = "Gennemført beregn4"
    return done

def straktider_nr(loebnr):
    antalbaner = antalBaner(loebnr)
    alle = []
    hver = dict()
    for q in range (0, antalbaner):
        bane = "Bane " + str(q + 1) 
        for s in db.session.query(deltager_strak).\
            filter(Konkurrence.id==loebnr).\
            filter(Deltager.bane==bane).\
            filter(deltager_strak.deltager_id==Deltager.id).all():
            hver['id'] = s.id
            hver['deltager_id'] = s.deltager_id
            hver['postnr'] = s.postnr
            hver['post_code'] = s.post_code
            hver['tidTil'] = s.tidTil
            hver['tidTilPlac'] = s.tidTilPlac
            hver['tidIalt'] = s.tidIalt
            hver['tidIaltPlac'] = s.tidIaltPlac
            alle.append(hver)
            hver = dict()
        newlist = []
        newlistsamlet = []
        #newlist = sorted(alle, key=lambda k: (k['postnr'], k['tidTil']))
        newlist = sorted(alle, key=itemgetter('postnr', 'tidTil'))
        #testlist = list(enumerate(newlist,1))
        #newlistsamlet = sorted(alle, key=lambda l: (l['postnr'], l['tidIalt']))
        newlistsamlet = sorted(alle, key=itemgetter('postnr', 'tidIalt'))
        antaltemp1 = (len(newlist))

    
        antal = sum(x.get('postnr') == 1 for x in newlist)
        y = 0
        for x in range(int(antaltemp1/antal)):
            i = 0
            res = [j for j in newlist if (j['postnr'] == x + 1)]
            while i < len(res):
                tempdict = res[i]
                baneid = tempdict['id']
                posttid = tempdict['tidTil']
                if posttid == 0:
                    banepostplac = 0
                else:
                    banepostplac = i + 1
                i = i + 1
                y = y + 1

                c = db.session.query(deltager_strak).get(baneid)
                #print ("Id ", c.id, "Postcode ", c.Post_code)
                c.TidTilPlac = banepostplac
                #c2 = deltager_strak(id = baneid, TidTilPlac = banepostplac)
                #session.add(c2)
                db.session.commit()

                #c1 = deltager_strak(id=baneid, deltager_id=tempdict['deltager_id'], postnr=tempdict['postnr'], post_code=tempdict['post_code'], tidTil=tempdict['tidTil'], tidTilPlac=banepostplac, tidIalt=tempdict['tidIalt'], tidIaltPlac=tempdict['tidIaltPlac'])
                
                #db.session.merge(c1)
            #db.session.commit()
                
    
        antaltemp2 = (len(newlistsamlet))
        #antal = sum(x.get('post') == 1 for x in newlist)

        yy = 0
        for xx in range(int(antaltemp2/antal)):
            ii = 0
            while ii < antal:
                tempdict2 = newlistsamlet[yy]
                baneid2 = tempdict2['id']
                posttidialt = tempdict2['tidIalt']
                if posttidialt == 0:
                    banesamletpostplac = 0
                else:
                    banesamletpostplac = ii + 1
                ii = ii + 1
                yy = yy + 1
                c8 = deltager_strak(id=baneid2, deltager_id=tempdict2['deltager_id'], postnr=tempdict2['postnr'], post_code=tempdict2['post_code'], tidTil=tempdict2['tidTil'], tidTilPlac=banesamletpostplac, tidIalt=tempdict2['tidIalt'], tidIaltPlac=tempdict2['tidIaltPlac'])
                #c8 = db.session.query(deltager_strak).get(baneid2)
                #c8.tidIaltPlac = banesamletpostplac
                db.session.merge(c8)
                db.session.commit()
            
    #c3 = deltager_strak(id = baneid, TidTilPlac = banepostplac)
    #db.session.commit()
    #print ('Næste    !!')
    #q = q + 1
    #db.session.commit()

    done = "Gennemført beregn4"
    return done