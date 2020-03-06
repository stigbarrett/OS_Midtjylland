from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, HiddenField, validators, RadioField
from wtforms.fields.html5 import DateField  
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_babel import _, lazy_gettext as _l
from app.models import User, Konkurrence, Grunddata, Klub, Medlemmer, Deltager, deltager_strak, Baner, PostBaner


def enabled_klubber():
    AlleKlubber = Klub.query.all()
    return AlleKlubber

def enabled_grunddata():
    AlleGrunddata = Grunddata.query.all()
    return AlleGrunddata

def enabled_konkurrencer():
    AlleKonkurrencer = Konkurrence.query.all()
    return AlleKonkurrencer

def enabled_baner():
    AlleBaner = Baner.query.all()
    return AlleBaner

class AdminForm(FlaskForm):
    "Opsætnings form"
    KonkurrenceType = StringField(_l('KonkurrenceType', validators=[DataRequired()]))
    Skov = StringField(_l('Skov', validators=[DataRequired()]))
    Dato = DateField(_l('Dato', validators=[DataRequired()]))
    #Path = StringField(_l('Path', validators=[DataRequired()]))
    Mappenavn = StringField(_l('Mappenavn', validators=[DataRequired()]))
    Klub = QuerySelectField(query_factory=enabled_klubber, get_label='langtnavn', 
                        allow_blank=True, blank_text=(u'Klik for at vælge'))
    Grunddata = QuerySelectField(query_factory=enabled_grunddata, get_label='aar', 
                        allow_blank=True, blank_text=(u'Klik for at vælge'))
    submit = SubmitField(_l('Indsend'))

class BeregnForm(FlaskForm):
    "Beregner form"
    KonKur = QuerySelectField(query_factory=enabled_konkurrencer, get_label='mappenavn', 
                        allow_blank=True, blank_text=(u'Klik for at vælge'))

    submit = SubmitField(_l('Omform'))
    submit1 = SubmitField(_l('Tilret'))
    submit2 = SubmitField(_l('Indlæs'))
    #submit3 = SubmitField('Indsend beregn4')

class Statistik(FlaskForm):
    form_name = HiddenField('Form Name')
    statistik = SelectField('Statistik:', choices=[('klubber', 'Klubber'), ('delt1', 'Deltager pr. bane'), ('delt2', 'Deltager pr. klub')])
    submit = SubmitField(_l('Vælg'))

class Straktider(FlaskForm):
    form_name1 = HiddenField('Form Name')
    konkurrence = SelectField('Konkurrence:', validators=[DataRequired()], id='select_konkurrence')
    bane = SelectField('Bane:', validators=[DataRequired()], id='select_bane')
    art = RadioField('Hvad:', validators=[DataRequired()], choices=[('resultat', 'Resultater'),('straktider', 'Stræktider')], default='resultat' ,id='select_type')
    submit1 = SubmitField('Vælg')

class Point(FlaskForm):
    form_name2 = HiddenField('Form Name')
    banepoint = SelectField('Banepoint', validators=[DataRequired()], choices=[('Bane 1', 'Bane 1'), ('Bane 2', 'Bane 2'), ('Bane 3', 'Bane 3'), ('Bane 4', 'Bane 4'), ('Bane 5', 'Bane 5')], id='select_bane_point')
    submit2 = SubmitField('Vælg', id='point')
    
class brugerbaner(FlaskForm):
    form_name3 = HiddenField('Form Name')
    brugerbaner = SelectField('Brugerbaner:', validators=[DataRequired()], id='select_brugerbaner')
    #bane = SelectField('Bane:', validators=[DataRequired()], id='select_bane')
    #art = RadioField('Hvad:', validators=[DataRequired()], choices=[('resultat', 'Resultater'),('straktider', 'Stræktider')], default='resultat' ,id='select_type')
    submit3 = SubmitField('Vælg')



