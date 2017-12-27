from datetime import datetime
from catalog import db

# Tables ctlg_category, ctlg_item, ctlg_user are been created in the database


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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id
        }


class User(db.Model):
    __tablename__ = 'ctlg_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    gplus_id = db.Column(db.String(40), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    categories = db.relationship('Category', backref='ctlg_user',
                                 lazy='dynamic')
    items = db.relationship('Item', backref='ctlg_user', lazy='dynamic')
