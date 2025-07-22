from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app import db, csrf
from models import Project, LoadProfile, LoadValue, Customer, InvestmentCost, ReferencePrice, SpotPrice, SolarData, HydroData, WeatherData
from datetime import datetime, timedelta
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/projects')
def projects():
    return render_template('projects.html')

@main_bp.route('/customers')
def customers():
    return render_template('customers.html')

@main_bp.route('/spot_prices')
def spot_prices():
    return render_template('spot_prices.html')

@main_bp.route('/reference_prices')
def reference_prices():
    return render_template('reference_prices.html')

@main_bp.route('/preview_data')
def preview_data():
    return render_template('preview_data.html')

@main_bp.route('/import_data')
def import_data():
    return render_template('import_data.html')

@main_bp.route('/new_project')
def new_project():
    return render_template('new_project.html')

@main_bp.route('/new_customer')
def new_customer():
    return render_template('new_customer.html')

@main_bp.route('/project/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@main_bp.route('/edit_project')
def edit_project():
    return render_template('edit_project.html')

@main_bp.route('/view_customer')
def view_customer():
    return render_template('view_customer.html')

@main_bp.route('/edit_customer')
def edit_customer():
    return render_template('edit_customer.html')

@main_bp.route('/import_load')
def import_load():
    return render_template('import_load.html')

@main_bp.route('/bess-peak-shaving-analysis')
def bess_peak_shaving_analysis():
    return render_template('bess_peak_shaving_analysis.html')

# API Routes für Projekte
@main_bp.route('/api/projects')
def api_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'location': p.location
    } for p in projects])

@main_bp.route('/api/projects', methods=['POST'])
@csrf.exempt
def api_create_project():
    try:
        data = request.get_json()
        project = Project(
            name=data['name'],
            location=data.get('location'),
            customer_id=data.get('customer_id'),
            date=datetime.fromisoformat(data['date']) if data.get('date') else None,
            bess_size=data.get('bess_size'),
            bess_power=data.get('bess_power'),
            pv_power=data.get('pv_power'),
            hp_power=data.get('hp_power'),
            wind_power=data.get('wind_power'),
            hydro_power=data.get('hydro_power')
        )
        db.session.add(project)
        db.session.commit()
        return jsonify({'success': True, 'id': project.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/projects/<int:project_id>')
def api_get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        'id': project.id,
        'name': project.name,
        'location': project.location,
        'date': project.date.isoformat() if project.date else None,
        'bess_size': project.bess_size,
        'bess_power': project.bess_power,
        'pv_power': project.pv_power,
        'hp_power': project.hp_power,
        'wind_power': project.wind_power,
        'hydro_power': project.hydro_power,
        'customer_id': project.customer_id,
        'customer': {
            'id': project.customer.id,
            'name': project.customer.name
        } if project.customer else None,
        'created_at': project.created_at.isoformat()
    })

@main_bp.route('/api/projects/<int:project_id>', methods=['PUT'])
@csrf.exempt
def api_update_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        data = request.get_json()
        
        project.name = data['name']
        project.location = data.get('location')
        project.customer_id = data.get('customer_id')
        
        # Datum sicher parsen
        if data.get('date') and data['date'].strip():
            try:
                project.date = datetime.fromisoformat(data['date'])
            except ValueError:
                project.date = None
        else:
            project.date = None
            
        project.bess_size = data.get('bess_size')
        project.bess_power = data.get('bess_power')
        project.pv_power = data.get('pv_power')
        project.hp_power = data.get('hp_power')
        project.wind_power = data.get('wind_power')
        project.hydro_power = data.get('hydro_power')
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/projects/<int:project_id>', methods=['DELETE'])
@csrf.exempt
def api_delete_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/projects/<int:project_id>/load-profiles')
def api_project_load_profiles(project_id):
    project = Project.query.get_or_404(project_id)
    load_profiles = LoadProfile.query.filter_by(project_id=project_id).all()
    return jsonify({
        'project': {
            'id': project.id,
            'name': project.name
        },
        'load_profiles': [{
            'id': lp.id,
            'name': lp.name
        } for lp in load_profiles]
    })

# API Routes für Kunden
@main_bp.route('/api/customers')
def api_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'company': c.company,
        'contact': c.contact,
        'phone': c.phone,
        'projects_count': len(c.projects)
    } for c in customers])

@main_bp.route('/api/customers', methods=['POST'])
@csrf.exempt
def api_create_customer():
    try:
        data = request.get_json()
        print(f"Received customer data: {data}")
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name ist erforderlich'}), 400
        
        customer = Customer(
            name=data['name'].strip(),
            company=data.get('company', '').strip() or None,
            contact=data.get('contact', '').strip() or None,
            phone=data.get('phone', '').strip() or None
        )
        
        db.session.add(customer)
        db.session.commit()
        
        print(f"Customer created successfully: {customer.id}")
        return jsonify({'success': True, 'id': customer.id}), 201
        
    except Exception as e:
        print(f"Error creating customer: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/customers/<int:customer_id>')
def api_get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'company': customer.company,
        'contact': customer.contact,
        'phone': customer.phone,
        'created_at': customer.created_at.isoformat()
    })

@main_bp.route('/api/customers/<int:customer_id>', methods=['PUT'])
@csrf.exempt
def api_update_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()
        
        customer.name = data['name']
        customer.company = data.get('company')
        customer.contact = data.get('contact')
        customer.phone = data.get('phone')
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/customers/<int:customer_id>', methods=['DELETE'])
@csrf.exempt
def api_delete_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/customers/<int:customer_id>/projects')
def api_customer_projects(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    projects = Project.query.filter_by(customer_id=customer_id).all()
    return jsonify({
        'customer': {
            'id': customer.id,
            'name': customer.name
        },
        'projects': [{
            'id': p.id,
            'name': p.name,
            'location': p.location,
            'created_at': p.created_at.isoformat()
        } for p in projects]
    })

# API Routes für Investitionskosten
@main_bp.route('/api/investment-costs')
def api_investment_costs():
    project_id = request.args.get('project_id')
    if project_id:
        costs = InvestmentCost.query.filter_by(project_id=project_id).all()
    else:
        costs = InvestmentCost.query.all()
    
    return jsonify([{
        'id': c.id,
        'component_type': c.component_type,
        'component_subtype': c.component_subtype,
        'cost_eur': c.cost_eur,
        'cost_per_unit': c.cost_per_unit,
        'power_kw': c.power_kw,
        'capacity_kwh': c.capacity_kwh,
        'description': c.description,
        'manufacturer': c.manufacturer,
        'model': c.model,
        'quantity': c.quantity
    } for c in costs])

@main_bp.route('/api/investment-costs', methods=['POST'])
@csrf.exempt
def api_create_investment_cost():
    try:
        data = request.get_json()
        cost = InvestmentCost(
            project_id=data['project_id'],
            component_type=data['component_type'],
            component_subtype=data.get('component_subtype'),
            cost_eur=data['cost_eur'],
            cost_per_unit=data.get('cost_per_unit'),
            power_kw=data.get('power_kw'),
            capacity_kwh=data.get('capacity_kwh'),
            description=data.get('description'),
            manufacturer=data.get('manufacturer'),
            model=data.get('model'),
            quantity=data.get('quantity', 1)
        )
        db.session.add(cost)
        db.session.commit()
        return jsonify({'success': True, 'id': cost.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/investment-costs/<int:cost_id>')
def api_get_investment_cost(cost_id):
    cost = InvestmentCost.query.get_or_404(cost_id)
    return jsonify({
        'id': cost.id,
        'project_id': cost.project_id,
        'component_type': cost.component_type,
        'component_subtype': cost.component_subtype,
        'cost_eur': cost.cost_eur,
        'cost_per_unit': cost.cost_per_unit,
        'power_kw': cost.power_kw,
        'capacity_kwh': cost.capacity_kwh,
        'description': cost.description,
        'manufacturer': cost.manufacturer,
        'model': cost.model,
        'quantity': cost.quantity
    })

@main_bp.route('/api/investment-costs/<int:cost_id>', methods=['PUT'])
@csrf.exempt
def api_update_investment_cost(cost_id):
    try:
        cost = InvestmentCost.query.get_or_404(cost_id)
        data = request.get_json()
        
        cost.component_type = data['component_type']
        cost.component_subtype = data.get('component_subtype')
        cost.cost_eur = data['cost_eur']
        cost.cost_per_unit = data.get('cost_per_unit')
        cost.power_kw = data.get('power_kw')
        cost.capacity_kwh = data.get('capacity_kwh')
        cost.description = data.get('description')
        cost.manufacturer = data.get('manufacturer')
        cost.model = data.get('model')
        cost.quantity = data.get('quantity', 1)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/investment-costs/<int:cost_id>', methods=['DELETE'])
@csrf.exempt
def api_delete_investment_cost(cost_id):
    try:
        cost = InvestmentCost.query.get_or_404(cost_id)
        db.session.delete(cost)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API Routes für Referenzpreise
@main_bp.route('/api/reference-prices')
def api_reference_prices():
    prices = ReferencePrice.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price_type': p.price_type,
        'price_eur_mwh': p.price_eur_mwh,
        'region': p.region,
        'valid_from': p.valid_from.isoformat() if p.valid_from else None,
        'valid_to': p.valid_to.isoformat() if p.valid_to else None
    } for p in prices])

@main_bp.route('/api/reference-prices', methods=['POST'])
@csrf.exempt
def api_create_reference_price():
    try:
        data = request.get_json()
        price = ReferencePrice(
            name=data['name'],
            price_type=data['price_type'],
            price_eur_mwh=data['price_eur_mwh'],
            region=data.get('region'),
            valid_from=datetime.fromisoformat(data['valid_from']) if data.get('valid_from') else None,
            valid_to=datetime.fromisoformat(data['valid_to']) if data.get('valid_to') else None
        )
        db.session.add(price)
        db.session.commit()
        return jsonify({'success': True, 'id': price.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API Routes für Spot-Preise
@main_bp.route('/api/spot-prices', methods=['POST'])
@csrf.exempt
def api_spot_prices():
    try:
        data = request.get_json()
        
        # Demo-Daten generieren basierend auf Zeitraum
        time_range = data.get('time_range', 'month')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
        else:
            # Standard-Zeitraum
            end = datetime.now()
            if time_range == 'today':
                start = end.replace(hour=0, minute=0, second=0, microsecond=0)
            elif time_range == 'week':
                start = end - timedelta(days=7)
            elif time_range == 'month':
                start = end - timedelta(days=30)
            else:  # year
                start = end - timedelta(days=365)
        
        # Demo Spot-Preise generieren
        prices = []
        current = start
        price_id = 1
        
        while current <= end:
            for hour in range(24):
                # Basis-Preis mit Tageszeit-Schwankungen
                base_price = 50 + 30 * (0.5 + 0.5 * (hour - 6) / 12)
                if hour >= 6 and hour <= 18:
                    base_price += 20
                
                # Jahreszeitliche Anpassungen
                month = current.month
                if month in [12, 1, 2]:  # Winter
                    base_price *= 1.3
                elif month in [6, 7, 8]:  # Sommer
                    base_price *= 0.8
                
                # Zufällige Schwankungen
                random_factor = 0.8 + 0.4 * random.random()
                price = base_price * random_factor
                
                prices.append({
                    'id': price_id,
                    'timestamp': current.replace(hour=hour).isoformat(),
                    'price': round(price, 2)
                })
                price_id += 1
            
            current += timedelta(days=1)
        
        return jsonify(prices)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/spot-prices/import', methods=['POST'])
@csrf.exempt
def api_spot_prices_import():
    try:
        # Demo-Import-Funktionalität
        return jsonify({'success': True, 'message': 'Import erfolgreich (Demo)'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/load-profiles/<int:load_profile_id>/data-range', methods=['POST'])
@csrf.exempt
def api_load_profile_data_range(load_profile_id):
    """API für Lastdaten eines Lastprofils für einen spezifischen Datumsbereich"""
    try:
        load_profile = LoadProfile.query.get_or_404(load_profile_id)
        
        # Request-Daten parsen
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Keine JSON-Daten empfangen'}), 400
            
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        date_range = data.get('date_range', 'month')
        
        if not start_date_str or not end_date_str:
            return jsonify({'error': 'Start- und Enddatum erforderlich'}), 400
        
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError as e:
            return jsonify({'error': f'Ungültiges Datumsformat: {e}'}), 400
        
        # Generiere Demo-Daten für den Zeitraum
        demo_data = []
        current_date = start_date
        
        while current_date <= end_date:
            for hour in range(24):
                timestamp = current_date + timedelta(hours=hour)
                
                # Basis-Last basierend auf Tageszeit und Jahreszeit
                base_load = 800 + 400 * (0.5 + 0.5 * (hour - 6) / 12)
                if hour >= 6 and hour <= 18:
                    base_load += 200
                
                # Jahreszeitliche Anpassungen
                month = timestamp.month
                if month in [12, 1, 2]:  # Winter
                    base_load *= 1.2
                elif month in [6, 7, 8]:  # Sommer
                    base_load *= 0.9
                
                # Zufällige Schwankungen
                random_factor = 0.8 + 0.4 * random.random()
                load = base_load * random_factor
                
                demo_data.append({
                    'timestamp': timestamp.isoformat(),
                    'load_kw': round(load, 2),
                    'hour': hour,
                    'day': timestamp.day,
                    'month': timestamp.month
                })
            
            current_date += timedelta(days=1)
        
        return jsonify({
            'load_profile': {
                'id': load_profile.id,
                'name': load_profile.name
            },
            'date_range': {
                'start': start_date_str,
                'end': end_date_str,
                'type': date_range
            },
            'data': demo_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Server-Fehler: {str(e)}'}), 500 

@main_bp.route('/api/test-customer', methods=['POST'])
def test_customer():
    try:
        data = request.get_json()
        return jsonify({
            'success': True, 
            'received_data': data,
            'message': 'Test customer endpoint working'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400 

# Lastprofil-Import Route
@main_bp.route('/load_profile_import')
def load_profile_import():
    return render_template('load_profile_import.html')

# API Route für Lastprofil-Import
@main_bp.route('/api/load-profiles', methods=['POST'])
@csrf.exempt
def api_create_load_profile():
    try:
        data = request.get_json()
        
        # Import-Einstellungen
        time_interval = data.get('time_interval', 15)  # Minuten
        date_format = data.get('date_format', 'auto')
        meter_combination = data.get('meter_combination', 'sum')
        
        # Lastprofil erstellen
        load_profile = LoadProfile(
            project_id=data['project_id'],
            name=data['name']
        )
        db.session.add(load_profile)
        db.session.flush()  # ID generieren
        
        # Daten verarbeiten und normalisieren
        processed_data = process_load_data(data['data'], time_interval, date_format, meter_combination)
        
        # Lastwerte hinzufügen
        for item in processed_data:
            load_value = LoadValue(
                load_profile_id=load_profile.id,
                timestamp=datetime.fromisoformat(item['timestamp']),
                load_kw=item['load']
            )
            db.session.add(load_value)
        
        db.session.commit()
        return jsonify({'success': True, 'id': load_profile.id, 'data_points': len(processed_data)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

def process_load_data(raw_data, time_interval, date_format, meter_combination):
    """Verarbeitet und normalisiert Lastdaten"""
    processed_data = []
    
    # Daten nach Zeitstempel sortieren
    sorted_data = sorted(raw_data, key=lambda x: x['timestamp'])
    
    # Zeitintervalle normalisieren
    current_interval_start = None
    interval_data = []
    
    for item in sorted_data:
        timestamp = datetime.fromisoformat(item['timestamp'])
        
        # Zeitstempel auf Intervall runden
        if time_interval == 15:
            # Auf 15-Minuten-Intervalle runden
            rounded_time = timestamp.replace(minute=(timestamp.minute // 15) * 15, second=0, microsecond=0)
        elif time_interval == 30:
            # Auf 30-Minuten-Intervalle runden
            rounded_time = timestamp.replace(minute=(timestamp.minute // 30) * 30, second=0, microsecond=0)
        elif time_interval == 60:
            # Auf Stunden-Intervalle runden
            rounded_time = timestamp.replace(minute=0, second=0, microsecond=0)
        else:
            rounded_time = timestamp
        
        if current_interval_start is None:
            current_interval_start = rounded_time
            interval_data = [item['load']]
        elif rounded_time == current_interval_start:
            # Gleiches Intervall - Daten sammeln
            interval_data.append(item['load'])
        else:
            # Neues Intervall - vorheriges verarbeiten
            if interval_data:
                combined_load = combine_load_values(interval_data, meter_combination)
                processed_data.append({
                    'timestamp': current_interval_start.isoformat(),
                    'load': combined_load
                })
            
            # Neues Intervall starten
            current_interval_start = rounded_time
            interval_data = [item['load']]
    
    # Letztes Intervall verarbeiten
    if interval_data:
        combined_load = combine_load_values(interval_data, meter_combination)
        processed_data.append({
            'timestamp': current_interval_start.isoformat(),
            'load': combined_load
        })
    
    return processed_data

def combine_load_values(values, combination):
    """Kombiniert Lastwerte nach der gewählten Methode"""
    if not values:
        return 0
    
    if combination == 'sum':
        return sum(values)
    elif combination == 'max':
        return max(values)
    elif combination == 'average':
        return sum(values) / len(values)
    else:
        return sum(values)  # Standard: Summe

# API Route für BESS-Analyse
@main_bp.route('/api/load-profiles/<int:load_profile_id>/bess-analysis', methods=['POST'])
@csrf.exempt
def api_bess_analysis(load_profile_id):
    try:
        data = request.get_json()
        bess_capacity = data['bess_capacity']  # kWh
        bess_power = data['bess_power']  # kW
        
        # Alle Lastwerte abrufen
        load_values = LoadValue.query.filter_by(
            load_profile_id=load_profile_id
        ).order_by(LoadValue.timestamp).all()
        
        if not load_values:
            return jsonify({'error': 'Keine Lastdaten verfügbar'}), 400
        
        # BESS-Simulation
        bess_energy = 0  # Aktueller Batteriestand (kWh)
        peak_reduction = 0
        total_energy_stored = 0
        total_energy_discharged = 0
        
        bess_data = []
        
        for value in load_values:
            original_load = value.load_kw
            
            # BESS-Logik: Bei niedriger Last laden, bei hoher Last entladen
            if original_load < bess_power * 0.3:  # Niedrige Last - laden
                charge_power = min(bess_power, (bess_capacity - bess_energy) / 0.25)  # 15 Minuten
                bess_energy = min(bess_capacity, bess_energy + charge_power * 0.25)
                bess_load = original_load + charge_power
                total_energy_stored += charge_power * 0.25
            else:  # Hohe Last - entladen
                discharge_power = min(bess_power, bess_energy / 0.25)  # 15 Minuten
                bess_energy = max(0, bess_energy - discharge_power * 0.25)
                bess_load = max(0, original_load - discharge_power)
                total_energy_discharged += discharge_power * 0.25
                peak_reduction = max(peak_reduction, original_load - bess_load)
            
            bess_data.append({
                'timestamp': value.timestamp.isoformat(),
                'original_load': original_load,
                'bess_load': bess_load,
                'bess_energy': bess_energy
            })
        
        # Kosteneinsparung berechnen (vereinfacht)
        # Annahme: 0.30 €/kWh für Peak-Strom
        cost_savings = total_energy_discharged * 0.30
        
        results = {
            'peak_reduction': peak_reduction,
            'energy_stored': total_energy_stored,
            'energy_discharged': total_energy_discharged,
            'cost_savings': cost_savings
        }
        
        return jsonify({
            'success': True,
            'data': bess_data,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400 

# Datenimport-Center Route
@main_bp.route('/data_import_center')
def data_import_center():
    return render_template('data_import_center.html')

# API Route für Lastprofil-Import (erweitert)
@main_bp.route('/api/data-import/load', methods=['POST'])
@csrf.exempt
def api_import_load_data():
    try:
        data = request.get_json()
        project_id = data['project_id']
        raw_data = data['data']
        settings = data['settings']
        
        # Daten verarbeiten
        processed_data = process_energy_data(raw_data, 'load', settings)
        
        # Lastprofil erstellen
        load_profile = LoadProfile(
            project_id=project_id,
            name=f"Lastprofil {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        db.session.add(load_profile)
        db.session.flush()
        
        # Lastwerte hinzufügen
        for item in processed_data:
            load_value = LoadValue(
                load_profile_id=load_profile.id,
                timestamp=item['timestamp'],
                load_kw=item['value']
            )
            db.session.add(load_value)
        
        db.session.commit()
        return jsonify({'success': True, 'data_points': len(processed_data)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# API Route für Einstrahlungsdaten-Import
@main_bp.route('/api/data-import/solar', methods=['POST'])
@csrf.exempt
def api_import_solar_data():
    try:
        data = request.get_json()
        project_id = data['project_id']
        raw_data = data['data']
        settings = data['settings']
        
        # Daten verarbeiten
        processed_data = process_energy_data(raw_data, 'solar', settings)
        
        # Solar-Daten speichern
        for item in processed_data:
            solar_data = SolarData(
                project_id=project_id,
                timestamp=item['timestamp'],
                irradiation_wm2=item['value'],
                data_source='import'
            )
            db.session.add(solar_data)
        
        db.session.commit()
        return jsonify({'success': True, 'data_points': len(processed_data)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# API Route für Pegelstände-Import
@main_bp.route('/api/data-import/hydro', methods=['POST'])
@csrf.exempt
def api_import_hydro_data():
    try:
        data = request.get_json()
        project_id = data['project_id']
        raw_data = data['data']
        settings = data['settings']
        
        # Daten verarbeiten
        processed_data = process_energy_data(raw_data, 'hydro', settings)
        
        # Hydro-Daten speichern
        for item in processed_data:
            hydro_data = HydroData(
                project_id=project_id,
                timestamp=item['timestamp'],
                water_level_m=item['value'],
                data_source='import'
            )
            db.session.add(hydro_data)
        
        db.session.commit()
        return jsonify({'success': True, 'data_points': len(processed_data)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# API Route für PVSol-Export-Import
@main_bp.route('/api/data-import/pvsol', methods=['POST'])
@csrf.exempt
def api_import_pvsol_data():
    try:
        data = request.get_json()
        project_id = data['project_id']
        raw_data = data['data']
        settings = data['settings']
        
        # Daten verarbeiten
        processed_data = process_energy_data(raw_data, 'pvsol', settings)
        
        # PVSol-Daten speichern
        for item in processed_data:
            pv_data = SolarData(
                project_id=project_id,
                timestamp=item['timestamp'],
                power_kw=item['value'],
                data_source='pvsol_simulation'
            )
            db.session.add(pv_data)
        
        db.session.commit()
        return jsonify({'success': True, 'data_points': len(processed_data)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# API Route für Wetterdaten-Import
@main_bp.route('/api/data-import/weather', methods=['POST'])
@csrf.exempt
def api_import_weather_data():
    try:
        data = request.get_json()
        project_id = data['project_id']
        raw_data = data['data']
        settings = data['settings']
        
        # Daten verarbeiten
        processed_data = process_energy_data(raw_data, 'weather', settings)
        
        # Wetterdaten speichern
        for item in processed_data:
            weather_data = WeatherData(
                project_id=project_id,
                timestamp=item['timestamp'],
                temperature_c=item['value'],
                data_source='import'
            )
            db.session.add(weather_data)
        
        db.session.commit()
        return jsonify({'success': True, 'data_points': len(processed_data)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

def process_energy_data(raw_data, data_type, settings):
    """Intelligente Datenverarbeitung für alle Energie-Datentypen"""
    processed_data = []
    
    # Daten nach Zeitstempel sortieren
    sorted_data = sorted(raw_data, key=lambda x: x['timestamp'])
    
    # Zeitintervalle normalisieren
    time_interval = settings.get('time_interval', 15)  # Minuten
    data_combination = settings.get('data_combination', 'sum')
    quality_check = settings.get('quality_check', 'normal')
    
    current_interval_start = None
    interval_data = []
    
    for item in sorted_data:
        timestamp = item['timestamp']
        
        # Sicherstellen, dass timestamp ein datetime Objekt ist
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                continue
        
        # Zeitstempel auf Intervall runden
        if time_interval == 15:
            rounded_time = timestamp.replace(minute=(timestamp.minute // 15) * 15, second=0, microsecond=0)
        elif time_interval == 30:
            rounded_time = timestamp.replace(minute=(timestamp.minute // 30) * 30, second=0, microsecond=0)
        elif time_interval == 60:
            rounded_time = timestamp.replace(minute=0, second=0, microsecond=0)
        elif time_interval == 1440:
            rounded_time = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            rounded_time = timestamp
        
        # Qualitätsprüfung
        if not quality_check_data(item, data_type, quality_check):
            continue
        
        if current_interval_start is None:
            current_interval_start = rounded_time
            interval_data = [item['value']]
        elif rounded_time == current_interval_start:
            # Gleiches Intervall - Daten sammeln
            interval_data.append(item['value'])
        else:
            # Neues Intervall - vorheriges verarbeiten
            if interval_data:
                combined_value = combine_data_values(interval_data, data_combination)
                processed_data.append({
                    'timestamp': current_interval_start,
                    'value': combined_value
                })
            
            # Neues Intervall starten
            current_interval_start = rounded_time
            interval_data = [item['value']]
    
    # Letztes Intervall verarbeiten
    if interval_data:
        combined_value = combine_data_values(interval_data, data_combination)
        processed_data.append({
            'timestamp': current_interval_start,
            'value': combined_value
        })
    
    return processed_data

def quality_check_data(item, data_type, quality_level):
    """Qualitätsprüfung für Datenpunkte"""
    value = item['value']
    
    # Grundlegende Prüfungen
    if value is None or value == '':
        return False
    
    # Sicherstellen, dass value eine Zahl ist
    try:
        value = float(value)
    except (ValueError, TypeError):
        return False
    
    # Typ-spezifische Prüfungen
    if data_type == 'load':
        if quality_level == 'strict':
            return 0 <= value <= 10000  # kW
        elif quality_level == 'normal':
            return 0 <= value <= 50000
        else:  # loose
            return -1000 <= value <= 100000
    elif data_type == 'solar':
        if quality_level == 'strict':
            return 0 <= value <= 1200  # W/m²
        elif quality_level == 'normal':
            return 0 <= value <= 1500
        else:  # loose
            return -100 <= value <= 2000
    elif data_type == 'hydro':
        if quality_level == 'strict':
            return 0 <= value <= 100  # m
        elif quality_level == 'normal':
            return -10 <= value <= 200
        else:  # loose
            return -50 <= value <= 500
    elif data_type == 'pvsol':
        if quality_level == 'strict':
            return 0 <= value <= 10000  # kW
        elif quality_level == 'normal':
            return 0 <= value <= 50000
        else:  # loose
            return -1000 <= value <= 100000
    elif data_type == 'weather':
        if quality_level == 'strict':
            return -50 <= value <= 60  # °C
        elif quality_level == 'normal':
            return -100 <= value <= 100
        else:  # loose
            return -200 <= value <= 200
    
    return True

def combine_data_values(values, combination):
    """Kombiniert Datenwerte nach der gewählten Methode"""
    if not values:
        return 0
    
    # Sicherstellen, dass alle Werte Zahlen sind
    numeric_values = []
    for value in values:
        try:
            numeric_values.append(float(value))
        except (ValueError, TypeError):
            continue
    
    if not numeric_values:
        return 0
    
    if combination == 'sum':
        return sum(numeric_values)
    elif combination == 'max':
        return max(numeric_values)
    elif combination == 'average':
        return sum(numeric_values) / len(numeric_values)
    elif combination == 'weighted':
        # Gewichtete Mittelung (neueste Werte haben höheres Gewicht)
        total_weight = 0
        weighted_sum = 0
        for i, value in enumerate(numeric_values):
            weight = i + 1
            weighted_sum += value * weight
            total_weight += weight
        return weighted_sum / total_weight if total_weight > 0 else 0
    else:
        return sum(numeric_values)  # Standard: Summe 