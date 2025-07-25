from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    date = db.Column(db.Date)
    bess_size = db.Column(db.Float)  # kWh
    bess_power = db.Column(db.Float)  # kW
    pv_power = db.Column(db.Float)  # kW
    hp_power = db.Column(db.Float)  # kW
    wind_power = db.Column(db.Float)  # kW
    hydro_power = db.Column(db.Float)  # kW
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer', backref='projects')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoadProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref='load_profiles')
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    data_type = db.Column(db.String(50))
    time_resolution = db.Column(db.Integer, default=15)  # Minuten
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoadValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    load_profile_id = db.Column(db.Integer, db.ForeignKey('load_profile.id'))
    load_profile = db.relationship('LoadProfile', backref='load_values')
    timestamp = db.Column(db.DateTime, nullable=False)
    power_kw = db.Column(db.Float, nullable=False)
    energy_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SpotPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    price_eur_mwh = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50))  # 'EPEX', 'ENTSO-E', 'APG'
    region = db.Column(db.String(50))  # 'AT', 'DE', 'CH'
    price_type = db.Column(db.String(20))  # 'day_ahead', 'intraday'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class InvestmentCost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    component_type = db.Column(db.String(50), nullable=False)
    component_subtype = db.Column(db.String(50))  # z.B. 'battery', 'inverter', 'modules'
    cost_eur = db.Column(db.Float, nullable=False)
    cost_per_unit = db.Column(db.Float)  # €/kW oder €/kWh
    power_kw = db.Column(db.Float)  # Leistung in kW
    capacity_kwh = db.Column(db.Float)  # Kapazität in kWh
    description = db.Column(db.Text)
    manufacturer = db.Column(db.String(100))  # Hersteller
    model = db.Column(db.String(100))  # Modell
    quantity = db.Column(db.Integer, default=1)  # Anzahl
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Beziehung zum Projekt
    project = db.relationship('Project', backref='investment_costs')

class ReferencePrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_eur_mwh = db.Column(db.Float, nullable=False)
    price_type = db.Column(db.String(50))  # 'electricity', 'gas', 'heating'
    region = db.Column(db.String(50))
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    temperature_c = db.Column(db.Float)  # Temperatur in °C
    humidity_percent = db.Column(db.Float)  # Luftfeuchtigkeit in %
    wind_speed_ms = db.Column(db.Float)  # Windgeschwindigkeit in m/s
    wind_direction_deg = db.Column(db.Float)  # Windrichtung in Grad
    pressure_hpa = db.Column(db.Float)  # Luftdruck in hPa
    data_source = db.Column(db.String(50))  # 'import', 'weather_station'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    project = db.relationship('Project', backref='weather_data')

class WeatherValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weather_data_id = db.Column(db.Integer, db.ForeignKey('weather_data.id'))
    weather_data = db.relationship('WeatherData', backref='weather_values')
    timestamp = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float)  # °C
    humidity = db.Column(db.Float)  # %
    wind_speed = db.Column(db.Float)  # m/s
    pressure = db.Column(db.Float)  # hPa
    cloud_cover = db.Column(db.Integer)  # 0-8
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SolarData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    irradiation_wm2 = db.Column(db.Float)  # Globalstrahlung in W/m²
    power_kw = db.Column(db.Float)  # PV-Leistung in kW (für PVSol-Export)
    data_source = db.Column(db.String(50))  # 'import', 'pvsol_simulation', 'weather_station'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    project = db.relationship('Project', backref='solar_data')

class SolarValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solar_data_id = db.Column(db.Integer, db.ForeignKey('solar_data.id'))
    solar_data = db.relationship('SolarData', backref='solar_values')
    timestamp = db.Column(db.DateTime, nullable=False)
    global_irradiance = db.Column(db.Float)  # W/m²
    direct_irradiance = db.Column(db.Float)  # W/m²
    diffuse_irradiance = db.Column(db.Float)  # W/m²
    module_temp = db.Column(db.Float)  # °C
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HydroData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    water_level_m = db.Column(db.Float)  # Wasserstand in m
    flow_rate_ms = db.Column(db.Float)  # Durchfluss in m³/s
    data_source = db.Column(db.String(50))  # 'import', 'measurement_station'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    project = db.relationship('Project', backref='hydro_data')

class HydroValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hydro_data_id = db.Column(db.Integer, db.ForeignKey('hydro_data.id'))
    hydro_data = db.relationship('HydroData', backref='hydro_values')
    timestamp = db.Column(db.DateTime, nullable=False)
    flow_rate = db.Column(db.Float)  # m³/s
    water_level = db.Column(db.Float)  # m
    power_potential = db.Column(db.Float)  # kW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WindData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref='wind_data')
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WindValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wind_data_id = db.Column(db.Integer, db.ForeignKey('wind_data.id'))
    wind_data = db.relationship('WindData', backref='wind_values')
    timestamp = db.Column(db.DateTime, nullable=False)
    wind_speed = db.Column(db.Float)  # m/s
    wind_direction = db.Column(db.Float)  # °
    pressure = db.Column(db.Float)  # hPa
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
