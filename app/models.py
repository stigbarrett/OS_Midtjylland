from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(SearchableMixin, db.Model):
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Klub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    langtnavn = db.Column(db.String(80))
    kortnavn = db.Column(db.String(40))
    tom = db.Column(db.String(10))
    medlem = db.relationship('Medlemmer', backref="Medlemmer", lazy='dynamic')
    konkurrence = db.relationship('Konkurrence', backref="Konkurrence", lazy='dynamic')

class Medlemmer(db.Model):
    """
    Holder navne på medlemmer
    """
    id = db.Column(db.Integer, primary_key = True)
    navn = db.Column(db.String(80))
    navn_ok = db.Column(db.Integer)
    emitbrik = db.Column(db.Integer)
    samlet_point = db.Column(db.Integer)
    klub_id = db.Column(db.Integer, db.ForeignKey('klub.id'))
 
class Deltager(db.Model):
    """
    Tabel der holder oplsyninger om deltagernes løb
    """
    id = db.Column(db.Integer, primary_key = True)
    bane = db.Column(db.String(10))
    placering = db.Column(db.Integer)
    status = db.Column(db.String(20))
    statuskode = db.Column(db.Integer)
    tid = db.Column(db.String(20))
    tidSekunder = db.Column(db.Integer)
    strak = db.Column(db.String(200))
    point = db.Column(db.Integer)
    emit_Brik = db.Column(db.Integer)
    medlemmer_id = db.Column(db.Integer, db.ForeignKey("medlemmer.id"), index=True,)
    konkurrence_id = db.Column(db.Integer, db.ForeignKey("konkurrence.id"), index=True,)
    deltager_strak = db.relationship('deltager_strak', backref="deltager_strak", lazy='dynamic')
    
class deltager_strak(db.Model):
    """
    Tabel der holder deltagers stræktider
    """
    id = db.Column(db.Integer, primary_key = True)
    deltager_id = db.Column(db.Integer, db.ForeignKey("deltager.id"), index=True,)
    postnr = db.Column(db.Integer)
    post_code = db.Column(db.Integer)
    tidTil = db.Column(db.Integer)
    tidTilPlac = db.Column(db.Integer)
    tidIalt = db.Column(db.Integer)
    tidIaltPlac = db.Column(db.Integer)

class Grunddata(db.Model):
    """
    Tabel der holder grunddata for ÅRET
    """
    id = db.Column(db.Integer, primary_key = True)
    basisPath = db.Column(db.String(80))
    aar = db.Column(db.String(10))
    resultatFilnavn = db.Column(db.String(40))
    konkurrenceG = db.relationship('Konkurrence', backref="KonkurrenceG", lazy='dynamic')

class Konkurrence(db.Model):
    """
    Tabel der holder konkurrence data
    """
    id = db.Column(db.Integer, primary_key = True)
    konkurrence_type = db.Column(db.String(80))
    resultatOK = db.Column(db.Integer())
    skov = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    resultater = db.Column(db.String(4))
    dato = db.Column(db.Date())
    path = db.Column(db.String(80))
    mappenavn = db.Column(db.String(40))
    klub_id = db.Column(db.Integer, db.ForeignKey("klub.id"))
    grunddata_id = db.Column(db.Integer, db.ForeignKey("grunddata.id"))
    #def __repr__(self):
    #    return self.skov

class Baner(db.Model):
    """
    Tabel der holder Bane data
    """
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    baneNavn = db.Column(db.String(20))
    baneLaengde = db.Column(db.Integer)
    konkurrence_id = db.Column(db.Integer, db.ForeignKey("konkurrence.id"))
    postbaner = db.relationship('PostBaner', backref="PostBaner", lazy='dynamic')

class PostBaner(db.Model):
    """
    Tabel der holder poster på banerne
    """
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    postNr = db.Column(db.Integer)
    controlNr = db.Column(db.Integer)
    baner_id = db.Column(db.Integer, db.ForeignKey("baner.id"))