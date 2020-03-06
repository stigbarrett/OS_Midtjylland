#3_Laes_InsertDB_2019M.py

from app.models import Klub, Konkurrence, Medlemmer, Deltager, Grunddata, Baner, PostBaner, deltager_strak
from app import db
import json
from operator import itemgetter

def find_medlemID(medlem):
    ''' Finder medlems ID '''
    temp1 = db.session.query(Medlemmer).filter(Medlemmer.navn == str(medlem)).all()
    MedlemmerID = int(temp1[0].id)
    print (MedlemmerID)
    return MedlemmerID

def find_poster_Bane(bane1, Konkurrence_id):
    temp2 = db.session.query(Baner).filter(Baner.konkurrence_id == Konkurrence_id).\
        filter(Baner.baneNavn==bane1).first()
    Bane_ID_er = int(temp2.id)
    Bane_Poster = []
    for p in db.session.query(PostBaner).\
        filter(PostBaner.baner_id==Bane_ID_er).all():
        Bane_Poster.append(p.controlNr)
    return Bane_Poster

def indsaet_deltager(bane1, plac, status, Statuskode, tid, tid_sekunder, strak, point, emitbrik, MedlemID, Konkurrence_id):
    ''' Indsæt resultat data i tabel DELTAGER '''
    c1 = Deltager(bane = bane1, placering = plac, status = status, statuskode = Statuskode, tid = tid ,tidSekunder = tid_sekunder, strak = strak , point = point , emit_Brik = emitbrik, medlemmer_id = MedlemID, konkurrence_id = Konkurrence_id)
    db.session.add(c1)
    #db.session.flush(c1)
    db.session.commit()
    return c1.id
    #session.commit()

def indsaet_baner(banenavn, konkurrenceid):
    ''' Indsæt banenavn i tabel Baner '''
    c2 = Baner(baneNavn = banenavn, konkurrence_id = konkurrenceid)
    db.session.add(c2)
    #db.session.flush(c2)
    db.session.commit()
    return c2.id

def indsaet_poster(post, controlnr, Baneid):
    ''' Indsæt postnr og Controlnummer i tabel PostBaner '''
    c3 = PostBaner(postNr = post, controlNr = controlnr, baner_id = Baneid)
    db.session.add(c3)
    #db.session.flush(c3)
    db.session.commit()

def indsaet_deltager_strak(deltager_ID, post, Post_code, TidTil, TidTilPlac, TidIalt, TidIaltPlac):
    ''' Indsæt stræktider i strætidstabellen'''
    c4 = deltager_strak(deltager_id = deltager_ID, postnr = post, post_code = Post_code, tidTil = TidTil, tidTilPlac=TidTilPlac, tidIalt = TidIalt, tidIaltPlac=TidIaltPlac)
    db.session.add(c4)
    #db.session.flush(c4)
    db.session.commit()

def update_konkurrence(loebnr):
    ''' Sæt flag for resultater indlæst '''
    c5 = Konkurrence(id = loebnr, resultatOK = 1)
    db.session.merge(c5)
    #db.session.flush(c5)
    db.session.commit()

def afgoer_poster(Poster, strak, taeller):
    postcoder = list(strak)
    print (strak)
    if len(Poster) >= len(postcoder):
        for x in range(len(postcoder)):
            pcode = postcoder[x]
            Post_code = int(pcode[-3:])
            if Poster[x] == Post_code:
                taeller = taeller + 1
    else:
        for x in range(len(Poster)):
            pcode = postcoder[x]
            Post_code = int(pcode[-3:])
            if Poster[x] == Post_code:
                taeller = taeller + 1

    return taeller

def klargoer_poster(Poster, Statuskode, strak, bane1,  Konkurrence_id, medlem):
    '''finder den rigtige postsekvens for banen'''
    NyPoster = {}
    for y in range(len(Poster)):
        NyPoster['Post' + str(y + 1) + ' - ' + str(Poster[y])] = 0

    postcoder_strak = list(strak)
    postcoder_rigtig = list(NyPoster)
    #sidste_post_rigtig = (postcoder_rigtig[-1])

    StrakControllerTider = []
    StrakPostController = []
    for q in range(len(postcoder_strak)):
        postControlTemp = int((postcoder_strak[q][-3:]))
        StrakPostController.append(postControlTemp)

    StrakControllerTider = list(strak.values())
    sidste_post_rigtig = (StrakPostController[-2])
    NyStrak = {}
   
    
    for key in range(len(Poster)):
        #if key < (len(strak)-1):
        Post_code_strak = StrakPostController[key]
        Post_code_rigtig = Poster[key]
        while key < (len(StrakPostController)-2):
            Post_code_strak_naeste = StrakPostController[key + 1]
            break
        while key < (len(Poster)-1):
            Post_code_rigtig_naeste = Poster[key + 1]
            break
        if Post_code_strak == Post_code_rigtig:
            ''' rigtig post er klippet '''
            NyStrak[postcoder_rigtig[key]] = StrakControllerTider[key]
        elif Post_code_strak_naeste == Post_code_rigtig_naeste and Post_code_strak_naeste==sidste_post_rigtig:
            ''' der er så klippet en forkert post. Rigtig post sættes til 0 '''
            NyStrak[postcoder_rigtig[key]] = StrakControllerTider[key]
        elif Post_code_strak_naeste == Post_code_rigtig:
            ''' så er der klippet en post for meget og tæller skal + 1 
            den rigtige post følger umiddelbart efter '''
            del StrakPostController[key]
            del StrakControllerTider[key]
            NyStrak[postcoder_rigtig[key]] = StrakControllerTider[key]
        elif Post_code_strak_naeste == Post_code_rigtig_naeste:
            ''' der er så klippet en forkert post. Rigtig post sættes til 0 '''
            NyStrak[postcoder_rigtig[key]] = 0
        elif Post_code_rigtig_naeste == Post_code_strak:
            ''' Der er klippet én post for lidt. Rigtig post sættes til 0'''
            StrakPostController.insert(key, Post_code_rigtig)
            StrakControllerTider.insert(key, 0)
            NyStrak[postcoder_rigtig[key]] = 0
        elif Post_code_strak_naeste != Post_code_rigtig_naeste:
            StrakPostController.insert(key, Post_code_rigtig)
            StrakControllerTider.insert(key, 0)
            NyStrak[postcoder_rigtig[key]] = 0
        else:
            ''' der er klippet for få poster. Resten sættes til posten og 0 i tid '''
            #del StrakPostController[key]
            #del StrakControllerTider[key]
            NyStrak[postcoder_rigtig[key]] = 0
        #else:
        #    NyStrak[postcoder_rigtig[key]] = 0
    
    return NyStrak

def indsaet(loebnr, skov, path):
    '''Variable der skal sættes inden hvert løb'''
    #path = 'C:\\Users\\sba\\OneDrive\\Orientering\\O-trainingsloeb_2019\\'
    #skov = '01_FeldborgNord'
    #fil_resultat = 'Resultat.dat'
    #il_bearbejdet = 'Bearbejdet1.json'
    fil_endelig = 'Endelig1.json'
    fil_baner = 'PostBaner1.json'
    Konkurrence_id = loebnr
    fil_res = (path + skov + '\\' + fil_endelig)
    fil_ban = (path + skov + '\\' + fil_baner)

    
    with open(fil_ban, 'r', encoding='utf8') as f1:
        finalBaner = json.load(f1)

        for i in range (len(finalBaner)):
            data1 = finalBaner[i]
            banenavn = ('Bane ' + str(i + 1))
            data2 = data1.get(banenavn)
            #banenavn = ('Bane ' + str(i + 1))
            BaneID = indsaet_baner(banenavn, Konkurrence_id)
            #taeller = 0
            #Bane_Tjek = []
            for ii in range (len(data2)):
                taeller = ii + 1
                postnr = taeller
                controlnr = data2['Post ' + str(taeller)]
                baneID = BaneID
                indsaet_poster(postnr, controlnr, baneID)
    

    test2 = dict()
    p = 1
    with open(fil_res, 'r', encoding='utf8') as f:
        final = json.load(f)
        x = 1
        alle = []
        for i in range (len(final)):
            data1 = final['Deltager' + str(i + 1)]
            #klub = (data1['Klub'])
            medlem = (data1['Navn'])
            #emitbrik1 = (data1['Emit'])
            bane1 = (data1['Bane'])
            status = (data1['Status'])
            Statuskode = (data1['Statuskode'])
            plac = (data1['Placering'])
            point = (data1['Point'])
            tid = (data1['Tid'])
            strak = data1['StrakTider']
            tid_sekunder = 0
            emitbrik = 0
            #klublang = ""
            #print (medlem)
            MedlemID = find_medlemID(medlem)
            #print (MedlemID)
            deltagerID = indsaet_deltager(bane1, plac, status, Statuskode, tid, tid_sekunder, str(strak), point, emitbrik, MedlemID, Konkurrence_id)
            #tidtilOld = 0
            tidtil = 0
            tidialt = 0
            x = 1
            q = 0

            Poster = find_poster_Bane(bane1, Konkurrence_id)
    
            strak_klar = klargoer_poster(Poster, Statuskode, strak, bane1, Konkurrence_id, medlem)

            #print (medlem)
            #print ('Klargjort liste')
            #print (strak_klar)
            postcoder = list(strak_klar)
            
            
            for z in strak_klar:
                postErKlar = dict()
                postEr = dict()
                post = x
                pcode = postcoder[x - 1]
                Post_code = int(pcode[-3:])
                tidialt = int(strak_klar[z])
                if x == 1:
                    tidialtOld = 0
                    tidtil = tidialt
                    tidialtOld = tidialt
                else:
                    if tidialt != 0:
                        tidtil = tidialt - tidialtOld
                        tidialtOld = int(strak_klar[z])
                    else:
                        tidtil = 0

                deltagernr = "Deltager" + (str(p))
                postEr['deltagerID'] = deltagerID
                postEr['bane'] = bane1
                postEr['post'] = post
                postEr['Post_code'] = Post_code
                postEr['tidtil'] = tidtil
                postEr['tidialt'] = tidialt
                alle.append(postEr)
                test2[deltagernr] = postEr
                postErKlar.update(test2)
                #indsaet_deltager_strak(deltagerID, post, Post_code, tidtil, tidialt)
                x = x + 1
                q = q + 1
                p = p + 1

    newlist = sorted(alle, key=itemgetter('bane', 'post', 'tidtil'))
    #antal = sum(x.get('bane') == 1 for x in newlist)
    newlist2 = []
    for u in range(1,6):
        antalposter = db.session.query(PostBaner).filter(PostBaner.baner_id==u).count()
        post_taeller = 1
        for o in range(len(newlist)):
            banenavn = 'Bane ' + str(u)
            res = [j for j in newlist if (j['bane'] == banenavn)]
            if post_taeller <= antalposter:
                res2 = [k for k in res if (k['post'] == post_taeller)]
                #newlist2 = []
                plac_taeller = 1
                for pp in range(len(res2)):
                    newlist1 = res2[pp]
                    if newlist1['tidtil'] == 0:
                        newlist1['tidtilplac'] = 0
                    else:
                        newlist1['tidtilplac'] = plac_taeller
                        plac_taeller = plac_taeller + 1
                    newlist2.append(newlist1)
            post_taeller = post_taeller + 1

    newlist3 = sorted(newlist2, key=itemgetter('bane', 'post', 'tidialt'))

    newlist4 = []
    for u in range(1,6):
        antalposter = db.session.query(PostBaner).filter(PostBaner.baner_id==u).count()
        post_taeller = 1
        for o in range(len(newlist3)):
            banenavn = 'Bane ' + str(u)
            res = [j for j in newlist3 if (j['bane'] == banenavn)]
            if post_taeller <= antalposter:
                res2 = [k for k in res if (k['post'] == post_taeller)]
                #newlist2 = []
                plac_taeller = 1
                for pp in range(len(res2)):
                    newlist5 = res2[pp]
                    if newlist5['tidialt'] == 0:
                        newlist5['tidialtplac'] = 0
                    else:
                        newlist5['tidialtplac'] = plac_taeller
                        plac_taeller = plac_taeller + 1
                    newlist4.append(newlist5)
            post_taeller = post_taeller + 1

    for w in range(len(newlist4)):
        deltagerID = newlist4[w]['deltagerID']
        post = newlist4[w]['post']
        Post_code = newlist4[w]['Post_code']
        tidtil = newlist4[w]['tidtil']
        TidTilPlac = newlist4[w]['tidtilplac']
        tidialt = newlist4[w]['tidialt']
        TidIaltPlac = newlist4[w]['tidialtplac']
        indsaet_deltager_strak(deltagerID, post, Post_code, tidtil, TidTilPlac, tidialt, TidIaltPlac)
    
    update_konkurrence(loebnr)


    with open(path + skov + '\\' + 'sorteret_til.json', 'w', encoding='utf8') as sorteretSkriv:
        SorteretJson = json.dumps(newlist4, ensure_ascii=False)
        sorteretSkriv.write(SorteretJson)

    db.session.commit()
    done = "Gennemført beregn3 testsorteret"
    return done

