from . import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    company = db.Column(db.String(128))
    contact = db.Column(db.String(128))
    projects = db.relationship('Project', backref='customer', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128))
    date = db.Column(db.Date)
    bess_size = db.Column(db.Float)
    pv_power = db.Column(db.Float)
    hydro_power = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    profiles = db.relationship('BESSProfile', backref='project', lazy=True)

class BESSProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class SimulationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    total_load = db.Column(db.Float)
