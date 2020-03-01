from datetime import datetime
from app import db

class Cukier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dostawa = db.Column(db.String(64), index=True, unique=False)
    ilosc = db.Column(db.Float(), index=True, unique=False)
    zuzyte = db.Column(db.Float(), default=0)
    stan = db.Column(db.Float(), default=ilosc)
    cena = db.Column(db.Float())
    timestamp = db.Column(db.String(64), index=True, default=datetime.now().isoformat())

    def as_dict(self):
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

    def __repr__(self):
        return '<Cukier {}>'.format(self.dostawa)

class Syrop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dostawa = db.Column(db.String(64), index=True, unique=False)
    ilosc = db.Column(db.Float(), index=True, unique=False)
    zuzyte = db.Column(db.Float(), default=0)
    stan = db.Column(db.Float(), default=ilosc)
    cena = db.Column(db.Float())
    timestamp = db.Column(db.String(64), index=True, default=datetime.now().isoformat())

    def as_dict(self):
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

    def __repr__(self):
        return '<Syrop {}>'.format(self.dostawa)

class Ziola(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dostawa = db.Column(db.String(64), index=True, unique=False)
    ilosc = db.Column(db.Float(), index=True, unique=False)
    zuzyte = db.Column(db.Float(), default=0)
    stan = db.Column(db.Float(), default=ilosc)
    cena = db.Column(db.Float())
    timestamp = db.Column(db.String(64), index=True, default=datetime.now().isoformat())

    def as_dict(self):
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

    def __repr__(self):
        return '<Ziola {}>'.format(self.dostawa)

class Ciasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partia = db.Column(db.String(64), index=True, unique=False)
    ilosc = db.Column(db.Float(), index=True, unique=False)
    stan = db.Column(db.Float(), default=ilosc)
    cena = db.Column(db.Float())
    cukier = db.Column(db.String(254))
    syrop = db.Column(db.String(254))
    ziola = db.Column(db.String(254))
    timestamp = db.Column(db.String(64), index=True, default=datetime.now().isoformat())

    def as_dict(self):
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

    def __repr__(self):
        return '<Ciasto {}>'.format(self.partia)