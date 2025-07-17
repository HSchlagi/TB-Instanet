import csv
import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename

from . import db
from .forms import CustomerForm, ProjectForm, UploadForm
from .models import Customer, Project, BESSProfile, SimulationResult
from .config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@main_bp.route('/customers', methods=['GET', 'POST'])
def customers():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data, company=form.company.data, contact=form.contact.data)
        db.session.add(customer)
        db.session.commit()
        flash('Customer saved.')
        return redirect(url_for('main.customers'))
    customers = Customer.query.all()
    return render_template('customers.html', form=form, customers=customers)

@main_bp.route('/project/new', methods=['GET', 'POST'])
def project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, location=form.location.data, date=form.date.data,
                          bess_size=form.bess_size.data, pv_power=form.pv_power.data,
                          hydro_power=form.hydro_power.data)
        db.session.add(project)
        db.session.commit()
        flash('Project created.')
        return redirect(url_for('main.index'))
    return render_template('project_form.html', form=form)

@main_bp.route('/project/<int:project_id>/upload', methods=['GET', 'POST'])
def upload_profile(project_id):
    project = Project.query.get_or_404(project_id)
    form = UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        f.save(path)
        profile = BESSProfile(filename=filename, project=project)
        db.session.add(profile)
        db.session.commit()
        flash('File uploaded.')
        return redirect(url_for('main.index'))
    return render_template('upload.html', form=form, project=project)

@main_bp.route('/project/<int:project_id>/simulate')
def simulate(project_id):
    project = Project.query.get_or_404(project_id)
    profile = BESSProfile.query.filter_by(project_id=project_id).first()
    if not profile:
        flash('No profile uploaded.')
        return redirect(url_for('main.index'))
    path = os.path.join(Config.UPLOAD_FOLDER, profile.filename)
    total = 0
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                try:
                    total += float(row[0])
                except ValueError:
                    continue
    result = SimulationResult(project_id=project_id, total_load=total)
    db.session.add(result)
    db.session.commit()
    flash(f'Simulation complete. Total load: {total}')
    return redirect(url_for('main.index'))
