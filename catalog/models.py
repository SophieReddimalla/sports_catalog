from datetime import datetime
from catalog import db


class Category(db.Model):
    __tablename__ = 'ctlg_category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('ctlg_user.id'),
                        nullable=False)
    items = db.relationship('Item', backref='ctlg_category', lazy='dynamic')


class Item(db.Model):
    __tablename__ = 'ctlg_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('ctlg_category.id'),
                            nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('ctlg_user.id'),
                        nullable=False)


class User(db.Model):
    __tablename__ = 'ctlg_user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True)
    categories = db.relationship('Category', backref='ctlg_user',
                                 lazy='dynamic')
    items = db.relationship('Item', backref='ctlg_user', lazy='dynamic')
