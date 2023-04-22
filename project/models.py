from . import db
from flask_login import UserMixin
from flask_security import RoleMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.String(1000), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(UserMixin, db.Model):
    id = db.Column(db.String(1000), primary_key=True)  # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def has_role(self, role):
        """
        Check if the User has the role
        """
        return role in [r.name for r in self.roles]

