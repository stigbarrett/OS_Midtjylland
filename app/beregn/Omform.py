import datetime
import json, codecs

def baner(indholdList, path, skov, fil_baner):
    '''Danner banedata. Bane nummer og poster på bane. Skriver fil med banens indhold'''
    #BanerKlar = dict()
    Poster = dict()
    Test = dict()
    for y in range(len(indholdList)):
        x = 1
        if y == 1:
            Bane = indholdList[y]
            Bane = Bane[0:6]
        elif y > 1 and y < len(indholdList) - 1:
            Postnr = "Post " + (str(y - 1))
            Poster[Postnr] = indholdList[y]
            Test[Bane] = Poster
        
        #BanerKlar.update(Test)
    #if x == 1:
    #    with open(path + skov + '\\' + fil_baner, 'a', encoding='utf8') as PostBaner:
    #        PostBaner.write(json.dumps(BanerKlar))
    #else:
    #    with open(path + skov + '\\' + fil_baner, 'a', encoding='utf8') as PostBaner:
    #        PostBaner.write(json.dumps(BanerKlar))
    return Bane, Test

def vendom(indholdList):
    navn = indholdList[3]
    opdelt = navn.split()
    efternavn = opdelt[0]
    del opdelt[0]
    seperator = ' '
    print (navn)
    if len(opdelt) >= 1:
        fornavn = seperator.join(opdelt)
    else:
        fornavn = opdelt[-1]
    nytnavn = fornavn + " " + efternavn
    return nytnavn

def statusdisk(indholdList, Bane):
    ''' Danner løberdata for diskvalificerede løbere. '''
    indholdList.insert(0, Bane)
    indholdList.insert(1, "Diskvalificeret")
    del indholdList[2]
    del indholdList[2]
    indholdList.insert(2, 0)
    indholdList.insert(-1, 0)
    return 3

def statusudgaet(indholdList, Bane):
    ''' Danne løberdata for udgåede løbere. '''
    indholdList.insert(0, Bane)
    indholdList.insert(1, "Udgaaet")
    del indholdList[2]
    del indholdList[2]
    indholdList.insert(2, 0)
    indholdList.insert(-1, 0)
    return 2

def statusingensluttid(indholdList, Bane):
    ''' Danne løberdata for løbere uden en sluttid'''
    indholdList.insert(0, Bane)
    indholdList.insert(1, "IngenTid")
    del indholdList[2]
    del indholdList[2]
    indholdList.insert(2, 0)
    indholdList.insert(-1, 0)
    return 4

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def statusgodkendt(indholdList, Bane):
    ''' Danner løberdata for godkendte løbere og giver løber point. 100 point for vinder. Efterfølgende fratrækkes antal minutter efter vinder. '''
    indholdList.insert(1, Bane)
    del indholdList[0]
    indholdList.insert(1, "OK")
    del indholdList[2]
    indholdList.insert(2, 0)
    indholdList.insert(-1, 0)
    return 1

def omdan(loebnr, mappe, path):
    '''Variable der skal sættes for hvert løb'''
    #path = 'C:\\Users\\sba\\OneDrive\\Orientering\\O-trainingsloeb_2019\\'
    #skov = '01_FeldborgNord'
    fil_resultat = 'Resultat.dat'
    fil_baner = 'PostBaner1.json'
    fil_bearbejdet = 'Bearbejdet1.json'
    efternavn_forst = 1
    BanerKlar = []
    #path_baner = (path + mappe + '\\' + fil_baner)
    #(path + skov + '\\' + fil_baner, 'w')
    fil = (path + mappe + '\\' + fil_resultat)
    with open(fil, 'r') as f:
        indhold = f.readlines()
        #Test = dict()
        Deltager = dict()
        DeltagerKlar = []
        #k1 = 0
        for i in range(len(indhold)):
            indholdList = [int(e) if e.isdigit() else e for e in indhold[i].split(',')]
            if str(indholdList[0]) == ('"R"'):
                #stig = str(indholdList[0])
                Bane, Test = baner(indholdList, path, mappe, fil_baner)
                BanerKlar.append(Test)
                continue
            elif str(indholdList[0]) == ('"X"#Diskvalificeret'):
                Statuskode = statusdisk(indholdList, Bane)
            elif str(indholdList[0]) == ('"X"#Udgået'):
                Statuskode = statusudgaet(indholdList, Bane)
            elif str(indholdList[0]) == ('"X"#Ingen sluttid'):
                Statuskode = statusingensluttid(indholdList, Bane)
            elif str(indholdList[0]) == ('"X"'):
                Statuskode = statusgodkendt(indholdList, Bane)
            
            if str(indholdList[0]) == (Bane):
                Deltager['Bane'] = indholdList[0]
                Deltager['Status'] = indholdList[1]
                Deltager['Statuskode'] = Statuskode
                Deltager['Placering'] = ""
                if efternavn_forst == 1:
                    Deltager['Navn'] = vendom(indholdList)
                else:
                    Deltager['Navn'] = indholdList[3]
                Deltager['Klub'] = indholdList[4]
                Deltager['Emit'] = indholdList[5]
                Deltager['Point'] = ""
                if len(indholdList) > 8:
                    Straktider = (indholdList[6:len(indholdList) - 2])
                    Minutter = str(datetime.timedelta(seconds=(Straktider[-3])))
                    Deltager['Tid'] = Minutter
                    Deltager['TidSek'] = Straktider[-3]
                    Strak = {}
                    Tid = 0
                    x = 1
                    for y in range (len(Straktider)):            
                        if y % 2 == 0:
                            ''' finder kontrol nummeret '''
                            Control = str('Post' + str(x) + ' - ' + str(Straktider[y]))
                            x = x + 1
                        else:
                            ''' finder tiden til kontrollen (sekunder) '''
                            Tid = Straktider[y]
                            Strak[Control] = Tid
                    Deltager['StrakTider'] = Strak
                else:
                    Deltager['Tid'] = 0
                    Deltager['StrakTider'] = 0
                
                ''' Skriver deltager til et dictionarie som til slut skrives til json fil '''
                DeltagerKlar.append(Deltager)
            Deltager = dict()
        #BanerKlar.append(Test)
        ''' Sorterer deltagerne efter bane og tid '''
        DeltagerKlar = sorted(DeltagerKlar, key = lambda i: (i['Bane'], i['Statuskode'], i['Tid']))
        #print (Deltagerklar)
        #DeltagerKlar = sorted(DeltagerKlar, key = lambda i: (i['Status']), reverse=True)

        with open(path + mappe + '\\' + fil_baner, 'w', encoding='utf8') as PostBaner:
            PostBaner.write(json.dumps(BanerKlar))

        with open(path + mappe + '\\' + fil_bearbejdet, 'w', encoding='utf8') as DeltagerSkriv:
            DeltagerJson = json.dumps(DeltagerKlar, ensure_ascii=False)
            DeltagerSkriv.write(DeltagerJson)

    done = "Gennemført beregn1"
    return done
