# BESS Simulation - Dokumentation

## 📋 Übersicht

Die BESS (Battery Energy Storage System) Simulation-Anwendung ist eine Flask-basierte Webanwendung zur Verwaltung von Projekten und dem Import verschiedener Datentypen für Energiesystem-Simulationen.

## 🚀 Schnellstart

### Einfacher Server-Start
Die Anwendung kann über zwei einfache Methoden gestartet werden:

#### Option 1: Batch-Datei (Empfohlen)
```bash
# Doppelklick auf:
start_server.bat
```
- Aktiviert automatisch die virtuelle Umgebung
- Startet den Server
- Zeigt die URL an: http://127.0.0.1:5000

#### Option 2: PowerShell-Skript
```bash
# Rechtsklick → "Mit PowerShell ausführen" auf:
start_server.ps1

# Oder in PowerShell:
.\start_server.ps1
```

### Manueller Start (für Entwickler)
```bash
cd project
..\venv\Scripts\activate
python run.py
```

### Datenbank-Migrationen
Bei Änderungen am Datenbankschema müssen Migrationen ausgeführt werden:

```bash
# Telefonnummer-Spalte hinzufügen (bereits ausgeführt)
python add_phone_column.py

# Weitere Migrationen bei Bedarf
python init_db.py
```

## 📋 Übersicht

Die BESS (Battery Energy Storage System) Simulation-Anwendung ist eine Flask-basierte Webanwendung zur Verwaltung von Projekten und dem Import verschiedener Datentypen für Energiesystem-Simulationen.

## 🎨 Benutzeroberfläche

### Modernes Header-Menü
Die Anwendung verfügt über ein modernes, responsives Header-Menü mit folgenden Features:

#### Desktop-Navigation
- **Dashboard:** Direkter Zugriff mit Hover-Effekten
- **Projekte Dropdown:** 
  - Alle Projekte anzeigen
  - Neues Projekt erstellen
- **Kunden Dropdown:**
  - Alle Kunden anzeigen
  - Neuen Kunden erstellen
- **Daten Dropdown:**
  - Spot-Preise
  - Investitionskosten
  - Referenzpreise
  - Datenvorschau
  - Datenimport
- **Wirtschaftlichkeit:** Direkter Zugriff

#### Mobile Navigation
- **Hamburger-Menü** für mobile Geräte
- **Responsive Design** für alle Bildschirmgrößen
- **Touch-optimiert** für Tablets und Smartphones

#### Design-Features
- **Hover-Effekte** mit gelben Unterstreichungen
- **Smooth Transitions** und Animationen
- **Dropdown-Menüs** mit Schatten-Effekten
- **Moderne Icons** (Font Awesome)
- **Konsistente Farbgebung** (Blau-Gelb Theme)

### Benutzerfreundlichkeit
- **Intuitive Navigation** durch logische Gruppierung
- **Schneller Zugriff** auf häufig genutzte Funktionen
- **Klare Struktur** durch Dropdown-Organisation
- **Professionelles Design** für Business-Anwendungen

## 🏗️ Architektur

### Technologie-Stack
- **Backend:** Flask (Python)
- **Datenbank:** SQLite mit SQLAlchemy ORM
- **Frontend:** HTML/CSS mit Tailwind CSS
- **Formulare:** Flask-WTF
- **Datenverarbeitung:** Pandas, NumPy

### Projektstruktur
```
TB-Instanet/
├── project/
│   ├── app/
│   │   ├── templates/          # Jinja2 Templates
│   │   ├── __init__.py         # Flask App Initialisierung
│   │   └── routes.py           # URL-Routen
│   ├── config.py               # Konfiguration
│   ├── forms.py                # WTForms Formulare
│   ├── models.py               # SQLAlchemy Modelle
│   ├── data_importers.py       # Datenimport-Logik
│   └── instance/
│       └── bess.db            # SQLite Datenbank
├── venv/                       # Virtuelle Umgebung
├── start_server.bat           # Server-Start (Windows)
├── start_server.ps1           # Server-Start (PowerShell)
└── requirements.txt            # Python-Abhängigkeiten
```

## 🚀 Installation & Setup

### Voraussetzungen
- Python 3.9+
- pip

### Installation
```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Virtuelle Umgebung aktivieren
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Datenbank initialisieren
python init_db.py

# Anwendung starten
python run.py
```

### Datenbank-Initialisierung
```bash
python init_db.py
```

## 📊 Datenimport-Formate

### 1. Lastprofil-Import

#### Unterstützte Formate:

**Standard-Format:**
```csv
timestamp,power_kw,energy_kwh
2024-01-15 00:00:00,8.2,2.05
2024-01-15 00:15:00,7.8,1.95
2024-01-15 00:30:00,6.5,1.625
```

**PVSol-Export-Format (Deutsch):**
```csv
Datum,Zeit,Leistung,Energie
2024-01-15,00:00:00,8.2,2.05
2024-01-15,00:15:00,7.8,1.95
2024-01-15,00:30:00,6.5,1.625
```

**PVSol-Export-Format (Alternative):**
```csv
Datum,Zeit,Last,Energie
2024-01-15,00:00:00,8.2,2.05
2024-01-15,00:15:00,7.8,1.95
2024-01-15,00:30:00,6.5,1.625
```

**PVSol-Export-Format (Englisch):**
```csv
Date,Time,Power,Energy
2024-01-15,00:00:00,8.2,2.05
2024-01-15,00:15:00,7.8,1.95
2024-01-15,00:30:00,6.5,1.625
```

#### Anforderungen:
- **Zeitstempel:** YYYY-MM-DD HH:MM:SS Format
- **Leistung:** Dezimalzahl in kW (Punkt als Dezimaltrennzeichen)
- **Energie:** Optional, in kWh
- **Kodierung:** UTF-8 empfohlen
- **Trennzeichen:** Komma (,)
- **Header:** Erste Zeile mit Spaltennamen

### 2. Wetterdaten-Import

#### DWD-Format (Deutscher Wetterdienst):
```csv
MESS_DATUM;TT_TU;RF_TU;F;P;N
2024011500;12.5;65.2;3.2;1013.2;7
2024011501;11.8;67.1;2.8;1012.8;6
2024011502;10.9;69.5;2.1;1012.5;5
```

#### Custom-Format:
```csv
timestamp,temperature,humidity,wind_speed,pressure,cloud_cover
2024-01-15 00:00:00,12.5,65.2,3.2,1013.2,7
2024-01-15 01:00:00,11.8,67.1,2.8,1012.8,6
2024-01-15 02:00:00,10.9,69.5,2.1,1012.5,5
```

#### Spalten-Mapping:
- `MESS_DATUM` → `timestamp`
- `TT_TU` → `temperature` (°C)
- `RF_TU` → `humidity` (%)
- `F` → `wind_speed` (m/s)
- `P` → `pressure` (hPa)
- `N` → `cloud_cover` (0-8)

### 3. Solardaten-Import

#### PVSol-Export-Format:
```csv
Datum;Zeit;Globalstrahlung;Direktstrahlung;Diffusstrahlung;Modultemperatur
2024-01-15;00:00:00;0;0;0;5.2
2024-01-15;00:15:00;0;0;0;5.1
2024-01-15;06:00:00;45.2;12.8;32.4;8.7
```

#### Custom-Format:
```csv
timestamp,global_irradiance,direct_irradiance,diffuse_irradiance,module_temp
2024-01-15 00:00:00,0,0,0,5.2
2024-01-15 00:15:00,0,0,0,5.1
2024-01-15 06:00:00,45.2,12.8,32.4,8.7
```

### 4. Wasserkraftdaten-Import

#### Standard-Format:
```csv
timestamp,flow_rate,water_level,power_potential
2024-01-15 00:00:00,12.5,2.3,45.2
2024-01-15 00:15:00,13.1,2.4,47.8
2024-01-15 00:30:00,11.8,2.2,42.1
```

#### Einheiten:
- **Durchfluss:** m³/s, l/s oder m³/h
- **Wasserstand:** m
- **Leistungspotential:** kW

### 5. Windkraftdaten-Import

#### DWD-Winddaten:
```csv
MESS_DATUM;F;D;P
2024011500;5.2;180;1013.2
2024011501;6.1;175;1012.8
2024011502;4.8;185;1012.5
```

#### Custom-Format:
```csv
timestamp,wind_speed,wind_direction,pressure
2024-01-15 00:00:00,5.2,180,1013.2
2024-01-15 01:00:00,6.1,175,1012.8
2024-01-15 02:00:00,4.8,185,1012.5
```

#### Windkraft-Parameter:
- **Nabenhöhe:** Standard 80m
- **Rotordurchmesser:** Standard 90m
- **Leistungskurve:** Automatische Berechnung

### 6. PVSol-System-Import

#### Systemkonfiguration (JSON):
```json
{
  "system_name": "PV-Anlage Hinterstoder",
  "modules": [
    {
      "type": "Jinko JKM400M-72H",
      "count": 24,
      "power": 400
    }
  ],
  "inverters": [
    {
      "type": "SMA Sunny Tripower 10.0",
      "power": 10000
    }
  ],
  "location": {
    "latitude": 47.6969,
    "longitude": 14.1697,
    "elevation": 800
  }
}
```

#### Simulationsergebnisse (JSON):
```json
{
  "annual_yield": 12500,
  "monthly_yields": [
    850, 950, 1200, 1400, 1600, 1700,
    1800, 1700, 1400, 1100, 900, 800
  ],
  "performance_ratio": 0.82
}
```

#### Zeitreihendaten (CSV):
```csv
timestamp,power_ac,energy_dc,irradiance
2024-01-15 00:00:00,0,0,0
2024-01-15 06:00:00,0,0,45.2
2024-01-15 12:00:00,8500,9200,850.5
```

## 🗄️ Datenbank-Schema

### Projekte
```sql
CREATE TABLE project (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    date DATE,
    bess_size FLOAT,
    bess_power FLOAT,
    pv_power FLOAT,
    hp_power FLOAT,
    wind_power FLOAT,
    hydro_power FLOAT,
    customer_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Kunden
```sql
CREATE TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    company VARCHAR(200),
    contact VARCHAR(200),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Lastprofile
```sql
CREATE TABLE load_profile (
    id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    data_type VARCHAR(50),
    time_resolution INTEGER DEFAULT 15,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Lastwerte
```sql
CREATE TABLE load_value (
    id INTEGER PRIMARY KEY,
    load_profile_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    power_kw FLOAT NOT NULL,
    energy_kwh FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Konfiguration

### config.py
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///instance/bess.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
```

## 🚀 Verwendung

### 1. Kundenverwaltung

#### Neuen Kunden erstellen
1. **Navigation:** Kunden → "Neuer Kunde" oder Header → "Kunden" → "Neuer Kunde"
2. **Pflichtfelder:**
   - **Name:** Vollständiger Name des Kunden (erforderlich)
3. **Optionale Felder:**
   - **Firma:** Firmenname oder Organisation
   - **E-Mail:** E-Mail-Adresse für Kontakt
   - **Telefon:** Telefonnummer (internationales Format empfohlen, z.B. +43 123 456 789)
4. **Speichern:** "Kunde speichern" klicken

#### Kunden bearbeiten
1. **Navigation:** Kunden → "Bearbeiten" bei gewünschtem Kunden
2. **Verfügbare Aktionen:**
   - **Daten ändern:** Name, Firma, E-Mail, Telefon
   - **Projekte anzeigen:** Alle zugehörigen Projekte werden angezeigt
   - **Kunde löschen:** Mit Bestätigung (alle Projekte werden ebenfalls gelöscht)
3. **Speichern:** "Änderungen speichern" klicken

#### Kundenliste
- **Übersicht:** Alle Kunden mit Name, Firma, E-Mail, Telefon
- **Projektanzahl:** Anzahl der zugehörigen Projekte
- **Aktionen:** Anzeigen, Bearbeiten, Löschen
- **Suche:** Filterung nach Name oder Firma
- **Sortierung:** Nach Name oder Projektanzahl

### 2. Projekt erstellen
1. Dashboard → "Neues Projekt"
2. Projektinformationen eingeben
3. Kunde auswählen oder neuen Kunden erstellen
4. Speichern

### 3. Daten importieren
1. Projekt auswählen
2. "Daten importieren" klicken
3. Datentyp auswählen
4. Datei hochladen
5. Parameter konfigurieren
6. Import starten

### 4. Datenvorschau
1. "Datenvorschau" im Hauptmenü
2. Datei auswählen
3. Datentyp wählen
4. Vorschau anzeigen

## 📈 Zeitauflösungen

### Standard-Einstellungen:
- **Lastprofile:** 15 Minuten
- **Wetterdaten:** 60 Minuten
- **Solardaten:** 15 Minuten
- **Wasserkraftdaten:** 15 Minuten
- **Windkraftdaten:** 60 Minuten

### Unterstützte Auflösungen:
- **Minimal:** 1 Minute
- **Maximal:** 1440 Minuten (24 Stunden)
- **Empfohlen:** 15 Minuten für PVSol-Daten

## 🔍 Fehlerbehebung

### Häufige Probleme:

1. **"CSV muss 'timestamp' und 'power_kw' Spalten enthalten"**
   - Überprüfe Spaltennamen
   - Verwende unterstützte Formate
   - Prüfe UTF-8 Kodierung

2. **"TemplateNotFound"**
   - Alle Templates sind vorhanden
   - Flask-App neu starten

3. **Datenbankfehler**
   - `python init_db.py` ausführen
   - Datenbank-Datei löschen und neu initialisieren

4. **Datei zu groß**
   - Maximale Dateigröße: 10MB
   - Datei komprimieren oder aufteilen

5. **CSRF-Token Fehler**
   - API-Routes sind mit `@csrf.exempt` markiert
   - Server neu starten bei Änderungen

## 📝 API-Endpunkte

### Projekte
- `GET /` - Dashboard
- `GET /projects` - Projektübersicht
- `GET /projects/new` - Neues Projekt
- `POST /projects/new` - Projekt erstellen
- `GET /projects/<id>` - Projekt anzeigen
- `GET /projects/<id>/edit` - Projekt bearbeiten
- `POST /projects/<id>/edit` - Projekt aktualisieren

### Kunden
- `GET /customers` - Kundenübersicht
- `GET /customers/new` - Neuer Kunde
- `POST /customers/new` - Kunde erstellen
- `GET /customers/<id>` - Kunde anzeigen
- `GET /customers/<id>/edit` - Kunde bearbeiten
- `PUT /customers/<id>` - Kunde aktualisieren
- `DELETE /customers/<id>` - Kunde löschen
- `GET /customers/<id>/projects` - Projekte des Kunden

### Datenimport
- `GET /import/<project_id>` - Import-Übersicht
- `GET /import/<project_id>/load` - Lastprofil importieren
- `POST /import/<project_id>/load` - Lastprofil hochladen
- `GET /import/<project_id>/weather` - Wetterdaten importieren
- `POST /import/<project_id>/weather` - Wetterdaten hochladen
- `GET /import/<project_id>/solar` - Solardaten importieren
- `POST /import/<project_id>/solar` - Solardaten hochladen
- `GET /import/<project_id>/hydro` - Wasserkraftdaten importieren
- `POST /import/<project_id>/hydro` - Wasserkraftdaten hochladen
- `GET /import/<project_id>/wind` - Windkraftdaten importieren
- `POST /import/<project_id>/wind` - Windkraftdaten hochladen
- `GET /import/<project_id>/pvsol` - PVSol-System importieren
- `POST /import/<project_id>/pvsol` - PVSol-System hochladen

### Datenvorschau
- `GET /preview` - Datenvorschau
- `POST /preview` - Datei vorschauen

## 🔒 Sicherheit

- **CSRF-Schutz:** Aktiviert für alle Formulare (API-Routes sind mit `@csrf.exempt` markiert)
- **Datei-Validierung:** Nur erlaubte Dateitypen
- **Größenbeschränkung:** 10MB pro Datei
- **SQL-Injection-Schutz:** SQLAlchemy ORM
- **Input-Validierung:** Alle Benutzereingaben werden validiert und bereinigt

## 📊 Monitoring

### Import-Status
```python
# Anzahl importierter Datensätze pro Projekt
def get_import_status(project_id):
    return {
        'load_profiles': count_load_profiles(project_id),
        'weather_data': count_weather_data(project_id),
        'solar_data': count_solar_data(project_id),
        'hydro_data': count_hydro_data(project_id),
        'wind_data': count_wind_data(project_id),
        'total_data_points': count_total_data_points(project_id)
    }
```

## 🚀 Deployment

### Produktions-Setup
```bash
# Umgebungsvariablen setzen
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///instance/bess.db

# Gunicorn starten
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker (optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 🧪 Testing

### API-Tests
Die Anwendung verfügt über umfassende Test-Skripte:

```bash
# Test der Customer-API
python test_api.py

# Test der Telefonnummer-Funktionalität
python test_phone_api.py
```

### Test-Features
- **Customer-API:** Vollständige CRUD-Operationen
- **Telefonnummer:** Speicherung und Abruf
- **Validierung:** Eingabevalidierung und Fehlerbehandlung
- **Datenbank:** Migration und Schema-Updates

## 📞 Support

Bei Fragen oder Problemen:
1. Dokumentation durchlesen
2. Fehlerbehebung-Sektion prüfen
3. Logs überprüfen
4. Datenbank-Integrität testen
5. API-Tests ausführen

## 🔄 Changelog

### Version 1.1.0 (Aktuell)
- ✅ **Telefonnummer-Feld** zu Kunden hinzugefügt
- ✅ **Datenbank-Migration** für phone-Spalte
- ✅ **API-Erweiterung** für Telefonnummer
- ✅ **Template-Updates** für alle Kunden-Formulare
- ✅ **Moderne Navigation** mit Dropdown-Menüs
- ✅ **Responsive Design** für mobile Geräte
- ✅ **Server-Start-Skripte** für einfache Bedienung

### Version 1.0.0
- ✅ **Grundfunktionen** implementiert
- ✅ **Projekt- und Kundenverwaltung**
- ✅ **Datenimport-System**
- ✅ **Basis-API** und Templates

---

**Version:** 1.1.0  
**Letzte Aktualisierung:** Juli 2025  
**Entwickler:** BESS Simulation Team 