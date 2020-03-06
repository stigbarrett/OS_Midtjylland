from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session
#from flask_login import current_user, login_required
from flask_babel import _, get_locale
from werkzeug.urls import url_parse
from guess_language import guess_language
from app import db
#from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.models import Klub, Konkurrence, Grunddata, Medlemmer, Deltager, Baner, PostBaner, deltager_strak
from app.translate import translate
from app.beregn import bp
from app.beregn.controllerloeb import hent_sensteskov, hent_konkurrencer, hent_k, resultater_strak, hent_baner, hent_klub, resultater, hentPoint, hent_brugerdata, hent_statistik1, hent_statistik2, hent_statistik3
from app.beregn.Omform import omdan
from app.beregn.Navnetjek import NavneTjek
from app.beregn.strakberegn import straktider_nr
from app.beregn.forms import AdminForm, BeregnForm, Straktider, Point, brugerbaner, Statistik
from app.beregn.indsaet import indsaet

@bp.route('/vis_resultater', methods=['GET', 'POST'])
def vis_resultater():
    form1 = Straktider(form_name1='Straktider')
    form2 = Point(form_name2='Point')
    form3 = brugerbaner(form_name3='brugerbaner')
    form3.brugerbaner.choices = [(str(row.id), row.navn) for row in Medlemmer.query.order_by(Medlemmer.navn).all()]
    form1.konkurrence.choices = [(str(row.id), row.skov) for row in Konkurrence.query.filter(Konkurrence.resultatOK==1).order_by(Konkurrence.id.desc()).all()]
    form1.bane.choices = [(row.baneNavn, row.baneNavn) for row in Baner.query.all()]
    loeb_temp = Konkurrence.query.filter(Konkurrence.resultatOK==1).order_by(Konkurrence.id.desc()).first()
    loeb = loeb_temp.id
    resultat = resultater('Bane 1', loeb)
    art = 'resultat'
    skov = hent_sensteskov(loeb)
    skov1 = skov.skov
    klubid = skov.klub_id
    klub = hent_klub(klubid)
    klub = klub.langtnavn
    tid = skov.dato
    tid = tid.strftime("%d-%m-%Y")
    if request.method == 'GET':
        return render_template('beregn/resultater.html', art=art, resultat=resultat, skov=skov1, klub=klub, bane="Bane 1", tid=tid, form1=form1, form2=form2, form3=form3)
    if form1.validate_on_submit() and request.form['form_name1'] == 'Straktider':
        loeb = int(form1.konkurrence.data)
        baner1 = form1.bane.data
        art = form1.art.data
        strak = resultater_strak(baner1, loeb)
        resultat = resultater(baner1, loeb)
        skov = hent_sensteskov(loeb)
        skov1 = skov.skov
        klubid = skov.klub_id
        klub = hent_klub(klubid)
        klub = klub.langtnavn
        tid = skov.dato
        tid = tid.strftime("%d-%m-%Y")
        return render_template("beregn/resultater.html", resultat=resultat, strak=strak, art=art, skov=skov1, klub=klub, bane=baner1, tid=tid, form1=form1, form2=form2, form3=form3)
    if form2.validate_on_submit() and request.form['form_name2'] == 'Point':
        baner2 = form2.banepoint.data
        point = hentPoint(baner2)
        art = 'point'
        return render_template("beregn/resultater.html", point=point, art=art, bane=baner2, form1=form1, form2=form2, form3=form3)
    if form3.validate_on_submit() and request.form['form_name3'] == 'brugerbaner':
        bruger = int(form3.brugerbaner.data)
        brugerdata, Navn = hent_brugerdata(bruger)
        navn = Navn
        art = 'bruger'
        return render_template("beregn/resultater.html", bruger=bruger, brugerdata=brugerdata, navn=navn, art=art, form1=form1, form2=form2, form3=form3)
    return redirect('beregn.resultater')

@bp.route('/vis_bruger', methods=('GET', 'POST'))
def vis_bruger():
    form1 = brugerbaner(form_name='brugerbaner')
    form1.brugerbaner.choices = [(str(row.id), row.navn) for row in Medlemmer.query.order_by(Medlemmer.navn).all()]
    if request.method == 'GET':
        return render_template('beregn/visbruger.html', form1=form1)
    if form1.validate_on_submit() and request.form['form_name'] == 'brugerbaner':
        bruger = int(form1.brugerbaner.data)
        brugerdata, Navn = hent_brugerdata(bruger)
        navn = Navn
        art = 'bruger'
        #print (bruger)
        return render_template("beregn/visbruger.html", bruger=bruger, brugerdata=brugerdata, navn=navn, art=art, form1=form1)
    return redirect(url_for('beregn.vis_bruger'))

@bp.route('/statistik1', methods=('GET', 'POST'))
def statistik1():
    statistik_data = hent_statistik1()
    return render_template("beregn/_statistik.html", statistik=statistik_data)

@bp.route('/statistik2', methods=('GET', 'POST'))
def statistik2():
    statistik_data = hent_statistik2()
    return render_template("beregn/_statistik.html", statistik=statistik_data)

@bp.route('/statistik3', methods=('GET', 'POST'))
def statistik3():
    statistik_data = hent_statistik3()
    return render_template("beregn/_statistik.html", statistik=statistik_data)

@bp.route('/vis_statistik', methods=['GET', 'POST'])
def vis_statistik():
    form = Statistik(form_name='Statistik')
    art = form.statistik.data
    if request.method == 'GET':
        return render_template('beregn/statistik.html', form=form, art=art)
    if form.validate_on_submit():
            statistik_data = hent_statistik1()
            statistik_data1 = hent_statistik3()
            statistik_data2 = hent_statistik2()
            return render_template("beregn/statistik.html", form=form, statistik2=statistik_data1, statistik1=statistik_data, statistik3=statistik_data2, art=art)
    return redirect(url_for('beregn.statistik'))


@bp.route('point', methods=['GET', 'POST'])
def point():
    point = hentPoint()
    return render_template("beregn/point.html", point=point)

@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    form=BeregnForm()
    Konkurrencer = hent_k()
    if form.validate_on_submit():
        if form.submit.data:
            loeb = form.KonKur.data.id
            mappe = form.KonKur.data.mappenavn
            path = form.KonKur.data.KonkurrenceG.basisPath
            svar = omdan(loeb, mappe, path)
        elif form.submit1.data:
            loeb = form.KonKur.data.id
            mappe = form.KonKur.data.mappenavn
            path = form.KonKur.data.KonkurrenceG.basisPath
            svar = NavneTjek(loeb, mappe, path)
        elif form.submit2.data:
            loeb = form.KonKur.data.id
            mappe = form.KonKur.data.mappenavn
            path = form.KonKur.data.KonkurrenceG.basisPath
            svar = indsaet(loeb, mappe, path)
 
        flash(svar, category="message")
        return redirect(url_for('beregn.admin'))
    
    return render_template("beregn/admin.html", form=form, Konkurrencer=Konkurrencer)

@bp.route('/_get_banerne/')
def _get_banerne():
    konkurrence2 = request.args.get('konkurrence', '01', type=str)
    konkurrence3 = int(konkurrence2)
    Banerne = [(row.baneNavn, row.baneNavn) for row in Baner.query.filter_by(konkurrence_id=konkurrence3).all()]
    return jsonify(Banerne)

@bp.route('/_get_resultat')
def _get_resultat():
    loeb2 = request.form1['konkurrence']
    res1 = request.form1['bane']
    art = 'resultat'
    res2 = resultater(res1, loeb2)
    return res2, art

@bp.route('/opsat', methods=['GET', 'POST'])
def opsat():
    form=AdminForm()
    Konkurrencer = hent_k()
    if form.validate_on_submit():
        nyloeb = Konkurrence(konkurrence_type=form.KonkurrenceType.data, skov=form.Skov.data, dato=form.Dato.data, mappenavn=form.Mappenavn.data, klub_id=form.Klub.data.id, grunddata_id=form.Grunddata.data.id)
        db.session.add(nyloeb)
        db.session.commit()
        flash("Dine data er skrevet til databasen", category="message")
        return redirect(url_for('beregn.opsat'))
    return render_template("beregn/opsat.html", form=form, Konkurrencer=Konkurrencer)

#@bp.route('/action_page', methods=['GET', 'POST'])
#def action_page():
#    svar = omdan()
#    flash(svar, category="message")
#    return redirect(url_for('beregn.admin'))
    
#@bp.route('/action_page1', methods=['GET', 'POST'])
#def action_page1():
#    flash("Du har klikket på - Ret konkurrence", category="message")
#    return redirect(url_for('beregn.admin'))