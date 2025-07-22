import csv
from datetime import datetime, timedelta
import random

def create_pumpsation_demo():
    """Erstellt eine Demo-CSV-Datei im Pumpsation-Format"""
    
    # Zeitreihe für einen Tag (15-Minuten-Intervalle)
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    time_series = []
    for i in range(96):  # 24 Stunden * 4 (15-Minuten-Intervalle)
        time_series.append(start_time + timedelta(minutes=15*i))
    
    # Pumpsation 1: Hauptlast (Gebäude)
    pumpsation1 = []
    for i, time in enumerate(time_series):
        hour = time.hour
        if 6 <= hour <= 8:  # Morgen
            base_load = 25 + random.uniform(-2, 2)
        elif 18 <= hour <= 22:  # Abend
            base_load = 30 + random.uniform(-3, 3)
        elif 23 <= hour or hour <= 5:  # Nacht
            base_load = 5 + random.uniform(-1, 1)
        else:  # Tag
            base_load = 15 + random.uniform(-2, 2)
        
        pumpsation1.append(max(0, base_load))
    
    # Pumpsation 2: Produktion (Maschinen)
    pumpsation2 = []
    for i, time in enumerate(time_series):
        hour = time.hour
        if 7 <= hour <= 17:  # Arbeitszeit
            base_load = 20 + random.uniform(-5, 5)
        else:  # Nachtschicht minimal
            base_load = 2 + random.uniform(-1, 1)
        
        pumpsation2.append(max(0, base_load))
    
    # Pumpsation 3: Klimaanlage
    pumpsation3 = []
    for i, time in enumerate(time_series):
        hour = time.hour
        if 8 <= hour <= 18:  # Bürozeiten
            base_load = 15 + random.uniform(-2, 2)
        else:  # Nachts aus
            base_load = 1 + random.uniform(-0.5, 0.5)
        
        pumpsation3.append(max(0, base_load))
    
    # Pumpsation 9: Beleuchtung
    pumpsation9 = []
    for i, time in enumerate(time_series):
        hour = time.hour
        if 6 <= hour <= 22:  # Beleuchtung an
            base_load = 8 + random.uniform(-1, 1)
        else:  # Nachts aus
            base_load = 1 + random.uniform(-0.3, 0.3)
        
        pumpsation9.append(max(0, base_load))
    
    # CSV-Datei erstellen
    with open('demo_pumpsation.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header
        writer.writerow([
            'Datum',
            'Pumpsation1_kWh', 'Pumpsation1_Status',
            'Pumpsation2_kWh', 'Pumpsation2_Status',
            'Pumpsation3_kWh', 'Pumpsation3_Status',
            'Pumpsation9_kWh', 'Pumpsation9_Status',
            'Viertelstundenwerte_kWh_Gesamt',
            'Tageswerte_kWh_Gesamt'
        ])
        
        # Daten
        for i, time in enumerate(time_series):
            # Viertelstundenwerte (Summe aller Pumpsationen)
            total_quarter = pumpsation1[i] + pumpsation2[i] + pumpsation3[i] + pumpsation9[i]
            
            # Tageswerte (nur für 00:00 Uhr)
            daily_total = 0
            if time.hour == 0 and time.minute == 0:
                # Summe aller Werte des Tages
                daily_total = sum(pumpsation1) + sum(pumpsation2) + sum(pumpsation3) + sum(pumpsation9)
            
            writer.writerow([
                time.strftime("%d.%m.%Y %H:%M:%S"),
                round(pumpsation1[i], 2), 'VALID',
                round(pumpsation2[i], 2), 'VALID',
                round(pumpsation3[i], 2), 'VALID',
                round(pumpsation9[i], 2), 'VALID',
                round(total_quarter, 2),
                round(daily_total, 2) if daily_total > 0 else ''
            ])
    
    print("✅ Demo-Pumpsation-Datei erstellt: demo_pumpsation.csv")
    print("📊 Struktur:")
    print("  - Pumpsation 1: Hauptlast (Gebäude)")
    print("  - Pumpsation 2: Produktion (Maschinen)")
    print("  - Pumpsation 3: Klimaanlage")
    print("  - Pumpsation 9: Beleuchtung")
    print("  - Viertelstundenwerte: Summe aller Pumpsationen")
    print("  - Tageswerte: Tagesgesamtsumme")
    print("")
    print("💡 Diese Datei entspricht der Excel-Struktur aus dem Bild!")

if __name__ == "__main__":
    create_pumpsation_demo() 